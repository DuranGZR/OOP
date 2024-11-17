# %%
from datetime import datetime

# Kullanici Arayuzu (Interface)
# Bu sınıf, tüm kullanıcıların sahip olması gereken temel özellikleri ve metodları tanımlar.
class IKullanici:
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        self.__kullanici_id = kullanici_id  # Kullanıcı ID'si (gizli)
        self.__ad = ad  # Kullanıcının adı (gizli)
        self.__soyad = soyad  # Kullanıcının soyadı (gizli)
        self.__email = email  # Kullanıcının e-posta adresi (gizli)
        self.__sifre = sifre  # Kullanıcının şifresi (gizli)
        self.rol = None  # Kullanıcının rolü atanacak

    # Getter ve Setter örnekleri
    @property
    def ad(self):
        return self.__ad

    @ad.setter
    def ad(self, yeni_ad):
        if yeni_ad:
            self.__ad = yeni_ad

    @property
    def soyad(self):
        return self.__soyad

    @soyad.setter
    def soyad(self, yeni_soyad):
        if yeni_soyad:
            self.__soyad = yeni_soyad

    @property
    def email(self):
        return self.__email

    @property
    def sifre(self):
        return self.__sifre

    def giris_yap(self, email, sifre):
        pass

    def cikis_yap(self):
        pass

    def bilgi_goster(self):
        pass

# Temel Kullanici Sınıfı
# Kullanıcıların genel özelliklerini ve işlevlerini tanımlar.
class Kullanici(IKullanici):
    kullanici_listesi = {}  # Tüm kullanıcıları saklamak için bir sınıf değişkeni

    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        Kullanici.kullanici_listesi[email] = self  # Kullanıcıyı genel listeye ekler

    @classmethod
    def giris_yap(cls, email, sifre):
        """Kullanıcı giriş yapar"""
        kullanici = cls.kullanici_listesi.get(email)
        if kullanici and kullanici.sifre == sifre:
            print(f"Giriş başarılı: {kullanici.ad} {kullanici.soyad}")
            return kullanici
        else:
            print("Giriş başarısız: Bilgiler yanlış.")
            return None

    def cikis_yap(self):
        """Kullanıcı çıkış yapar"""
        print(f"{self.ad} {self.soyad} çıkış yaptı.")

    def rol_ata(self, rol):
        """Kullanıcıya rol atanır"""
        self.rol = rol
        print(f"{self.ad} {self.soyad} kullanıcısına '{rol.adi}' rolü atandı.")

    def bilgi_goster(self):
        """Kullanıcı bilgilerini gösterir"""
        print(f"Kullanıcı ID: {self._IKullanici__kullanici_id}, Ad: {self.ad}, Soyad: {self.soyad}, Email: {self.email}, Rol: {self.rol}")

# Rol sınıfı
# Kullanıcılara atanabilecek rolleri tanımlar.
class Rol:
    def __init__(self, adi):
        self.adi = adi  # Rol adı

    def __str__(self):
        return self.adi

