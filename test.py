from tkinter import E
from neo4j import GraphDatabase, work
from Codex import Connector
from Codex.node import syncTypes

import logging

logging.basicConfig(level=logging.INFO)

c = Connector("bolt://localhost:7687", "neo4j", "password")

#a = c.createNode("Legume", 1)
#b = c.createNode("Legume", 5, name="Carotte")

bet = c.getNode("Legume", 1)
cat = c.getNode("Legume", 5)

bet.unlink(cat, "PSLFKSMLDKFSDLMF")


#c.createNode("Champion", 107, name="Rengar", role="Jungle")

#rt = c.run("CREATE (m:Match {id:\"SDF123\"}) RETURN m")
#print(rt)

#[status, data] = c.createNode("Game", 123)
#t = c.createNode("Game", 124)

#print("Worked ? : ", status)
#print("d : ", data)

#print("Another : ", t)

#n = c.getNode()
#aatrox = c.getNode("Champion", 203)
#current = c.getNode("Match", 456)

#aatrox.unlink(current, "PRESENT_IN")


#b.set(type="bruiser", size="enourmours", baseHP=633)

#b["size"] = "enourmous"
#b.sync(syncTypes.ALLOW_EMPTY)

#b.getLinks("Match")

#print("Before ", b["size"])
#b["size"] = "big"
#print("After ", b["size"])

#b.commit()

#print("Outside : ", rt)

#b = Block(s, "Match")

#b.setAttribute("Greeting")
#rt = b.get(message="boink")

#print(rt)

#c.close()
