import customtkinter as tk
import Database as d
database = d.veritabani()

class guest_2:
    def __init__(self):
        self.form = None
        self.text = None
    def FORM(self):
        pass   
    def Show(self,data):
        self.text = data
        if type(self.text)==str:
            self.text = tuple(data.split())
        try:
            self.text = database.OnlyRequest(data[0])[0]
        except Exception as e:
            database1 = d.veritabani()
            self.text = database1.OnlyRequest(int(data[0]))
        self.app = tk.CTk()
        self.app.title("Düzenleme")
        self.app.geometry("500x500")
        self.gorevadi = tk.CTkLabel(self.app,text="Görevin Adı : ")
        self.gorevadi.place(x=100,y=100)
        self.gorevadi2 = tk.CTkLabel(self.app,text=self.text[1])
        self.gorevadi2.place(x=240,y=100)

        self.gorevaciklama = tk.CTkLabel(self.app,text="Görevin Acıklaması : ")
        self.gorevaciklama.place(x=100,y=150)
        self.gorevaciklama2 = tk.CTkLabel(self.app,text=self.text[2])
        self.gorevaciklama2.place(x=240,y=150)

        self.gorevdate = tk.CTkLabel(self.app,text="Görevin Zamanı : ")
        self.gorevdate.place(x=100,y=200)
        self.gorevdate2 = tk.CTkLabel(self.app,text=self.text[3])
        self.gorevdate2.place(x=240,y=200)

        self.gorevzamani = tk.CTkLabel(self.app,text="Görevin Saati : ")
        self.gorevzamani.place(x=100,y=250)
        self.gorevzamani2 = tk.CTkLabel(self.app,text=self.text[4])
        self.gorevzamani2.place(x=240,y=250)
        
        self.gorevvoice = tk.CTkLabel(self.app,text="Bildirim Sesi : ")
        self.gorevvoice.place(x=100,y=300)
        self.gorevvoice2 = tk.CTkLabel(self.app,text=self.text[3])
        self.gorevvoice2.place(x=240,y=300)
        self.app.mainloop()
        pass
if __name__ == "__main__":
    app = guest_2()
    app.FORM()