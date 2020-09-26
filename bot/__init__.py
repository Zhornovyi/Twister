import telebot
from Player import Player
from Game import Game

from pymongo import MongoClient
import bot.db_script as db
import bot.keyboards as kb

import config
import logging
import time

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

#   Data base connection
client = MongoClient('localhost', 27017)
database = client['UserDB']
user_collection = database['users']

bot = telebot.TeleBot(config.TOKEN)

class END(Exception):
    pass
@bot.message_handler(commands=['new_game'])
def start_game(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    # if user doesn't exist in db, add him
    if db.find_document(user_collection, {'_id':user_id}) == None:
        db.insert_document(user_collection, {'_id': user_id,'username': message.from_user.username})

    bot.send_message(chat_id,"Hey, Let`s start a game!\n" + "Send me,please, first player's name")
    db.update_document(user_collection, {'_id': user_id}, {'pl_names': []})
    bot.register_next_step_handler(message, get_names)

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Information about help menu will be published later", reply_markup = kb.help_kb)

@bot.message_handler(commands=['end'])
def end_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    logger.info(str(user_id)+ "end")
    bot.send_message(chat_id, "Unbelievable! So fast game! Try one more time!")
    db.delete_document(user_collection, {'_id':user_id})



@bot.callback_query_handler(func=lambda call: True)
def callback(query):
   data = query.data
   bot.answer_callback_query(query.id)
   user_id = query.from_user.id
   chat_id = query.message.chat.id

   if data.startswith('mode-'):
       db.update_document(user_collection, {'_id': user_id}, {'mode': data[5:]})
       start(query)

   if data.endswith('sec'):
        timer = int(data[:-3])
        game = game_load(query)
    #timer mode handler
        while True:
            for i, pl in enumerate(game.players):
                text = pl.name+' : '+ game.get_move_str(i)
                bot.send_message(chat_id, text)
                time.sleep(timer)
                if not db.find_document(user_collection, {'_id':user_id}):
                    return
    # referee mode handler
   if  data =='continue':
       game = game_load(query)
       if game:
        edit_message_callback(query, game)

   if data == 'break':
       bot.send_message(chat_id, "Unbelievable! So fast game! Try one more time!")
       db.delete_document(user_collection, {'_id': user_id})

def get_names(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    names = db.find_document(user_collection,{'_id' : user_id})['pl_names']
    names.append(message.text)
    db.update_document(user_collection, {'_id': user_id}, {'pl_names': names})
    if len(names)==1:
        bot.send_message(chat_id,"Got it, second player's name")
        bot.register_next_step_handler(message, get_names)
    else:
        bot.send_message(chat_id, "Choose a game mode:", reply_markup = kb.mode_kb)

def game_load(query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    curr_user = db.find_document(user_collection,{'_id' : user_id})
    if not curr_user:
        bot.send_message(chat_id, "You have finished the game. To start new game, send me /new_game command.")
        return
    players = []
    for i,n in enumerate(curr_user['pl_names']):
        players.append(Player(n,i))
    return Game(players, curr_user['mode'])

def start(query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    curr_user = db.find_document(user_collection, {'_id' : user_id})

    if curr_user['mode'] == 't':
        bot.send_message(chat_id,"You chose game mode with timer. To end the game send me \end command")
        bot.send_message(chat_id, "Please choose how much time do you need between turns", reply_markup = kb.time_kb)

    elif curr_user['mode'] == 'r':
        db.update_document(user_collection, {'_id': user_id}, {'queue': 0})
        bot.send_message(chat_id, "Game will be started after button click", reply_markup=kb.referee_kb)

def edit_message_callback(query, game):
    user_id = query.from_user.id
    logger.info(str(user_id)+"emc")
    curr_user = db.find_document(user_collection, {'_id': user_id})
    queue = curr_user['queue']
    text = game.get_move_str(queue)
    name = game.players[queue].name
    db.update_document(user_collection, {'_id': user_id}, {'queue': queue^1})

    if query.message:
        bot.edit_message_text(
            name + " : " + text,
            query.message.chat.id,
            query.message.message_id,
            reply_markup = kb.referee_kb,
            parse_mode='HTML')

if __name__ == '__main__':
    bot.polling(none_stop=True)
