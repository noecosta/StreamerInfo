from __future__ import annotations

import inspect
import sys
from datetime import datetime
from enum import Enum
from os import path
from time import time

from pytz import timezone


class Logger:
    class Mode(Enum):
        CONSOLE = 0
        FILE = 1
        BOTH = 2

    class Severity(Enum):
        TRACE = 0
        DEBUG = 1
        INFO = 2
        WARN = 3
        ERROR = 4
        FATAL = 5

    mode = Mode.BOTH
    __logfile = None
    __init_time = time().real

    @classmethod
    def change_logfile(cls: Logger, name) -> None:
        if cls.__logfile:
            cls.__logfile.close()
        cls.__logfile = open(file=name + '.log', mode='ab+')

    @classmethod
    def shutdown(cls: Logger):
        if cls.__logfile:
            cls.__logfile.close()

    @classmethod
    def __print(cls: Logger, message: str, severity: Severity = Severity.DEBUG, overwrite_class: str = None, overwrite_method: str = None) -> None:
        # get calling class and method
        caller = inspect.currentframe().f_back.f_back
        c_method = overwrite_method if overwrite_method else caller.f_code.co_name
        c_class = overwrite_class if overwrite_class else path.splitext(path.basename(caller.f_code.co_filename))[0]
        if c_method == '<module>':
            c_method = None

        # get timestamps
        now = datetime.now(tz=timezone('Europe/Zurich'))
        now_t = time().real

        # build log message respecting the IntelliJ Log Format: https://regex101.com/r/m2rrfp/1
        msg = "{} [{}]   {} - {} - {}".format(
            str(now.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]).ljust(23, ' '),
            str(((now_t - cls.__init_time) * 1000).__trunc__()).rjust(10, ' '),
            str(severity.name).ljust(5, ' '),
            '.'.join(filter(None, (c_class, c_method))),
            message.strip()
        )

        # check where to output the logged message
        if cls.mode == Logger.Mode.BOTH or cls.mode == Logger.Mode.CONSOLE:
            # log to console
            if severity in (Logger.Severity.TRACE, Logger.Severity.DEBUG, Logger.Severity.INFO):
                # to stdout
                sys.__stdout__.write(msg + '\n')
                sys.__stdout__.flush()
            else:
                # to stderr
                sys.__stdout__.flush()
                sys.__stderr__.write(msg + '\n')
                sys.__stdout__.flush()
        if cls.mode == Logger.Mode.BOTH or cls.mode == Logger.Mode.FILE:
            # log to file
            if not cls.__logfile:
                cls.__logfile = open(file='run.log', mode='ab+')
            cls.__logfile.write((msg + chr(13) + chr(10)).encode('UTF-8'))
            cls.__logfile.flush()

    @classmethod
    def trace(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.TRACE,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )

    @classmethod
    def debug(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.DEBUG,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )

    @classmethod
    def info(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.INFO,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )

    @classmethod
    def warn(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.WARN,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )

    @classmethod
    def error(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.ERROR,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )

    @classmethod
    def fatal(cls: Logger, message: str, overwrite_class: str = None, overwrite_method: str = None) -> None:
        cls.__print(
            severity=Logger.Severity.FATAL,
            message=message,
            overwrite_class=overwrite_class,
            overwrite_method=overwrite_method
        )
