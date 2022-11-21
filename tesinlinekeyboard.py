from ast import In
from distutils.cmd import Command
import telebot
#Import telegram API
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler,Filters, JobQueue
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext


bot = telebot.TeleBot("5420307418:AAHF3IuTif8D8BR_HDyd8fFq6tL4WPfoL9w")
#tokenbot
tokenbot = "5420307418:AAHF3IuTif8D8BR_HDyd8fFq6tL4WPfoL9w" #diganti kalau reset token bot , untuk Asmentebot
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,text="Selamat datang di Virtual Assistant REWA (Reliable and Eco Warehouse")
    buttons = [[InlineKeyboardButton("JTM",callback_data="jtm")],
    [InlineKeyboardButton("JTR",callback_data="jtr")]]
    # [InlineKeyboardButton("MCCB",callback_data="mccb")],
    # [InlineKeyboardButton("Trafo",callback_data="trafo")]]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update,context):
    query = update.callback_query
    context.bot.send_message(text="Yang dipilih : %s" % query.data,chat_id = query.message.chat_id)
    if(query.data == "jtm"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material JTM berikut : ")
    elif(query.data == "jtr"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material JTR berikut : ")
        listjtr(query)
    elif(query.data == "app"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material APP berikut : ")
        listapp(query)
    elif(query.data == "kwh"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih Unit : ")
        listmeter(query)
def listjtr(query):
    buttons = [[InlineKeyboardButton("APP",callback_data="app")],
    [InlineKeyboardButton("SR",callback_data="sr")],[InlineKeyboardButton("SUTR",callback_data="sutr")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text('Silahkan pilih:', reply_markup=reply_markup)
def listapp(query):
    buttons = [[InlineKeyboardButton("kWh Meter",callback_data="kwh")],
    [InlineKeyboardButton("MCB",callback_data="mcb")],[InlineKeyboardButton("MCCB",callback_data="mccb")],[InlineKeyboardButton("NFB",callback_data="nfb")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def listmeter(query):
    buttons = [[InlineKeyboardButton("3P (5/80)",callback_data="3p")],
    [InlineKeyboardButton("1P Pascabayar",callback_data="1ppsc")],[InlineKeyboardButton("1P Prabayar",callback_data="1plpb")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def main():
    # Create updater and pass in Bot's auth key.
    updater = Updater(token=tokenbot, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher

    #calling predefined method
    dispatcher.add_handler(CommandHandler('start',start,run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # start the bot
    updater.start_polling()
    # Stop
    updater.idle()
if __name__ == '__main__':
    main()

