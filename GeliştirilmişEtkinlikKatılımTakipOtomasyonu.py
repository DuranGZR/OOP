
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



# Kullanıcı Menüsü Uygulaması

def main():
    kullanici = None
    yonetici = None
    while True:
        print("\n--- Kullanıcı Sistemi ---")
        print("1. Yönetici Girişi")
        print("2. Katılımcı Girişi")
        print("3. Yeni Kullanıcı Kayıt")
        print("4. Yönetici ve Katılımcı Bilgilerini Göster")
        print("5. Çıkış")

        secim = input("Seçiminizi yapınız: ")

        if secim == "1":
            email = input("E-posta: ")
            sifre = input("Şifre: ")
            kullanici = Kullanici.giris_yap(email, sifre)
            if kullanici and isinstance(kullanici, Yonetici):
                yonetici_menusu(kullanici)
            elif kullanici is None:
                print("Giriş başarısız. E-posta veya şifre yanlış.")
            else:
                print("Geçersiz yönetici girişi.")
        elif secim == "2":
            email = input("E-posta: ")
            sifre = input("Şifre: ")
            kullanici = Kullanici.giris_yap(email, sifre)
            if kullanici and isinstance(kullanici, Katilimci):
                katilimci_menusu(kullanici)
            elif kullanici is None:
                print("Giriş başarısız. E-posta veya şifre yanlış.")
            else:
                print("Geçersiz katılımcı girişi.")
        elif secim == "3":
            kayit_menusu()
        elif secim == "4":
            tum_kullanici_bilgileri_goster()
        elif secim == "5":
            print("Sistemden çıkış yapıldı.")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

def kayit_menusu():
    print("\n--- Yeni Kullanıcı Kayıt ---")
    kullanici_turu = input("Kullanıcı türü (1: Yönetici, 2: Katılımcı): ")
    kullanici_id = input("Kullanıcı ID: ")
    ad = input("Ad: ")
    soyad = input("Soyad: ")
    email = input("E-posta: ")
    sifre = input("Şifre: ")

    if kullanici_turu == "1":
        Yonetici(kullanici_id, ad, soyad, email, sifre)
        print("Yönetici kaydedildi.")
    elif kullanici_turu == "2":
        Katilimci(kullanici_id, ad, soyad, email, sifre)
        print("Katılımcı kaydedildi.")
    else:
        print("Geçersiz kullanıcı türü.")

def yonetici_menusu(yonetici):
    while True:
        print("\n--- Yönetici Menüsü ---")
        print("1. Etkinlik Oluştur")
        print("2. Kullanıcı Bilgilerini Göster")
        print("3. Etkinlik Katılımcılarını Göster")
        print("4. Etkinlik Güncelle")
        print("5. Etkinlik Sil")
        print("6. Kullanıcı Sil")
        print("7. Raporlama ve İstatistik")
        print("8. Çıkış")

        secim = input("Seçiminizi yapınız: ")

        if secim == "1":
            etkinlik_id = input("Etkinlik ID: ")
            etkinlik_adi = input("Etkinlik Adı: ")
            tarih = input("Tarih (YYYY-MM-DD): ")
            kontenjan = int(input("Kontenjan: "))
            yonetici.etkinlik_olustur(etkinlik_id, etkinlik_adi, tarih, kontenjan)
        elif secim == "2":
            yonetici.bilgi_goster()
        elif secim == "3":
            etkinlik_adi = input("Etkinlik adı veya ID: ")
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_adi == etkinlik_adi or e.etkinlik_id == etkinlik_adi), None)
            if etkinlik:
                etkinlik.katilimci_listesi()
            else:
                print("Etkinlik bulunamadı.")
        elif secim == "4":
            etkinlik_adi = input("Güncellenecek etkinlik adı veya ID: ")
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_adi == etkinlik_adi or e.etkinlik_id == etkinlik_adi), None)
            if etkinlik:
                yeni_ad = input("Yeni Etkinlik Adı (boş bırakılırsa aynı kalır): ")
                yeni_tarih = input("Yeni Tarih (YYYY-MM-DD, boş bırakılırsa aynı kalır): ")
                yeni_kontenjan = input("Yeni Kontenjan (boş bırakılırsa aynı kalır): ")
                if yeni_ad:
                    etkinlik.etkinlik_adi = yeni_ad
                if yeni_tarih:
                    etkinlik.tarih = yeni_tarih
                if yeni_kontenjan:
                    etkinlik.kontenjan = int(yeni_kontenjan)
                print("Etkinlik güncellendi.")
            else:
                print("Etkinlik bulunamadı.")
        elif secim == "5":
            etkinlik_adi = input("Silinecek etkinlik adı veya ID: ")
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_adi == etkinlik_adi or e.etkinlik_id == etkinlik_adi), None)
            if etkinlik:
                Etkinlik.etkinlik_listesi.remove(etkinlik)
                print("Etkinlik silindi.")
            else:
                print("Etkinlik bulunamadı.")
        elif secim == "6":
            email = input("Silinecek kullanıcının e-posta adresi: ")
            if email in Kullanici.kullanici_listesi:
                del Kullanici.kullanici_listesi[email]
                print("Kullanıcı silindi.")
            else:
                print("Kullanıcı bulunamadı.")
        elif secim == "7":
            print("\n--- Raporlama ve İstatistik ---")
            print(f"Toplam Etkinlik Sayısı: {len(Etkinlik.etkinlik_listesi)}")
            for etkinlik in Etkinlik.etkinlik_listesi:
                print(f"Etkinlik Adı: {etkinlik.etkinlik_adi}, Katılımcı Sayısı: {len(etkinlik.katilim_kayitlari)}")
        elif secim == "8":
            print("Yönetici menüsünden çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

def katilimci_menusu(katilimci):
    while True:
        print("\n--- Katılımcı Menüsü ---")
        print("1. Etkinliğe Katıl")
        print("2. Kullanıcı Bilgilerini Göster")
        print("3. Etkinlik Katılımını İptal Et")
        print("4. Şifre Güncelle")
        print("5. Çıkış")

        secim = input("Seçiminizi yapınız: ")

        if secim == "1":
            etkinlik_adi = input("Etkinlik adı veya ID: ")
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_adi == etkinlik_adi or e.etkinlik_id == etkinlik_adi), None)
            if etkinlik:
                katilimci.etkinlige_katil(etkinlik)
            else:
                print("Etkinlik bulunamadı.")
        elif secim == "2":
            katilimci.bilgi_goster()
        elif secim == "3":
            etkinlik_adi = input("İptal edilecek etkinlik adı veya ID: ")
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_adi == etkinlik_adi or e.etkinlik_id == etkinlik_adi), None)
            if etkinlik and katilimci in [k.katilimci for k in etkinlik.katilim_kayitlari]:
                etkinlik.katilim_kayitlari = [k for k in etkinlik.katilim_kayitlari if k.katilimci != katilimci]
                print("Etkinlik katılımı iptal edildi.")
            else:
                print("Etkinlik veya katılım bulunamadı.")
        elif secim == "4":
            yeni_sifre = input("Yeni şifre: ")
            katilimci.sifre = yeni_sifre
            print("Şifre güncellendi.")
        elif secim == "5":
            print("Katılımcı menüsünden çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

def tum_kullanici_bilgileri_goster():
    print("\n--- Tüm Kullanıcı Bilgileri ---")
    for kullanici in Kullanici.kullanici_listesi.values():
        kullanici.bilgi_goster()

if __name__ == "__main__":
    main()
