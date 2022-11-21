from importlib.resources import path
from lib2to3.pgen2 import driver
import os
from threading import TIMEOUT_MAX
from tkinter import E
from typing import Pattern
from matplotlib.pyplot import cla, title
from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pywinauto.application import Application
from pywinauto import Desktop
#Import pyautogui
import pyautogui
#import library untuk copy paste file
import shutil
#Import Library readdataexcel
import readdataexcel

import requests
# import Action chains
from selenium.webdriver import ActionChains
# IMport library select
from selenium.webdriver.support.ui import Select
import time

from setuptools import Command

class eksekusiSAP:
    def __init__(self,pathori,pathtx,showdelay,spreadsheetdelay,downloaddelay):
        self.pathori = pathori
        self.pathtx = pathtx
        self.showdelay = showdelay
        self.spreadsheetdelay = spreadsheetdelay
        self.downloaddelay = downloaddelay

    def eksekusi(self,xstockoverview,ystockoverview,xfieldmaterial,yfieldmaterial):
        #buka TX
        pathori = self.pathori
        pathtx = self.pathtx
        original = pathori+"tx.sap"
        target = pathtx+"tx.sap"
        kodematerial = "2190224"
        kodeunit = "7428"
        #coordinate Stock overview
        x = xstockoverview
        y = ystockoverview
        x1 = xfieldmaterial
        y1 = yfieldmaterial
        # x = xst
        # y = 214
        # #coordinate input field kode material
        # x1 = 281
        # y1 = 38


        #arahkann ke direktori TX original
        os.chdir(pathori)
        dir_list = os.listdir(pathori)
        print("Files and directories in '", pathori, "' :")
        # print the list
        print(dir_list)
        shutil.copyfile(original,target)

        time.sleep(2)

        os.startfile((pathtx+"tx.sap")) # Open any program, text or office document

        time.sleep(2)

        #get ALL opened window
        top_windows = Desktop(backend="uia").windows() # or backend="win32" by default
        time.sleep(2)
        # walk the returned list of wrappers
        titleapp = "blank"
        for w in top_windows:
            print(w.window_text())
            if(w.window_text()=="SAP Easy Access"):
                titleapp = w.window_text()
                break

        print("Title APP : "+titleapp)
        app = Application().connect(title=u"SAP Easy Access",timeout=10)
        window = app.SAP_FRONTEND_SESSION
        window.set_focus()
        window.maximize()
        time.sleep(5)

        #Move to stock overview
        pyautogui.click(x,y,2)
        time.sleep(3)
        #Move to entry material code
        pyautogui.click(x1,y1)
        pyautogui.typewrite(kodematerial)
        time.sleep(1)
        #masukkan kode unit
        pyautogui.press('tab')
        pyautogui.typewrite(kodeunit)
        time.sleep(1)
        pyautogui.press("f8")
        time.sleep(1)

        app = Application().connect(title=u"Stock Overview: Basic List",timeout=10)
        window = app.SAP_FRONTEND_SESSION
        window.set_focus()
        print("Berhasil buka daftar stock material")
        screenshot = pyautogui.screenshot(self.pathtx+"screenshoot.png")
    def eksekusireport(self,lokasigudang,nomormaterial,bulan,tahun,xerp,yerp,x,y,xbulan,ybulan,filepathexcel):
        print("Eksekusi report")
        pathori = self.pathori
        pathtx = self.pathtx
        original = pathori+"tx.sap"
        target = pathtx+"tx.sap"
        tcode = r"/nzm_lap_pers_log"
        companycode = "7400"
        plantms = "7428"
        kdunit = str(lokasigudang)
        kdmaterial = str(nomormaterial)
        kdbulan = str(bulan)
        kdtahun = str(tahun)

        #klik link erp
        time.sleep(10)
        pyautogui.click(xerp,yerp)
        # shutil.copyfile(original,target)
        print("mencoba buka sap TX")
        time.sleep(5)

        try:
            os.startfile((pathtx+"tx.sap")) # Open any program, text or office document
        except:
            print("Gagal Buka Aplikasi SAP")

        time.sleep(3)

        #get ALL opened window
        top_windows = Desktop(backend="uia").windows() # or backend="win32" by default
        time.sleep(2)
        titleapp = "blank"
        for w in top_windows:
            print(w.window_text())
            if(w.window_text()=="SAP Easy Access"):
                titleapp = w.window_text()
                break

        print("Title APP : "+titleapp)
        app = Application().connect(title=u"SAP Easy Access",timeout=10)
        window = app.SAP_FRONTEND_SESSION
        window.set_focus()
        window.maximize()
        time.sleep(2)

        #Move to Laporan persediaan barang logistik, enter the T-CODE
        #pyautogui.click(x,y,2) sebelumnya haru d klik menunya, tapi sekarang tingal masukkan t code
        #time.sleep(3)
        #Input T code
        pyautogui.typewrite(tcode)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(20)
        #isi company code
        pyautogui.typewrite(companycode)
        time.sleep(1)
        pyautogui.press('tab',3,0.3)
        pyautogui.typewrite(plantms)
        pyautogui.press('tab',3,0.3)
        pyautogui.typewrite(kdunit)
        pyautogui.press('tab',6,0.3)
        pyautogui.typewrite(kdmaterial)
        time.sleep(1)
        pyautogui.click(xbulan,ybulan)
        pyautogui.typewrite(kdbulan)
        time.sleep(1)
        pyautogui.press('tab',1,0.3)
        time.sleep(0.5)
        pyautogui.typewrite(kdtahun)
        time.sleep(1)
        pyautogui.press("f8")
        #tunggu proses terbuka
        time.sleep(self.showdelay)
        #Alihkan ke kenan screensnya
        time.sleep(10)
        pyautogui.press('down',presses=13)
        time.sleep(0.5)
        pyautogui.press('right',presses=13)
        time.sleep(2)
        #Proses screenshoot
        screenshot = pyautogui.screenshot(self.pathtx+"capturereport.png")
        #connect ke tampilan persediaan barang
        app = Application().connect(title=u"Laporan Persediaan Barang",timeout=10)
        window = app.SAP_FRONTEND_SESSION
        window.set_focus()
        #window.print_control_identifiers()
        time.sleep(1)
        #Proses cetak excel
        pyautogui.keyDown('shift')
        pyautogui.press('f9')
        pyautogui.keyUp('shift')
        #delay spreadsheet
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.press('enter')
        pyautogui.press('left')
        time.sleep(.5)
        pyautogui.press('enter')
        #delay download data
        time.sleep(self.downloaddelay)
        #Close data FIle Excelnya
        pyautogui.keyDown('alt')
        pyautogui.press('f4')
        pyautogui.keyUp('alt')

        time.sleep(2)
        #coba read data excel
        re = readdataexcel.readxls(filepathexcel)
        print("Memulai proses membaca data excel : ")
        if(self.downloaddelay>5):
            hasilbaca = "Berhasil download full data"
            time.sleep(2)
            #close SAP
            pyautogui.keyDown('alt')
            pyautogui.press('f4')
            pyautogui.keyUp('alt')
            return hasilbaca
        else:
            hasilbaca = re.readdata()
            time.sleep(2)
            #close SAP
            pyautogui.keyDown('alt')
            pyautogui.press('f4')
            pyautogui.keyUp('alt')
            return hasilbaca

        #read dataframe

