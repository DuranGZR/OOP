from datetime import datetime


class Kullanici:
    kullanici_listesi = {}

    def __init__(self, kullanici_id, ad, soyad, email, sifre):  # düzeltme: __init__
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.soyad = soyad
        self.email = email
        self.sifre = sifre
        self.rol = None
        Kullanici.kullanici_listesi[email] = self

    @classmethod
    def giris_yap(cls, email, sifre):
        kullanici = cls.kullanici_listesi.get(email)
        if kullanici and kullanici.sifre == sifre:
            print(f"Giriş başarılı: {kullanici.ad} {kullanici.soyad}")
            return kullanici
        else:
            print("Giriş başarısız: Bilgiler yanlış.")
            return None

    def cikis_yap(self):
        print(f"{self.ad} {self.soyad} çıkış yaptı.")

    def rol_ata(self, rol):
        self.rol = rol
        print(f"{self.ad} {self.soyad} kullanıcısına '{rol.adi}' rolü atandı.")

    def bilgi_goster(self):
        print(
            f"Kullanıcı ID: {self.kullanici_id}, Ad: {self.ad}, Soyad: {self.soyad}, Email: {self.email}, Rol: {self.rol}")

    def sifre_guncelle(self, yeni_sifre):
        self.sifre = yeni_sifre
        print(f"{self.ad} {self.soyad} için şifre güncellendi.")


class Rol:
    def __init__(self, adi):  # düzeltme: __init__
        self.adi = adi

    def __str__(self):  # düzeltme: __str__
        return self.adi


class Yonetici(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):  # düzeltme: __init__
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Yonetici"))

    def etkinlik_olustur(self, etkinlik_id, etkinlik_adi, tarih, kontenjan, etkinlik_turu):
        etkinlik = Etkinlik(etkinlik_id, etkinlik_adi, tarih, kontenjan, etkinlik_turu)
        Etkinlik.etkinlik_listesi.append(etkinlik)
        print(f"{self.ad} {self.soyad} tarafından '{etkinlik_adi}' etkinliği oluşturuldu.")
        return etkinlik

    def etkinlik_raporla(self, etkinlik):
        print(f"{etkinlik.etkinlik_adi} Raporu:")
        etkinlik.etkinlik_bilgisi()
        etkinlik.katilimci_listesi()

    def etkinlik_sil(self, etkinlik):
        if etkinlik in Etkinlik.etkinlik_listesi:
            Etkinlik.etkinlik_listesi.remove(etkinlik)
            print(f"'{etkinlik.etkinlik_adi}' etkinliği silindi.")
        else:
            print("Etkinlik bulunamadı.")

    def kayit_onayla(self, kayit):
        kayit.onayla()


class Katilimci(Kullanici):
    def __init__(self, kullanici_id, ad, soyad, email, sifre):  # düzeltme: __init__
        super().__init__(kullanici_id, ad, soyad, email, sifre)
        self.rol_ata(Rol("Katilimci"))

    def etkinlige_katil(self, etkinlik):
        if etkinlik.tarih < datetime.now():
            print("Bu etkinliğe katılım süresi geçmiş.")
        else:
            etkinlik.katilimci_ekle(self)


class Etkinlik:
    etkinlik_listesi = []

    def __init__(self, etkinlik_id, etkinlik_adi, tarih, kontenjan, etkinlik_turu):  # düzeltme: __init__
        self.etkinlik_id = etkinlik_id
        self.etkinlik_adi = etkinlik_adi
        self.tarih = datetime.strptime(tarih, "%Y-%m-%d")
        self.kontenjan = kontenjan
        self.etkinlik_turu = etkinlik_turu
        self.katilim_kayitlari = []

    def katilimci_ekle(self, katilimci):
        if len(self.katilim_kayitlari) < self.kontenjan:
            kayit = KatilimKaydi(self, katilimci)
            self.katilim_kayitlari.append(kayit)
            print(f"{katilimci.ad} {katilimci.soyad} etkinliğe başarıyla kaydedildi.")
        else:
            print("Etkinlik dolu, daha fazla katılımcı eklenemez.")

    def katilimci_listesi(self):
        print(f"Etkinlik: {self.etkinlik_adi} ({self.tarih.date()}) - Katılımcılar:")
        for kayit in self.katilim_kayitlari:
            kayit.katilimci.bilgi_goster()

    def etkinlik_bilgisi(self):
        print(
            f"Etkinlik: {self.etkinlik_adi}, Tarih: {self.tarih.date()}, Kontenjan: {self.kontenjan}, Tür: {self.etkinlik_turu}")

    @classmethod
    def etkinlikleri_listele(cls):
        if cls.etkinlik_listesi:
            print("Kayıtlı Etkinlikler:")
            for etkinlik in cls.etkinlik_listesi:
                print(f"- {etkinlik.etkinlik_adi} ({etkinlik.tarih.date()}) - Kontenjan: {etkinlik.kontenjan}")
        else:
            print("Henüz kayıtlı etkinlik bulunmamaktadır.")

    @classmethod
    def etkinlik_ara(cls, ad):
        print(f"{ad} adlı etkinlik arama sonuçları:")
        for etkinlik in cls.etkinlik_listesi:
            if ad.lower() in etkinlik.etkinlik_adi.lower():
                etkinlik.etkinlik_bilgisi()


class KatilimKaydi:
    def __init__(self, etkinlik, katilimci):  # düzeltme: __init__
        self.etkinlik = etkinlik
        self.katilimci = katilimci
        self.onay_durumu = False
        self.kayit_tarihi = datetime.now()

    def onayla(self):
        self.onay_durumu = True
        print(f"{self.katilimci.ad} {self.katilimci.soyad} katılımı onaylandı.")

    def kayit_bilgisi(self):
        onay_durum = "Onaylı" if self.onay_durumu else "Onaysız"
        print(f"{self.katilimci.ad} {self.katilimci.soyad} - {onay_durum} - Kayıt Tarihi: {self.kayit_tarihi}")


# Örnek Kullanım

# Yöneticinin kayıt olması
yonetici1 = Yonetici(1, "Mehmet", "Kara", "mehmet.kara@example.com", "sifre123")


# Katılımcının kayıt olması
katilimci1 = Katilimci(2, "Ali", "Yılmaz", "ali@example.com", "sifre456")

# Giriş yapma
kullanici1 = Kullanici.giris_yap("mehmet.kara@example.com", "sifre123")
kullanici2 = Kullanici.giris_yap("ali@example.com", "sifre456")

# Şifre güncelleme
kullanici1.sifre_guncelle("yeniSifre123")

# Yöneticinin etkinlik oluşturması
if isinstance(kullanici1, Yonetici):
    etkinlik1 = kullanici1.etkinlik_olustur(101, "Python Bootcamp", "2024-11-15", 3, "Eğitim")

# Katılımcının etkinliğe katılması
if isinstance(kullanici2, Katilimci):
    kullanici2.etkinlige_katil(etkinlik1)

# Etkinlik arama
Etkinlik.etkinlik_ara("Python")

# Çıkış yapma
if kullanici1:
    kullanici1.cikis_yap()
