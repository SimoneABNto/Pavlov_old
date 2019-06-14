

ERROR = -1

# debug
USE_GLOBAL_FILE_ONLY = True  # deprecated


TELEGRAM = 'telegram'
DISCORD = 'discord'

# Languages Handled for messages
ITA = 'ita'
ENG = 'eng'


# message max length for analyze
MEX_MAX_LENGTH = 70


# situational reply settings
AVOID_REPLY = 0
STD_REPLAY = 1
POWER_REPLAY = 2
STATIC_REPLAY = 3
STATIC_SPLIT_KEY = '&&&'
STATIC_SPLIT_MODE = '%%%'
STATIC_OVERRIDE_MODE = '!'


# CONFIGURATION SETTINGS
# prefix type
NO_PREFIX = -1
COMMAND_PREFIX = 0
OVERRIDE_PREFIX = 1
SUDO_PREFIX = 2

# global setting for auto reply commands
DISABLED_MODE = -1
QUIET_MODE = 0
NORMAL_MODE = 1
SPAM_MODE = 2
AGGRESSIVE_MODE = 3

# module type, to define the scope of the module
TYPE_LISTENER = 0
TYPE_COMMAND = 1


# ERRORS CONFIG
# message_reply_error
WRONG_STATIC_MODE_STRING = 1


# USER_DATA_LOG CONFIG
SAMPLE_STRING_LEN = 30
# Time spent to type
TIME_SAMPLE_VALUE = 11
# XP gain by message
XP_SAMPLE_VALUE = 20
XP_MAX_VALUE = 30

# BITS gain by message
BITS_SAMPLE_VALUE = 5
BITS_MAX_VALUE = 2
# XP for next level
XP_NEXT_LEVEL = 450
# User MESSAGE destination
MSG_DISABLED = 0
MSG_DIRECT = 1
MSG_ON_SAME_CHAT = 2
MSG_ON_STATIC_CHAT = 3
