"""
#####################################################################################################################

    Mattia Nov 2022   ~   Bot Telegram for Cooffe consumption in the office

#####################################################################################################################
"""

import os
import pickle

import telebot


# All the global variables
LOG          = True
TOKEN        = None                  # unique bot ID
PWORD        = None                  # unique password
LNAME        = "coffee_count.pickle" # pickle file to store the list of cookies
ANAME        = "admin_list.pickle"   # pickle file to store the list of admins
WNAME        = "warehouse.pickle"    # pickle file to store the list of cookies
RNAME        = "residual.pickle"     # pickle file to store the list of admins
ONAME        = "log.txt"             # log file
PWNAME       = "password.txt"        # password file 
admin_list   = dict()                # dict with superusers
coffee_count = dict()                # dict with the users and their scores
residuals    = dict()
warehouse    = dict()
coffee_emoji = "\U00002615"

# Trick to share bot as global variable
with open( "TOKEN.txt", 'r' ) as f:
	TOKEN = f.read()
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
with open( PWNAME, 'r' ) as f:
	PWORD = f.read()

def check_user( user, message ):
	""" -------------------------------------------------------------------------------------------------------------
	Check if user has @username
	------------------------------------------------------------------------------------------------------------- """
	if user in ( None, 'None' ):
		txt     = "ERROR: you must have a Telegram username to log coffee.\n"
		txt    += "You can set your username in the setting menu."
		bot.reply_to(message, txt )
		return False
	return True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	""" -------------------------------------------------------------------------------------------------------------
	Start bot or ask for help
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	if not check_user( user, message ):
		return
	txt     = "Welcom to Make Coffee Great Again" + coffee_emoji + "the coffee counter for special people!" 
	txt    += "add a coffee with /coffee ."
	txt    += "Check your coffee consumption with /stats . "
	txt    += "If you need help, type /help."
	bot.reply_to(message, txt)

@bot.message_handler(commands=['coffee'])
def add_coffee(message):
	""" -------------------------------------------------------------------------------------------------------------
	Add a coffee
	------------------------------------------------------------------------------------------------------------- """
	name = message.from_user.first_name
	user = message.from_user.username
	if user in coffee_count.keys():
		coffee_count[user] += 1
	else:
		coffee_count[user] = 1
	bot.reply_to(message, coffee_emoji + "Coffee added for " + name + " User: " + user)
	residuals["cialde_num"] = residuals["cialde_num"] - 1
	# save the dict
	with open( LNAME, 'wb' ) as f:
		pickle.dump( coffee_count, f, protocol=pickle.HIGHEST_PROTOCOL )
	with open( RNAME, 'wb' ) as f:
		pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )
	day     = int( message.date )
	if LOG:
		olog     = open( ONAME, 'a' )
    # get day and score
		olog.write( f"Day { day }\t{ user }\n" )
		olog.close()

@bot.message_handler(commands=['stats'])
def print_stats(message):
	""" -------------------------------------------------------------------------------------------------------------
	Print stats
	------------------------------------------------------------------------------------------------------------- """
	name = message.from_user.first_name
	user = message.from_user.username
	if user in coffee_count.keys():
		bot.reply_to(message, f"You owe N. {coffee_count[user]} coffee" + coffee_emoji)
	else:
		# add user with zero coffee
		coffee_count[user] = 0
		bot.reply_to(message, f"You owe N. {coffee_count[user]} coffee" + coffee_emoji)
	# save the dict
	with open( LNAME, 'wb' ) as f:
		pickle.dump( coffee_count, f, protocol=pickle.HIGHEST_PROTOCOL )

@bot.message_handler(commands=['globalstats'])
def print_global_stats(message):
	""" -------------------------------------------------------------------------------------------------------------
	Print stats global
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	txt = coffee_emoji + "Total consumption of coffee:\n\n"
	if user in admin_list.keys():
		for user_i in coffee_count.keys():
			avrg_price = residuals["avrg_price"]
			txt += f"{ user_i }. N.  { coffee_count[user_i] }   ({avrg_price*coffee_count[user_i]:2.2f} EURO ) \n"
		cialde_num = residuals["cialde_num"]
		txt += f"\nResidual cialde:  { cialde_num }. \n"
	bot.reply_to(message, txt)


# @bot.message_handler(commands=['warehouse'])
# def add_coffe_in_warehouse(message):
# 	""" -------------------------------------------------------------------------------------------------------------
# 	Print stats global
# 	------------------------------------------------------------------------------------------------------------- """
# 	user = message.from_user.username
# 	if user in admin_list.keys():
# 		args = extract_arg(message.text)
# 	bot.reply_to(message, "COSE")


