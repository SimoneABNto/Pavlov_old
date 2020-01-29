import os
from importlib import import_module
import logging
from pvlv_commando.descriptors.command_descriptor import CommandDescriptor

logger = logging.getLogger('pvlv_command')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('pvlv_command.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


class Commando(object):
    def __init__(self, dir_commands: str):
        """
        Load all the packages and commands should be done only once.
        For efficiency it must be put as a static class for all the project.

        :param dir_commands: the dir of the commands folder, must end with / (example: 'pvlv/commands/')
        """
        self.__command_list = []

        import_point = dir_commands.replace('/', '.')

        # List all the main modules
        for package in os.listdir(os.path.dirname(dir_commands)):
            # List all the commands inside the single package
            for command in os.listdir(os.path.dirname('{}{}/'.format(dir_commands, package))):

                command_import_point = '.{}.{}'.format(command, command)
                module = import_module(command_import_point, package=import_point+package)

                # Build class name of the command
                spl = []
                for el in command.split('_'):
                    spl.append(str(el.capitalize()))
                class_name = ''.join(spl)

                """
                Read the command description file and create the class to store and access all the data
                Set data
                - package membership
                - command name
                - read the command file and extract all the other data
                """
                cd = CommandDescriptor()
                cd.package = package
                cd.name = command
                cd.read_command('{}{}/{}/{}.json'.format(dir_commands, package, command, command))

                # append command (command_descriptor, module, class_name)
                self.__command_list.append((cd, module, class_name))
                logger.info(class_name)

        del module

        """
        Structure of the command found
        Stored to be executed
        """
        self.__command_found = None
        self.error = ''
        self.language = None
        self.trigger = 'eng'
        self.arg = None
        self.params = {}

    def find_command(self, text: str, language: str):
        """
        Find if there is a command in the text
        N.B.: YOU HAVE TO REMOVE THE COMMAND CHAR/STR TRIGGER AND SEND CLEAN TEXT

        :param text: the message without the chat/str command invocation
        :param language: the language code for message response
        :return: True if there is a command else False
        """
        self.language = language

        self.__read_command_structure(text)

        for command in self.__command_list:
            command_descriptor, module, class_name = command
            if self.trigger in command_descriptor.invocation_words:
                self.__command_found = command
                return True

        return False

    @property
    def command(self):
        """
        Get the command item object to access to all the information of the command
        :return: command_descriptor
        """
        command_descriptor: CommandDescriptor
        command_descriptor, module, class_name = self.__command_found
        return command_descriptor

    def run_command(self, bot):
        """
        Execute the command
        :param bot: the bot var, that will be passed to the command. Used to send message and perform actions.
        If you have multiple params to pass to the command use a tuple inside the bot or a dict
        """
        command_descriptor, module, class_name = self.__command_found

        command_class = getattr(
            module,
            class_name
        )

        try:
            command = command_class(bot, self.language, command_descriptor, self.arg, self.params)
            command.run()
        except Exception as exc:
            print(exc)

    def __read_command_structure(self, text):
        """
        :param text: must be a string
        :return: argument as string, parameters as tuple [parameter, data]

        example:
        mal the cat is on the table -f lol this is cute -d 12
        """
        text_list = text.split()

        self.trigger = text_list.pop(0)  # remove the command trigger

        if len(text_list) is 1:
            self.arg = text_list[0]

        read_params = False
        current_param = None
        while text_list:
            word = text_list.pop(0)

            if str.startswith(word, '-'):
                read_params = True
                current_param = text_list[1:]
                self.params[current_param] = None

            elif read_params:
                self.params[current_param] += word + ' '

            else:
                self.arg += word + ' '
