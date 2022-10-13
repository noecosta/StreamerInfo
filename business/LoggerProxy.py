from __future__ import annotations

import inspect
from os import path

from business.Logger import Logger


class LoggerProxy:
    __severity = None
    __message_buffer = []

    def __init__(self: LoggerProxy, severity: Logger.Severity = Logger.Severity.INFO) -> None:
        self.__severity = severity
        self.__message_buffer = []

    @staticmethod
    def isatty() -> bool:
        return Logger.mode in (Logger.Mode.CONSOLE, Logger.Mode.BOTH)

    def write(self: LoggerProxy, message: str) -> None:
        if message.endswith('\n'):
            # remove newline character from message as it will be handled by the logger function
            self.__message_buffer.append(
                message.removesuffix('\n')
            )
            if self.__severity in (Logger.Severity.TRACE, Logger.Severity.DEBUG, Logger.Severity.INFO):
                caller = inspect.currentframe().f_back
                c_method = caller.f_code.co_name
                c_class = path.splitext(path.basename(caller.f_code.co_filename))[0]
                if self.__severity == Logger.Severity.TRACE:
                    Logger.trace(message=''.join(self.__message_buffer), overwrite_method=c_method, overwrite_class=c_class)
                elif self.__severity == Logger.Severity.DEBUG:
                    Logger.debug(message=''.join(self.__message_buffer), overwrite_method=c_method, overwrite_class=c_class)
                elif self.__severity == Logger.Severity.INFO:
                    Logger.info(message=''.join(self.__message_buffer), overwrite_method=c_method, overwrite_class=c_class)
            else:
                c_method = 'stderr'
                c_class = 'System'
                Logger.fatal(message=''.join(self.__message_buffer), overwrite_method=c_method, overwrite_class=c_class)
            # reset buffer
            self.__message_buffer = []
        else:
            # append to buffer as there's no line break
            self.__message_buffer.append(message)

    def flush(self):
        pass
