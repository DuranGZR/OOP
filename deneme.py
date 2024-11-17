from datetime import datetime


# Kullanici Arayuzu (Interface)
class IKullanici:
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        self.__kullanici_id = kullanici_id
        self.__ad = ad
        self.__soyad = soyad
        self.__email = email
        self.__sifre = sifre
        self.rol = None

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
class Kullanici(IKullanici):
    kullanici_listesi = {}

    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        Kullanici.kullanici_listesi[email] = self

    @classmethod
    def giris_yap(cls, email, sifre):
        kullanici = cls.kullanici_listesi.get(email)
        if kullanici and kullanici.sifre == sifre:
            print(f"Giriş başarılı: {kullanici.ad} {kullanici.soyad}")
            return kullanici
        else:
            print("Giriş başarısız: Bilgiler yanlış. Tekrar deneyin.")
            return None

    def cikis_yap(self):
        print(f"{self.ad} {self.soyad} çıkış yaptı.")

    def rol_ata(self, rol):
        self.rol = rol
        print(f"{self.ad} {self.soyad} kullanıcısına '{rol.adi}' rolü atandı.")

    def bilgi_goster(self):
        print(
            f"Kullanıcı ID: {self._IKullanici__kullanici_id}, Ad: {self.ad}, Soyad: {self.soyad}, Email: {self.email}, Rol: {self.rol}")


# Rol sınıfı
class Rol:
    def __init__(self, adi):
        self.adi = adi

    def __str__(self):
        return self.adi


