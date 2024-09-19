import time
import requests
import random
import urllib.parse
import os
from colorama import Fore, Style, init
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Set bot token
TOKEN = os.getenv("BOT_TOKEN")

# Initialize colorama
init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art():
    print("\033[1;92m" + r"""
                           _   
                          | |  
  ___ _ __ ___   __ _ _ __| |_ 
 / __| '_ ` _ \ / _` | '__| __|
 \__ | | | | | | (_| | |  | |_ 
 |___|_| |_| |_|\__,_|_|   \__|
                               
                               

 """ + "\033[0m" + "\033[1;92m" + r"""""" + "\033[0m" + "\033[1;92m" + r"""
  _______          _ 
 |__   __|        | |
    | | ___   ___ | |
    | |/ _ \ / _ \| |
    | | (_) | (_) | |
    |_|\___/ \___/|_|
                     
                     
                     """ + "\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;93mScript created by: SmaRt Tool HaNiF\033[0m\n\033[1;92mJoin Telegram: \https://t.me/smartoolhanif\033[0m\n\033[1;91mVisit my GitHub: \nhttps://github.com/smartoolhanif/\033[0m\n\033[1;96m---------------------------------------\033[0m\n\033[1;38;2;139;69;19;48;2;173;216;230m-------------[XKucoin Bot]-------------\033[0m\n\033[1;96m---------------------------------------\033[0m")

def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"{Fore.CYAN + Style.BRIGHT}Wait {hours:02}:{mins:02}:{secs:02}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Wait 00:00:00          ", end='\r')

def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))

    decoded_user = urllib.parse.unquote(params['user'])
    decoded_start_param = urllib.parse.unquote(params['start_param'])

    return {
        "decoded_user": decoded_user,
        "decoded_start_param": decoded_start_param,
        "hash": params['hash'],
        "auth_date": params['auth_date'],
        "chat_type": params['chat_type'],
        "chat_instance": params['chat_instance']
    }

def login(decoded_data):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3"
    }
    
    body = {
        "inviterUserId": "5496274031",
        "extInfo": {
            "hash": decoded_data['hash'],
            "auth_date": decoded_data['auth_date'],
            "via": "miniApp",
            "user": decoded_data['decoded_user'],
            "chat_type": decoded_data['chat_type'],
            "chat_instance": decoded_data['chat_instance'],
            "start_param": decoded_data['decoded_start_param']
        }
    }

    session = requests.Session()
    response = session.post(url, headers=headers, json=body)
    cookie = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])             
    return cookie

def data(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data").get("availableAmount")
    molecule = data.get("data").get("feedPreview").get("molecule")
    print(f"{Fore.GREEN + Style.BRIGHT}Balance: {Fore.WHITE + Style.BRIGHT}{balance}")
    return molecule

def tap(cookie, molecule):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }

    total_increment = 0

    while total_increment < 3000:
        increment = random.randint(55, 60)  # Randomize increment value each iteration
        form_data = {
            'increment': str(increment),
            'molecule': str(molecule)
        }

        response = requests.post(url, headers=headers, data=form_data)
        total_increment += increment
        
        colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.RED]
        random_color = random.choice(colors)
        print(f"{random_color}{Style.BRIGHT}▄︻┻═┳一: {Fore.WHITE + Style.BRIGHT}{increment} | {random_color}Total Tap ████████████████: {Fore.WHITE + Style.BRIGHT}{total_increment}/3000 {Style.RESET_ALL}")
        
        time.sleep(2)

def new_balance(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data").get("availableAmount")
    print(f"{Fore.MAGENTA + Style.BRIGHT}New Balance: {balance}")

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}, I'm XKucoin Bot. Choose an action:",
                              reply_markup=get_keyboard())

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # Callback data
    data = query.data

    if data == 'start_auto_tap':
        file_path = "data.txt"
        encoded_data_list = read_data_file(file_path)

        for index, encoded_data in enumerate(encoded_data_list, start=1):
            print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
            decoded_data = decode_data(encoded_data)
            cookie = login(decoded_data)
            molecule = data(cookie)
            tap(cookie, molecule)
            new_balance(cookie)

        query.answer("Auto Tap started!")
        query.edit_message_text(text="Auto Tap started! If you want to stop, press Stop Auto Tap button")

    elif data == 'stop_auto_tap':
        query.answer("Auto Tap stopped!")
        query.edit_message_text(text="Auto Tap stopped! If you want to start, press Start Auto Tap button")

    elif data == 'get_balance':
        file_path = "data.txt"
        encoded_data_list = read_data_file(file_path)

        for index, encoded_data in enumerate(encoded_data_list, start=1):
            print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
            decoded_data = decode_data(encoded_data)
            cookie = login(decoded_data)
            molecule = data(cookie)
            new_balance(cookie)

        query.answer("Balance updated!")
        query.edit_message_text(text="Balance updated! If you want to start, press Start Auto Tap button")

def auto_tap(update: Update, context: CallbackContext) -> None:
    """Handles the /autotap command."""
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)

    for index, encoded_data in enumerate(encoded_data_list, start=1):
        print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
        decoded_data = decode_data(encoded_data)
        cookie = login(decoded_data)
        molecule = data(cookie)
        tap(cookie, molecule)
        new_balance(cookie)

    update.message.reply_text("Auto Tap started! If you want to stop, use /stoptap command")

def stop_tap(update: Update, context: CallbackContext) -> None:
    """Handles the /stoptap command."""
    update.message.reply_text("Auto Tap stopped! If you want to restart, use /autotap command")

def get_balance(update: Update, context: CallbackContext) -> None:
    """Handles the /balance command."""
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)

    for index, encoded_data in enumerate(encoded_data_list, start=1):
        print(f"{Fore.CYAN + Style.BRIGHT}------Account No.{index}------")
        decoded_data = decode_data(encoded_data)
        cookie = login(decoded_data)
        molecule = data(cookie)
        new_balance(cookie)

    update.message.reply_text("Balance updated! If you want to start auto-tap, use /autotap command.")

def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Start Auto Tap", callback_data='start_auto_tap'),
            InlineKeyboardButton("Stop Auto Tap", callback_data='stop_auto_tap'),
        ],
        [InlineKeyboardButton("Get Balance", callback_data='get_balance')],
    ]
    return InlineKeyboardMarkup(keyboard)

def main() -> None:
    """Starts the bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("autotap", auto_tap))
    dispatcher.add_handler(CommandHandler("stoptap", stop_tap))
    dispatcher.add_handler(CommandHandler("balance", get_balance))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