@bot.message_handler(commands=['setprice'])
def set_avg_price(message):
	""" -------------------------------------------------------------------------------------------------------------
	Set average price of coffee
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	if user in admin_list.keys():
		args = extract_arg(message.text)
		residuals["avrg_price"] = float(args[0])
		# save the dict
		with open( RNAME, 'wb' ) as f:
			pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )
		bot.reply_to(message, "Changed average price of coffee")

@bot.message_handler(commands=['fill'])
def add_cialde_num(message):
	""" -------------------------------------------------------------------------------------------------------------
	Add number of cialde
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	if user in admin_list.keys():
		args = extract_arg(message.text)
		residuals["cialde_num"] += int(args[0])
		# save the dict
		with open( RNAME, 'wb' ) as f:
			pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )
		bot.reply_to(message, "Changed number of cialde")

@bot.message_handler(commands=['overridecialde'])
def set_cialde_num(message):
	""" -------------------------------------------------------------------------------------------------------------
	Set number of cialde
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	if user in admin_list.keys():
		args = extract_arg(message.text)
		residuals["cialde_num"] = int(args[0])
		# save the dict
		with open( RNAME, 'wb' ) as f:
			pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )
		bot.reply_to(message, "Changed number of cialde")


@bot.message_handler(commands=['sudo'])
def add_sudo(message):
	""" -------------------------------------------------------------------------------------------------------------
	Add sudo
	------------------------------------------------------------------------------------------------------------- """
	user = message.from_user.username
	if user in admin_list.keys():
		bot.reply_to(message, "User " + user + " is already in the admin list")
	else:
		bot.reply_to(message, "User " + user + " is not in the admin list")
		PW = extract_arg(message.text)[0]
		if PW == PWORD:
			admin_list[user] = True
			bot.reply_to(message, "Password correct. Now you are an admin")
		else:
			bot.reply_to(message, "Password wrong. Yow are not an admin")
	chatID = message.chat.id
	messID = message.message_id
	bot.delete_message(chatID, messID)
	# save the dict
	with open( ANAME, 'wb' ) as f:
		pickle.dump( admin_list, f, protocol=pickle.HIGHEST_PROTOCOL )

def extract_arg(arg):
	""" -------------------------------------------------------------------------------------------------------------
	Split arguments of message
	------------------------------------------------------------------------------------------------------------- """
	return arg.split()[1:]


def gen_markup():
	""" -------------------------------------------------------------------------------------------------------------
	gen markup
	------------------------------------------------------------------------------------------------------------- """
	# buttons 
	button_coffee = telebot.types.KeyboardButton('/coffee ' + coffee_emoji)
	button_stats = telebot.types.KeyboardButton('/stats')
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(button_coffee)
	markup.add(button_stats)
	return markup


@bot.message_handler(commands=['key'])
def addkey(message):
	bot.send_message(message.chat.id, message.text + "  Get keyboard", reply_markup=gen_markup())

@bot.message_handler(commands=['nokey'])
def rem_key(message):
    bot.send_message(message.chat.id, message.text + "  Remove keyboard", reply_markup = telebot.types.ReplyKeyboardRemove())

# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, message.text + "  ???", reply_markup=gen_markup())

# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
# 	cqd = call.data
# 	print(cqd)
# 	if cqd == 'cb_coffee':
# 		print("Enter in add coffe by button")
# 		add_coffee(call.message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	""" -------------------------------------------------------------------------------------------------------------
	Echo all messages not supported
	------------------------------------------------------------------------------------------------------------- """
	bot.reply_to(message, message.text)

# ===================================================================================================================
#
#   MAIN
#
# ===================================================================================================================

def main():
	global coffee_count
	global admin_list
	global warehouse
	global residuals

	if LOG:
		with open( ONAME, 'a' ) as olog:
			olog.write( ">>> BOT STARTED <<<\n" )
	else:
		print( ">>> BOT STARTED <<<" )

	# if exists, load the last pickled dict of coffee_count
	if os.path.isfile( LNAME ):
		with open( LNAME, "rb" ) as f:
			coffee_count = pickle.load( f )

	# if exists, load the last pickled dict of admin_list
	if os.path.isfile( ANAME ):
		with open( ANAME, "rb" ) as f:
			admin_list = pickle.load( f )

	if os.path.isfile( WNAME ):
		with open( WNAME, "rb" ) as f:
			warehouse = pickle.load( f )

	if os.path.isfile( RNAME ):
		with open( RNAME, "rb" ) as f:
			residuals = pickle.load( f )
			if "avrg_price" not in residuals.keys():
				residuals["avrg_price"] = 0
			if "cialde_num" not in residuals.keys():
				residuals["cialde_num"] = 0
			with open( RNAME, 'wb' ) as f:
				pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )
	else:
		residuals["avrg_price"] = 0
		residuals["cialde_num"] = 0
		# save the dict
		with open( RNAME, 'wb' ) as f:
			pickle.dump( residuals, f, protocol=pickle.HIGHEST_PROTOCOL )

	

	bot.infinity_polling()

if __name__ == '__main__':
    main()
