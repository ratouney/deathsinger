from neo4j import GraphDatabase, work
from Codex import Connector
from Codex.node import syncTypes
from Spider.account import Account
from Spider.match import Match
from Spider.riot import RiotApi, Region, Continents

import logging

logging.basicConfig(level=logging.INFO)

c = Connector("bolt://localhost:7687", "neo4j", "password")

rito = RiotApi()

a = rito.getAccount("Quantum", Region.NA)

ms = a.getLastMatchIds()

print(ms)

m = Match(ms[0], Continents.AME, rito, True)

matchups = m.getMatchups()

for elem in matchups["matchups"]:
    print(elem)
