from pvlv.settings import *
from old_core.src.static_modules import db
from old_core.src.internal_log import Log
# listeners
from old_core.modules.user_data_handler import UserData
from old_core.modules.message_reply import Respond
from old_core.modules.bestemmia_reply import BestemmiaReply
from old_core.modules.badass_character_reply import BadAssCharacterReply
from old_core.modules.pickup_line_reply import PickupLineReply
# audio converter
from old_core.src.speech_to_text import speech_to_text
from pydub import AudioSegment


class Starter(object):

    def __init__(self, bot_abstraction):

        self.bot = bot_abstraction

        self.prefix_type = NO_PREFIX
        self.module_enabled = 1
        self.module_mode = 1

        self.in_text = ''

    def update(self, scope, real_bot, real_bot_message):

        self.bot.update_bot_data(scope, real_bot, real_bot_message)

        # update db data
        db.update_data(self.bot.scope, self.bot.guild.id, self.bot.user.id)

        self.bot.update_output_permission(db.guild.bot_paused)

        self.prefix_type = NO_PREFIX
        self.module_enabled = 1
        self.module_mode = 1

    @staticmethod
    def is_bot_disabled():
        if db.guild.bot_disabled is True:
            return True
        return False

    def _catch_prefix(self):
        """
        find and cut away the prefix
        """
        if str.startswith(self.in_text, db.guild.prefix):
            self.in_text = self.in_text[len(db.guild.prefix):]
            self.prefix_type = COMMAND_PREFIX

        elif str.startswith(self.in_text, db.guild.quiet_prefix):
            self.in_text = self.in_text[len(db.guild.quiet_prefix):]
            Log.modules_handler_prefix(self.bot.scope, self.bot.guild.id, self.bot.user.id, db.guild.quiet_prefix)
            self.prefix_type = OVERRIDE_PREFIX

        elif str.startswith(self.in_text, db.guild.sudo_prefix):
            self.in_text = self.in_text[len(db.guild.sudo_prefix):]
            Log.modules_handler_prefix(self.bot.scope, self.bot.guild.id, self.bot.user.id, db.guild.sudo_prefix)
            self.prefix_type = SUDO_PREFIX

        else:
            self.prefix_type = NO_PREFIX

    def _has_permissions(self, module_name):
        """
        check if there are the requisites to run the module (listener)
        """
        module = db.guild.modules.get(module_name)
        if module is None:
            field = db.guild.modules[module_name] = {}
            field['enabled'] = self.module_enabled
            field['module_mode'] = self.module_mode
            db.set_data()
        else:
            self.module_enabled = module.get('enabled')
            self.module_mode = module.get('module_mode')

        if self.prefix_type == SUDO_PREFIX:
            return True
        if self.module_enabled is DISABLED_MODE:
            return False
        if self.module_mode is DISABLED_MODE:
            return False
        if self.module_mode is QUIET_MODE and self.prefix_type == OVERRIDE_PREFIX:
            return True
        if self.module_mode is NORMAL_MODE or SPAM_MODE or AGGRESSIVE_MODE:
            return True
        return False

    def _natural_response(self):

        # don't analyze long messages
        if len(self.in_text) > MEX_MAX_LENGTH:
            return None

        output = ""

        if self._has_permissions('message_reply'):
            respond = Respond(
                self.bot,
                self.in_text,
                self.module_mode,
                self.prefix_type
            )
            output += respond.message_reply()

        if self._has_permissions('bestemmia_reply'):
            bestemmia_reply = BestemmiaReply()
            output += bestemmia_reply.message_reply(db.guild.languages[0], self.in_text)

        if self._has_permissions('badass_character_reply'):
            badass_character_reply = BadAssCharacterReply()
            output += badass_character_reply.message_reply(db.guild.languages[0], self.in_text)

        if self._has_permissions('pickup_line_reply'):
            pickup_line_reply = PickupLineReply()
            output += pickup_line_reply.message_reply(db.guild.languages[0], self.in_text)

        if output != "":
            self.bot.send_message(output, MSG_ON_SAME_CHAT, write_en=True)

    def _update_statistics(self, message_type, time_spent_extra=0):

        user_data = UserData(
            self.bot,
            db,
            db.guild.languages[0],
            self.in_text,
            message_type,
            self.prefix_type,
            db.user.deep_logging,
            time_spent_extra=time_spent_extra,
        )
        user_data.log_data()

    def analyze_image_message(self):
        self._update_statistics(IMAGE, time_spent_extra=5)

    def analyze_command_message(self, text):
        self.in_text = text
        self.prefix_type = COMMAND_PREFIX
        self._update_statistics(COMMAND)

    def analyze_vocal_message(self, raw_file, vocal_duration):

        raw_file.seek(0)
        ogg_audio = AudioSegment.from_ogg(raw_file)
        filename = 'audio.wav'
        ogg_audio.export(filename, format='wav')

        self.in_text = speech_to_text(filename, ITA)

        if self._has_permissions('speech_to_text'):
            t = 'SPEECH TO TEXT:\n{}'.format(self.in_text)
            self.bot.send_message(t, MSG_ON_SAME_CHAT, write_en=True)

        self._update_statistics(VOICE, time_spent_extra=vocal_duration*2)
        self._natural_response()

    def analyze_text_message(self, text):

        self.in_text = text
        self._catch_prefix()
        self._update_statistics(TEXT, time_spent_extra=5)
        self._natural_response()
