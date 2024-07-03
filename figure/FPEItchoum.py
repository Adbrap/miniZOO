# ----- initialisation des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import multiprocessing
import math
# from playsound import playsound
from ib_insync import *
import sys
import subprocess
import tempfile
from ftplib import FTP
from ib_insync import *
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import datetime
import ftplib

# ----- initialisation des modules -----#
def achat(ticker,target2,target):
    commande = ["python", "assets/acheter.py", ticker, target2, target]
    subprocess.run(commande, check=True)
# ----- initialisation des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE


w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialisation des couleurs du modules pystyle -----#

# ----- initialisation des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-25))[0:10]
start_12h = str(pd.Timestamp.today() + pd.DateOffset(-35))[0:10]
start_18h = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialisation des temps de recherches -----#

# ----- initialisation de l'API key et ticker -----#
#api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
ticker = 'FPEI'
tiker_live = ticker

argument2 = 0
argument3 = 0


# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#


# ----- fonction Principale -----#
def Finder_IETE(time1, time_name1, start1):
    # global proxies
    global argument2
    global argument3
    global tiker_live
    global time2
    global time_name2
    time2 = time1
    time_name2 = time_name1
    # while True:

    # ----- Appel des données Polygon.io OHLC et creation du DF -----#
    passed1 = False
    with my_lock:
        try:
            api_url_livePrice = f'http://api.polygon.io/v2/last/trade/{tiker_live}?apiKey={api_key}'
            data = requests.get(api_url_livePrice).json()
            df_livePrice = pd.DataFrame(data)

            api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start1}/{end}?adjusted=true&limit=50000&apiKey={api_key}'

            data = requests.get(api_url_OHLC).json()
            df = pd.DataFrame(data['results'])
            la_place_de_p = 0

            for k in range(0, len(df_livePrice.index)):
                if df_livePrice.index[k] == 'p':
                    la_place_de_p = k
            livePrice = df_livePrice['results'].iloc[la_place_de_p]
            passed1 = True
        except:
            Write.Print("<⛔> <⛔> <⛔> <⛔> ERREUR CRITIQUE <⛔> <⛔> <⛔> <⛔>", Colors.red, interval=0.000)
            print('')

    # ----- Appel des données Polygon.io OHLC et creation du DF -----#

    # ----- suppression de la dernière valeur du df pour y rajouter un LIVEPRICE plus precis -----#
    if passed1 == True:
        dernligne = len(df['c']) - 1
        df.drop([dernligne], axis=0, inplace=True)

        # df = df.drop(columns=['o', 'h', 'l', 'v', 'vw', 'n'])
        # df = df.append({'o': NAN, 'h': NAN, 'l': NAN, 'v': NAN, 'vw': NAN, 'n': NAN, 'c': livePrice, 't': NAN}, ignore_index=True)
        df_new_line = pd.DataFrame([[NAN, NAN, NAN, NAN, NAN, NAN, livePrice, NAN]],
                                   columns=['o', 'h', 'l', 'v', 'vw', 'n', 'c', 't'])
        df = pd.concat([df, df_new_line], ignore_index=True)
        df_data_date = []
        df_data_price = []
        for list_df in range(len(df)):
            df_data_date.append(df['t'].iloc[list_df])
            df_data_price.append(df['c'].iloc[list_df])
        data_date = pd.DataFrame(df_data_date, columns=['Date'])
        data_price = pd.DataFrame(df_data_price, columns=['Price'])
        df_wise_index = pd.concat([data_date, data_price], axis=1)

        place_liveprice = (len(df) - 1)

        for data in range(len(df_wise_index)):

            try:

                if df_wise_index['Price'].iloc[data] == df_wise_index['Price'].iloc[data + 1]:
                    df = df.drop(df_wise_index['Date'].iloc[data + 1])
            except:
                # print('ok')
                aaa = 0
        # ----- suppression de la dernière valeur du df pour y rajouter un LIVEPRICE plus precis -----#

        # ----- creation des locals(min/max) -----#
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

        # ----- creation des locals(min/max) -----#

        # ----- suppression des points morts de la courbe -----#
        test_min = []
        test_max = []

        # if local_min[0] > local_max[0]:
        #        local_max = local_max[1:]
        #        print('On a supprimer le premier point')
        #
        q = 0
        p = 0

        len1 = len(local_min)
        len2 = len(local_max)
        while p < len1 - 5 or p < len2 - 5:
            if local_min[p + 1] < local_max[p]:
                test_min.append(local_min[p])
                local_min = np.delete(local_min, p)

                p = p - 1
            if local_max[p + 1] < local_min[p + 1]:
                test_max.append(local_max[p])
                local_max = np.delete(local_max, p)

                p = p - 1
            p = p + 1

            len1 = len(local_min)
            len2 = len(local_max)

        decalage = 0
        # ----- suppression des points morts de la courbe -----#

        # ----- initialisation des pointeurs de la figure -----#
        passed2 = False
        try:
            A = float(df['c'].iloc[local_max[-3]])
            B = float(df['c'].iloc[local_min[-3]])
            C = float(df['c'].iloc[local_max[-2]])
            D = float(df['c'].iloc[local_min[-2]])
            E = float(df['c'].iloc[local_max[-1]])


            passed2 = True

        except:
            Write.Print("<🟡> <🟡> <🟡> <🟡> PAS ASSEZ DE DONNEES <🟡> <🟡> <🟡> <🟡>", Colors.yellow, interval=0.000)
            print('')
        # ----- initialisation des pointeurs de la figure -----#
        if passed2 == True:
            # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#
            if C > E:
                differ = (C - E)
                pas = (local_max[-1] - local_max[-2])
                suite = differ / pas
            if C < E:
                differ = (E - C)
                pas = (local_max[-1] - local_max[-2])
                suite = differ / pas
            # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#

            # ----- PRINT affichage dans la console -----#
            Write.Print("  >> RECHERCHE IETE  :", Colors.white, interval=0.000)
            Write.Print(f"  {ticker}", Colors.green, interval=0.000)
            Write.Print(f"  {time1} {time_name1}", Colors.cyan, interval=0.000)
            Write.Print("  <<", Colors.white, interval=0.000)
            print('')
            # ----- PRINT affichage dans la console -----#

            # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#
            rouge = []
            vert = []
            bleu = []

            rouge.append(local_max[-3])
            rouge.append(local_min[-3])
            rouge.append(local_max[-2])
            rouge.append(local_min[-2])
            rouge.append(local_max[-1])
            rouge.append(local_min[-1])
            rouge.append(place_liveprice)

            vert.append(local_max[-3])
            vert.append(local_max[-2])
            vert.append(local_max[-1])
            vert.append(place_liveprice)

            i = 0
            passed3 = False
            try:
                for i in range(local_max[-4] - 1, len(df)):
                    bleu.append(i)
                    passed3 = True
            except:
                Write.Print("<🟠> <🟠> <🟠> <🟠> PAS ASSEZ DE DONNEES 2 <🟠> <🟠> <🟠> <🟠>", Colors.orange, interval=0.000)
                print('')
            if passed3 == True:
                mirande = df.iloc[rouge, :]
                mirande3 = df.iloc[bleu, :]
                # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#

        
                # ----- transformer le tableau en DF avec les donnée du DF reel -----#
                vert1 = {'c': vert}
                vert2 = pd.DataFrame(data=vert1)
                rouge1 = {'c': rouge}
                rouge2 = pd.DataFrame(data=rouge1)
                bleu1 = {'c': bleu}
                bleu2 = pd.DataFrame(data=bleu1)
                # ----- transformer le tableau en DF avec les donnée du DF reel -----#

                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!
                pop = 0
                verif = 0

                for pop in range(0, len(test_min)):
                    if test_min[pop] > local_max[-3] and test_min[pop] < place_liveprice:
                        verif = verif + 1
                pop = 0
                for pop in range(0, len(test_max)):
                    if test_max[pop] > local_max[-3] and test_max[pop] < place_liveprice:
                        verif = verif + 1
                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!

                # ----- condition pour que l'ordre des point de la figure soit respecter -----#
                ordre = False
                if local_max[-3] < local_min[-3] < local_max[-2] < local_min[-2] < local_max[-1] < local_min[-1]:
                    ordre = True
                # ----- condition pour que l'ordre des point de la figure soit respecter -----#

                # ----- condition pour garantir la forme de l'iete  -----#
                if (C - B) < (C - D) and (C - B) < (E - D) and (E > D) and B > D  and B < C and verif == 0 and ordre == True:
                    
                    moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                    moyenne_tete = ((C - D) + (E - D)) / 2
                    # ----- creation variable des moyennes de la tete et epaules  pour les prochaines conditions-----#

                    tuche = 0
                    noo = 0
                    place_pc = 0
                    point_max = J[0] + ((J[0] - I[0]))
                    point_max = int(round(point_max, 0))





                    # ----- condition pour filtrer iete  -----#
                    if moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and accept == True:
                        
                        print(f"Data for {ticker}:")
                        print(df)
                        fig1 = plt.figure(figsize=(10, 7))
                        plt.plot([], [], " ")
                        fig1.patch.set_facecolor('#17DE17')
                        fig1.patch.set_alpha(0.3)
                        df['c'].plot(color=['blue'], label='Clotures')
                        plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
                        plt.show()

                print('----------------------------------------------------------------------', flush=True)
                time.sleep(0.5)


# ----- fonction Principale -----#
time2 = None
time_name2= None
# ----- traduction francais anglais pour appel polygon -----#
minute = "minute"
heure = "hour"
jour = "day"
# ----- traduction francais anglais pour appel polygon -----#

# ----- enssembles des Process à lancer en meme temps -----#
th1 = Process(target=Finder_IETE, args=(1, heure, start_1h))

th1.start()

th1.join()

