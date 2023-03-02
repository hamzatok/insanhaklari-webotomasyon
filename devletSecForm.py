from driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

class Devletler:
    driver = driver

    def __init__(self):
        self.devletSozluk = {}

    # Devletlerin bulunduğu formdaki tamam butonu
    @property
    def tamam(self):
        return driver.find_element(By.ID, "ContentPlaceHolder1_ButtonDevlet")

    # Devletlerin bulunduğu formdaki Vazgeç butonu
    @property
    def vazgec(self):
        return driver.find_element(By.LINK_TEXT, "Vazgeç")

    # devletlerin bulunduğu formdaki checkbox ve label'ları barındıran td elementinin listesini döndürüyor 
    # (list[td(input,label)])
    def __devletListElement(self) -> list[WebElement]:
        # devlet checkboxlarının bulunduğu "table" etiketine ID üzerinden ulaştık.
        tableElement = driver.find_element(By.ID, "ContentPlaceHolder1_CheckBoxListDevlet")
        # devlet chexkboxlarının bulunduğu satırların yani "tr" elementlerinin listesini oluşturduk[trWebelement[td,td,td]]
        satirlar = tableElement.find_elements(By.TAG_NAME, "tr")   
        devletlerList = []
        # ulaştığımmız satırların(tr elementinin) kolonlarına(td elementlerine) for döngüsü ile ulaşıyoruz.
        for satir in satirlar:
            # satırlardaki kolonların (td etiketlerin) her birine ulaşıyoruz."[td,td,td]
            kolonlar = satir.find_elements(By.TAG_NAME, "td")
            devletlerList.extend(kolonlar)
        

        return devletlerList
    

    # herbir "td" web elementinin bulunduğu listeyi bu fonksiyona vereceğiz daha sonra bunların içindeki label ve inputaları bir sözlük şeklinde kaydedeceğiz. -> {"devletAdi:checkBoxId"}
    def devletlerSozluk(self) -> dict:
        # yukarıda oluşturduğum her bir td webelementinin listesini değişkene atadık.
        devletlerList = self.__devletListElement()
        devletlerSozluk = {}
        for devlet in devletlerList:
            try:
                checkBox = devlet.find_element(By.TAG_NAME, "input")
                checkBoxId = checkBox.get_attribute("id")
                labelText = devlet.find_element(By.TAG_NAME, "label").text
                devletlerSozluk[labelText] = checkBoxId
            except NoSuchElementException:
                continue
        return devletlerSozluk
        

    def devletIsaretle(self, devletList:list[str]):
        for devletName in devletList:
            devletInput = self.driver.find_element(By.ID, self.devletlerSozluk()[devletName])
            devletInput.click()