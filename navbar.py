from driver import driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Navbar:
    driver = driver

    def __init__(self):
        driver.get("https://insanhaklari.gen.tr/")
        # Her ihtimale karşı şuraya bir if kontrol ekleyelim :) çünkü diğer sayfalar iframe'e basılmamış.
        if driver.current_url=="https://insanhaklari.gen.tr/":
            Navbar.__switchToIframe()

        
    # iframe üzerindeki elemanlara ulaşabilmek için iframe'e geçiş fonksiyonu
    def __switchToIframe():
        iframe = driver.find_element(By.ID, "iframe")
        driver.switch_to.frame(iframe)

    # Anasayfa webelementini döndürür.
    @property
    def anasayfa(self):
        anasayfa = driver.find_element(By.LINK_TEXT, "Anasayfa")
        return anasayfa

    # Belgeler web elementi üzerine hover olayını gerçekleştirir.
    def __belgelerHover():
        belgeler = driver.find_element(By.LINK_TEXT, "Belgeler  ↓")
        ActionChains(driver).move_to_element(belgeler).perform()
    
    # Belgeler webelementi üzerine gerçekleşen hover olayından sonra görünen başlıca belgeler webelementini döndürür.
    @property
    def baslicaBelgeler(self):
        Navbar.__belgelerHover()
        baslica_belgeler = driver.find_element(By.LINK_TEXT, "Başlıca belgeler")
        return baslica_belgeler
    
    # Belgeler webelementi üzerine gerçekleşen hover olayından sonra görünen tüm belgeler web elementini döndürür.
    @property
    def tumBelgeler(self):
        Navbar.__belgelerHover()
        tum_belgeler = driver.find_element(By.LINK_TEXT, "Tüm belgeler")
        return tum_belgeler
    
    # Aym karar arama linki webelementini döndürür.
    @property
    def aymKararArama(self):
        aymKararArama = driver.find_element(By.LINK_TEXT, "AYM Karar arama")
        return aymKararArama
    
    # iham karar arama linki webelementini döndürür.
    @property
    def ihamKararArama(self):
        ihamKararArama = driver.find_element(By.LINK_TEXT, "İHAM (AİHM) Karar arama")
        return ihamKararArama
    



        