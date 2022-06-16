import json
import logging

f = open("./champColorRatio.json", "r")

data = json.load(f)

teams = [
    ["darius", "trundle", "leblanc", "sivir", "braum"],
    ["ornn", "sejuani", "malzahar", "vayne", "taric"]
]

class TeamScale:
    def __init__(self, size:int = 5) -> None:
        self.champs = []
        self.defaultScale = []
        self.size = size
        for k in range(0, size):
            self.defaultScale.append(0)
        print("DefaultScale set to : ", self.defaultScale)
        self.scalesTotal = list(self.defaultScale)

    def addChamp(self, name:str):
        if name in self.champs:
            logging.error(f'{name} is already in this team')
            return
        self.champs.append(name)
        
        print(f'Adding {name} ', data[name]['scales'])
        for k in range(len(self.scalesTotal)):
            self.scalesTotal[k] += data[name]["scales"][k]

    def removeChamp(self, name:str):
        if name not in self.champs:
            logging.error(f'{name} is not in this team, cannnot remove')
            return
        
        self.champs.remove(name)
        for k in self.scalesTotal:
            self.scalesTotal[k] -= data[name]["scales"][k]

    def weightedScale(self):
        rt = list(self.defaultScale)
        for k in range(len(self.scalesTotal)):
            rt[k] = self.scalesTotal[k] / len(self.scalesTotal)
        return rt

    def decomposeWhiteScale(self):
        rt = list(self.defaultScale)
        if len(self.champs) <= 1:
            logging.error("Not enough champions to form white relations")
            return
        
        isWhite = []
        other = []
        for k in self.champs:
            if data[k]['scales'][3] > 0:
                isWhite.append(k)
            else:
                other.append(k)

        if len(isWhite) == 0:
            logging.error("No white champs to compute")
            return

        nonWhiteScale = list(self.defaultScale)
        for k in other:
            for i in range(0, self.size):
                nonWhiteScale[i] += data[k]['scales'][i]
                # print(f'Added {k}\'s value of ', data[k]['scales'][i])
        print("Non white ? ", nonWhiteScale)

        whiteScale = list(self.defaultScale)
        for k in isWhite:
            for i in range(0, self.size):
                whiteScale[i] += data[k]['scales'][i]
        print("is White ? ", whiteScale)

        # highestScale = max(nonWhiteScale)
        # idx = [i for i, j in enumerate(nonWhiteScale) if j == highestScale]
        # print("Highest ? ", idx)
        nonWhiteTotal = sum(nonWhiteScale)
        whiteTotal = sum(whiteScale)

        decomposedWhiteScale = list(nonWhiteScale)
        for k in range(0, self.size):
            #Take the % of the total Non white each part represents
            nonWhitePercentForColor = nonWhiteScale[k] / nonWhiteTotal
            # Add the %'ed total of to that color
            decomposedWhiteScale[k] += whiteTotal * nonWhitePercentForColor
        decomposedWhiteScale[3] = 0
        print("===", decomposedWhiteScale)

t1 = TeamScale()
for champ in teams[0]:
    t1.addChamp(champ)
t2 = TeamScale()
for champ in teams[1]:
    t2.addChamp(champ)

print(t1.champs)
print(t1.scalesTotal)
print(t1.decomposeWhiteScale())
print(t2.champs)
print(t2.scalesTotal)
print(t2.decomposeWhiteScale())
