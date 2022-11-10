"""
#####################################################################################################################

    Mattia Oct 2022   ~   Bot Telegram for Cooffe consumption in the office

#####################################################################################################################
"""

import 							telebot
import              pickle
import              os

with open( "TOKEN.txt", 'r' ) as f:
	TOKEN = f.read()
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


LOG                 = True
TOKEN               = None                                              # unique bot ID
LNAME               = "leaderboard.pickle"                              # pickle file to store the list of cookies
ONAME               = "log.txt"                                         # log file
score_dict          = dict()                                            # dict with the users and their scores

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['coffee'])
def send_coffee(message):
	'''
	username coffee
	@place   5
	'''
	bot.reply_to(message, "Coffee added for ... WIP")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)



# ===================================================================================================================
#
#   MAIN
#
# ===================================================================================================================

def main():

	if LOG:
		with open( ONAME, 'w' ) as olog:
			olog.write( ">>> BOT STARTED <<<\n" )
	else:
		print( ">>> BOT STARTED <<<" )

	# if exists, load the last pickled dict of leaderboard
	if os.path.isfile( LNAME ):
		with open( LNAME, "rb" ) as f:
			score_dict = pickle.load( f )

	bot.infinity_polling()

if __name__ == '__main__':
    main()
