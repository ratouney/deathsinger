from neo4j import GraphDatabase, work
from Codex import Connector
from Codex.node import syncTypes

import logging

logging.basicConfig(level=logging.INFO)

c = Connector("bolt://localhost:7687", "neo4j", "password")

f = open('./Spider/champIds', 'r')
lines = f.readlines()

c.query("MATCH (c:Champion) DETACH DELETE c")

for line in lines:
    toks = line.strip().split(':')
    print(f'--{toks[1]}[{toks[0]}]--')
    c.createNode("Champion", toks[0], name=toks[1])