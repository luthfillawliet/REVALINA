#Import pandas library
import imp
from operator import index
import pandas as pd
import numpy as np

class readxls:
    def __init__(self,filepathexcel):
        self.filepathexcel = filepathexcel
    def readdata(self):
        reportpath = self.filepathexcel
        df = pd.read_excel(reportpath,header=None)
        #print(df)
        print(df.head())
        data = df[5]
        dataq = df[13]

        malino = 0
        takalar = 0
        kalebajeng = 0
        sungguminasa = 0
        mattoanging = 0
        panakkukang = 0
        up3ms = 0
        #deklarasi array kosong
        arr = np.empty((len(data),2),dtype=object)
        print("Empty array")
        print(arr)
        try:
            if(data is None):
                return "Failed to read data"
            else:
                #looping untuk assign nilai data dan dataq pada arr
                for x in range(len(data)):
                    arr[x][0] = str(data[x])
                    arr[x][1] = dataq[x]
                #buat arr jadi dataframe untuk diberikan header
                datafinal = pd.DataFrame(arr,columns=("unit","jumlah"))
                print(datafinal)
                for y in range(len(datafinal)):
                    #vlookup quantity berdasarkan anam gudang unit dan menjumlahkan
                    if(datafinal["unit"][y] == "Gd Ar Mksar Sltn"):
                        up3ms = up3ms+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Panakkukan"):
                        panakkukang = panakkukang+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Mattoangin"):
                        mattoanging = mattoanging+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Sunggumina"):
                        sungguminasa = sungguminasa+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Kalebajeng"):
                        kalebajeng = kalebajeng+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Takalar"):
                        takalar = takalar+datafinal["jumlah"][y]
                    elif(datafinal["unit"][y] == "Gd Ry Malino"):
                        malino = malino+datafinal["jumlah"][y]

                malino = str(malino)
                takalar = str(takalar)
                kalebajeng = str(kalebajeng)
                sungguminasa = str(sungguminasa)
                mattoanging = str(mattoanging)
                panakkukang = str(panakkukang)
                up3ms = str(up3ms)

                print("JUlah saldo : \n"+"UP3 MS : "+up3ms+"\nPanakkukang : "+
                panakkukang+"\nMattoanging : "+mattoanging+"\nSungguminasa : "+
                sungguminasa+"\nKalebajeng : "+kalebajeng+"\nTakalar : "+
                takalar+"\nMalino : "+malino)

                hasilbaca = ("\n"+"UP3 MS : "+up3ms+"\nPanakkukang : "+
                            panakkukang+"\nMattoanging : "+mattoanging+"\nSungguminasa : "+
                            sungguminasa+"\nKalebajeng : "+kalebajeng+"\nTakalar : "+
                            takalar+"\nMalino : "+malino)
                return  hasilbaca
        except:
            return "Failed to read XLS file"