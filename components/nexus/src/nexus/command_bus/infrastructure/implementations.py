import glob, inspect, os, yaml, time
from typing import List, Set, NoReturn, Dict

from nexus.command_bus.domain.commands.v1.db_clusters.provision import \
    ProvisionDBCluster
from nexus.command_bus.domain.ports import CommandPublisher, CommandSubscriber
from nexus.core.domain.command import Command


class DiskCommandSubscriber(CommandSubscriber):
    """
    Infrastructure implementation of a message broker based on disk persistence.
    This is purely an implementation for the prototype and demonstration
    purposes.
    """

    def __init__(self, delete_file_after_retrieve: bool = True):
        self.delete_file_after_retrieve = delete_file_after_retrieve

    def retrieve(self) -> List[Command]:
        """
        Retrieves a list of Command messages from the 'persistence_layer'.

        :return: List of Command messages.
        """

        commands_map = self.__load_commands_from_disk()
        commands = []
        for command_raw in commands_map.values():
            # Not Implemented: identification of the message based on the
            # Schema ID, assuming all are ProvisionDBCluster
            commands.append(
                ProvisionDBCluster(**command_raw)
            )

        # Adding a fake delay
        time.sleep(0.2)
        return commands

    def __load_commands_from_disk(self) -> Dict:
        """
        Loads the serialized YAML messages for later consumption.

        :return: Dictionary of command file contents.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        commands_path = os.path.join(
            f'{current_path}',
            '../../../../../../persistence_layer/command_bus/')

        command_files: Dict[str, Dict] = dict()
        pattern = f"{commands_path}*.yaml"

        for file_path in glob.iglob(pattern, recursive=False):
            file_name = os.path.basename(file_path)
            command_files[file_name] = self._load_content_from_file(file_path)

            # Assuming the Command will be processed correctly
            # No retries or redriving strategies has been considered.
            os.remove(file_path)

        return command_files

    def _load_content_from_file(self, file_path: str) -> Dict:
        """
        Load and return the content of a YAML file.

        :param file_path: The path to the YAML file to load.
        :type file_path: str

        :return: The content of the specified YAML file.
        :rtype: Dict
        """

        with open(file_path, "r") as yml_file:
            return yaml.safe_load(yml_file)


class DiskCommandPublisher(CommandPublisher):
    """
    Infrastructure implementation of a message broker based on disk
    persistence. This is purely an implementation for the prototype
    and demonstration purposes.
    """

    def dispatch(self, commands: Set[Command]) -> NoReturn:
        """"
        Dispatches a set of Command messages that will be persisted as files
        into the 'persistence_layer'.

        :param commands: Set of Command messages to be dispatched.
        """

        for command in commands:
            self.__write_command_as_file(command)

    def __write_command_as_file(self, command: Command) -> NoReturn:
        """
        Writes a Command message to the 'persistence_layer'.

        :param command: The Command message to be persisted.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

        command_file_path = os.path.join(
            f'{current_path}/../../../../../../persistence_layer/command_bus/',
            f'{command.id}.yaml')

        with open(command_file_path, "w") as yml_file:
            yaml.dump(command.as_dict(), yml_file, default_flow_style=False)
