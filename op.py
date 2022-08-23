from re import T
import re
from turtle import width
from bs4 import BeautifulSoup
import pandas as pd
import requests
from tkinter import *
from tkinter import ttk
import webbrowser
from time import sleep
from tkinter import Tk
import pickle
from riotwatcher import LolWatcher, ApiError
import json
# [c1.get(), ms[0], r[0], t[0], c2.get(), ms[1], r[1], t[1], c2.get(), ms[2], r[2], t[2], c3.get(), ms[3], r[3], t[3], c4.get(), ms[4], r[4], t[4], c5.get(), c6.get(), c7.get(), c8.get(), c9.get(), c10.get()]
from pathlib import Path
import sklearn
import xgboost
bundle_dir = Path(__file__).parent
path_to_c = Path.cwd() / bundle_dir / "champion.json"
f = open(path_to_c)

bundle_dir = Path(__file__).parent
path_to_m = Path.cwd() / bundle_dir / "finalized_model.sav"
champions = json.load(f)['data']
champs = []
for c in champions.keys():
    champs.append(c)

api_key = 'RGAPI-01777209-f4d6-4278-9950-e5bccbeefdec'
watcher = LolWatcher(api_key)
my_region = 'na1'

filename = 'finalized_model.sav'
model = pickle.load(open(path_to_m, 'rb'))

def rankbot_activation():
    players = []
    for p in summoners:
        players.append(p.get())
    ms = list((0,0,0,0,0))
    r = list((0,0,0,0,0))
    t = list((0,0,0,0,0))
    level = list((0,0,0,0,0))
    cTotal = list((0,0,0,0,0))
    cwr = list((0,0,0,0,0))
    kda = list((0,0,0,0,0))
    for p in range(5):
        player = None
        playerName = players[p]
        try:
            if int(players[p]) < 6:
                player = watcher.summoner.by_name(my_region,legend[p])
                playerName = legend[p]
            else:
                player = watcher.summoner.by_name(my_region,players[p])
        except:
            player = watcher.summoner.by_name(my_region,players[p])
        sid = player['id']
        level[p] = player['summonerLevel']
        champ = ""
        if (entries[p].get() == 'Wukong'):
            champ = "Monkeyking"
        else:
            champ = entries[p].get().replace("'", "")
        mastery = watcher.champion_mastery.by_summoner_by_champion(my_region, sid, champions[champ]['key'])['championPoints']
        ms[p] = mastery
        url = 'https://u.gg/lol/profile/na1/' + playerName + '/overview'
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "html.parser")
        wr = soup.find('body').find("div", {"id": "root"}).find("div", {"class": "desktop-container router-container"}).find("div", {"id": "page-content"}).find("div", {"style": "width:100%"}).find("div", {"id": "main-content"}).find("div", {"id": "content-wrapper"}).find("div", {"id": "content"}).find("div", {"class": "summoner-profile-page"}).find("div", {"class": "summoner-profile-container content-side-padding"}).find("div", {"class": "summoner-profile_content-container"}).find("div", {"class": "summoner-profile_overview2"}).find("div", {'class': 'summoner-profile_overview__side'}).find("div", {"class": "rank-block"}).find("div", {"class": "rank-list"}).find("div", {"class": "rank-lp-container"}).find("div", {"class": "content-section content-section_no-padding rank-content"}).find("div", {"class": 'rank-sub-content'}).find("div", {"class": "text-container"}).find("div", {"class": "rank-wins"}).find_all('span')
        wrInt = float(wr[1].getText().replace('% Win Rate', ""))
        total = wr[0].getText()
        total = float(total[0: str(total).find('W')]) + float(total[str(total).find('W') + 2: str(total).find('L')])
        r[p] = wrInt / 100
        t[p] = total

        url = 'https://u.gg/lol/profile/na1/' + playerName + '/champion-stats'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        source = requests.get(url, headers=headers).text
        soup = BeautifulSoup(source, "html.parser")
        ugg = soup.find('body').find('div', {'id': 'root'}).find('div', {'class': 'desktop-container router-container'}).find('div', {'id': 'page-content'}).find('div', {'style': 'width:100%'}).find('div', {'id': 'main-content'}).find('div', {'id': 'content-wrapper'}).find('div', {'id': 'content'}).find('div', {'class': 'summoner-profile-page'}).find('div', {'class': 'summoner-profile-container content-side-padding'}).find('div', {'class': 'summoner-profile_content-container'}).find('div', {'class': 'summoner-profile_champion-stats'}).find('div', {'class': 'content-section ReactTable ugg-table-2 profile-champion-stats-table'}).find('div', {'class': 'rt-tbody'}).find_all('div', {'class': 'rt-tr-group'})
        for d in ugg:
            if d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'champion-cell'}).find('a').find('span').getText() == entries[p].get():
                temp = d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'win-rate-cell'}).find('div').find('span', {'class': 'match-record'}).getText()
                temp = float(temp[0: str(temp).find('W')]) + float(temp[str(temp).find('W') + 2: str(temp).find('L')])
                cTotal[p] = temp
                cwr[p] = float(d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'win-rate-cell'}).find('div').find('strong').getText().strip('%')) / 100
                kda[p] = float(d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'kda-cell'}).find('div').find('div').find('strong').getText())
                break
    new_row = {'blueTops' : [entries[0].get()], 'btlevel': level[0], 'btmp': ms[0],'btwr': r[0], 'btcwr': cwr[0], 'btkda': kda[0], 'btct': cTotal[0], 'btt': t[0],'blueJngs': [entries[1].get()], 'bjlevel': level[1], 'bjmp': ms[1],'bjwr': r[1],  'bjcwr': cwr[1], 'bjkda': kda[1], 'bjct': cTotal[1], 'bjt': t[1],'blueMids': [entries[2].get()], 'bmlevel': level[2], 'bmmp': ms[2],'bmwr': r[2], 'bmcwr': cwr[2], 'bmkda': kda[2], 'bmct': cTotal[2], 'bmt': t[2],'blueBots': [entries[3].get()], 'bblevel': level[3], 'bbmp': ms[3],'bbwr': r[3], 'bbcwr': cwr[3], 'bbkda': kda[3], 'bbct': cTotal[3], 'bbt': t[3],'blueSups': [entries[4].get()], 'bslevel': level[4], 'bsmp': ms[4],'bswr': r[4],  'bscwr': cwr[4], 'bskda': kda[4], 'bsct': cTotal[4], 'bst': t[4],'redTops': [entries[5].get()],'redJngs': [entries[6].get()],'redMids': [entries[7].get()],'redBots': [entries[8].get()],'redSups': [entries[9].get()]}
    df = pd.DataFrame(new_row)
    print(df.to_string())

    prediction = model.predict_proba(df)
    print(prediction)
    predstr = "{:.2f}".format(prediction[0][1] * 100) + "% Win, " + "{:.2f}".format(prediction[0][0] * 100) + "% Lose"
    result.set(predstr)
    
