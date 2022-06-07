import riot
import account
import match
from regions import Region, Continents
import logging

logging.basicConfig(level=logging.INFO)

c = riot.RiotApi()

a = c.getAccount("Quantum", Region.NA)

ms = a.getLastMatchIds()

print(ms)

#mats = match.Matches(ms, Continents.AME, c, True)

#print(mats[0].getTeams())

m = match.Match(ms[0], Continents.AME)
m.bind(c)
m.load()

#print(m.rawData)

print(m.getMatchups())
print(m.getTeams())
  