# Yonetici sınıfı
# Yönetici kullanıcıları temsil eder ve özel işlevler ekler.
class Yonetici(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Yönetici"))  # Yöneticilere varsayılan olarak "Yönetici" rolü atanır

    def etkinlik_olustur(self, etkinlik_id, etkinlik_adi, tarih, kontenjan):
        """Yeni bir etkinlik oluşturur"""
        etkinlik = Etkinlik(etkinlik_id, etkinlik_adi, tarih, kontenjan)
        Etkinlik.etkinlik_listesi.append(etkinlik)
        print(f"Etkinlik '{etkinlik_adi}' başarıyla oluşturuldu.")
        return etkinlik

# Katılımcı sınıfı
# Etkinliklere katılabilecek kullanıcıları temsil eder.
class Katilimci(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Katılımcı"))  # Katılımcılara varsayılan olarak "Katılımcı" rolü atanır

    def etkinlige_katil(self, etkinlik):
        """Belirtilen etkinliğe katılır"""
        if etkinlik.katilim_mumkun_mu():
            etkinlik.katilimci_ekle(self)
        else:
            print("Bu etkinliğe katılım süresi geçmiş veya kontenjan dolu.")

# Etkinlik sınıfı
# Etkinliklerin detaylarını ve katılım yönetimini tanımlar.
class Etkinlik:
    etkinlik_listesi = []  # Etkinlikleri saklamak için sınıf değişkeni

    def __init__(self, etkinlik_id, etkinlik_adi, tarih, kontenjan):
        self.etkinlik_id = etkinlik_id  # Etkinlik ID'si
        self.etkinlik_adi = etkinlik_adi  # Etkinlik adı
        self.tarih = datetime.strptime(tarih, "%Y-%m-%d")  # Etkinlik tarihi
        self.kontenjan = kontenjan  # Etkinlik için katılım kontenjanı
        self.katilim_kayitlari = []  # Katılım kayıtlarını tutar

    def katilim_mumkun_mu(self):
        """Etkinliğe katılımın mümkün olup olmadığını kontrol eder"""
        return self.tarih >= datetime.now() and len(self.katilim_kayitlari) < self.kontenjan

    def katilimci_ekle(self, katilimci):
        """Etkinliğe katılımcı ekler"""
        if self.katilim_mumkun_mu():
            kayit = KatilimKaydi(self, katilimci)
            self.katilim_kayitlari.append(kayit)
            print(f"{katilimci.ad} {katilimci.soyad} etkinliğe başarıyla kaydedildi.")
        else:
            print("Etkinlik dolu veya tarih geçmiş, daha fazla katılımcı eklenemez.")

    def katilimci_listesi(self):
        """Etkinlik katılımcılarını listeler"""
        print(f"Etkinlik: {self.etkinlik_adi} ({self.tarih.date()}) - Katılımcılar:")
        for kayit in self.katilim_kayitlari:
            kayit.katilimci.bilgi_goster()

# Katılım Kaydı sınıfı
# Etkinliklere katılan katılımcılarla ilgili kayıt bilgilerini tutar.
class KatilimKaydi:
    def __init__(self, etkinlik, katilimci):
        self.etkinlik = etkinlik  # Katılım yapılan etkinlik
        self.katilimci = katilimci  # Katılımcı bilgisi
        self.kayit_tarihi = datetime.now()  # Kayıt tarihi

    def kayit_bilgisi(self):
        """Katılım kaydı bilgilerini gösterir"""
        print(f"{self.katilimci.ad} {self.katilimci.soyad} - Kayıt Tarihi: {self.kayit_tarihi}")

# %%

# Kullanıcılar oluşturuluyor
yonetici1 = Yonetici(1, "Mehmet", "Kara", "mehmet.kara@gmail.com", "yonetici123")
katilimci1 = Katilimci(2, "Ali", "Yılmaz", "ali@gmail.com", "katilimci123")
katilimci2 = Katilimci(3, "Ayşe", "Demir", "ayse@gmail.com", "katilimci123")
katilimci3 = Katilimci(4, "Fatma", "Çelik", "fatma@gmail.com", "katilimci456")
katilimci4 = Katilimci(5, "Ahmet", "Güneş", "ahmet@gmail.com", "katilimci789")

# Giriş yapılıyor
yonetici1.giris_yap("mehmet.kara@gmail.com", "yonetici123")
katilimci1.giris_yap("ali@gmail.com", "katilimci123")
katilimci2.giris_yap("ayse@gmail.com", "katilimci123")
katilimci3.giris_yap("fatma@gmail.com", "katilimci456")
katilimci4.giris_yap("ahmet@gmail.com", "katilimci789")

# Yöneticinin etkinlik oluşturması
etkinlik1 = yonetici1.etkinlik_olustur(101, "Python Eğitimi", "2024-12-01", 3)
etkinlik2 = yonetici1.etkinlik_olustur(102, "Veri Bilimi Atölyesi", "2024-12-10", 2)

# Katılımcıların etkinliklere katılması
katilimci1.etkinlige_katil(etkinlik1)
katilimci2.etkinlige_katil(etkinlik1)
katilimci3.etkinlige_katil(etkinlik1)

katilimci1.etkinlige_katil(etkinlik2)
katilimci4.etkinlige_katil(etkinlik2)
katilimci2.etkinlige_katil(etkinlik2)  # Bu katılım kontenjan dolu olduğu için reddedilecektir

# Etkinlikte katılımcıların bilgilerinde değişiklik yapılması
katilimci1.ad = "Ali Veli"
katilimci2.soyad = "Çelik"
katilimci4.ad = "Ahmet Can"

katilimci1.ad
katilimci1.soyad
katilimci1.sifre
# Güncellenmiş bilgilerle etkinliklere katılan katılımcıların listesi
etkinlik1.katilimci_listesi()
etkinlik2.katilimci_listesi()

# Katılımcıların çıkış yapması
katilimci1.cikis_yap()
katilimci2.cikis_yap()
katilimci3.cikis_yap()
katilimci4.cikis_yap()

# Yöneticinin çıkış yapması
yonetici1.cikis_yap()
