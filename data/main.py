import requests
import numpy as np

apikey = "RGAPI-776294dc-4b33-4b18-96a6-1279018d506d"

class LeagueApi:
    def __init__(self, key):
        self.apikey = key
        self.defaultRegion = "euw1"
        self.headers = {"X-Riot-Token": apikey}

    def query(self, url, params = {}, givenRegion = None):
        if givenRegion == None:
            region = self.defaultRegion
        else:
            region = givenRegion

        baseUrl = f'https://{region}.api.riotgames.com/lol'

        return requests.get(baseUrl + url, params=params, headers=self.headers).json()

    def getAccount(self, username: str):
        searchUrl = f"/summoner/v4/summoners/by-name/{username}"

        return Account(self.query(searchUrl))

    def getAccountFromId(self, puuid: str):
        searchUrl = f"/summoner/v4/summoners/by-puuid/{puuid}"

        return Account(self.query(searchUrl))

    def getMatch(self, matchId):
        return Match(matchId, load=True, givenApi=self)
    
    def getMatchData(self, matchId, givenRegion="europe"):
        searchUrl = f"/match/v5/matches/{matchId}"

        return self.query(searchUrl, {}, givenRegion)

    def getLastMatchIds(self, given, givenRegion = "europe"):
        puuid = None
        if type(given) == Account:
            puuid = given.puuid
        elif type(given) == str:
            puuid = self.getAccount(given).puuid

        searchUrl = f"/match/v5/matches/by-puuid/{puuid}/ids"

        return self.query(searchUrl, {}, givenRegion)

class Account:
    def __init__(self, params, boundApi = None):
        print("Building from : ", params)
        self.api = boundApi
        self.id = params['id']
        self.accountId = params['accountId']
        self.puuid = params['puuid']
        self.name = params['name']
        self.profileIconId = params['profileIconId']
        self.summonerLevel = params['summonerLevel']

    def bind(self, api):
        self.api = api

    def __repr__(self):
        return f'Account[{self.name}::{self.accountId}]'

    def getLastMatchIds(self):
        return api.getLastMatchIds(self)


name = "i am Vander"
headers = {"X-Riot-Token": apikey}
params = {""}

api = LeagueApi(apikey)
# rt = api.getMatchData("EUW1_5595465818")
#import json
#with open('data.json', 'r') as json_file:
#    rt = json.load(json_file)
#
#ps = rt['metadata']['participants']
#psAccounts = []

class Match:
    def __init__(self, matchId, load=False, givenApi=None):
        self.matchId = matchId
        self.api = givenApi
        self.rawData = None
        if load:
            self.load()

    def bind(self, givenApi):
        self.api = givenApi

    def setMatchId(self, givenId):
        if self.matchId != givenId:
            print("Reset the class !")
        self.matchId = givenId

    def load(self, force=None):
        if self.api == None and force == None:
            print("Not connected to API")
            return False
        
        if force == None:
            self.rawData = self.api.getMatchData(self.matchId)
        else:
            self.rawData = force

    def getTeams(self):
        for player in self.rawData['info']['participants']:
            print(f'.. {player["summonerName"]} playing {player["championName"]}::{player["championId"]} in {player["lane"]}::{player["role"]}')

    def getMatchups(self):
        data = {}
        participants = []
        for player in self.rawData['info']['participants']:
            participants.append(player["summonerId"])
            pos = player["teamPosition"]
            champId = player["championId"]
            if pos not in data:
                data[pos] = {"champs": [], "winner": None}
            if pos in data:
                data[pos]["champs"].append(champId)
            if player["win"]:
                data[pos]["winner"] = champId
        rt = {"matchId": self.matchId,  "participants": participants, "matchups": data}
        return rt

#m = Match("EUW1_5595465818")
#m.load(rt)
#rt = m.getMatchups()
#print(rt)

#acc = api.getAccount("AwAlcea")
#ids = acc.getLastMatchIds()
#
#print(ids)
#matches = []
#for id in ids:
#    m = api.getMatch(id)
#    rt = m.getMatchups()
#    matches.append(rt)

#np.save("matches", matches)
matches = np.load("./matches.npy", allow_pickle=True)

#print(matches)

m = api.getMatch("EUW1_5595465818")
rt = m.getMatchups()

f = filter(lambda match: match['matchId'] == "EUW1_5595465818", matches)
print(list(f))