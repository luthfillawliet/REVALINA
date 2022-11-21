#Import selenium webdriver
from turtle import update
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
#import option untuk mwngolah file hasil download
from selenium.webdriver.chrome.options import Options
#Import telegram API
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
#Import request untuk kirim screenshoot
import requests
#Import pywinauto
from pywinauto.application import Application
 #Import pyautogui
import pyautogui
#Import pandas for processing xls data
import pandas as pd
#import datetime library
import datetime
#IMport for accessing file
#access file
import glob
import os
#import CLass INFOMATERIAL
import INFOMATERIAL
import time
# Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Defining prerequirement parameter
#Defining filepath for chromewebdriver
#PATH = "C:\\Users\\WIN 10\\Documents\\SAP\\MS Rewa\\chromedriver.exe"   #pathchromedriver file
PATH = r"C:\Users\server-pc\Documents\SAP\MS Rewa\chromedriver.exe"   #pathchromedriver file
#direktori penyimpanan screenshoot
direktori = "C:\\Users\\server-pc\\Documents\\SAP\\MS Rewa"
#tokenbot = "5433101545:AAGiab3E_U1GyimzWqxQZUMDHPrcEmbq4vY" #rewa backup
tokenbot = "5420307418:AAHF3IuTif8D8BR_HDyd8fFq6tL4WPfoL9w" #diganti kalau reset token bot , untuk Asmentebot
#chatid Telegram Luthfil
#chatid = 1029804860
chatid = -1001587497550
currentmonth = datetime.datetime.now().month
currentyear = datetime.datetime.now().year
days = (0,1,2,3,4,5,6)
#eksekusi waktu pertama
t = datetime.time(6,8,00) #pake jam GMT
#eksekusi waktu ke 2
t2 = datetime.time(3,26,00)

#coordinat screenshoot
x1,y1 = 130,291
x2,y2 = 648,599
#FIlename report harian
filenamereportharian = "reportharian.xlsx"

