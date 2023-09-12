import Utils
import FileHandling
import os

manga = "Berserk"
minimum = "Episode"
division = "Chapter"

naming = {"Episode":{"inversion":False,"numeration":False},
          "Title":{"inversion":False,"numeration":True},
          "Volume":{"inversion":False,"numeration":False},
          "Chapter":{"inversion":True,"numeration":False},
          "Arc":{"inversion":True,"numeration":False}}


Utils.preparationForCBZ(manga,minimum,division,naming)


quit()
