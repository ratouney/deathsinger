from email.mime import base
from account import Account
from match import Match
from regions import Region, Continents
import requests
import logging

class RiotApi:
    def __init__(self, defaultRegion = Region.EUW) -> None:
        #Load apikey from file 
        self.apikey = open("token", "r").read()
        self.defaultRegion = defaultRegion
        self.headers = {"X-Riot-Token": self.apikey}

    def query(self, url, params = {}, givenRegion = None):
        if givenRegion == None:
            region = self.defaultRegion.value
        else:
            region = givenRegion.value

        baseUrl = f'https://{region}.api.riotgames.com/lol'

        logging.info(f'Querying ' + baseUrl + url)

        r = None
        try:
            r = requests.get(baseUrl + url, params=params, headers=self.headers).json()
        except Exception as err:
            logging.error("Query Failed : ", err)

        return r

    def selectRegion(self, givenRegion):
        if givenRegion == Region.EUNE or givenRegion == Region.EUW:
            return Continents.EUR
        if givenRegion == Region.NA:
            return Continents.AME
        if givenRegion == Region.KR:
            return Continents.ASIA
        
        return None

    def getAccount(self, username: str, region = Region.EUW):
        searchUrl = f"/summoner/v4/summoners/by-name/{username}"

        s = self.query(searchUrl, {}, region)

        a = Account(s, self, region)
        return a

    def getLastMatchIds(self, given, givenRegion = Region.EUW):
        puuid = None
        region = givenRegion

        if type(given) == Account:
            puuid = given.puuid
            region = given.region
        elif type(given) == str:
            puuid = self.getAccount(given).puuid

        region = self.selectRegion(region)
        searchUrl = f"/match/v5/matches/by-puuid/{puuid}/ids"

        return self.query(searchUrl, {}, region)

    def getMatchData(self, match):
        searchUrl = f"/match/v5/matches/{match.matchId}"

        return self.query(searchUrl, {}, match.region)

    def getMatch(self, matchId, givenRegion = Continents.EUR):
        searchUrl = f"/match/v5/matches/{matchId}"

        dt = self.query(searchUrl, {}, givenRegion)

        m = Match(matchId, givenRegion, self)

        m.bind(API)

        m.rawData = dt

        return m
