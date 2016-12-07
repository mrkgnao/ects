import coloredlogs
import logging
import os
import platform
from datetime import datetime
import settings

from flask import request
from coloredlogs import ColoredFormatter

DATE_FORMAT = '%H:%M:%S'

LOG_FORMAT_PRE = '%(levelname)8s %(asctime)s.%(msecs).03d'
LOG_FORMAT_POST = '%(message)s'
LOG_FORMAT = LOG_FORMAT_PRE + " " + LOG_FORMAT_POST

LEVEL_STYLES = {
    'debug': {},
    'critical': {
        'color': 'red',
    },
    'error': {
        'color': 'red'
    },
    'info': {
        'color': 'blue',
        'bold': True
    },
    'warn': {
        'color': 'yellow'
    }
}

FIELD_STYLES = {
    'hostname': {
        'color': 'cyan'
    },
    'programname': {
        'color': 'cyan'
    },
    'name': {
        'color': 'blue'
    },
    'levelname': {},
    'asctime': {
        'color': 'green'
    },
    'threadname': {
        'color': 'magenta'
    }
}

LEVEL_STYLES_PLAIN = {
    'debug': {},
    'critical': {},
    'error': {},
    'info': {},
    'warn': {}
}

FIELD_STYLES_PLAIN = {
    'hostname': {},
    'programname': {},
    'name': {},
    'levelname': {},
    'asctime': {},
    'threadname': {}
}

if settings.SHOW_COLORED_LOGS:
    formatter = ColoredFormatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        level_styles=LEVEL_STYLES,
        field_styles=FIELD_STYLES)
else:
    formatter = ColoredFormatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        level_styles=LEVEL_STYLES_PLAIN,
        field_styles=FIELD_STYLES_PLAIN)


class Logging(object):
    """Configure flask logging with nice formatting and syslog support."""

    def __init__(self, app=None):
        """Boiler plate extension init with log_level being declared"""
        self.log_level = None
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Setup the logging handlers, level and formatters.
        Level (DEBUG, INFO, CRITICAL, etc) is determined by the
        app.config['FLASK_LOG_LEVEL'] setting, and defaults to
        ``None``/``logging.NOTSET``.
        """
        try:
            config_log_level = app.config.get('FLASK_LOG_LEVEL', None)
        except AttributeError:
            config_log_level = logging.NOTSET

        # Set up format for default logging
        hostname = platform.node().split('.')[0]

        config_log_int = None
        set_level = None

        if config_log_level:
            config_log_int = getattr(logging, config_log_level.upper(), None)
            if not isinstance(config_log_int, int):
                raise ValueError('Invalid log level: {0}'.format(
                    config_log_level))
            set_level = config_log_int

        # Set to NotSet if we still aren't set yet
        if not set_level:
            set_level = config_log_int = logging.NOTSET
        self.log_level = set_level

        # Setup basic StreamHandler logging with format and level (do
        # setup in case we are main, or change root logger if we aren't.
        logging.basicConfig(format=formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(set_level)

        # Get everything ready to setup the syslog handlers
        # Add syslog handler before adding formatters
        self.set_formatter(formatter)

        return config_log_int

    @staticmethod
    def set_formatter(log_formatter):
        """Override the default log formatter with your own."""
        # Add our formatter to all the handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.setFormatter(log_formatter)


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """ Provide some extra variables to give our logs some
            better info """
        log_record.utcnow = (datetime.utcnow()
                             .strftime('%Y-%m-%d %H:%M:%S,%f %Z'))
        log_record.url = request.path
        log_record.method = request.method
        # Try to get the IP address of the user through reverse proxy
        log_record.ip = request.environ.get('HTTP_X_REAL_IP',
                                            request.remote_addr)
