#Import pandas library
import imp
from operator import index
import pandas as pd
import numpy as np

reportpath = 'C:\\Users\\WIN 10\\Documents\\SAP\\SAP GUI\\export.xlsx'
df = pd.read_excel(reportpath,header=None)
#print(df)
print(df.head())
# print(df.shape)
#print(df.loc[:,"Valuation Class"])
data = df[5]
dataq = df[13]
# malino = str(data[1]+data[2])
# takalar = str(data[3] + data[4])
# kalebajeng = str(data[5] + data[6])
# sungguminasa = str(data[7] + data[8])
# mattoanging = str(data[9] + data[10])
# panakkukang = str(data[11] + data[12])
# up3ms = str(data[13])
malino = 0
takalar = 0
kalebajeng = 0
sungguminasa = 0
mattoanging = 0
panakkukang = 0
up3ms = 0
# print("JUlah saldo : \n"+"UP3 MS : "+up3ms+"\nPanakkukang : "+
#     panakkukang+"\nMattoanging : "+mattoanging+"\nSungguminasa : "+
#     sungguminasa+"\nKalebajeng : "+kalebajeng+"\nTakalar : "+
#     takalar+"\nMalino : "+malino)
print("Jumlah data : "+str(len(data)))
arr = np.empty((len(data),2),dtype=object)
print(arr)
print(len(arr))

for x in range(len(data)):
    arr[x][0] = str(data[x])
    arr[x][1] = dataq[x]

print(arr[13][1])
datafinal = pd.DataFrame(arr,columns=("unit","jumlah"))
#print(datafinal["unit"])

print("Hasil looping : ")
for y in range(len(datafinal)):
    print(datafinal["unit"][y])
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

print(up3ms)
# arr = np.concatenate(data,dataq)
# print(arr)
