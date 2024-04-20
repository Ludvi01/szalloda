import tkinter as tk
from tkinter import messagebox, simpledialog, font as tkFont
from datetime import date, datetime, timedelta

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = {}
        self.foglalasok = []
        self.alap_adatok_betoltese()

    def szoba_hozzaadas(self, szoba):
        self.szobak[szoba.szobaszam] = szoba

    def alap_adatok_betoltese(self):
        self.szobak[101] = Szoba(101, 15000)
        self.szobak[102] = Szoba(102, 20000)
        self.szobak[103] = Szoba(103, 18000)
        mai_nap = date.today() + timedelta(days=30)
        for i in range(5):
            nap = mai_nap + timedelta(days=i * 4)
            self.foglalas(101 + i % 3, nap)
    def foglalas(self, szobaszam, nap):
        # Ellenőrizzük, hogy létezik-e a szobaszám
        if szobaszam not in self.szobak:
            raise ValueError("A megadott szobaszám nem létezik.")

        # Ellenőrizzük, hogy a szoba már foglalt-e erre a napra
        if any(foglalas[0] == szobaszam and foglalas[1] == nap for foglalas in self.foglalasok):
            raise ValueError("A szoba már foglalt erre a napra.")

        # Ha a szoba létezik és nem foglalt erre a napra, akkor rögzíthetjük
        self.foglalasok.append((szobaszam, nap))
        return self.szobak[szobaszam].ar

    def lemondas(self, szobaszam, nap):
        for foglalas in self.foglalasok:
            if foglalas[0] == szobaszam and foglalas[1] == nap:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def foglalasok_listazasa(self):
        return self.foglalasok

# GUI osztály
class SzallodaGUI:
    def __init__(self, master, szalloda):
        self.master = master
        self.szalloda = szalloda
        self.master.title("Foglalási rendszer")

        # Ablak méretének beállítása
        window_width = 350
        window_height = 250
        self.master.geometry(f'{window_width}x{window_height}')

        # Ablak középre helyezése
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"+{x_coordinate}+{y_coordinate}")

        # Betűtípusok beállítása
        self.header_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=12)

        # szálloda neve címkéje
        header_label = tk.Label(master, text=self.szalloda.nev, font=self.header_font)
        header_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Foglalások címkéje
        tk.Label(master, text="Foglalások:", font=self.header_font).grid(row=1, column=0, sticky="w", padx=15)

        # Foglalások listájának megjelenítése
        self.foglalasok_listbox = tk.Listbox(master, width=35, height=2, font=self.normal_font)
        self.foglalasok_listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15)

        # Új foglalás gomb
        tk.Button(master, text='Új Foglalás', command=self.uj_foglalas, font=self.normal_font).grid(row=3, column=0, sticky="nsew", padx=15, pady=10)

        # Lemondás gomb
        tk.Button(master, text='Lemondás', command=self.lemondas, font=self.normal_font).grid(row=3, column=1, sticky="nsew", padx=15, pady=10)

        # A foglalások listájának frissítése
        self.frissit_foglalasok_listajat()

    def frissit_foglalasok_listajat(self):
        self.foglalasok_listbox.delete(0, tk.END)
        for foglalas in self.szalloda.foglalasok_listazasa():
            self.foglalasok_listbox.insert(tk.END, f"Szoba: {foglalas[0]}, Nap: {foglalas[1]}")

    def uj_foglalas(self):
        szobaszam = simpledialog.askinteger("Új Foglalás", "Szoba száma:")
        if szobaszam and szobaszam in self.szalloda.szobak:
            nap = simpledialog.askstring("Új Foglalás", "Dátum (ÉÉÉÉ.HH.NN):")
            try:
                date_obj = datetime.strptime(nap, '%Y.%m.%d').date()
                if date_obj < date.today():
                    raise ValueError("A dátum nem lehet a mai napnál korábbi.")
                ar = self.szalloda.foglalas(szobaszam, date_obj)
                messagebox.showinfo("Siker", f"Foglalás rögzítve. Ár: {ar} Ft")
            except ValueError as e:
                messagebox.showerror("Hiba", str(e))
        else:
            messagebox.showerror("Hiba", "Érvénytelen szobaszám vagy nincs ilyen szoba.")

    def lemondas(self):
        selected = self.foglalasok_listbox.curselection()
        if selected:
            foglalas = self.foglalasok_listbox.get(selected)
            szobaszam, nap = map(lambda x: x.split(": ")[1], foglalas.split(", "))
            date_obj = datetime.strptime(nap, '%Y.%m.%d').date()
            if self.szalloda.lemondas(int(szobaszam), date_obj):
                messagebox.showinfo("Siker", "Foglalás lemondva.")
            else:
                messagebox.showerror("Hiba", "Nem lehet lemondani a foglalást.")
        else:
            messagebox.showerror("Hiba", "Válassz ki egy foglalást a listából!")

root = tk.Tk()
szalloda = Szalloda("Grand Prima Hotel & Spa")
app = SzallodaGUI(root, szalloda)
root.mainloop()
