import json
import math
import logging
from PIL import Image
from typing import List

class TeamScale:
    def __init__(self, size:int = 5) -> None:
        self.champs = []
        self.defaultScale = []
        self.size = size
        for k in range(0, size):
            self.defaultScale.append(0)
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
        return decomposedWhiteScale

class ColorScale:
    def __init__(self, width:int=500, height:int=100) -> None:
        self.width = width
        self.height = height
        self.im = Image.new('RGB', (width, height))
        self.ld = self.im.load()

    def gaussian(self, x, a, b, c, d=0):
        return a * math.exp(-(x - b)**2 / (2 * c**2)) + d

    def pixel(self, x, width=100, map=[], spread=1.5):
        width = float(width)
        r = sum([self.gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
        g = sum([self.gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
        b = sum([self.gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
        return min(1.0, r), min(1.0, g), min(1.0, b)

    def buildScale(self, ratios: List[int]):
        print("Building with : ", ratios)
        s = sum(ratios)
        heatmap = []
        # Adding red
        p = 0
        # Colors are : [factor, (R, G, B)]
        red = [p, (1, 0, 0)]
        p += ratios[0] / s
        green = [p, (0, 1, 0)]
        p += round(ratios[1] / s, 2) + 0.1
        blue = [p, (0, 0, 1)]
        p += round(ratios[2] / s, 2) + 0.1
        white = [p, (.3, .3, .3)]
        p += round(ratios[3] / s, 2) + 0.1
        black = [p, (1, 1, 1)]
        print("S : ", s)
        print("Red : ", round(ratios[0] / s, 2))
        print("Green : ", round(ratios[1] / s, 2))
        print("Blue : ", round(ratios[2] / s, 2))
        print("White : ", round(ratios[3] / s, 2))
        print("Black : ", round(ratios[4] / s, 2))
        heatmap = [red, blue, green, white, black]
        print("Heatmap : ", heatmap)

        for x in range(self.width):
            r, g, b = self.pixel(x, width=self.width, map=heatmap, spread=1.3)
            r, g, b = [int(256*v) for v in (r, g, b)]
            for y in range(self.height):
                self.ld[x, y] = r, g, b
    
    def output(self, filename:str = "grad.png"):
        self.im.save(filename)


f = open("./champColorRatio.json", "r")

data = json.load(f)

teams = [
    ["renekton", "trundle", "leblanc", "draven", "taric"],
    ["ornn", "sejuani", "malzahar", "vayne", "taric"]
]

t1 = TeamScale()
for champ in teams[0]:
    t1.addChamp(champ)
# t2 = TeamScale()
# for champ in teams[1]:
    # t2.addChamp(champ)

g = ColorScale()
g.buildScale(t1.scalesTotal)
# g.buildScale(t1.decomposeWhiteScale())
g.output("t1.png")

# print(t1.champs)
# print(t1.scalesTotal)
# print(t1.weightedScale())
# print(t1.decomposeWhiteScale())
# print(t2.champs)
# print(t2.scalesTotal)
# print(t2.weightedScale())
# print(t2.decomposeWhiteScale())
