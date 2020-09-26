import telebot

mode_kb = telebot.types.InlineKeyboardMarkup()
mode_kb.row(telebot.types.InlineKeyboardButton('With referee', callback_data='mode-r'))
mode_kb.row(telebot.types.InlineKeyboardButton('With timer', callback_data='mode-t'))

help_kb = telebot.types.InlineKeyboardMarkup()
help_kb.add(telebot.types.InlineKeyboardButton('Rules of Twister',
                                                url = 'https://www.math.uni-bielefeld.de/~sillke/Twister/rules/ '))

time_kb = telebot.types.InlineKeyboardMarkup()
time_kb.row(telebot.types.InlineKeyboardButton('20 seconds', callback_data='20sec'))
time_kb.row(telebot.types.InlineKeyboardButton('30 seconds', callback_data='30sec'))
time_kb.row(telebot.types.InlineKeyboardButton('45 seconds', callback_data='45sec'))

referee_kb = telebot.types.InlineKeyboardMarkup()
referee_kb.row(telebot.types.InlineKeyboardButton('continue', callback_data='continue'),
               telebot.types.InlineKeyboardButton('break', callback_data='break'))