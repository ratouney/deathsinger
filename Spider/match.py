import logging
from .regions import Region, Continents

class Match:
    def __init__(self, matchId, givenRegion:Continents = Continents.EUR, givenApi = None, load:bool=False):
        self.matchId = matchId
        self.region = givenRegion
        self.api = givenApi
        self.rawData = None
        logging.info(f'Creating match with [{self.region.value}:{matchId}]')
        if load:
            self.load()

    def __repr__(self) -> str:
        return f'[{self.region}:{self.matchId}]'

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
            self.rawData = self.api.getMatchData(self)
        else:
            self.rawData = force

    def getTeams(self):
        data = []
        i = 0
        #print(self.rawData['info']['participants'][0])
        for player in self.rawData['info']['participants']:
            block = {}
            print(player['teamId'])
            block["teamId"] = player['teamId']
            block["summonerName"] = player["summonerName"]
            block["championName"] = player["championName"]
            block["championId"] = player["championId"]
            block["lane"] = player["lane"]
            block["role"] = player["role"]
            data.append(block)
            print(f'.. {player["summonerName"]} playing {player["championName"]}::{player["championId"]} in {player["lane"]}::{player["role"]}')
            i += 1
        return data

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

    def laningPhase(self):
        data = {}
        for player in self.rawData['info']['participants']:
            block = {}
            'laneMinionsFirst10Minutes'
            'laningPhaseGoldExpAdvantage'
            'laningPhaseMinionDifference'
            'laningPhaseItemDifference'

class Matches:
    def __init__(self, matchIds, givenRegion = Continents.EUR, givenApi=None, load=False) -> None:
        self.matchIds = matchIds
        self.region = givenRegion
        self.api = givenApi
        self.rawData = []
        logging.info(f'Creating matches with {self.region.value}:{matchIds}')
        if load:
            for id in matchIds:
                m = Match(id, givenRegion, givenApi, True)
                self.rawData.append(m)

    def size(self) -> int:
        return self.rawData.__sizeof__()

    def __getitem__(self, key) -> Match:
        return self.rawData[key]

    def __setitem__(self, key, value):
        self.rawData[key] = value