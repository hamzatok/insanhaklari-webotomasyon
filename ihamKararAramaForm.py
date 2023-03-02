from driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Burada okunurluk açısından güzel durduğu için bu şekil bir tasarım kullandım fakat performans açısından düşünüldüğünde formdaki her seçim işlemimizden (madde no seç, davalı devlet seç gibi) sonra tekrar bu sayfaya geldiğimizde sınıfın tekrar tekrar örneklenmesi ve  sayfadaki tüm elemanların bulunup değişkenlere ataması performans kaybına neden olacağından dolayı her bir eleman fonksiyon ve ya property içinde bulunup sınıfın örneklenmesi durumunda sadece ihtiyacımız olan elemanın bulunması için gerekli kod çalıştırılabilir.
class IhamKararAramaForm:
    driver = driver
    def __init__(self):
        self._davaliDevletSec = driver.find_element(By.ID, "ContentPlaceHolder1_ButtonDevPanel")
        self._temelKavramlarSec = driver.find_element(By.ID, "ContentPlaceHolder1_ButtonHakPanel")
        self._maddeNoSec = driver.find_element(By.ID, "ContentPlaceHolder1_ButtonMaddePanel")
        self._sonucSec = driver.find_element(By.ID, "ContentPlaceHolder1_ButtonSonPanel")
        self._ara = driver.find_element(By.ID ,"ButtonAra")
        self._temizle = driver.find_element(By.ID, "ContentPlaceHolder1_ButtonTemizle")
        
    @property
    def ara(self):
        return self._ara
    
    @property
    def temizle(self):
        return self._temizle

    @property
    def davaliDevletSec(self):
        return self._davaliDevletSec
        
    @property
    def temelKavramlarSec(self):
        return self._temelKavramlarSec
    
    @property
    def maddeNoSec(self):
        return self._maddeNoSec
    
    @property
    def sonucSec(self):
        return self._sonucSec