# Yonetici sınıfı
class Yonetici(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Yönetici"))

    def etkinlik_olustur(self, etkinlik_id, etkinlik_adi, tarih, kontenjan):
        etkinlik = Etkinlik(etkinlik_id, etkinlik_adi, tarih, kontenjan)

        print(f"Etkinlik '{etkinlik_adi}' başarıyla oluşturuldu.")
        return etkinlik


# Katılımcı sınıfı
class Katilimci(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Katılımcı"))

    def etkinlige_katil(self, etkinlik):
        if etkinlik.katilim_mumkun_mu():
            etkinlik.katilimci_ekle(self)
        else:
            print("Bu etkinliğe katılım süresi geçmiş veya kontenjan dolu.")


# Etkinlik sınıfı
class Etkinlik:
    etkinlik_listesi = []

    def __init__(self, etkinlik_id, etkinlik_adi, tarih, kontenjan):
        self.etkinlik_id = etkinlik_id
        self.etkinlik_adi = etkinlik_adi
        self.tarih = datetime.strptime(tarih, "%Y-%m-%d")
        self.kontenjan = kontenjan
        self.katilim_kayitlari = []

    def katilim_mumkun_mu(self):
        return self.tarih >= datetime.now() and len(self.katilim_kayitlari) < self.kontenjan

    def katilimci_ekle(self, katilimci):
        if self.katilim_mumkun_mu() and katilimci not in [kayit.katilimci for kayit in self.katilim_kayitlari]:
            kayit = KatilimKaydi(self, katilimci)
            self.katilim_kayitlari.append(kayit)
            print(f"{katilimci.ad} {katilimci.soyad} etkinliğe başarıyla kaydedildi.")
        else:
            print("Etkinlik dolu veya tarih geçmiş, daha fazla katılımcı eklenemez.")

    def katilimci_listesi(self):
        print(f"Etkinlik: {self.etkinlik_adi} ({self.tarih.date()}) - Katılımcılar:")
        for kayit in self.katilim_kayitlari:
            kayit.katilimci.bilgi_goster()


# Katılım Kaydı sınıfı
class KatilimKaydi:
    def __init__(self, etkinlik, katilimci):
        self.etkinlik = etkinlik
        self.katilimci = katilimci
        self.kayit_tarihi = datetime.now()

    def kayit_bilgisi(self):
        print(f"{self.katilimci.ad} {self.katilimci.soyad} - Kayıt Tarihi: {self.kayit_tarihi}")


# Kullanıcı ve Etkinlik Oluşturma
# Kullanıcıları input ile oluşturma
def kullanici_olustur():
    kullanici_id = 1
    while True:
        print("\nYeni kullanıcı oluşturmak için bilgileri girin (iptal etmek için 'q' tuşuna basın):")
        ad = input("Ad: ")
        if ad.lower() == 'q':
            break
        soyad = input("Soyad: ")
        email = input("Email: ")
        sifre = input("Şifre: ")
        rol = input("Rol (Yönetici/Katılımcı): ")

        if rol.lower() == 'yönetici':
            Yonetici(kullanici_id, ad, soyad, email, sifre)
        elif rol.lower() == 'katılımcı':
            Katilimci(kullanici_id, ad, soyad, email, sifre)
        else:
            print("Geçersiz rol, lütfen 'Yönetici' veya 'Katılımcı' giriniz.")
            continue

        kullanici_id += 1


# Etkinlik oluşturma
def etkinlik_olustur():
    while True:
        print("\nYeni etkinlik oluşturmak için bilgileri girin (iptal etmek için 'q' tuşuna basın):")
        etkinlik_adi = input("Etkinlik Adı: ")
        if etkinlik_adi.lower() == 'q':
            break
        tarih = input("Tarih (YYYY-AA-GG): ")
        kontenjan = int(input("Kontenjan: "))

        yonetici_email = input("Yönetici email: ")
        yonetici_sifre = input("Şifre: ")
        yonetici = Kullanici.giris_yap(yonetici_email, yonetici_sifre)

        if isinstance(yonetici, Yonetici):
            etkinlik = yonetici.etkinlik_olustur(len(Etkinlik.etkinlik_listesi) + 1, etkinlik_adi, tarih, kontenjan)
            Etkinlik.etkinlik_listesi.append(etkinlik)
        else:
            print("Geçersiz yönetici bilgileri.")


# Kullanıcıları ve etkinlikleri oluştur
kullanici_olustur()
etkinlik_olustur()

# Bütün metodları test etmek için basit bir menü
def kullanici_menusu():
    while True:
        print("\nKullanıcı Menüsü:")
        print("1. Kullanıcıları Listele")
        print("2. Etkinlikleri Listele")
        print("3. Etkinliğe Katılım")
        print("4. Etkinlik Katılımcılarını Listele")
        print("5. Çıkış")
        secim = input("Seçiminizi yapın: ")

        if secim == '1':
            for email, kullanici in Kullanici.kullanici_listesi.items():
                kullanici.bilgi_goster()
        elif secim == '2':
            for etkinlik in Etkinlik.etkinlik_listesi:
                print(
                    f"Etkinlik ID: {etkinlik.etkinlik_id}, Adı: {etkinlik.etkinlik_adi}, Tarih: {etkinlik.tarih.date()}, Kontenjan: {etkinlik.kontenjan}")
        elif secim == '3':
            email = input("Katılmak istediğiniz etkinlik için katılımcı email: ")
            sifre = input("Şifre: ")
            katilimci = Kullanici.giris_yap(email, sifre)
            if isinstance(katilimci, Katilimci):
                etkinlik_id = int(input("Katılmak istediğiniz etkinlik ID'sini girin: "))
                etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_id == etkinlik_id), None)
                if etkinlik:
                    katilimci.etkinlige_katil(etkinlik)
                else:
                    print("Geçersiz etkinlik ID.")
            else:
                print("Giriş başarısız: Bilgiler yanlış veya yetkiniz yok.")
        elif secim == '4':
            etkinlik_id = int(input("Katılımcılarını listelemek istediğiniz etkinlik ID'sini girin: "))
            etkinlik = next((e for e in Etkinlik.etkinlik_listesi if e.etkinlik_id == etkinlik_id), None)
            if etkinlik:
                etkinlik.katilimci_listesi()
            else:
                print("Geçersiz etkinlik ID.")
        elif secim == '5':
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")


kullanici_menusu()
