# import Codex
import Spider.match
import json

f = open("./Spider/data.json", "r")
data = f.readlines()

jdat = json.loads(data[0])
print(jdat)

# m = Spider.match.Match("None")
# m.load(jdat)

for k in jdat:
    print(f'{k} -> ', jdat[k])

# m.getMatchups()