from selenium.webdriver.common.by import By
from abc import ABC, abstractmethod
from modules import Internet


class BaseDownloader(ABC):

    chapterLinks: list[str]
    foundName: str
    mainUrl: str

    def __init__(self, manga: str):
        """
        Initializes the BaseDownloader with the name of the manga to be downloaded.

        Args:
            - manga (str): The name of the manga to be downloaded.

        Returns:
            - None
        """
        self.manga = manga

    @abstractmethod
    def findChapters(self) -> None:
        """
        This funtion needs store the a list of the urls
        of each chapter of the manga as set self.chapterLinks.
        If nothing is found, self.chapterLinks should be an empty list.

        If len(self.chapterLinks) > 0 it must also set:
            - self.foundName
            - self.mainUrl

        Args:
            - None

        Returns:
            - None
        """
        pass

    @abstractmethod
    def getChapterImages(self, chapterUrl: str) -> list[str]:
        """
        This function needs to return a list of the urls of
        the images of the chapter given by chapterUrl.

        Args:
            - chapterUrl (str): The url of the chapter.

        Returns:
            - list[str]: A list of the urls of the images of the chapter.
        """
        pass

    def getDriver(self) -> Internet.webdriver.Chrome:
        """
        Returns a configured Chrome WebDriver instance.

        Args:
            - None

        Returns:
            - Internet.webdriver.Chrome: A configured Chrome WebDriver instance.
        """
        driver = Internet.configureChrome()

        # Override attachShadow BEFORE page load
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": """
                (function() {
                    const originalAttachShadow = Element.prototype.attachShadow;
                    Element.prototype.attachShadow = function(init) {
                        return originalAttachShadow.call(this, { mode: 'open' });
                    };
                })();
                """},
        )

        return driver

    def skipCloudflare(
        self, driver: Internet.webdriver.Chrome
    ) -> Internet.webdriver.Chrome:
        """
        Try to skip Cloudflare protection if it is present.

        Args:
            - driver (Internet.webdriver.Chrome): The Chrome WebDriver instance.

        Returns:
            - Internet.webdriver.Chrome: The Chrome WebDriver instance after trying to skip Cloudflare.
        """
        hosts = driver.find_elements(By.CSS_SELECTOR, "div")

        for host in hosts:
            shadow_root = driver.execute_script("return arguments[0].shadowRoot", host)
            if shadow_root:
                break

        outer_iframe = shadow_root.find_element(By.CSS_SELECTOR, "iframe")
        driver.switch_to.frame(outer_iframe)
