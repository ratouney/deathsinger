# import Codex
import Spider.match
import Codex.connector
import Codex.node
import logging
import Spider.riot
from Spider.regions import Continents, Region
import json

class Norra():
    def __init__(self, connector:Codex.connector.Connector, api:Spider.riot.RiotApi) -> None:
        self.api = api
        self.db = connector

    def __initAccount__(self, puuid:str, username:str):
        newAcc = self.db.createNode("Account", puuid, username=username)
        return newAcc

    def __initMatch__(self, matchId:str, region:Region = Region.EUW):
        # Checking if it exists, by any chance
        matchNode = self.db.getNode("Match", matchId)
        print("MatchNode : ", matchNode)
        print("MatchID : ", matchId)
        if matchNode == None:
            matchData = self.api.getMatch(matchId, region)
            print("MatchData : ", matchData)

            for k in matchData.rawData:
                print("keys:", k)
            matchNode = self.db.createNode("Match", matchId, meta=matchData.rawData['metadata'], data=matchData.rawData['info'])
        else:
            raise Exception(f'MatchNode[{region}:{matchId}] already exists, please dont fuck it up')
        print("Creating match in Database with links")
        if len(matchNode['meta']['participants']) != 10:
            logging.info(f'Match{matchId} is not a standard 5vs5, care!')
        # for k in matchDB['meta']:
        for k in matchNode['meta']['participants']:
            print(f'Find user with puuid[{k}]')
            accountNode = self.db.getNode("Account", k)
            # If there is no node ready in the DB
            if accountNode == None:
                # Load data from RIOT
                acc = self.api.getAccountbyId(k, region)
                # Create a node of our own
                accountNode = self.__initAccount__(k, acc.name)
            # Link the node to our current match
            accountNode.link(matchNode, "PLAYED_IN")

        return matchNode

    def getMatch(self, matchId:str, region:Region = Region.EUW):
        m = None
        print("Getting a match")
        try:
            m = self.db.getNode("Match", matchId)
        except Codex.node.IDNotFound:
            print("Not found in DB, load from API")
            pass
        except Codex.connector.NotConnected:
            print("Not connected to DB")
            return None

        # Match isn't in DB, building node and relations
        if m == None:
            print("Loading it")
            m = self.__initMatch__(matchId, region)
        
        return m

c = Codex.connector.Connector("bolt://localhost:7687", "neo4j", "password")
key = open("./Spider/riotApiToken", "r").read()
r = Spider.riot.RiotApi(key)

# c.deleteNode("Match", "EUW1_5832516599")

a = r.getAccount("Aurea")
mids = a.getLastMatchIds()
print(mids)

n = Norra(c, r)

ms = []
for id in mids:
    ms.append(n.getMatch(id, Region.EUW))


import json

j = json.loads(ms[0].rawData["data"])
print(ms[0].id)
m = Spider.match.Match(ms[0].id, Region.EUW)


# m = n.getMatch("EUW1_5832516597")
# m = n.getMatch("EUW1_5832516598")
# m = n.getMatch("EUW1_5832516599")
# n.__initMatch__("EUW1_5832516597", Region.EUW)

#print("M : ", m)
