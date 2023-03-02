from driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class Kararlar:
    driver = driver

    def __init__(self):
        self.columnNameList = ["Dava adı","Başvuru no","Başvuru tarihi","Karar süresi","Karar türü","Karar organı","Önem derecesi", "Karara erişim"]

    # Tüm kayıtlar yüklenene kadar Scrollu çevirme işlemi
    # Tüm kayıtlar yüklendikten sonra çekme işlemini yapıyorum.
    # şimdilik scrollu kontrol etme işlemini yapamadım bu nedenle sadece rastgele bir döngüye soktum almak istediğimiz veriye özel olarak. Daha sonra bununla ilgileneceğim.
    def tumKayitlariYukle(self):
        tablo = driver.find_element(By.ID, "tablo")
        
        for i in range(3000):
            
            scroll_origin = ScrollOrigin.from_element(tablo)
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, 4000).perform()


    # Her bir kayıt ve kolon bilgileri sayfadaki tr elementinin altında bulunuyor. Fakat sayfa görünümünde kolon bilgilerinin olduğu kayıtların altındaki içeriklerde tr elementinin altında bulunuyor ve bunların bazıları bu kolon bilgilerinin bulunduğu elementle aynı seviyede bazıları ise bu elementlerin altında bulunuyor. bunları ayrıştırmak çok problemli olduğu için sayfadaki bütün tr elementlerini çekip öyle işlem gördüm. Bunları çektikten sonra ilk kaydın tr elementi elde ettiğimiz tr element listesinin 27. indeksinden başlıyor ve her 5 tr elementinden sonra diğer kaydımızın bulunduğu tr elmentine geçiyor. Ve bu durum şimdilik gördüğüm kadarıyla sayfalarda bir değişkenliğe sebep olmuyor.
    def __gettrWebelement(self) -> list[WebElement]:
        trler = driver.find_elements(By.TAG_NAME, "tr")
        return trler
    
    # Döngüden gelen kararlar sayfamızdaki kolon bilgilerimizin bulunduğu tr elementinden bilgileri kazıyıp sözlük biçinmine çevirme işlemi
    def __createKararlarSozluk(self, trWebelement:WebElement):
        kararlarSozluk = {}  # {Karar Tarihi:"", Başvuru No:"", Dava Adı:"", Mahkeme:"", Karar Türü:""}
        td = trWebelement.find_elements(By.TAG_NAME,"td")
            
        kararlarSozluk["Karar Tarihi"] = td[1].text
        kararlarSozluk["Başvuru No"] = td[2].text
        kararlarSozluk["Dava Adı"] = td[3].text
        kararlarSozluk["Mahkeme"] = td[4].text
        karaTürü = td[5].text
        # trler satır , tdler kolon
        # kayıt kolonlarının her biri  td etiketlerinin içinde bulunuyor. Fakat her bir tr etiketinin içindeki td etiketlerinin 5. indeksi içinde diğer etiketlere göre fazladan başka etiketlerde bulunduğundan dolayı textini aldığımızda diğer etiketlerinde texti geliyor. Bu nedenle 5. index için bir string formatlama yapıyoruz.
        kararTürüIndex = karaTürü.index("\n")
        karaTürü = karaTürü[:kararTürüIndex]
        kararlarSozluk["Karar Türü"] = karaTürü
        return kararlarSozluk

    # kararlar sayfasındaki kolon bilgilerimizin bulunduğu sözlükleri döngü kullanarak listeleme işlemi.
    def kararlariListele(self) -> list[dict]:
        trler = self.__gettrWebelement() 

        kararlarList = []
        # tüm tr etiketlerini alınca sayfa yapısından dolayı ilk kaydın tr etiketi listenin 27. indeksindeki elemana karşılık geliyor. Bundan dolayı döngüyü 27. tr etiketinden başlatıyorum. her bir 5 adım sonraki tr elementi kolon bilgielrimizin bulunduğu elemente denk geliyor.
        for i in range(27,len(trler)-1,5):
           
            kararlarSozluk = self.__createKararlarSozluk(trler[i])
            kararlarList.append(kararlarSozluk)
            

        # list[kayitlarSozluk]
        return kararlarList 
    

    #Kararlar sayfası ilk açıldıktan sonra kolon bilgilerini alma ve karar bilgilerine tıklayıp detay bilgilerini alma ve hepsini tek bir sözlükte toplama işlemi
    def getAllInformation(self) -> list[dict]:
        trler = driver.find_elements(By.TAG_NAME, "tr")
        kararlarDetayList = []
        for i in range(27,len(trler)-1,5):
            #Kararlar sayfasındaki kolonları al
            kararlarSozluk = self.__createKararlarSozluk(trler[i])
            # tr elementinin karar bilgileri butonuna ulaşma
            kararBilgileri = trler[i].find_element(By.LINK_TEXT, "Karar bilgileri")
            kararBilgileri.click()

            # Karar bilgileri butonuna tıkladıktan sonra açılan sekmeye(window) geçme işlemi
            # driver.window_handles propertysi bize tarayıcıda açık olan tüm windowların(sekmelerin) isimlerini(window_name) bir liste şeklinde döndürüyor.driver.window_handles = [kararlarPenceresi, DetaylarPenceresi]
            driver.switch_to.window(driver.window_handles[1])

            # Karar bilgilerine tıkladıktan sonra açılan detay sayfasının tamamının içeriğini metin biçiminde aldım ve daha sonra bu içerikte metin kazıma işlemi uygulayarak istediğim kısımları aldım. Bunu yapmamın sebebi sayfanın genel görünüm yapısı ve metin yapısı  aynı olmasına rağmen etiketlerin iskelet yapısının farklı olmasıdır. Mesela Url nin bulunduğu td etiketini kapsayan div etiketinin id si sayfalarda değişkenlik gösteriyordu. Url bazı sayfada div0, bazısında div1, bazısında div2, id'li etiketlerin altında bulunduğundan dolayı tek bir Xpath yapısı oluşmuyordu, bazı kayıtlar boş dönüyordu ve bunu kontrol etmekte zorluk çıkarıyordu. Bu nedenle hepsini kapsayan "icerik" id li etiketi aldım ve metin kazıma yaptım. Bu durum elde ettiğim metinde bir değişiklik oluşturmuyordu ki oluştursada metinleri elde etme biçimim metnin indexine ulaşma şeklinde olduğu için bu yöntem daha kolay oluyordu.
            icerik = driver.find_element(By.ID, "icerik").text
            # Sayfa iceriğinden hüküm özetini kazıma
            # hukumOzeti = self.__getHukumOzeti(icerik)
            kararlarSozluk["url"] = self.__getUrl(icerik)
            # Sayfa içeriğinden atıfları kazıma
            atiflar = self.__getAtiflar(icerik)
            for atif in atiflar.split("\n"):
                newSozluk = {}
                for key in kararlarSozluk.keys():
                    newSozluk[key] = kararlarSozluk[key]
                self.__addColumnsInformationToSozluk(icerik, newSozluk)
                newSozluk["Atıflar"] = atif.strip()
                kararlarDetayList.append(newSozluk)
            
            # Driverımız şu an detay sayfasında bu sayfayı kapatıyoruz.
            driver.close()
            # driverımızı tekrar driver.window_handles aracılığıyla kararlar sayfasına geçiriyoruz.
            # driver.window_handles=[kararlarSayfası]
            driver.switch_to.window(driver.window_handles[0])

        # list[kararlarDetaySozluk]
        return kararlarDetayList
    
    # karar bilgileri sayfasının içeriğinde kolon isimleri ard arda geldiği için kolon isimlerini bir listeden alarak tek bir fonksiyon kullanarak bu bilgileri aldım. Bu fonksiyon aşağıdaki "__getColumnsInformation" fonksiyonununalternatifi olarak bir sözlük döndürmeyip verilen listeye bilgileri ekleme işlemi yapmaktadır.
    def __addColumnsInformationToSozluk(self, icerik, sozluk):
        for i in range(len(self.columnNameList)-1):
            startIndex = icerik.index(self.columnNameList[i]+":") + len(self.columnNameList[i]+":")
            endIndex = icerik.index(self.columnNameList[i+1]+":")
            sozluk[self.columnNameList[i]] = icerik[startIndex:endIndex]

    # Aşağıdaki tekrarlanan fonksiyonların tek bir çatı altında toplama işlemi
    # bu fonksiyon yukarkıdaki "__addColumnsInformationToSozluk" fonksiyonunun alternatifi olarak bir sözlük döndürür.
    def __getColumnsInformation(self, icerik:str)-> dict:
        kararlarDict = {}
        for i in range(self.columnNameList-2):
            startIndex = icerik.index(self.columnNameList[i]+":") + len(self.columnNameList[i]+":")
            endIndex = icerik.index(self.columnNameList[i+1]+":")
            kararlarDict[self.columnNameList[i]] = icerik[startIndex:endIndex]
        return kararlarDict
                
    # Karar bilgileri sayfasınını metin içeriğinden url bilgisini çekme
    def __getUrl(self,icerik:str):

        startIndex = icerik.index("https://insanhaklari.gen.tr")
        endIndex = icerik.index("URL kopyala")
        url = icerik[startIndex:endIndex]
        return url
    
    # Karar bilgileri sayfasının metin içeriğinden Dava Adı bilgisini çekme
    def __getDavaAdi(self, icerik:str):
        startIndex = icerik.index("Dava adı:")+ len("Dava adı:")
        endIndex = icerik.index("Başvuru no:")
        davaAdi = icerik[startIndex:endIndex]
        return davaAdi

    # Karar bilgileri sayfasının metin içeriğinden Başvuru No bilgisini çekme
    def __getBasvuruNo(self, icerik:str):
        startIndex = icerik.index("Başvuru no:")+ len("Başvuru no:")
        endIndex = icerik.index("Başvuru tarihi:")
        basvuruNo = icerik[startIndex:endIndex]

    # Karar bilgileri sayfasının metin içeriğinden Başvuru Tarihi bilgisini çekme
    def __getBasvuruTarihi(self, icerik:str):
        startIndex = icerik.index("Başvuru tarihi:") + len("Başvuru tarihi:")
        endIndex = icerik.index("Karar süresi:")
        basvuruTarihi = icerik[startIndex:endIndex]
        return basvuruTarihi

    # Karar bilgileri sayfasının metin içeriğinden Karar Süresi bilgisini çekme
    def __getKararSuresi(self, icerik:str):
        startIndex = icerik.index("Karar süresi:") +len("Karar süresi:")
        endIndex = icerik.index("Karar türü:")
        kararSuresi = icerik[startIndex:endIndex]
        return kararSuresi

    # Karar bilgileri sayfasının metin içeriğinden Karar Türü bilgisini çekme
    def __getKararTuru(self, icerik:str):
        startIndex = icerik.index("Karar türü:") +len("Karar türü:")
        endIndex = icerik.index("Karar organı:")
        kararTuru = icerik[startIndex:endIndex]
        return kararTuru

    # Karar bilgileri sayfasının metin içeriğinden Karar Organı bilgisini çekme
    def __getKararOrgani(self, icerik:str):
        startIndex = icerik.index("Karar organı:") +len("Karar organı:")
        endIndex = icerik.index("Önem derecesi:")
        kararOrgani = icerik[startIndex:endIndex]
        return kararOrgani

    # Karar bilgileri sayfasının metin içeriğinden Önem Derecesi bilgisini çekme
    def __getOnemDerecesi(self, icerik:str):
        startIndex = icerik.index("Önem derecesi:") +len("Önem derecesi:")
        endIndex = icerik.index("Karara erişim:")
        onemDerecesi = icerik[startIndex:endIndex]
        return onemDerecesi

    # Karar bilgileri sayfasının metin içeriğinden Hüküm Özeti bilgisini çekme
    def __getHukumOzeti(self, icerik:str):
        startIndex = icerik.index("Hüküm özeti:")+len("HükümÖzeti:")
        endIndex = icerik.index("Atıflar:")
        hukumOzeti = icerik[startIndex:endIndex]
        return hukumOzeti
            
    # Karar bilgileri sayfasının metin içeriğinden Atıflar bilgisini çekme
    def __getAtiflar(self,icerik:str):
        startIndex = icerik.index("Atıflar:")+len("Atıflar:")
        atiflar = icerik[startIndex:]
        return atiflar



    def exceleKaydet(self ,liste:list[dict], dosyaAdi):
        df = pd.DataFrame(liste)
        df.to_excel(dosyaAdi)




        

                