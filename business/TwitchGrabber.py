from __future__ import annotations

from datetime import datetime

import requests
from requests import Response, HTTPError

from business.Logger import Logger
from data.IMCache import IMCache


class TwitchGrabber:
    __key: str = 'r8s4dac0uhzifbpu9sjdiwzctle17ff'
    __uri: str = 'https://gql.twitch.tv/gql'

    @staticmethod
    def __parse_date(date_string: str) -> datetime | bool:
        try:
            dt: datetime = datetime.fromisoformat(date_string)
            return dt
        except ValueError:
            return False

    @classmethod
    def grab(cls: TwitchGrabber, channel_name: str) -> IMCache.ChannelInformation | bool:
        payload: dict = {
            'query': 'query ChannelAboutPage_Query(  $login: String!  $url: String!) {  channel: user(login: $login) {    ...ChannelLayout_user    id    __typename    login    stream {      id      __typename    }    panels {      __typename      type      ... on DefaultPanel {        id        __typename        ...DefaultPanel_panel      }      id      __typename    }  }  ...SeoHead_query}fragment ChannelCover_user on User {  login  bannerImageURL  primaryColorHex}fragment ChannelDescription_user on User {  login  displayName  description  lastBroadcast {    game {      displayName      id      __typename    }    id    __typename  }  videos(first: 30) {    edges {      node {        id        __typename        game {          id          __typename          displayName        }      }    }  }}fragment ChannelLayout_user on User {  ...ChannelCover_user  ...ChannelProfileInfo_user  id  __typename  login}fragment ChannelName_user on User {  displayName  login  roles {    isPartner  }}fragment ChannelProfileInfo_user on User {  ...ChannelStatus_user  ...ChannelDescription_user  ...ChannelName_user  ...SocialMediaLinks_user  ...useFollowChannelFragment  profileImageURL(width: 150)  login  displayName  primaryColorHex  followers {    totalCount  }  stream {    id    __typename  }}fragment ChannelStatus_user on User {  hosting {    id    __typename    login    displayName  }  lastBroadcast {    id    __typename    startedAt    game {      id      __typename      displayName    }  }  stream {    id    __typename    createdAt    game {      id      __typename      displayName    }    type    viewersCount  }}fragment DefaultPanel_panel on DefaultPanel {  id  __typename  title  linkURL  imageURL  description}fragment SeoHead_query on Query {  urlMetadata(url: $url) {    title    metatags {      name      attributes {        key        value      }    }    jsonld    share {      title      text      url    }  }}fragment SocialMediaLinks_user on User {  channel {    id    __typename    socialMedias {      id      __typename      name      title      url    }  }}fragment useFollowChannelFragment on User {  id  __typename  self {    follower {      followedAt    }  }}',
            'variables': {
                'login': channel_name,
                'url': 'https://m.twitch.tv/' + channel_name + 'papaplatte/about'
            }
        }
        headers: dict = {
            'Client-ID': cls.__key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': None
        }
        try:
            res: Response = requests.request('POST', cls.__uri, json=payload, headers=headers, timeout=10)
            if not res.status_code == 200:
                Logger.warn(message="Requesting Twitch GQL Data went wrong: {}".format(res.content))
                return False
            data: dict = res.json()
            if data['data'] and data['data']['channel']:
                channel: dict = data['data']['channel']
                started_at: datetime = TwitchGrabber.__parse_date(date_string=channel['lastBroadcast']['startedAt'])
                return IMCache.ChannelInformation(
                    name=channel['login'],
                    displayed_name=channel['displayName'],
                    is_partnered=channel['roles']['isPartner'],
                    avatar_uri=channel['profileImageURL'].replace('150x150', '50x50'),
                    live_count=channel['stream']['viewersCount'] if channel['stream'] is not None else None,
                    follower_count=channel['followers']['totalCount'],
                    latest_stream=started_at if started_at is not False else None,
                    timestamp=datetime.now()
                )
            else:
                Logger.warn(message="Twitch GQL answered with an unsupported format: {}".format(data))
        except HTTPError as err:
            Logger.warn(message="Request to Twitch GQL couldn't be established: {}".format(err))
        except Exception as exc:
            Logger.warn(message="An exception occurred while trying to parse Twitch GQL data: {}".format(exc))
        return False
