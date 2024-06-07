import traceback
from signal import signal, SIGTERM
from typing import NoReturn, List

from nebula.application.settings import app_logger
from nebula.domain.ports import Handler
from nexus.command_bus.application.command_bus import CommandBus
from nexus.core.domain.command import Command


class SingleThreadCommandBusConsumer:
    """
    Consumer bus that queries and consumes messages received via the CommandBus
    and delivers them to the handler specified in the constructor.

    Note: This is a simplified approach to a real CommandBusConsumer. The
    important aspect here is the decoupling between the component responsible
    for receiving and sending messages (CommandBus), the component responsible
    for processing these messages (Handler), and the component orchestrating the
    previous two in a pulling approach.
    """

    def __init__(self, bus: CommandBus, message_handler: Handler):
        self.bus = bus
        self.message_handler = message_handler
        self.sig_quit = False
        signal(SIGTERM, self.signal_shutdown)

    def signal_shutdown(self, signum, frame) -> NoReturn:
        """
        Handle the SIGTERM signal to stop the loop in a controlled manner.

        :param signum: The received signal number.
        :type signum: int
        :param frame: The current execution frame.
        :type frame: frame
        """
        log_msg = f'{self.__class__.__name__} - Signal Received {signum}. ' \
                  f'Stopping the consumer loop in a controlled exit'
        app_logger.info(log_msg)
        self.sig_quit = True

    def run(self) -> NoReturn:
        """
        Entry point to the execution of the infinite loop that pulls
        messages from the CommandBus and processes them in the Handler.
        """

        log_msg = f'{self.bus.__class__.__name__} loop consumer started'
        app_logger.info(log_msg)

        # Main consumer loop handling errors during its execution.
        while not self.sig_quit:
            try:
                self.perform_loop_iteration()
            except KeyboardInterrupt:
                self.sig_quit = True
            except Exception as ex:
                stack_trace = traceback.format_exc()
                warn_msg = f'Unexpected error during the run() loop execution: ' \
                           f'Exception message: {str(ex)}'
                app_logger.warning(warn_msg)
                exc_msg = f'Exception Type: {ex.__class__}, StackTrace: ' \
                          f'{stack_trace}'
                app_logger.error(exc_msg)
                raise ex

        log_msg = f'Exiting {self.__class__.__name__} consumer loop'
        app_logger.info(log_msg)

    def perform_loop_iteration(self) -> NoReturn:
        """
        Assume we have only one type of message, which is a Command of type
        ProvisionDBCluster, to simplify the implementation and focus on the
        prototype's objectives.
        """

        commands: List[Command] = self.bus.retrieve()

        for command in commands:
            self.message_handler.handle(command)
