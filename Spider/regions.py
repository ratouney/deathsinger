from enum import Enum

# The split is only made for API side which requires Continents
# and the servers which themselves require a different tag that I call Region

class Region(Enum):
    EUW = "euw1"
    NA = "na1"
    EUNE = "eun1"
    KR = "kr"

class Continents(Enum):
    EUR = "europe"
    AME = "americas"
    ASIA = "asia"

