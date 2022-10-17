from __future__ import annotations

import io
from datetime import datetime
from io import BytesIO

import requests
from dateutil import parser
from dateutil.parser import ParserError
from dateutil.tz import UTC
from requests import Response, HTTPError

from business.Logger import Logger
from data.IMCache import IMCache


class TwitchGrabber:
    __key: str = 'r8s4dac0uhzifbpu9sjdiwzctle17ff'
    __uri: str = 'https://gql.twitch.tv/gql'

    @staticmethod
    def __parse_date(date_string: str) -> datetime | bool:
        try:
            dt: datetime = parser.parse(date_string)
            return dt.astimezone(UTC)
        except ParserError:
            return False

    @classmethod
    def grab(cls: TwitchGrabber, channel_name: str) -> IMCache.ChannelInformation | bool:
        payload: dict = {
            'query': '''
                query ChannelAboutPage_Query($login: String!) {
                  channel: user(login: $login) {
                    id
                    login
                    displayName
                    profileImageURL(width: 50)
                    followers {
                      totalCount
                    }
                    lastBroadcast {
                      startedAt
                    }
                    stream {
                      viewersCount
                    }
                    roles {
                      isPartner
                    }
                  }
                }
                ''',
            'variables': {
                'login': channel_name
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
                started_at: datetime = None
                if channel['lastBroadcast']['startedAt']:
                    started_at = TwitchGrabber.__parse_date(date_string=channel['lastBroadcast']['startedAt'])
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
    @classmethod
    def grab_avatar(cls: TwitchGrabber, url: str) -> BytesIO | bool:
        headers: dict = {
            'User-Agent': None
        }
        try:
            res: Response = requests.request('GET', url, json=None, data=None, headers=headers, timeout=5)
            if not res.status_code == 200:
                Logger.warn(message="Failed getting avatar: {}".format(res.content))
            return io.BytesIO(initial_bytes=res.content)
        except HTTPError as err:
            return False
