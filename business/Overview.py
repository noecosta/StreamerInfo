from __future__ import annotations

from pathlib import Path

from falcon import Request, Response, HTTP_200


class Overview(object):
    def on_get(self: Overview, request: Request, response: Response) -> None:
        response.status = HTTP_200
        response.content_type = 'text/html'
        response.stream = open(Path(str(Path(__file__).parent.parent) + '/static/overview.html'), 'rb')
