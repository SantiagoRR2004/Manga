from .baseDownloader import BaseDownloader


class MangaDexDownloader(BaseDownloader):

    def findChapters(self) -> None:
        # TODO
        self.chapterLinks = []

    def getChapterImages(self, chapterUrl: str) -> list[str]:
        # TODO
        return []
