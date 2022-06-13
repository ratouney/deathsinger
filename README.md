# Deathsinger - A colorful analysis of League champion data

## Why ?

A [certain LoL personality](https://twitter.com/LSXYZ9) had a justified obscession with the importance of drafting. Following a [long stream discussion with a MagicTheGathering pro](https://www.youtube.com/watch?v=Qj3JV5CeLBk&t=4807s), they tried to determine how you would represent it's color coding in League of Legends. I wanted to analyse this idea and apply it not only
to pro play but to every single ELO bracket.


---
## How ?

In the card game Magic the Gathering, all cards are split into 5 colors :
- <span style="color:red;background:#B1B1B1">Red</span>
- <span style="color:blue;background:#B1B1B1">Blue</span>
- <span style="color:green;background:#B1B1B1">Green</span>
- <span style="color:white;background:#B1B1B1">White</span>
- <span style="color:black;background:#B1B1B1">Black</span>

Depending on that color, the card belongs to a certain archetype or strategic familly of options. It can also have multiple colors.

The goal of this analysis is to attribute a color to each champion in League of Legends and compare if certain schools are more effective than others.

To do this, colors have been "simplified" to these criteria :

| Color | Description |
| --- | --- |
| Red | Aggressive, early game, requires snowball |
| Blue | Terrain control, denial |
| Green | Scaling, requires ressources or provides them |
| White | Fluid, reinforces team color |
| Black | Conditional, Quest System |

Now, with 5 champions on every team, we would build a "chromatic scale" to each and determine the dominant color of each. Then using the statistics of each game, be it early game advantages, midgame objectives and ultimately the win, we would try to determine which strategy has the highest succcess chance.

---

## Program Structure 

The project is made using Python and Neo4j. The database could have been a simple relational but I wanted to experience using a graph based one so it's purely fluff.

Different parts have been made to visualise it's progress : 

- Codex : a Python interface for Neo4J
- Spider : a Python interface for the RiotAPI
- Norra : the combined Data structure for the above

--- 

## Important Notes

All of the color definitions for the champions are subjective and might change depending on the evolution of League meta, patches, item changes and so forth. 
Using avaliables ressources and general consensus of Reddit Analysts (yeah, i know....), an initial table has been created. 

I will be choosing to represent each as a % instead of boleans for each color to better reflect each champion's main school of color, such as :

J4 [80% Red / 20%White]

Karthus [70% Black / 30% Green]

Some champions may even have different color schemes for different elo brackets but that would be a modelisation I won't be taking into account since I do not know how I would build it.