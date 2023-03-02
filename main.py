from navbar import Navbar
from ihamKararAramaForm import IhamKararAramaForm
from devletSecForm import Devletler
from maddeNoSecForm import Maddeler
from kararlar import Kararlar
from driver import driver
import time




Navbar().ihamKararArama.click()
IhamKararAramaForm().maddeNoSec.click()
Maddeler().maddeIsaretle(["Md. 10 (5 597 kararda 5 647 hüküm)"])
Maddeler().tamam.click()
IhamKararAramaForm().davaliDevletSec.click()
Devletler().devletIsaretle(["Türkiye (12 921 karar)"])
Devletler().tamam.click()
IhamKararAramaForm().ara.click()
Kararlar().tumKayitlariYukle()
myList = Kararlar().getAllInformation()
Kararlar().exceleKaydet(myList,"davalarDuzenli.xlsx")

time.sleep(2)
driver.close()