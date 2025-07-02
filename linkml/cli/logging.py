import logging

import click

LOG_LEVEL_STRINGS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
DEFAULT_LOG_LEVEL: str = "WARNING"
DEFAULT_LOG_LEVEL_INT: int = logging.WARNING


def log_level_option(fn):
    def callback(ctx, param, value):
        log_level_string = value.upper()
        log_level_int = getattr(logging, log_level_string, None)
        if not isinstance(log_level_int, int):
            raise ValueError(f"Invalid log level: {log_level_string}")
        logging.basicConfig(level=log_level_int)

    return click.option(
        "--log_level",
        type=click.Choice(LOG_LEVEL_STRINGS),
        help="Logging level",
        default=DEFAULT_LOG_LEVEL,
        show_default=True,
        callback=callback,
    )(fn)
