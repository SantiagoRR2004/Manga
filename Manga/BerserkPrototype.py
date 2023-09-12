import Utils
import FileHandling
import Internet
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


script = """
var mainContainerElements = document.getElementsByClassName('MainContainer');
var images = [];
for (var i = 0; i < mainContainerElements.length; i++) {
  var container = mainContainerElements[i];
  var imgElements = container.getElementsByTagName('img');
  for (var j = 0; j < imgElements.length; j++) {
    images.push(imgElements[j]);
  }
}
return images;
"""

folder = ".BerserkJPG"
web = "https://mangasee123.com/read-online/Berserk-chapter-99.5-index-2-page-1.html"


FileHandling.ensureExistance(folder)

driver = Internet.configureChrome()


    
driver.get(web)

Internet.clickButton(driver,"Long Strip")


image_elements = driver.execute_script(script)

png_image_urls = []

png_image_urls = Internet.findPNGs(driver)


for i in range(len(png_image_urls)):
    name = "Prototype" + "{:0>{}}".format(i, 3) + ".jpg" # Try to change it to png
    Internet.downloadImage(png_image_urls[i], os.path.join(folder,name))

    
print("Se ha descargado el prototipo ")

driver.quit()

FileHandling.zipAndDelete(folder)

quit()

