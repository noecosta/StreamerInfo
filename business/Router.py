from __future__ import annotations

import falcon
from falcon import App

from presentation.Overview import Overview
from presentation.TwitchWidget import TwitchWidget


class Router(App):
    def __init__(self: Router, version: str) -> None:
        super().__init__()
        self.resources: App = falcon.App()
        self.resources.add_route(
            uri_template='/',
            resource=Overview()
        )
        self.resources.add_route(
            uri_template='/{channel}',
            resource=TwitchWidget(version=version),
            compile=True
        )

    def get_resources(self: Router) -> App:
        return self.resources
