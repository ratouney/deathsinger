class Nothing:
    def __init__(self, name) -> None:
        self.name = name
        self.data = []

    def __repr__(self) -> str:
        s = self.name + '['
        prev = False
        for k in self.data:
            if prev == True:
                s += ';'
            s += k
            prev = True
        s += ']'
        return s

    def __str__(self) -> str:
        return "Nothing"

    def fill(self, stuff):
        self.data.append(stuff)

    def size(self) -> int:
        return self.data.__sizeof__()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    
n = Nothing("hello")
n.fill("big")
n.fill("alot of stuff")
# print(n)

def getStuff(s:str = None) -> str or bool:
    return "stuff"

stuff = getStuff()
