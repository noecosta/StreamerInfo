from __future__ import annotations

import os

from falcon import Request, Response, HTTP_200

from business.Utilities import Utilities


class Overview(object):
    def on_get(self: Overview, request: Request, response: Response) -> None:
        response.status = HTTP_200
        response.content_type = 'text/html'
        response.stream = open(Utilities.get_dynamic_path(path='static/internals/overview.html'), 'rb')
