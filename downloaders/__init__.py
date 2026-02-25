from .baseDownloader import BaseDownloader

# The list of individual downloaders
from .mangaboltDownloader import MangaboltDownloader
from .mangaclashDownloader import MangaClashDownloader
from .mangadexDownloader import MangaDexDownloader
from .mangafireDownloader import MangaFireDownloader
from .weebcentralDownloader import WeebCentralDownloader

DOWNLOADERS: list[type[BaseDownloader]] = [
    MangaboltDownloader,
    MangaClashDownloader,
    MangaDexDownloader,
    MangaFireDownloader,
    WeebCentralDownloader,
]


# Only export the MangaDownloader class
from .mangaDownloader import MangaDownloader

__all__ = ["MangaDownloader"]
