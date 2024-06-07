import logging.config, yaml, structlog
from typing import NoReturn, List, Any
from structlog import configure
from structlog.stdlib import LoggerFactory
from structlog.processors import TimeStamper
from structlog.dev import ConsoleRenderer


class LoggingBootstrap:

    @staticmethod
    def get_structlog_processors_for_console() -> List[Any]:
        """
        Retrieves a list of structlog processors for console logging.

        :return: A list of structlog processors configured for console output.
        :rtype: List[Any]
        """
        return [
            structlog.stdlib.filter_by_level,
            TimeStamper(fmt='%Y-%m-%d %H:%M:%S'),
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            ConsoleRenderer(sort_keys=False),
        ]

    @staticmethod
    def configure(logging_file_path: str) -> NoReturn:
        """
        This method reads the logging configuration from a YAML file specified
        in the logging_file_path parameter and applies it to the Python
        logging module.

        :raises FileNotFoundError: If the logging configuration file does not
            exist.
        :raises yaml.YAMLError: If there is an error parsing the YAML file.
        """

        with open(logging_file_path, "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        processors = LoggingBootstrap.get_structlog_processors_for_console()

        configure(
            processors=processors,
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )