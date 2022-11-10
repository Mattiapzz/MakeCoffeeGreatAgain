"""
#####################################################################################################################

    Mattia Oct 2022   ~   Bot Telegram for Cooffe consumption in the office

#####################################################################################################################
"""

import telebot
import pickle
import os

with open( "TOKEN.txt", 'r' ) as f:
	TOKEN = f.read()
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


LOG         = True
TOKEN       = None                                              # unique bot ID
LNAME       = "leaderboard.pickle"                              # pickle file to store the list of cookies
ONAME       = "log.txt"                                         # log file
coffee_count = dict()                                            # dict with the users and their scores

def check_user( user, message ):
	""" -------------------------------------------------------------------------------------------------------------
	Check if user has @username
	------------------------------------------------------------------------------------------------------------- """
	if user in ( None, 'None' ):
		txt     = "ERROR: you must have a Telegram username to play.\n"
		txt    += "You can set your username in the setting menu."
		bot.reply_to(message, txt )
		return False
	return True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	user = message.from_user.username
	if not check_user( user, message ):
		return
	bot.reply_to(message, "Welcom to Make Coffee Great Again the coffee counter for special people!")

@bot.message_handler(commands=['coffee'])
def add_coffee(message):
	name = message.from_user.first_name
	user = message.from_user.username
	if user in coffee_count.keys():
		coffee_count[user] += 1
	else:
		coffee_count[user] = 1
	bot.reply_to(message, "Coffee added for " + name + " User: " + user)
	
	# save the dict
	with open( LNAME, 'wb' ) as f:
		pickle.dump( coffee_count, f, protocol=pickle.HIGHEST_PROTOCOL )

	sent_txt    = message.text
	day     = int( sent_txt.split( "\n" )[ 0 ].split()[ 1 ] )
	if LOG:
		olog     = open( ONAME, 'a' )
    # get day and score
		olog.write( f"Day { day }\t{ user }\n" )
		olog.close()

@bot.message_handler(commands=['stats'])
def add_coffee(message):
	name = message.from_user.first_name
	user = message.from_user.username
	bot.reply_to(message, f"You owe N. {coffee_count[user]} coffee")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)



# ===================================================================================================================
#
#   MAIN
#
# ===================================================================================================================

def main():
	global coffee_count

	if LOG:
		with open( ONAME, 'w' ) as olog:
			olog.write( ">>> BOT STARTED <<<\n" )
	else:
		print( ">>> BOT STARTED <<<" )

	# if exists, load the last pickled dict of leaderboard
	if os.path.isfile( LNAME ):
		with open( LNAME, "rb" ) as f:
			coffee_count = pickle.load( f )

	bot.infinity_polling()

if __name__ == '__main__':
    main()
