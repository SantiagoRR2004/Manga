import mangaUtils
import os

directory = os.path.dirname(os.path.abspath(__file__))
manga = "Berserk"
division = "Episode"

mangaCreator = mangaUtils.MangaCreator(manga, directory)
mangaCreator.createFiles(division, "CBZ")
