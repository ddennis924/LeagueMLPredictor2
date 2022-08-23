from turtle import rt, st
from riotwatcher import LolWatcher, ApiError
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tkinter import *
import webbrowser
from time import sleep
from tkinter import Tk
from tqdm import tqdm
from wakepy import keepawake
import json
import warnings
# golbal variables
api_key = 'RGAPI-01777209-f4d6-4278-9950-e5bccbeefdec'
watcher = LolWatcher(api_key)
my_region = 'na1'

f = open('champion.json')
champions = json.load(f)['data']

# me: tUsIcXnShr_aQJoeR5Gxxb8YzlzWYjDFbUVDCcWiHIPvmzlIxtHSc0Y-JFS3YF73it2I0CUICEFNPw

master = watcher.league.entries(my_region, 'RANKED_SOLO_5x5', 'PLATINUM', 'II')
my_matches = []
for i in range(150):
    sid = master[i]['summonerId']
    puuid = watcher.summoner.by_id(my_region, sid)['puuid']
    temp = watcher.match.matchlist_by_puuid(my_region, puuid, queue=420, count=30)
    for match in temp:
        my_matches.append(match)

blueTops = []
blueJngs = []
blueMids = []
blueBots = []
blueSups = []

redTops = []
redJngs = []
redMids = []
redBots = []
redSups = []

btmp = []
bjmp = []
bmmp = []
bbmp = []
bsmp = []
rtmp = []
rjmp = []
rmmp = []
rbmp = []
rsmp = []
mps = [btmp, bjmp, bmmp, bbmp, bsmp, rtmp, rjmp, rmmp, rbmp, rsmp]

btwr = []
bjwr = []
bmwr = []
bbwr = []
bswr = []
rtwr = []
rjwr = []
rmwr = []
rbwr = []
rswr = []
wrs = [btwr, bjwr, bmwr, bbwr, bswr, rtwr, rjwr, rmwr, rbwr, rswr]

btt = []
bjt = []
bmt = []
bbt = []
bst = []
rtt = []
rjt = []
rmt = []
rbt = []
rst = []
ts = [btt, bjt, bmt, bbt, bst, rtt, rjt, rmt, rbt, rst]

winner = []
d = {'blueTops' : blueTops, 'btmp': btmp,'btwr': btwr,'btt': btt,'blueJngs': blueJngs, 'bjmp': bjmp,'bjwr': bjwr,'bjt': bjt,'blueMids': blueMids, 'bmmp': bmmp,'bmwr': bmwr,'bmt': bmt,'blueBots': blueBots, 'bbmp': bbmp,'bbwr': bbwr,'bbt': bbt,'blueSups': blueSups, 'bsmp': bsmp,'bswr': bswr,'bst': bst,'redTops': redTops, 'rtmp': rtmp,'rtwr': rtwr,'rtt': rtt,'redJngs': redJngs, 'rjmp': rjmp,'rjwr': rjwr,'rjt': rjt,'redMids': redMids, 'rmmp': rmmp,'rmwr': rmwr,'rmt': rmt,'redBots': redBots, 'rbmp': rbmp,'rbwr': rbwr,'rbt': rbt,'redSups': redSups, 'rsmp': rsmp,'rswr': rswr,'rst': rst,'winner': winner}

