from core.src.settings import *
from core.src.static_modules import db
from core.bot_abstraction import BotStd
from datetime import datetime
import math


class UserDataLog(object):

    def __init__(
            self,
            bot,
            language,
            text,
            message_type,
            prefix_type,
            time_spent_extra=0
    ):
        self.bot = bot
        self.language = language
        self.text = text
        self.text_len = len(text)
        self.message_type = message_type
        self.prefix_type = prefix_type

        self.time_spent_extra = time_spent_extra

    def __send_level_up_message(self, level, destination):

        if self.language == ITA:
            message = 'Grande {}\nHai raggiunto il livello {}'.format(self.bot.user.username, level)
        else:
            message = 'Cool {}\nYou\'ve gain to level {}'.format(self.bot.user.username, level)

        ms = BotStd()
        ms.send_message(message, destination)

    def log_data(self):

        db.user_name = self.bot.user.username

        now = datetime.utcnow()

        time_spent_to_type = math.ceil(self.text_len * TIME_SAMPLE_VALUE / SAMPLE_STRING_LEN) + self.time_spent_extra
        db.update_msg(now, time_spent_to_type)

        xp_by_string_len = int(math.ceil(self.text_len * XP_SAMPLE_VALUE / SAMPLE_STRING_LEN))
        xp_add = xp_by_string_len if xp_by_string_len <= XP_MAX_VALUE else XP_MAX_VALUE
        db.update_xp(xp_add)

        if db.is_user_level_up():
            destination = db.user_level_up_destination()
            if destination != MSG_DISABLED:
                self.__send_level_up_message(db.level, destination)

        if db.is_user_global_level_up():
            destination = db.user_global_level_up_destination()
            if destination != MSG_DISABLED:
                self.__send_level_up_message(db.global_level, destination)

        bits_by_string_len = int(math.ceil(self.text_len * BITS_SAMPLE_VALUE / SAMPLE_STRING_LEN))
        bits_add = bits_by_string_len if bits_by_string_len <= BITS_MAX_VALUE else BITS_MAX_VALUE
        db.update_bits(bits_add)

        db.update_messages_by_type(self.message_type, self.prefix_type)

        db.set_data()
