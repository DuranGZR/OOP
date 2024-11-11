class Ogrenci:
    def __init__(self,isim,notu):
        self.isim = isim
        self.notu = notu

    def get_info(self):
        return f"Öğrenci: {self.isim}, Notu: {self.notu}"

    def is_passing(self):
        if self.notu >= 50:
            return True
        else:
            return False


students = [
    Ogrenci("Ali", 45),
    Ogrenci("Ayşe", 75),
    Ogrenci("Sıla", 100)
]

for i in students:
    print(i.get_info())
    if i.is_passing():
        print(f"{i.isim} dersi geçti")
    else:
        print(f"{i.isim} dersi geçemedi")

 ###################################################################

class Book:
    def __init__(self, kitapAdı,yazar):
        self.kitapAdı =kitapAdı
        self.yazar = yazar

    def get_info(self):
        return f"Kitap: {self.kitapAdı}, Yazar: {self.yazar}"

class Library:
    def __init__(self):
        self.books = []

    def addBook(self,book):
        self.books.append(book)
        print(f"{book.kitapAdı} adlı kiptap kütüphaneye eklendi")

    def removeBook(self,isim):

        for book in self.books:
            if book.kitapAdı == isim:
                self.books.remove(book)
                print(f"{book.kitapAdı} adlı kitap kütüphaneden silindi")
                return
        print("bu kitap yok")

    def listBooks(self):
        if not self.books:
            print("kütüphanede kitap yok")
        else:
            print("kütüphendeki kitaplar")
            for book in self.books:
                print(book.get_info())

def librarySystem():
    library = Library()

    while True:
        print("\n--- Kütüphane Yönetim Sistemi ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Çıkış")

        secim = input("seçin (1-4")

        if secim == "1":
            isim = input("isim")
            yazar = input("yazar")
            book = Book(isim,yazar)
            library.addBook(book)

        elif secim == "2":
            isim = input("silinecek isim")
            library.removeBook(isim)

        elif secim == "3":
            library.listBooks()

        elif secim == "4":
            break
        else:
            print("geçersiz")

librarySystem()


########################################


from collections import deque

kuyruk = deque()

kuyruk.append("ali")
kuyruk.append("sıla")

kuyruk.popleft()


















