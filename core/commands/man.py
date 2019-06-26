from core.src.settings import (
    MSG_ON_SAME_CHAT
)
from core.src.command_reader import CommandReader
from core.src.static_modules import db
from core.src.text_reply.modules_reply_models import (
    man_invocation, man_handled_args, man_handled_params, man_command_mask
)
from core.src.text_reply.errors import arg_not_found_error


class Man(object):
    """
    """

    def __init__(self, bot, language, command, arg, params, *args, **kwargs):

        self.bot = bot
        self.language = language

        self.command = command
        self.arg = arg

        self.c_reader = CommandReader()

    def _build_title(self, command_function, command_name):
        out = '**{}**\n{}\n{}\n'.format(
            command_name.upper(),
            command_function.description,
            man_invocation(self.language, command_function.invocation_words)
        )
        return out

    def _build_args_params_list(self, title_function, dictionary):
        if dictionary != {}:
            out = '\n{}\n'.format(title_function(self.language))
            for key in dictionary.keys():
                key_description = dictionary.get(key)
                out += '**{}** -- {}\n'.format(
                    key if key != '' else 'void',
                    key_description
                )
            return out
        else:
            return ""

    def _build_full_man(self, command_name):

        try:
            self.c_reader.commands.read_command(self.language, command_name)
            out = self._build_title(self.c_reader.commands, command_name)
            out += self._build_args_params_list(man_handled_args, self.c_reader.commands.handled_args)
            out += self._build_args_params_list(man_handled_params, self.c_reader.commands.handled_params)
            return out

        except Exception as e:
            print(e)
            return e

    def _build_base_man(self, command_function, command_name):

        try:
            command_function.read_command(self.language, command_name)
            out = self._build_title(command_function, command_name)
            return out

        except Exception as e:
            print(e)
            return e

    def _print_found_command(self, command_function, command):
        try:
            command_name = command_function.key
            out = '{}\n{}'.format(
                self._build_title(command_function, command_name),
                man_command_mask(self.language, db.guild.prefix, command, command_function.sub_call)
            )
            return out

        except Exception as e:
            print(e)
            return e

    def man(self):

        out = ''
        if self.arg == '':
            out = self._build_full_man('man')

        elif self.arg == 'all':
            for key in self.c_reader.commands.commands_keys:
                out += '{}\n'.format(self._build_base_man(self.c_reader.commands, key))
            for key in self.c_reader.commands_shortcut.commands_keys:
                out += '{}\n'.format(self._build_base_man(self.c_reader.commands_shortcut, key))

        else:
            try:
                l, command_found, t = self.c_reader.get_command(db.guild.languages, self.arg)
            except Exception as e:
                print(e)
                return

            if command_found is None:
                out = arg_not_found_error(self.language)  # use guild main language
                self.bot.send_message(out, MSG_ON_SAME_CHAT, parse_mode_en=True)
                return

            if l is None:
                out = self._build_full_man(command_found)
            else:
                out = self._print_found_command(self.c_reader.commands_shortcut, command_found)

        self.bot.send_message(out, MSG_ON_SAME_CHAT, parse_mode_en=True)
