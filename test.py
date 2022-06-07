from neo4j import GraphDatabase, work
from Codex import Connector
from Codex.node import syncTypes

import logging

logging.basicConfig(level=logging.INFO)

c = Connector("bolt://localhost:7687", "neo4j", "password")

#rt = c.run("CREATE (m:Match {id:\"SDF123\"}) RETURN m")
#print(rt)


#n = c.getNode()
aatrox = c.getNode("Champion", 203)
current = c.getNode("Match", 456)

aatrox.unlink(current, "PRESENT_IN")


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
