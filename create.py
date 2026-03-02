from creators import MangaCreator
import os

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Manga")
manga = "Berserk"
division = "Episode"

mangaCreator = MangaCreator(manga, directory)
mangaCreator.createFiles(division, "CBZ")
