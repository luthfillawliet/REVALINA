import datetime
from matplotlib.pyplot import text
from pytz import HOUR
from telegram.ext import Updater, CommandHandler
import logging
import redis



updater = Updater(token='5420307418:AAHF3IuTif8D8BR_HDyd8fFq6tL4WPfoL9w', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

j = updater.job_queue
chatid = 1029804860

# writting functionality of the command
def start(update, context):
    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
def once(context):
    message = "Hello world"
    context.bot.send_message(chat_id=chatid,text=message)
# give a name to the command and add it to the dispaatcher
start_handler = CommandHandler('start', start)
t = datetime.time(8,9,00)
jobdaily = j.run_daily(once,time=t,days=(0,1,2,3,4,5,6))
dispatcher.add_handler(start_handler)
updater.start_polling() # enable bot to get updates
updater.idle()