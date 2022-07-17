from .account import Account
from .match import Match
from .regions import Region, Continents
import requests
import logging

class RiotApi:
    def __init__(self, key:str = None, defaultRegion:Region = Region.EUW) -> None:
        #Load apikey from file 
        if key == None:
            self.apikey = open("riotApiToken", "r").read()
        else:
            self.apikey = key
        self.defaultRegion = defaultRegion
        self.headers = {"X-Riot-Token": self.apikey}

    def query(self, url:str, params = {}, givenRegion:Region = None):
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

    def selectRegion(self, givenRegion:Region) -> Continents:
        if givenRegion == Region.EUNE or givenRegion == Region.EUW:
            return Continents.EUR
        if givenRegion == Region.NA:
            return Continents.AME
        if givenRegion == Region.KR:
            return Continents.ASIA
        
        return None

    def getAccountbyId(self, puuid:str, region:Region = Region.EUW) -> Account:
        searchUrl = f"/summoner/v4/summoners/by-puuid/{puuid}"

        s = self.query(searchUrl, {}, region)

        '''
        {
            "id": "0Hyo2B37TOKJ28QFrRdLFAFdbYlETQ0532wBfcZcghKEZE7dRjCM328Q_Q",
            "accountId": "dbxbB7Z2IRzwaDxcNyuNDy4miHuzrNzyRqEWtDJdgOzQO8fB0veMh1Fi",
            "puuid": "_VdDuxi52TkNO78cfZ1S5yFjjt1PEDbRnRIElOwafi8PsUJK__sFuJwAGcxpWG-GwqmObLbC6Am5zA",
            "name": "saponetta21212",
            "profileIconId": 1211,
            "revisionDate": 1654636615000,
            "summonerLevel": 359
        }
        '''

        a = Account(s, self, region)
        return a

    def getAccount(self, username: str, region:Region = Region.EUW) -> Account:
        searchUrl = f"/summoner/v4/summoners/by-name/{username}"

        s = self.query(searchUrl, {}, region)

        a = Account(s, self, region)
        return a

    def getLastMatchIds(self, given:str, givenRegion:Region = Region.EUW):
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

    def getMatchData(self, match:Match):
        searchUrl = f"/match/v5/matches/{match.matchId}"

        return self.query(searchUrl, {}, match.region)

    def getMatch(self, matchId:str, givenRegion:Region = Region.EUW) -> Match:
        searchUrl = f"/match/v5/matches/{matchId}"
        print("getMatch:SearchURL ", searchUrl)
        region = self.selectRegion(givenRegion)

        dt = self.query(searchUrl, {}, region)

        m = Match(matchId, region, self)

        m.bind(self)

        m.rawData = dt

        return m
