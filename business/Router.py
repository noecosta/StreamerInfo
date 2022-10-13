from __future__ import annotations

import falcon
from falcon import App

from presentation.TwitchWidget import TwitchWidget


class Router:
    def __init__(self: Router, version: str) -> None:
        self.resources: App = falcon.App()
        self.resources.add_route(
            uri_template='/{channel}',
            resource=TwitchWidget(version=version)
        )

    def get_resources(self: Router) -> App:
        return self.resources
