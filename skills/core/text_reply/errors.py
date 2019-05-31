from skills.core.settings import *


def command_error(language):
    if language is ITA:
        return 'Questo non è un comando.'
    else:  # auto fall back on english
        return 'This is not a command.'


def command_not_implemented(language):
    if language is ITA:
        return 'Questo comando non è ancora stato implementato.'
    else:  # auto fall back on english
        return 'This is not implemented jet.'


def parse_error(language, argument, suggestion):
    if language is ITA:
        return 'Il valore: "{}" non è valido.\nProva ad usare "{}"'.format(argument, suggestion)
    else:  # auto fall back on english
        return 'The value: "{}" is not valid.\nTry something like "{}"'.format(argument, suggestion)


WRONG_STATIC_MODE_STRING = 1


def message_reply_error(language, error_type, trigger=None):
    if language is ITA:
        if error_type is WRONG_STATIC_MODE_STRING:
            return 'Sintassi errata nel trigger: {}\nSTATIC_OVERRIDE_MODE: {}{}{}\nSTATIC_SPAM_MODE: {}{}{}'.format(
                trigger,
                STATIC_SPLIT_MODE, STATIC_OVERRIDE_MODE, STATIC_SPLIT_MODE,
                STATIC_SPLIT_MODE, STATIC_SPAM_MODE, STATIC_SPLIT_MODE
            )
    else:  # auto fall back on english
        if error_type is WRONG_STATIC_MODE_STRING:
            return 'Wrong syntax in trigger {}\nSTATIC_OVERRIDE_MODE: {}{}{}\nSTATIC_SPAM_MODE: {}{}{}'.format(
                trigger,
                STATIC_SPLIT_MODE, STATIC_OVERRIDE_MODE, STATIC_SPLIT_MODE,
                STATIC_SPLIT_MODE, STATIC_SPAM_MODE, STATIC_SPLIT_MODE
            )