showdelay = 12
showdelayfull = 19
spreadsheetdelay = 7
spreadsheetdelayfull = 18
downloaddelay = 5
downloaddelayfull = 30
#Filepathexcel
filepathexcel = 'C:\\Users\\server-pc\\Documents\\SAP\\SAP GUI\\export.xlsx'
pathori = "C:\\Users\\server-pc\\Documents\\SAP\\MS Rewa\\TX\\"
pathtx = "C:\\Users\\server-pc\\Documents\\SAP\\MS Rewa\\"
chrome_options = Options()
#chrome_options.add_argument(r"C:\Users\server-pc\AppData\Local\Google\Chrome\User Data")
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": pathtx,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "user-data-dir":"C:\\Users\\server-pc\\AppData\\Local\\Google\\Chrome\\User Data"
    }
)
def sendScreenshoot(query,hasilbaca):
    if(hasilbaca == "berhasil"):
        files = {"photo" : open(direktori+"\\range.png", "rb")}
        resp = requests.post("https://api.telegram.org/bot"+tokenbot+"/sendPhoto?chat_id="+str(query.message.chat_id), files=files)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,text="Selamat datang di Virtual Assistant REWA (Reliable and Eco Warehouse")
    buttons = [[InlineKeyboardButton("TM",callback_data="tm")],
    [InlineKeyboardButton("TR",callback_data="tr")],[InlineKeyboardButton("APP",callback_data="app")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update,context):
    query = update.callback_query
    context.bot.send_message(text="Yang dipilih : %s" % query.data,chat_id = query.message.chat_id)
    if(query.data == "tm"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material JTM berikut : ")
        listm(query=query)
    elif(query.data == "tr"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material JTR berikut : ")
        listjtr(query)
  #=================================== APP ============================================
    elif(query.data == "app"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list material APP berikut : ")
        listapp(query)
    #================================kWH meter========================
    elif(query.data == "kwh"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih Unit : ")
        listmeter(query)
    elif(query.data == "2190224"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter LPB 1P 5/60")
        hasilbaca = material(currentmonth,currentyear,query.data)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material kWh LPB 1P (5/60): "+hasilbaca)
        sendScreenshoot(query,hasilbaca)
    elif(query.data == "2190231"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 1P 5/40")
        hasilbaca = material(currentmonth,currentyear,query.data)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material kWh Pasca 1P (5/40): "+hasilbaca)
        sendScreenshoot(query,hasilbaca)
    elif(query.data == "2190218"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 3P 5/80")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2190253"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 3P 5/10 A 230/400 V (1)")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2190438"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 3P 5A 57/100-240 V (0.5)")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2190219"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 3P 5A-10A 57/100-240 V (0.5)")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2190264"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP kWh meter Pascabayar 3P 5A-10A 57/100-240/415 V (0.2)")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)

  #================================ Pembatas ========================
    elif(query.data == "pembatas"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list pembatas berikutt : ")
        pembatas(query)
    #================================MCB========================
    elif(query.data == "mcb"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list MCB berikut : ")
        mcb(query)
    elif(query.data == "3250046"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 2A")
        hasilbaca = material(currentmonth,currentyear,3250046)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250048"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 4A")
        hasilbaca = material(currentmonth,currentyear,3250048)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250050"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 6A")
        hasilbaca = material(currentmonth,currentyear,3250050)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250052"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 10A")
        hasilbaca = material(currentmonth,currentyear,3250052)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250054"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 16A")
        hasilbaca = material(currentmonth,currentyear,3250054)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250056"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 20A")
        hasilbaca = material(currentmonth,currentyear,3250056)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250058"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 25A")
        hasilbaca = material(currentmonth,currentyear,3250058)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250060"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB 50A")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
        
    #================================MCCB========================
    elif(query.data == "mccb"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list MCB berikut : ")
        mccb(query)
    elif(query.data == "3250097"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB  3 Ph _ 10 A")
        hasilbaca = material(currentmonth,currentyear,3250097)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250099"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB  3 Ph _ 16 A")
        hasilbaca = material(currentmonth,currentyear,3250099)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250100"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB  3 Ph _ 20 A")
        hasilbaca = material(currentmonth,currentyear,3250100)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250102"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB  3 Ph _ 25 A")
        hasilbaca = material(currentmonth,currentyear,3250102)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250103"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCB  3 Ph _ 35 A")
        hasilbaca = material(currentmonth,currentyear,3250103)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #========================================NFB==========================
    elif(query.data == "3250034"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP  MCCB 380/440V;;3P;;80A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250034)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250063"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCCB 380/440V;;3P;;100A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250063)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250064"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCCB 380/440V;;3P;;125A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250064)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250023"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCCB 380/440V;;3P;;160A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250023)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250076"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCCB 380/440V;;3P;;200A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250076)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3250077"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MCCB 380/440V;;3P;;225A;;50 Hz")
        hasilbaca = material(currentmonth,currentyear,3250077)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
  #================================= PANEL / BOX APP ==================
    elif(query.data == "panel"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list Panel berikut : ")
        panel(query)
    elif(query.data == "4120005"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;PENGUKURAN   LANGSUNG TR")
        hasilbaca = material(currentmonth,currentyear,4120005)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120463"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;KWH PJU")
        hasilbaca = material(currentmonth,currentyear,4120463)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120263"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;; KWH;;TR_ PUSAT;;9;;TITIK")
        hasilbaca = material(currentmonth,currentyear,4120263)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120262"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;; KWH;;TR_ PUSAT;;12;;TITIK")
        hasilbaca = material(currentmonth,currentyear,4120262)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120102"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  53 KVA")
        hasilbaca = material(currentmonth,currentyear,4120102)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120321"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  66 KVA")
        hasilbaca = material(currentmonth,currentyear,4120321)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120284"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  82,5 KVA")
        hasilbaca = material(currentmonth,currentyear,4120284)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120285"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  105  KVA")
        hasilbaca = material(currentmonth,currentyear,4120285)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120286"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  131  KVA")
        hasilbaca = material(currentmonth,currentyear,4120286)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120287"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  164 KVA")
        hasilbaca = material(currentmonth,currentyear,4120287)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120288"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX;;APP;;Pengukuran Tdk Langsung  197 KVA")
        hasilbaca = material(currentmonth,currentyear,4120288)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120015"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP GARDU MENARA  SUSUN")
        hasilbaca = material(currentmonth,currentyear,4120015)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120402"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX PANEL SPLU TYPE WALL 1 Kwh")
        hasilbaca = material(currentmonth,currentyear,str(query.data))
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "4120235"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP BOX PANEL SPLU TYPE HOOK 2 Kwh")
        hasilbaca = material(currentmonth,currentyear,str(query.data))
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
 #================================= Kawat penghantar  kabel ==================
    #================================= SR ==================
    elif(query.data == "sr"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list SR berikut : ")
        sr(query)
    elif(query.data == "3110025"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL TWISTED__TC 2 x 10 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110026"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL TWISTED__TC 2 x 16 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= LVTC ==================
    elif(query.data == "lvtc"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list LVTC berikut : ")
        lvtc(query)
    elif(query.data == "3110039"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL LVTC 4 x 35 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110542"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL LVTC 4 x 70 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "nyy"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list NYY berikut : ")
        nyy(query)
    elif(query.data == "3110514"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL NYY 1 x 70 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110515"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL NYY 1 x 95 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110516"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP KABEL NYY 1 x 150 mm2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= XLPE ==================

  #================================= TM ===================================
    #================================= TM ==================
    elif(query.data == "sutm"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list SUTM berikut : ")
        sutm(query)
    elif(query.data == "3050001"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP A3C 150")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3050006"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP A3Cs 150")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3050050"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP A3CS 240")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3050081"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP A3C 70")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3050088"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP A3CS 70")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= Trafo ==================
    elif(query.data == "trafo"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list Trafo berikut : ")
        trafo(query)
    elif(query.data == "1030116"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_50 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "1030074"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_100 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "1030075"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_160 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "1030076"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_200 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "1030077"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_250 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "1030079"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP Trafo 3 Ph_400 kVA")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= Isolator ==================
    elif(query.data == "isolator"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list Isolator berikut : ")
        isolator(query)
    elif(query.data == "3070151"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP ISOLATOR TUMPU PORCELIN")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3070152"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP ISOLATOR TUMPU POLYMER")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3070160"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP ISOLATOR ASFAN PORCELIN")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3070154"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP ISOLATOR ASFAN POLYMER")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= FCO & Arrester ==================
    elif(query.data == "fco"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list FCO dan Arrester berikut : ")
        fco(query)
    elif(query.data == "3190002"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP FUSE CUT OUT POLYMER")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2090032"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP LIGTHING ARRESTER POLYMER")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "2030022"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP DISCONNECTING SWITCH 630 AMPER")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= XLPE ==================
    elif(query.data == "xlpe"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list XLPE berikut : ")
        xlpe(query)
    elif(query.data == "3110014"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP XLPE 150 MM2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110015"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP XLPE 240 MM2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    #================================= MVTIC ==================
    elif(query.data == "mvtic"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Silahkan pilih list MVTIC berikut : ")
        mvtic(query)
    elif(query.data == "3110034"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MVTIC 150 MM2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
    elif(query.data == "3110526"):
        context.bot.send_message(chat_id=query.message.chat_id,text="Memulai cek saldo realtime SAP MVTIC 240 MM2")
        hasilbaca = material(currentmonth,currentyear,query.data)
        sendScreenshoot(query,hasilbaca)
        context.bot.send_message(chat_id=query.message.chat_id,text="Jumlah Stock Material : "+hasilbaca)
#===============  LIST GROUP MENU =========================
def listjtr(query):
    buttons = [[InlineKeyboardButton("SR",callback_data="sr")],[InlineKeyboardButton("LVTC",callback_data="lvtc")],[InlineKeyboardButton("NYY",callback_data="nyy")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text('Silahkan pilih:', reply_markup=reply_markup)
def listapp(query):
    buttons = [[InlineKeyboardButton("kWh Meter",callback_data="kwh")],
    [InlineKeyboardButton("Pembatas",callback_data="pembatas")],[InlineKeyboardButton("Panel",callback_data="panel")],[InlineKeyboardButton("CT/PT",callback_data="ctpt")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def listmeter(query):
    buttons = [[InlineKeyboardButton("3P (5/80)",callback_data="2190218")],[InlineKeyboardButton("3P (5/10 A 240/400 (1))",callback_data="2190253")],
    [InlineKeyboardButton("3P (5A 57/240 (0.5))",callback_data="2190438")],[InlineKeyboardButton("3P (5-10 A 57/240 (0.5))",callback_data="2190219")],[InlineKeyboardButton("3P (5-10 A 57/240-245/400 (0.2))",callback_data="2190264")],
    [InlineKeyboardButton("1P Pascabayar",callback_data="2190231")],[InlineKeyboardButton("1P Prabayar",callback_data="2190224")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def pembatas(query):
    buttons = [[InlineKeyboardButton("MCB",callback_data="mcb")],
    [InlineKeyboardButton("MCCB",callback_data="mccb")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def mcb(query):
    buttons = [[InlineKeyboardButton("MCB 2A",callback_data="3250046")],[InlineKeyboardButton("MCB 4A",callback_data="3250048")],[InlineKeyboardButton("MCB 6A",callback_data="3250050")],
    [InlineKeyboardButton("MCB 10A",callback_data="3250052")],[InlineKeyboardButton("MCB 16A",callback_data="3250054")],[InlineKeyboardButton("MCB 20A",callback_data="3250056")],
    [InlineKeyboardButton("MCB 25A",callback_data="3250058")],[InlineKeyboardButton("MCB 35A",callback_data="3250059")],[InlineKeyboardButton("MCB 50A",callback_data="3250060")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def mccb(query):
    buttons = [[InlineKeyboardButton("MCB  3 Ph _ 10 A",callback_data="3250097")],[InlineKeyboardButton("MCB  3 Ph _ 16 A",callback_data="3250099")],[InlineKeyboardButton("MCB  3 Ph _ 20 A",callback_data="3250100")],[InlineKeyboardButton("MCB  3 Ph _ 25 A",callback_data="3250102")],
    [InlineKeyboardButton("MCB  3 Ph _ 35 A",callback_data="3250103")],[InlineKeyboardButton(" MCCB 380/440V;;3P;;80A;;50 Hz",callback_data="3250034")],[InlineKeyboardButton("MCCB 380/440V;;3P;;100A;;50 Hz",callback_data="3250063")],
    [InlineKeyboardButton("MCCB 380/440V;;3P;;125A;;50 Hz",callback_data="3250064")],[InlineKeyboardButton("MCCB 380/440V;;3P;;160A;;50 Hz",callback_data="3250023")],[InlineKeyboardButton("MCCB 380/440V;;3P;;200A;;50 Hz",callback_data="3250076")],
    [InlineKeyboardButton("MCCB 380/440V;;3P;;225A;;50 Hz",callback_data="3250077")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def panel(query):
    buttons = [[InlineKeyboardButton("BOX;;APP;PENGUKURAN   LANGSUNG TR",callback_data="4120005")],[InlineKeyboardButton("BOX;;KWH PJU",callback_data="4120463")],[InlineKeyboardButton(" BOX;; KWH;;TR_ PUSAT;;9;;TITIK",callback_data="4120263")],
    [InlineKeyboardButton("BOX;; KWH;;TR_ PUSAT;;12;;TITIK",callback_data="4120262")],[InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  53 KVA",callback_data="4120102")],[InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  66 KVA",callback_data="4120321")],
    [InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  82,5 KVA",callback_data="4120284")],[InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  105  KVA",callback_data="4120285")],[InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  131  KVA",callback_data="4120286")],
    [InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  164 KVA",callback_data="4120287")],[InlineKeyboardButton("BOX;;APP;;Pengukuran Tdk Langsung  197 KVA",callback_data="4120288")],[InlineKeyboardButton("GARDU MENARA  SUSUN",callback_data="4120015")],
    [InlineKeyboardButton("BOX PANEL SPLU TYPE WALL 1 Kwh",callback_data="4120402")],[InlineKeyboardButton("BOX PANEL SPLU TYPE HOOK 2 Kwh",callback_data="4120235")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def sr(query):
    buttons = [[InlineKeyboardButton("KABEL TWISTED__TC 2 x 10 mm2",callback_data="3110025")],[InlineKeyboardButton("KABEL TWISTED__TC 2 x 16 mm2",callback_data="3110026")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def lvtc(query):
    buttons = [[InlineKeyboardButton("KABEL LVTC 4 x 35 mm2",callback_data="3110039")],[InlineKeyboardButton("KABEL LVTC 4 x 70 mm2",callback_data="3110542")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def nyy(query):
    buttons = [[InlineKeyboardButton("KABEL NYY 1 x 70 mm2",callback_data="3110514")],
    [InlineKeyboardButton("KABEL NYY 1 x 95 mm2",callback_data="3110515")],[InlineKeyboardButton("KABEL NYY 1 x 150 mm2",callback_data="3110516")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text('Silahkan pilih:', reply_markup=reply_markup)
def listm(query):
    buttons = [[InlineKeyboardButton("SUTM",callback_data="sutm")],[InlineKeyboardButton("XLPE",callback_data="xlpe")],[InlineKeyboardButton("MVTIC",callback_data="mvtic")],
    [InlineKeyboardButton("Trafo",callback_data="trafo")],[InlineKeyboardButton("Isolator",callback_data="isolator")],[InlineKeyboardButton("FCO dan Arrester",callback_data="fco")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def xlpe(query):
    buttons = [[InlineKeyboardButton("XLPE 150 MM2",callback_data="3110014")],[InlineKeyboardButton("XLPE 240 MM2",callback_data="3110015")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def mvtic(query):
    buttons = [[InlineKeyboardButton("MVTIC 150 MM2",callback_data="3110034")],[InlineKeyboardButton("MVTIC 240 MM2",callback_data="3110526")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def trafo(query):
    buttons = [[InlineKeyboardButton("Trafo 3 Ph_50 kVA",callback_data="1030116")],[InlineKeyboardButton("Trafo 3 Ph_100 kVA",callback_data="1030074")],[InlineKeyboardButton("Trafo 3 Ph_160 kVA",callback_data="1030075")],
    [InlineKeyboardButton("Trafo 3 Ph_200 kVA",callback_data="1030076")],[InlineKeyboardButton("Trafo 3 Ph_250 kVA",callback_data="1030077")],[InlineKeyboardButton("Trafo 3 Ph_400 kVA",callback_data="1030079")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def isolator(query):
    buttons = [[InlineKeyboardButton("ISOLATOR TUMPU PORCELIN",callback_data="3070151")],[InlineKeyboardButton("ISOLATOR TUMPU POLYMER",callback_data="3070152")],[InlineKeyboardButton("ISOLATOR ASFAN PORCELIN",callback_data="3070160")],
    [InlineKeyboardButton("ISOLATOR ASFAN POLYMER",callback_data="3070154")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def sutm(query):
    buttons = [[InlineKeyboardButton("A3C 150mm",callback_data="3050001")],[InlineKeyboardButton("A3CS 150mm",callback_data="3050006")],[InlineKeyboardButton("A3CS 240mm",callback_data="3050050")],
    [InlineKeyboardButton("A3C 70mm",callback_data="3050081")],[InlineKeyboardButton("A3Cs 70mm",callback_data="3050088")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)
def fco(query):
    buttons = [[InlineKeyboardButton("FUSE CUT OUT POLYMER",callback_data="3190002")],[InlineKeyboardButton("LIGTHING ARRESTER POLYMER",callback_data="2090032")],[InlineKeyboardButton("DISCONNECTING SWITCH 630 AMPER",callback_data="2030022")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.message.reply_text("Silahkan pilih:",reply_markup=reply_markup)



    #================================= COMMAND MATERIAL =================================
def material(currentmonth,currentyear,materialcode):
    #Memulai proses buka Report SAP
    ic = INFOMATERIAL.InfoMaterial(PATH,chrome_options,direktori,tokenbot,chatid,pathori,pathtx,showdelay,spreadsheetdelay,downloaddelay)
    hasilbaca = ic.getinfomaterial(direktori=direktori,filenamereportharian=filenamereportharian,fileexport=filepathexcel,kodematerial=materialcode,x1=x1,y1=y1,x2=x2,y2=y2)
    return hasilbaca
def materialfull(currentmonth,currentyear,materialcode):
    #Memulai proses buka Report SAP
    ic = INFOMATERIAL.InfoMaterial(PATH,chrome_options,direktori,tokenbot,chatid,pathori,pathtx,showdelayfull,spreadsheetdelayfull,downloaddelayfull)
    hasilbaca = ic.reportmaterial("",materialcode,currentmonth,currentyear,filepathexcel)
    files = {"photo" : open(direktori+"\\capturereport.png", "rb")}
    resp = requests.post("https://api.telegram.org/bot"+tokenbot+"/sendPhoto?chat_id="+str(chatid), files=files)
    return "berhasil"

    #comand
def infocmd(update,context):
    command = update.message.text
    print(command)
    if(command == "infokwhmeterpasca"):
        context.bot.send_message(chat_id=update.message.chat_id,text="Memulai Proses pengecekan stock Material")
        ic = INFOMATERIAL.InfoMaterial(PATH,direktori,tokenbot,chatid)
        message = ic.infokwhmeter("pusat\rijal.wicaksono","9214611zz=")
        files = {"photo" : open(direktori+"\\screenshoot.png", "rb")}
        resp = requests.post("https://api.telegram.org/bot"+tokenbot+"/sendPhoto?chat_id="+str(chatid), files=files)
        context.bot.send_message(chat_id=update.message.chat_id,text=message)
        #Close aplikasi SAP
        pyautogui.keyDown('alt')
        pyautogui.keyDown('f4')
        time.sleep(.5)
        pyautogui.keyUp('f4')
        pyautogui.keyUp('alt')
    if(command[:6] == "report"):
        unit = command[7:10]
        kdunit,kode = readkodeunit(unit)
        kdmaterial = command[11:18]
        bulan = command[19:]
        tahun = 2022
        context.bot.send_message(chat_id=update.message.chat_id,text="Memulai cek report material unit "+kdunit)
        context.bot.send_message(chat_id=update.message.chat_id,text="Kode Material "+kdmaterial)
        context.bot.send_message(chat_id=update.message.chat_id,text="Periode laporan bulan : "+bulan+"\n"+"Tahun : "+str(tahun))
        #Memulai proses buka Report SAP
        ic = INFOMATERIAL.InfoMaterial(PATH,chrome_options,direktori,tokenbot,chatid,pathori,pathtx)
        hasilbaca = ic.reportmaterial(kode,kdmaterial,bulan,tahun,filepathexcel)
        print(hasilbaca)
        files = {"photo" : open(direktori+"\\capturereport.png", "rb")}
        resp = requests.post("https://api.telegram.org/bot"+tokenbot+"/sendPhoto?chat_id="+str(chatid), files=files)
        context.bot.send_message(chat_id=update.message.chat_id,text = "Jumlah Stock Material : "+hasilbaca[14])

def readkodeunit(inputcommand):
    if(inputcommand == "pnk"):
        return "Panakkukang",2520
    elif(inputcommand == "mtg"):
        return "Mattoanging",2530
    elif(inputcommand == "sgm"):
        return "Sungguminasa",2540
    elif(inputcommand == "kbj"):
        return "Kalebajeng",2550
    elif(inputcommand == "tkl"):
        return "Takalar",2560
    elif(inputcommand == "mno"):
        return "Malino",2570
    elif(inputcommand == "ums"):
        return "Makassar Selatan",2180

#task scheduler once
def once(context:CallbackContext) :
    jam = datetime.datetime.now()
    jamFOrmatted = jam.strftime("%d/%m/%Y, %H:%M:%S")
    message = "Memulai download pembaharua database\n"+"pada jam : "
    message = message+jamFOrmatted
    context.bot.send_message(chat_id=chatid, text=message)
    try:
        message = materialfull(currentmonth,currentyear,materialcode="")
        context.bot.send_message(chat_id=chatid, text="Berhasil Memperbaharui database")
    except:
        context.bot.send_message(chat_id=chatid, text=message)
def main():
    # Create updater and pass in Bot's auth key.
    updater = Updater(token=tokenbot, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher

    j = updater.job_queue

    #execute run_daily job
    jobdaily = j.run_daily(once,time=t,days=days)
    jobdaily2 = j.run_daily(once,time=t2,days=days)
    #calling predefined method
    dispatcher.add_handler(CommandHandler('start',start
    ))
    #read Message Handler
    dispatcher.add_handler(MessageHandler(Filters.text, infocmd))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # #STart Updater Job Queue
    # j = updater.job_queue
    # j.run_once(once,3)

    # start the bot
    updater.start_polling()
    # Stop
    updater.idle()
if __name__ == '__main__':
    main()
