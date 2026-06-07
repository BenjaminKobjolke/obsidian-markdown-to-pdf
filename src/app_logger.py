import logging

from src.constants import APP_NAME

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class AppLogger:
    """Centralized logger wrapper — the single off/level switch for the app.

    Feature code calls ``AppLogger.info(...)`` / ``.error(...)`` etc. and never
    touches ``logging.getLogger`` or ``print`` directly.
    """

    _logger: logging.Logger | None = None

    @classmethod
    def _get(cls) -> logging.Logger:
        if cls._logger is None:
            logger = logging.getLogger(APP_NAME)
            if not logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
            cls._logger = logger
        return cls._logger

    @classmethod
    def debug(cls, msg: str, *args: object) -> None:
        cls._get().debug(msg, *args)

    @classmethod
    def info(cls, msg: str, *args: object) -> None:
        cls._get().info(msg, *args)

    @classmethod
    def warning(cls, msg: str, *args: object) -> None:
        cls._get().warning(msg, *args)

    @classmethod
    def error(cls, msg: str, *args: object) -> None:
        cls._get().error(msg, *args)
