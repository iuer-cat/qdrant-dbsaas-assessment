import structlog

"""
This is the specific logger of the application that should be used throughout
the module to centralize all the logs that occur in it.
"""
LOGGER_NAME = 'Nebula'
app_logger = structlog.getLogger(LOGGER_NAME)



