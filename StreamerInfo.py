from __future__ import annotations

import sys

from argparse import ArgumentParser, RawTextHelpFormatter

# allow CTRL + C and don't throw error
from signal import signal, SIGINT, SIGTERM
from typing import Any

import uvicorn

from business.Logger import Logger
from business.LoggerProxy import LoggerProxy
from business.Router import Router

signal(SIGINT, lambda x, y: (Logger.shutdown(), sys.exit(0)))
signal(SIGTERM, lambda x, y: (Logger.shutdown(), sys.exit(0)))
if sys.platform.startswith('win32'):
    from signal import SIGBREAK
    signal(SIGBREAK, lambda x, y: (Logger.shutdown(), sys.exit(0)))

# redirect stdout and stderr to custom logger proxy
#   deactivate buffering
sys.__stdout__.reconfigure(write_through=True, line_buffering=False)
sys.__stderr__.reconfigure(write_through=True, line_buffering=False)
#   redirect stdout and stderr to logger
sys.stdout = LoggerProxy(severity=Logger.Severity.DEBUG)
sys.stderr = LoggerProxy(severity=Logger.Severity.ERROR)

# set version
__version__: str = '0.1.0'

# force console output only
Logger.mode = Logger.Mode.CONSOLE

# build parser and parse arguments
parser: ArgumentParser = ArgumentParser(
    description="StreamerInfo ({}) serves dynamically generated illustrations containing current information about a streamers stream status (Twitch only).".format(__version__),
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(
    '--version',
    action='version',
    version='Running {} on version {}'.format('%(prog)s', __version__),
    help="Show application version."
)
args: Any = parser.parse_args()


class StreamerInfo:
    __ws_config = None
    __ws = None
    __router = None

    def __init__(self: StreamerInfo):
        self.__router = Router(version=__version__)
        self.__ws_config = uvicorn.Config(
            app=self.__router.get_resources(),
            port=5005,
            log_level='debug',
            interface='wsgi',
            lifespan='off',
            use_colors=False,
            server_header=False
        )
        self.__ws = uvicorn.Server(self.__ws_config)

    def run(self: StreamerInfo):
        self.__ws.run()


# MAIN ROUTINE (entry point)
if __name__ == '__main__':
    # init application
    Logger.debug(message="Loading application.")
    app = StreamerInfo()

    # run main logic
    app.run()

    # exit application
    Logger.debug(message="Exiting application.")
    Logger.shutdown()
    sys.exit(0)
