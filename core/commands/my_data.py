from core.src.settings import *
from core.src.static_modules import db
from core.src.text_reply.formatting import (
    sec_to_time_string, my_data_description, my_data_subtitle, weekdays_string
)
from core.src.utils.img_draw import DrawGraph
from datetime import datetime, timedelta, date
from calendar import monthrange


class MyData(object):
    """
    """

    def __init__(self, bot, language, command, arg, params, *args, **kwargs):

        self.bot = bot
        self.language = language

        self.command = command
        self.arg = arg

    def __build_data(self, time_array, msg_array, time_spent_array, timezone, max_len, time_scope):

        data = [[], [], [], []]

        if time_scope == 'hourly':
            now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

            def now_offset(diff): return now - timedelta(hours=diff)

            def condition(element, time):
                if element != time:
                    return True
                return False

            def colon_names(time_z): return '{}h'.format(time_z.hour)

        elif time_scope == 'daily':
            now = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

            def now_offset(diff): return now - timedelta(days=diff)

            def condition(element, time):
                if element != time:
                    return True
                return False

            def colon_names(time_z): return '{}\n{}/{}'.format(
                weekdays_string(time_z.weekday(), 0, self.language),
                time_z.day,
                time_z.month
            )

        else:
            now = datetime.utcnow()

            def now_offset(diff):
                month = now.month - 1 + diff
                year = now.year + month // 12
                month = month % 12 + 1
                day = min(now.day, monthrange(year, month)[1])
                return date(year, month, day)

            def condition(element, time):
                if element.month != time.month:
                    return True
                return False

            def colon_names(time_z): return '{}/{}'.format(time_z.month, time_z.year)

        t = iter(time_array)
        el = next(t, None)

        for offset in range(0, max_len):

            n = now_offset(offset)
            tz = n + timedelta(hours=timezone)
            if el is None or condition(el, n):
                data[0].append(colon_names(tz))
                data[1].append(0)
                data[2].append(0)
                data[3].append(sec_to_time_string(0, self.language, True))
            else:
                data[0].append(colon_names(tz))
                i = time_array.index(el)
                data[1].append(msg_array[i])
                data[2].append(time_spent_array[i]/2)
                data[3].append(sec_to_time_string(time_spent_array[i], self.language, True))
                el = next(t, None)

        section = {
                'section_title': time_scope.upper(),
                'graph_1': {
                    'subtitle': my_data_subtitle(self.language, time_scope),
                    'x_names': data[0],
                    'tower_1': {
                        'data': data[1],
                        'value_printed': data[1],
                        'printed_position': 'on_top',
                        'tower_dim': 1,
                        'color': DEFAULT_TOWER_1_COLOR
                    },
                    'tower_2': {
                        'data': data[2],
                        'value_printed': data[3],
                        'printed_position': 'on_top',
                        'tower_dim': 0.5,
                        'color': DEFAULT_TOWER_2_COLOR
                    },

                },
                'description': my_data_description(self.language, time_scope, sum(data[1]), sum(data[2]))
            }

        return section

    def my_data_pro(self):

        hourly_n_show = 18
        daily_n_show = 7
        monthly_n_show = 6

        if self.arg == "":
            title = self.bot.user.username
            timezone = 2

            log_time_by_hour = db.user.msg.log_time_by_hour
            by_hour = db.user.msg.by_hour
            time_spent_by_hour = db.user.msg.time_spent_by_hour

            log_time_by_day = db.user.msg.log_time_by_day
            by_day = db.user.msg.by_day
            time_spent_by_day = db.user.msg.time_spent_by_day

            log_time_by_month = db.user.msg.log_time_by_month
            by_month = db.user.msg.by_month
            time_spent_by_month = db.user.msg.time_spent_by_month

        elif self.arg.lower() == "guild":
            title = self.bot.guild.guild_name
            timezone = 2

            log_time_by_hour = db.guild.msg.log_time_by_hour
            by_hour = db.guild.msg.by_hour
            time_spent_by_hour = db.guild.msg.time_spent_by_hour

            log_time_by_day = db.guild.msg.log_time_by_day
            by_day = db.guild.msg.by_day
            time_spent_by_day = db.guild.msg.time_spent_by_day

            log_time_by_month = db.guild.msg.log_time_by_month
            by_month = db.guild.msg.by_month
            time_spent_by_month = db.guild.msg.time_spent_by_month

        elif self.arg.lower() == "global":
            title = self.bot.user.username + "\nGlobal Data"
            timezone = 2

            log_time_by_hour = db.user_global.msg.log_time_by_hour
            by_hour = db.user_global.msg.by_hour
            time_spent_by_hour = db.user_global.msg.time_spent_by_hour

            log_time_by_day = db.user_global.msg.log_time_by_day
            by_day = db.user_global.msg.by_day
            time_spent_by_day = db.user_global.msg.time_spent_by_day

            log_time_by_month = db.user_global.msg.log_time_by_month
            by_month = db.user_global.msg.by_month
            time_spent_by_month = db.user_global.msg.time_spent_by_month

        else:
            return

        dictionary_graph = {
            'top_title': title,
            'section_1': self.__build_data(
                log_time_by_hour,
                by_hour,
                time_spent_by_hour,
                timezone,
                hourly_n_show,
                'hourly'
                )
        }

        if len(log_time_by_day) > 2:
            dictionary_graph['section_2'] = self.__build_data(
                log_time_by_day,
                by_day,
                time_spent_by_day,
                timezone,
                daily_n_show,
                'daily'
            )

        if len(log_time_by_month) > 0:
            dictionary_graph['section_3'] = self.__build_data(
                log_time_by_month,
                by_month,
                time_spent_by_month,
                timezone,
                monthly_n_show,
                'monthly'
            )

        dg = DrawGraph(dictionary_graph)
        dg.draw_graph()
        img_bytes = dg.get_image()

        self.bot.send_image(img_bytes, MSG_ON_SAME_CHAT)

    def my_data(self):

        if self.arg.upper() == 'PRO':
            self.my_data_pro()
            return

        self.my_data_pro()