def init():
    players =  totsum.get().split(" joined the lobby")
    players.pop()
    for i in range(5):
        players[i] = players[i].strip()
    for i in range(5):
        legend[i] = players[i]
    text = ""
    for i in range(5):
        text += str(i) + ": " + players[i] + "  "
    legendtxt.set(text)

legend = list(("", "", "", "", ""))

master = Tk()
master.title('LOL skill')
frm = ttk.Frame(master, padding=10)
frm.grid()
entries = [StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master), StringVar(master)]
temp = []
for i in range(10):
    entries[i].set(champs[0])
    m  = OptionMenu(frm, entries[i], *champs)
    temp.append(m)
    m.configure(width=8)

s1 = Entry(frm)
s2 = Entry(frm)
s3 = Entry(frm)
s4 = Entry(frm)
s5 = Entry(frm)
summoners = [s1, s2, s3, s4, s5]
result = StringVar(frm)
result.set("LOL skill")
resultlabel = Label(frm, textvariable=result).grid(row=0, column=1)
Label(frm, text="My Team").grid(row=1, column=0)
Label(frm, text="Accounts").grid(row=1, column=1)
Label(frm, text="Enemy Team").grid(row=1, column=2)
totsum = Entry(frm)
totsum.grid(row=7, columnspan=2)
totsum.configure(width=30)
Button(frm, text='Init', command=init).grid(row=7, column=2, sticky=W, pady=3)
for i in range(1, 6):
    temp[i-1].grid(row=i+1, column=0)
    summoners[i-1].grid(row=i+1, column=1)
    temp[i+ 4].grid(row=i+1, column=2)
legendtxt = StringVar(frm)
legendlabel = Label(frm, textvariable=legendtxt).grid(row=8, columnspan=3)
s1 = OptionMenu(frm, entries[i], *champs)
Button(frm, text='Quit', command=master.quit).grid(row=9, column=0, pady=4)
Button(frm, text='Activate webbot', command=rankbot_activation).grid(row=9, column=1, sticky=W, pady=4)
mainloop()