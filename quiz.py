# Örnek 1: Bir banka hesabında; para çekmek, para yatırmak, havale ve kalan parayı göstermek
# gibi işlemleri bütün kullanıcılar için gerçekleştirebilecek
# programı sınıf ve miras alma yoluyla hazırlayınız.

# %%
class bankaHesabı():
    def __init__(self,ilkMiktar = 0):
        self.para =ilkMiktar
        print(f"Banka hesabınız {ilkMiktar} tl olarak oluşturuldu")

    def kalanPara(self):
        print(f"Kalan paranız: {self.para}")

    def paraYatırma(self,yatırılanMiktar):
        self.para += yatırılanMiktar
        print(f"Güncel bakiye: {self.para}")

    def paraÇek(self,çekilecekMiktar):
        self.para -= çekilecekMiktar
        print(f"Güncel bakiye: {self.para}")

    def havale(self,para,gönderilenKişi):
        self.para -= para
        gönderilenKişi.paraYatırma(para)

sıla = bankaHesabı(50000)
duran = bankaHesabı(10000)

duran.kalanPara()
duran.paraYatırma(500)
duran.havale(2000,sıla)


#Örnek 2: Aşağıda özellikleri verilen restoran programını klavyeden girilecek kişinin
# adına göre tüm kişiler ve seçenekler için çalıştırabilen programı hazırlayıp kişinin
# ödeyeceği hesabı ekrana çıkartan programı sınıf ve miras alma özelliklerini kullanarak Python dilinde hazırlayınız.

# %%



class restorant:
    yiyecek = {"Et": 25, "Tavuk": 20, "Balık": 25, "Köfte": 15}
    içecek = {"Su": 1,"Ayran": 1,"Kola": 3,"Fanta":3}
    tatlı = {"Baklava": 8,"Şöbiyet": 8,"Künefe": 10}

    print()
    print(f"Yiyecekler : {yiyecek}")
    print(f"İçecekler : {içecek}")
    print(f"Tatlılar: {tatlı}")

    def __init__(self,ücret = 0):
        self.hesap = ücret
        print(f"Hesap : {self.hesap}")

    def yiyecekSeç(self,seçilenYiyecek):
        self.hesap += self.yiyecek[seçilenYiyecek]

    def içecekSeç(self,seçilenİçecek):
        self.hesap += self.içecek[seçilenİçecek]

    def tatlıSeç(self,seçilenTatlı):
        self.hesap += self.tatlı[seçilenTatlı]

    def hesapGoster(self):
        print(f"Hesap : {self.hesap}")

sıla = restorant()

sıla.yiyecekSeç("Et")


sıla.hesapGoster()


# %%
#1) nokta adında bir sınıf için gerekli tanımlamaları yapınız. Bu sınıftan türeyecek objeler pozisyon, hareket ve mesafe adında metotlara erişim sağlayabilmelidir.
#•	poziyon, noktanın anlık koordinatlarını verebilmeli
#•	hareket, bu koordinatları güncelleyebilmeli
#•	mesafe metodu ise verilen iki nokta arasındaki mesafeyi hesaplayabilmelidir.

class nokta:
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def show(self):
        print(f"{self.x} {self.y}")

    def hereket(self,x,y):
        self.x += x
        self.y += y



    def mesafe(self,nokta):
        uzaklık = ((self.x - nokta.x)**2 + (self.y - nokta.y)**2)**0.5
        print(uzaklık)


p1 = nokta(5,5)
p2 = nokta(8,3)

p1.show()
p2.show()
p1.hereket(3,4)
p1.show()
p2.show()
p1.mesafe(p2)


# %%

#  Aşağıda belirtilenler ışığında gerekli kodlamayı yapınız.
#•	name ve age attribute ları olan bir person sınıfı tanımlayınız
#•	person sınıfı kullanılarak oluşturulan objenin name ve age bilgilerini ekrana yazan display adında bir metot yazınız
#•	person sınıfı attribute larına ilaveten section bilgisini içeren bir student sınıfı tanımlayınız (person dan türeyen)
#•	student sınıfı aracılığı ile oluşturulan objenin name, age ve section bilgilerini ekrana yazan display_student adında bir metot yazınız


class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name : {self.name}, Age : {self.age}")


class student(person):
    def __init__(self,name,age,section):
        person.__init__(self,name,age)
        self.section = section

    def display_student(self):
        print(f"Name : {self.name}, Age : {self.age}, Section : {self.section}")


kişi1 = person("duran",20)
kişi2 = student("sıla",18,"Math")

kişi1.display()
kişi2.display_student()










