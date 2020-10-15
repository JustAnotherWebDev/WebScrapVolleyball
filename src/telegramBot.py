from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, time, json

json_file = open('util/security.json')
API_KEY = json.load(json_file)["telegram_token"]

json_file = open('util/security.json')
CHAT_ID = json.load(json_file)["chat_id"]

json_file = open('util/security.json')
DEV_CHAT_ID = json.load(json_file)["dev_chatid"]

def start(update, context):
  """Send a message when the command /start is issued."""
  update.message.reply_text('Hey I am going to inform you about new Cups posted on https://www.beachvolleyball.nrw/')

def help_command(update, context):
  """Send a message when the command /help is issued."""
  update.message.reply_text('Help-Function is not implemented yet!')

def send_message(message):
  url = f'https://api.telegram.org/bot{API_KEY}/sendMessage'
  data = {'chat_id': CHAT_ID, 'text': message}
  requests.post(url, data).json()
  time.sleep(2)

def send_message_no_cups_found():
  bot_message = 'There are no Cups that could be found even after 30 retries with a intervall of 60 seconds.\nPls look at the site or the programming, there seems to be a Problem!'
  send_text = f'https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={DEV_CHAT_ID}&parse_mode=Markdown&text={bot_message}'
  response = requests.get(send_text)
  return response.json()

def main():
  # Get the dispatcher to register handlers
  updater = Updater(API_KEY, use_context=True)
  dp = updater.dispatcher

  # on diffrent commands - answer in telegram
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help_command))

  # Start the Bot
  updater.start_polling()
  #updater.idle()