df = pd.DataFrame()
# fetch last match detail
with keepawake(keep_screen_awake=True):
    
    for matchID in tqdm(my_matches, miniters=1000):
        try:
            bt = ""
            bj = ""
            bm = ""
            bb = ""
            bs = ""
            rt = ""
            rj = ""
            rm = ""
            rb = ""
            rs = ""
            ms = list((-1,-1,-1,-1,-1))
            r = list((-1,-1,-1,-1,-1))
            t = list((-1,-1,-1,-1,-1))
            level = list((0,0,0,0,0))

            cwr = list((0,0,0,0,0))
            kda = list((0,0,0,0,0))
            cTotal = list((0,0,0,0,0))
            winnerNow = 0
            match_detail = watcher.match.by_id(my_region, matchID)
            details = match_detail['info']['participants']
            bt = details[0]['championName']
            bj = details[1]['championName']
            bm = details[2]['championName']
            bb = details[3]['championName']
            bs = details[4]['championName']
            rt = details[5]['championName']
            rj = details[6]['championName']
            rm = details[7]['championName']
            rb = details[8]['championName']
            rs = details[9]['championName']
            for i in range(5):
                player = details[i]['puuid']
                champ = details[i]['championId']
                level[i] = details[i]['summonerLevel']
                champName = details[i]['championName']
                defName = champions[champName]['name']
                wins = 0
                total = 0
                playerID = details[i]['summonerId']
                name = details[i]['summonerName']
                mastery = watcher.champion_mastery.by_summoner_by_champion(my_region, playerID, champ)['championPoints']
                ms[i] = mastery
                url = 'https://u.gg/lol/profile/na1/' + name + '/overview'
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
                sleep(1)
                source = requests.get(url, headers=headers).text
                soup = BeautifulSoup(source, "html.parser")
                try:
                    wr = soup.find('body').find("div", {"id": "root"}).find("div", {"class": "desktop-container router-container"}).find("div", {"id": "page-content"}).find("div", {"style": "width:100%"}).find("div", {"id": "main-content"}).find("div", {"id": "content-wrapper"}).find("div", {"id": "content"}).find("div", {"class": "summoner-profile-page"}).find("div", {"class": "summoner-profile-container content-side-padding"}).find("div", {"class": "summoner-profile_content-container"}).find("div", {"class": "summoner-profile_overview2"}).find("div", {'class': 'summoner-profile_overview__side'}).find("div", {"class": "rank-block"}).find("div", {"class": "rank-list"}).find("div", {"class": "rank-lp-container"}).find("div", {"class": "content-section content-section_no-padding rank-content"}).find("div", {"class": 'rank-sub-content'}).find("div", {"class": "text-container"}).find("div", {"class": "rank-wins"}).find_all('span')
                    wrInt = float(wr[1].getText().replace('% Win Rate', ""))
                    total = wr[0].getText()
                    total = float(total[0: str(total).find('W')]) + float(total[str(total).find('W') + 2: str(total).find('L')])
                    r[i] = wrInt / 100
                    t[i] = total
                except Exception as e: 
                    print(e)
                    print(url)
                    continue
                    print('ugg error 1')
                try:
                    url = 'https://u.gg/lol/profile/na1/' + name + '/champion-stats'
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
                    sleep(1)
                    source = requests.get(url, headers=headers, timeout=10).text
                    soup = BeautifulSoup(source, "html.parser")
                    ugg = soup.find('body').find('div', {'id': 'root'}).find('div', {'class': 'desktop-container router-container'}).find('div', {'id': 'page-content'}).find('div', {'style': 'width:100%'}).find('div', {'id': 'main-content'}).find('div', {'id': 'content-wrapper'}).find('div', {'id': 'content'}).find('div', {'class': 'summoner-profile-page'}).find('div', {'class': 'summoner-profile-container content-side-padding'}).find('div', {'class': 'summoner-profile_content-container'}).find('div', {'class': 'summoner-profile_champion-stats'}).find('div', {'class': 'content-section ReactTable ugg-table-2 profile-champion-stats-table'}).find('div', {'class': 'rt-tbody'}).find_all('div', {'class': 'rt-tr-group'})
                    for d in ugg:
                        if d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'champion-cell'}).find('a').find('span').getText() == defName:
                            temp = d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'win-rate-cell'}).find('div').find('span', {'class': 'match-record'}).getText()
                            temp = float(temp[0: str(temp).find('W')]) + float(temp[str(temp).find('W') + 2: str(temp).find('L')])
                            cTotal[i] = temp
                            cwr[i] = float(d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'win-rate-cell'}).find('div').find('strong').getText().strip('%')) / 100
                            kda[i] = float(d.find('div', {'class': 'rt-tr'}).find('div', {'class': 'kda-cell'}).find('div').find('div').find('strong').getText())
                            break
                except Exception as e: 
                    print(e)
                    print(url)
                    continue
            win = match_detail['info']['participants'][0]['win']
            if (win == True):
                winnerNow = 1
            else:
                winnerNow = 0
            new_row = {'blueTops' : bt, 'btlevel': level[0], 'btmp': ms[0],'btwr': r[0], 'btcwr': cwr[0], 'btkda': kda[0], 'btct': cTotal[0], 'btt': t[0],'blueJngs': bj, 'bjlevel': level[1], 'bjmp': ms[1],'bjwr': r[1],  'bjcwr': cwr[1], 'bjkda': kda[1], 'bjct': cTotal[1], 'bjt': t[1],'blueMids': bm, 'bmlevel': level[2], 'bmmp': ms[2],'bmwr': r[2], 'bmcwr': cwr[2], 'bmkda': kda[2], 'bmct': cTotal[2], 'bmt': t[2],'blueBots': bb, 'bblevel': level[3], 'bbmp': ms[3],'bbwr': r[3], 'bbcwr': cwr[3], 'bbkda': kda[3], 'bbct': cTotal[3], 'bbt': t[3],'blueSups': bs, 'bslevel': level[4], 'bsmp': ms[4],'bswr': r[4],  'bscwr': cwr[4], 'bskda': kda[4], 'bsct': cTotal[4], 'bst': t[4],'redTops': rt,'redJngs': rj,'redMids': rm,'redBots': rb,'redSups': rs, 'winner': winnerNow}
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)
                df = df.append(new_row, ignore_index=True)
        except Exception as e: 
            print(e)
            sleep(2)

    
    print(df)
    df.to_csv('LeagueMatches4.csv')

