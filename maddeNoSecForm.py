from driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with


class Maddeler:
    driver = driver
    # Madde adlarını ve checkboxIdlerini alma işlemi zor ve bu işlemin gerçekleşmesi programı yavaşlattığından dolayı madde isimleri ve sahip oldukları checkboxIdlerini sözlük biçiminde, statik olarak ve bir örnek niteliği olarak Maddeler sınıfına ekledim. 
    maddeSozluk = {'Eski Md. 25 (20 kararda 20 hüküm)': 'k1', 'Eski Md. 27 (1 kararda 1 hüküm)': 'k2', 'Eski Md. 28 (1 kararda 1 hüküm)': 'k3', 'Md. 01 (623 kararda 586 hüküm)': 'k4', 'Md. 02 (4 829 kararda 5 329 hüküm)': 'k5', 'Md. 03 (16 868 kararda 18 374 hüküm)': 'k6', 'Md. 04 (420 kararda 424 hüküm)': 'k7', 'Md. 05 (13 699 kararda 16 150 hüküm)': 'k8', 'Md. 06 (59 970 kararda 61 694 hüküm)': 'k9', 'Md. 07 (2 011 kararda 2 106 hüküm)': 'k10', 'Md. 08 (13 768 kararda 14 143 hüküm)': 'k11', 'Md. 09 (1 648 kararda 1 697 hüküm)': 'k12', 'Md. 10 (5 597 kararda 5 647 hüküm)': 'k13', 'Md. 11 (2 111 kararda 2 170 hüküm)': 'k14', 'Md. 12 (302 kararda 298 hüküm)': 'k15', 'Md. 13 (17 290 kararda 18 236 hüküm)': 'k16', 'Md. 14 (8 016 kararda 8 489 hüküm)': 'k17', 'Md. 15 (110 kararda 87 hüküm)': 'k18', 'Md. 16 (10 kararda 8 hüküm)': 'k19', 'Md. 17 (892 kararda 917 hüküm)': 'k20', 'Md. 18 (799 kararda 824 hüküm)': 'k21', 'Md. 19 (72 kararda 68 hüküm)': 'k22', 'Md. 33 (34 kararda 26 hüküm)': 'k23', 'Md. 34 (3 000 kararda 2 734 hüküm)': 'k24', 'Md. 35 (16 122 kararda 17 338 hüküm)': 'k25', 'Md. 37 (14 547 kararda 15 744 hüküm)': 'k26', 'Md. 38 (611 kararda 105 hüküm)': 'k27', 'Md. 39 (6 700 kararda 5 088 hüküm)': 'k28', 'Md. 41 (10 077 kararda 19 291 hüküm)': 'k29', 'Md. 46 (6 461 kararda 6 264 hüküm)': 'k30', 'Md. 47 (1 kararda 1 hüküm)': 'k31', 'Md. 5 (1 kararda 1 hüküm)': 'k32', 'Md. 52 (3 kararda 1 hüküm)': 'k33', 'Md. 53 (50 kararda 55 hüküm)': 'k34', 'Md. 54 (1 karar)': 'k35', 'Md. 55 (1 kararda 1 hüküm)': 'k36', 'Md. 56 (18 kararda 11 hüküm)': 'k37', 'Md. 57 (121 kararda 78 hüküm)': 'k38', 'P1 (18 549 kararda 18 955 hüküm)': 'k39', 'P12 (438 kararda 455 hüküm)': 'k40', 'P13 (11 kararda 11 hüküm)': 'k41', 'P4 (1 016 kararda 1 049 hüküm)': 'k42', 'P6 (65 kararda 61 hüküm)': 'k43', 'P7 (1 417 kararda 1 461 hüküm)': 'k44'}

    # maddeleri seçme işlemi
    def maddeIsaretle(self, maddeler:list):
        for madde in maddeler:
            driver.find_element(By.ID, self.maddeSozluk[madde]).click()

    # Maddeler sayfasındaki Tamam butonu webelementi
    @property
    def tamam(self):
        return driver.find_element(By.ID, "ContentPlaceHolder1_ButtonMadde")
    
    # Maddeler sayfasındaki Vazgeç butonu webelementi
    @property
    def vazgec(self):
        return driver.find_element(By.LINK_TEXT, "Vazgeç")

    
            

    