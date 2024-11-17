from graphviz import Digraph

# Initialize a Digraph object
uml = Digraph("UML Diagram")
uml.attr(rankdir="LR", size="8,5")

# IKullanici Interface
uml.node("IKullanici", '''<<interface>> IKullanici
- __kullanici_id: int
- __ad: str
- __soyad: str
- __email: str
- __sifre: str
+ rol: Rol
+ giris_yap(email, sifre): void
+ cikis_yap(): void
+ bilgi_goster(): void''', shape="record")

# Kullanici Class
uml.node("Kullanici", '''Kullanici
- kullanici_listesi: dict
+ giris_yap(email, sifre): Kullanici
+ cikis_yap(): void
+ rol_ata(rol: Rol): void
+ bilgi_goster(): void''', shape="record")

# Yonetici Class
uml.node("Yonetici", '''Yonetici
+ etkinlik_olustur(etkinlik_id, etkinlik_adi, tarih, kontenjan): Etkinlik''', shape="record")

# Katilimci Class
uml.node("Katilimci", '''Katilimci
+ etkinlige_katil(etkinlik: Etkinlik): void''', shape="record")

# Rol Class
uml.node("Rol", '''Rol
+ adi: str
+ __str__(): str''', shape="record")

# Etkinlik Class
uml.node("Etkinlik", '''Etkinlik
+ etkinlik_id: int
+ etkinlik_adi: str
+ tarih: datetime
+ kontenjan: int
+ katilim_kayitlari: list
+ katilim_mumkun_mu(): bool
+ katilimci_ekle(katilimci: Katilimci): void
+ katilimci_listesi(): void''', shape="record")

# KatilimKaydi Class
uml.node("KatilimKaydi", '''KatilimKaydi
+ etkinlik: Etkinlik
+ katilimci: Katilimci
+ kayit_tarihi: datetime
+ kayit_bilgisi(): void''', shape="record")

# Relationships
uml.edge("IKullanici", "Kullanici", arrowhead="empty", style="dotted")  # Implements
uml.edge("Kullanici", "Yonetici", arrowhead="empty")  # Inheritance
uml.edge("Kullanici", "Katilimci", arrowhead="empty")  # Inheritance
uml.edge("Kullanici", "Rol", arrowhead="diamond", dir="both")  # Composition
uml.edge("Etkinlik", "KatilimKaydi", arrowhead="diamond")  # Composition
uml.edge("KatilimKaydi", "Katilimci", arrowhead="normal")  # Association
uml.edge("KatilimKaydi", "Etkinlik", arrowhead="normal")  # Association

# Save and render the UML diagram
uml_path = "/mnt/data/UML_Diagram"
uml.render(uml_path, format="png", cleanup=True)

uml_path + ".png"
