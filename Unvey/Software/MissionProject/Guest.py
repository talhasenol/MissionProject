import customtkinter as ctk
from tkcalendar import Calendar
from PIL import Image
import Database
import Guest_2
from datetime import datetime
import threading
import pystray
from plyer import notification
import time

database = Database.veritabani()

class Guest:
    def __init__(self):
        self.form = None
        self.item_frames = []
        self.item_buttons = []
        self.items2_frames = []
        self.items2_buttons = []
        self.alarm_active = False
        self.alarm_thread = None
        self.index = 0
        self.current_time = datetime.now().strftime("%H:%M")
    def FORM(self):
        self.icon = None
        def create_icon():
            global icon
            image = Image.open("MissionProject//Pictures//kitap.ico")  # Simge dosyası
            menu = pystray.Menu(
                pystray.MenuItem("Pencereyi Göster", show_window),
                pystray.MenuItem("Alarmı Kapat", stop_alarm),
                pystray.MenuItem("Çıkış", exit_app)
            )
            icon = pystray.Icon("my_app", image, "Alarm Uygulaması", menu)
            threading.Thread(target=icon.run, daemon=True).start()

        def show_window():
            self.form.deiconify()  # Pencereyi tekrar göster
        def start():
            global alarm_active, alarm_thread
            veritabani = Database.veritabani()
            aA = veritabani.todaytime()
            while not aA:
                aA = [('00', '00', '00', '00', '00', '00:00', '00')]
            alarm_time = str(aA[0][5])
            print(f"Alarm zamanı ayarlandı: {alarm_time}")
            
            if alarm_time and not self.alarm_active:
                try:
                    datetime.strptime(alarm_time, "%H:%M")
                    self.alarm_active = True
                    self.alarm_thread = threading.Thread(target=check_alarm, args=(alarm_time,), daemon=True)
                    self.alarm_thread.start()
                except ValueError:
                    print("Geçersiz zaman formatı! Lütfen HH:MM formatında girin.")
        def check_alarm(alarm_time):
            while self.alarm_active:
                self.current_time = datetime.now().strftime("%H:%M")
                print(f"Şu anki zaman: {self.current_time}, Alarm zamanı: {alarm_time}")
                
                if self.current_time == alarm_time:
                    if self.index==0:
                        show_notification(alarm_time)
                        self.index = 1
                    alarm_time = str(aA[0][5])
                else:
                    veritabani = Database.veritabani()
                    aA = veritabani.todaytime()
                    while not aA:
                        aA = [('00', '00', '00', '00', '00', '00:00', '00')]
                    alarm_time = str(aA[0][5])
                time.sleep(3)  # 3 saniyede bir kontrol
        def stop_alarm():
            global alarm_active
            alarm_active = False
            notification.notify(title="Alarm", message="Alarm durduruldu!", timeout=2)

        def exit_app():
            global icon
            if icon:
                icon.stop()
            self.form.destroy()  
            """
        def set_alarm(alarm_time):
            print("set alarm çalıştı")
            def check_time():
                current_time = datetime.now().strftime("%H:%M")
                if alarm_active and current_time == alarm_time:
                    show_notification(alarm_time)
                elif alarm_active:
                    self.form.after(30000, check_time)  # 30 saniyede bir kontrol
            check_time()"""

        def show_notification(alarm_time):
            notification.notify(
                title="Alarm",
                message=f"Alarm Zamanı: {alarm_time}",
                timeout=10
            )
        create_icon()
        def add_mission():
            if self.entry1.get()=="" or self.hour_spinbox.get()=="" or self.minute_spinbox.get()=="":
                self.label7.configure(text="Lütfen Boş Bırakmayınız\nSadece Acıklama Boş Kalabilir",text_color="red")
            elif self.hour_spinbox.get().isalpha()==True or self.minute_spinbox.get().isalpha==True:
                self.label7.configure(text="Lütfen Sadece Sayı Giriniz",text_color="red")
            elif int(self.hour_spinbox.get())>24 or int(self.minute_spinbox.get())>59:
                self.label7.configure(text="Lütfen Saati En Fazla 24\nDakikayı da En Fazla 59 Girin",text_color="red")
            else:
                def remembertime(text):
                    saat = ""
                    if text=="10 dakika kala":
                        hour = int(self.hour_spinbox.get())
                        minute = int(self.minute_spinbox.get())
                        total_minutes = hour * 60 + minute - 10
                        new_hour = total_minutes // 60
                        new_minute = total_minutes % 60
                    elif text=="30 dakika kala":
                        hour = int(self.hour_spinbox.get())
                        minute = int(self.minute_spinbox.get())
                        total_minutes = hour * 60 + minute - 30
                        new_hour = total_minutes // 60
                        new_minute = total_minutes % 60
                    elif text=="1 saat kala":
                        hour = int(self.hour_spinbox.get())
                        minute = int(self.minute_spinbox.get())
                        total_minutes = hour * 60 + minute - 60
                        new_hour = total_minutes // 60
                        new_minute = total_minutes % 60
                    elif text=="2 saat kala":
                        hour = int(self.hour_spinbox.get())
                        minute = int(self.minute_spinbox.get())
                        total_minutes = hour * 60 + minute - 120
                        new_hour = total_minutes // 60
                        new_minute = total_minutes % 60
                    elif text=="1 gün kala":
                        pass
                    return f"{new_hour:02d}:{new_minute:02d}"
                index = 0
                if database.index()[0][0]==None:
                    index==0
                else:
                    index == database.index()[0][0]
                
                mission_data = (
                    f"{str(index+1)}"f"{" "}"
                    f"{self.entry1.get()}"f"{" "}"
                    f"{self.hour_spinbox.get()}:{self.minute_spinbox.get()}"
                )
                remembertime = remembertime(str(self.combo2.get()))
                now = datetime.now()
                formatted = now.strftime("%Y-%m-%d")
                tarih = self.calendar.get_date()
                if formatted>tarih:
                    tarih = formatted
                time_str = f"{self.hour_spinbox.get()}:{self.minute_spinbox.get()}"
                database.addmission(
                    self.entry1.get(),
                    self.entry2.get(),
                    tarih,
                    time_str,
                    remembertime,
                    self.combo.get(),
                )
                #database.connectionclose()
                now = datetime.now()
                formatted = now.strftime("%Y-%m-%d")
                if self.combo3.get()=="Güncel Görevleriniz":
                    #mission data tuple olmalı
                    add_item_to_listbox(mission_data)
                    if formatted >= self.calendar.get_date():
                        add_item_to_listbox2(mission_data)
            """def add_item_to_listbox(item_text):
                item_frame = ctk.CTkFrame(self.listbox, fg_color="transparent")
                item_frame.pack(fill="x", pady=2, padx=5)
                
                btn = ctk.CTkButton(
                    item_frame,
                    text=item_text,
                    fg_color="transparent",
                    anchor="w",
                    command=lambda t=item_text: select_item(t),
                    width=200
                )
                btn.bind("<Double-Button-1>", lambda e, t=item_text: on_double_click(t))
                btn.pack(side="left", expand=True, fill="x")
                
                image = ctk.CTkImage(Image.open("MissionProject/Pictures/resim2.png"), size=(20, 20))
                delete_btn = ctk.CTkButton(
                    item_frame,
                    image=image,
                    text="",
                    width=30,
                    height=30,
                    fg_color="transparent",
                    hover_color="#d33b3b",
                    command=lambda t=item_text: delete_item(t)
                )
                delete_btn.pack(side="right", padx=5)
                
                # Eksik olan kısım - listelere ekleme
                self.item_frames.append((item_text, item_frame))
                self.item_buttons.append(btn)"""
        def add_item_to_listbox(item_data):
            if type(item_data)==str:
                item_data = tuple(item_data.split())
            # item_data örneğin: (id, görev_adı, açıklama, tarih, zaman, hatırlatma_zamanı, müzik)
            item_id = item_data[0]
            item_text = f"{item_data[1]} {item_data[2]}"  # ID + görev adı + hatırlatma saati

            item_frame = ctk.CTkFrame(self.listbox, fg_color="transparent")
            item_frame.pack(fill="x", pady=2, padx=5)

            btn = ctk.CTkButton(
                item_frame,
                text=item_text,
                fg_color="transparent",
                anchor="w",
                command=lambda data=item_data: select_item(data),
                width=200
            )
            btn.bind("<Double-Button-1>", lambda e, data=item_data: on_double_click(data))
            btn.pack(side="left", expand=True, fill="x")

            image = ctk.CTkImage(Image.open("MissionProject/Pictures/resim2.png"), size=(20, 20))
            delete_btn = ctk.CTkButton(
                item_frame,
                image=image,
                text="",
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="#d33b3b",
                command=lambda id=item_id: delete_item(item_id)
            )
            delete_btn.pack(side="right", padx=5)

            self.item_frames.append((item_id, item_frame))
            self.item_buttons.append(btn)
            
        def add_item_to_listbox2(item_data):
            if type(item_data)==str:
                item_data = tuple(item_data.split())
            # item_data örneğin: (id, görev_adı, açıklama, tarih, zaman, hatırlatma_zamanı, müzik
            item_text = f" {item_data[1]} {item_data[2]}"  # ID + görev adı + hatırlatma saati
            items2_frames = ctk.CTkFrame(self.listbox2, fg_color="transparent")
            items2_frames.pack(fill="x", pady=2, padx=5)
            
            btn = ctk.CTkButton(
                items2_frames,
                text=item_text,
                fg_color="transparent",
                anchor="w",
                command=lambda data=item_data: select_item(data),
                width=200
            )
            btn.bind("<Double-Button-1>", lambda e, data=item_data: on_double_click(data))
            btn.pack(side="left", expand=True, fill="x")
            image = ctk.CTkImage(Image.open("MissionProject/Pictures/resim2.png"), size=(20, 20))
            delete_btn = ctk.CTkButton(
                items2_frames,
                image=image,
                text="",
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="#d33b3b",
                command=lambda t=item_data: delete_item2(t)
            )
            delete_btn.pack(side="right", padx=5)
            
            self.items2_frames.append((item_data, items2_frames))
            self.items2_buttons.append(btn)

        def select_item(item_text):
            for text, frame in self.item_frames:
                for widget in frame.winfo_children():
                    if isinstance(widget, ctk.CTkButton) and widget.cget("text") == text:
                        widget.configure(fg_color="#3b8Ced0" if text == item_text else "transparent")

        def on_double_click(text):
            editor = Guest_2.guest_2()
            editor.Show(text)

        def delete_item(item_id):
            for i, (id, frame) in enumerate(self.item_frames):
                if id == item_id:
                    frame.destroy()
                    self.item_frames.pop(i)
                    database.DeleteMission(item_id)
                    break
            
            for i, (item_data, frame) in enumerate(self.items2_frames):
                if item_data[0] == item_id:  
                    frame.destroy()
                    self.items2_frames.pop(i)
                    break
        def delete_item2(item_text):
            item_id = item_text[0]  
            for i, (data, frame) in enumerate(self.items2_frames):
                if data[0] == item_id:
                    frame.destroy()
                    self.items2_frames.pop(i)
                    database.DeleteMission(item_id)
                    break            
            for i, (id, frame) in enumerate(self.item_frames):
                if id == item_id:
                    frame.destroy()
                    self.item_frames.pop(i)
                    break

        self.form = ctk.CTk()
        self.form.title("Guest Mode")
        self.form.geometry("1200x600")
        self.form.resizable(False, False)
        def bursa():
            self.form.withdraw()
            #create_icon()
        self.form.after(100,start)
        self.form.protocol("WM_DELETE_WINDOW", bursa)
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.listbox = ctk.CTkScrollableFrame(self.form, width=300, height=480, corner_radius=10)
        self.listbox.place(x=25, y=65)
        self.listbox2 = ctk.CTkScrollableFrame(self.form, width=300, height=480, corner_radius=10)
        self.listbox2.place(x=380, y=65)
        self.items = database.allrequest()
        self.item_frames = []
        self.item_buttons = []

        for item in self.items:
            add_item_to_listbox(item)

        self.items2 = database.todayrequest()
        self.items2_frames = []
        self.items2_buttons = []
        for item2 in self.items2:
            add_item_to_listbox2(item2)
        self.calendar = Calendar(
            self.form,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            background='#2b2b2b',  # Koyu arka plan
            foreground='white',     # Yazı rengi
            selectbackground='#3b8ed0',  # Seçili gün arka plan rengi
            selectforeground='white',    # Seçili gün yazı rengi
            headersbackground='#3b3b3b',  # Başlık arka plan rengi
            headersforeground='white',   # Başlık yazı rengi
            normalbackground='#2b2b2b',  # Normal günlerin arka plan rengi
            normalforeground='white',   # Normal günlerin yazı rengi
            weekendbackground='#2b2b2b', # Hafta sonu arka plan rengi
            weekendforeground='#ff6b6b', # Hafta sonu yazı rengi (kırmızımsı)
            othermonthbackground='#1f1f1f',  # Diğer ayların günleri
            othermonthforeground='gray50',   # Diğer ayların yazı rengi
            bordercolor='#3b3b3b',      # Kenarlık rengi
            borderwidth=1,
            font=('Arial', 10, 'bold'), # Yazı tipi
            cursor='hand2'              # Fare imleci
            )
        self.calendar.place(x=1100, y=25,width=350)

        self.label4 = ctk.CTkLabel(self.form,text="Görevleriniz :")
        self.label4.place(x=30,y=25)

        def on_combobox_select(choice):
            if choice == "Güncel Görevleriniz":
                for _,frame in self.item_frames:
                    frame.destroy()
                self.item_frames = []
                self.item_buttons = []
                self.items = database.allrequest()
                for item in self.items:
                    add_item_to_listbox(item)
            elif choice =="Geçmiş Görevleriniz":
                for _,frame in self.item_frames:
                    frame.destroy()
                self.items = database.oldmission()
                self.item_frames = []
                self.item_buttons = []
                for item in self.items:
                    add_item_to_listbox(item)

        screnn_options = ["Güncel Görevleriniz","Geçmiş Görevleriniz"]
        self.combo3 = ctk.CTkComboBox(self.form,values=screnn_options,command=on_combobox_select)
        self.combo3.place(x=110,y=25)
        
        self.label5 = ctk.CTkLabel(self.form,text="Bugünün Görevlerini")
        self.label5.place(x=380,y=25)
        
        self.label1 = ctk.CTkLabel(self.form, text="Görev Adı :")
        self.label1.place(x=830, y=220)
        
        self.entry1 = ctk.CTkEntry(self.form, width=250, placeholder_text="Görev Adı")
        self.entry1.place(x=900, y=220)

        self.label2 = ctk.CTkLabel(self.form, text="Görev Acıklama :")
        self.label2.place(x=795, y=270)
        
        self.entry2 = ctk.CTkEntry(self.form, width=250, placeholder_text="Görev Acıklaması")
        self.entry2.place(x=900, y=270)

        self.label3 = ctk.CTkLabel(self.form, text="Muzik :")
        self.label3.place(x=850, y=320)
        
        music_options = ["Davul Sesi", "Piano Sesi", "Çalar Saat", "Mehter Marşı"]
        self.combo = ctk.CTkComboBox(self.form, values=music_options, width=250)
        self.combo.place(x=900, y=320)

        remember_options = ["10 dakika kala", " 30 dakika kala", "1 saat kala", "2 saat kala","1 gün kala"]
        self.combo2 = ctk.CTkComboBox(self.form, values=remember_options, width=250)
        self.combo2.place(x=900, y=410)

        self.label6 = ctk.CTkLabel(self.form, text="Hatırlatma Zamanı :")
        self.label6.place(x=780, y=410)

        self.time_label = ctk.CTkLabel(self.form, text="Zaman:")
        self.time_label.place(x=845, y=370)
        
        self.hour_spinbox = ctk.CTkEntry(self.form, width=50, placeholder_text="HH")
        self.hour_spinbox.place(x=900, y=370)
        
        self.minute_spinbox = ctk.CTkEntry(self.form, width=50, placeholder_text="MM")
        self.minute_spinbox.place(x=955, y=370)
        self.label7 = ctk.CTkLabel(self.form,text="")
        self.label7.place(x=950,y=500)
        self.button = ctk.CTkButton(
            self.form,
            text="Görev Ekle",
            command=add_mission,
            width=250,
            height=40,
            corner_radius=8
        )
        self.button.place(x=900, y=450)         
        self.form.mainloop()

if __name__ == "__main__":
    app = Guest()
    app.FORM()