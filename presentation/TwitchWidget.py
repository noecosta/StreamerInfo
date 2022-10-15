from __future__ import annotations

import io
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFont
from falcon import Request, Response, HTTP_200

from business.Logger import Logger
from business.TwitchGrabber import TwitchGrabber
from data.IMCache import IMCache


class TwitchWidget:
    def __init__(self: TwitchWidget, version: str) -> None:
        self.__version__ = version
        self.ic: IMCache.__class__ = IMCache
        self.tg: TwitchGrabber.__class__ = TwitchGrabber

    def on_get(self: TwitchWidget, request: Request, response: Response, channel: str) -> None:
        if not channel:
            # TODO: add proper default image response
            Logger.debug('Default call. Returning information about the program')
        else:
            # grab channel information
            channel = channel.lower()
            information: IMCache.ChannelInformation = self.ic.get(channel)
            if not information or (information.timestamp + timedelta(seconds=60)) < datetime.now():
                # data doesn't exist or is older than one minute, refreshing it
                information = self.tg.grab(channel)
                if information:
                    self.ic.store(key=channel, value=information)
            print(information)

            # generate
            base: Image = Image.new('RGBA', (275, 221), (255, 0, 0, 0))
            base_font: ImageFont = ImageFont.truetype('static/monogram-extended.ttf')
            base_2d_draw: ImageDraw = ImageDraw.Draw(base)
            tpl_widget_bg: Image = Image.open('static/widget/widget_background.png').convert('RGBA')
            tpl_widget_title: Image = Image.open('static/widget/widget_title.png').convert('RGBA')
            tpl_content_bg: Image = Image.open('static/widget/content_background.png').convert('RGBA')
            tpl_channel_partnered: Image = Image.open('static/widget/channel_partnered.png').convert('RGBA')

            # title: ImageFont = base_font.font_variant(None, 40)
            base.alpha_composite(tpl_widget_bg)
            base.alpha_composite(tpl_widget_title)
            base.alpha_composite(tpl_content_bg)
            base.alpha_composite(tpl_channel_partnered)
            base_2d_draw.text(
                xy=(235, 6),
                text=self.__version__,
                fill='#10002b',
                font=base_font.font_variant(None, 16)
            )
            base_2d_draw.text(
                xy=(42, 188),
                text='GENERATED ON {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                fill='#391f54',
                font=base_font.font_variant(None, 16)
            )

            rendered_image = io.BytesIO()
            base.save(rendered_image, 'WEBP', lossless=True, quality=100)

            response.content_type = 'image/webp'
            response.status = HTTP_200
            # response.text = json.dumps(channel, ensure_ascii=False)
            response.data = rendered_image.getvalue()
