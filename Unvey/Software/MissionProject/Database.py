import sqlite3
import os
from datetime import datetime

now = datetime.now()
formatted = now.strftime("%Y-%m-%d")  
formatted2 = now.strftime("%H:%M")  
#print(formatted)  # '2023-12-25 14:30'
class veritabani:
    
    def __init__(self):
        try:
            self.yol = os.path.dirname(os.path.abspath(__file__)) + "\\Databases\\database.db"
            self.con = sqlite3.connect(self.yol)  
            self.cunsor = self.con.cursor()  
        except sqlite3.Error as e:
            print(f"Bağlantı hatası: {e}")
    def index(self):
        try:
            self.cunsor.execute("select max(MissionsId) from Missions")
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")
    def oldmission(self):
        try:
            self.cunsor.execute(f"select MissionsId,MissionAdi,MissionTime FROM Missions WHERE MissionDate < '{str(formatted)}';")
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")
    def connectionopen(self):
        try:
            if self.con is None:
                self.con = sqlite3.connect(self.yol)
                self.cunsor = self.con.cursor()
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
    def todaytime(self):
        try:
            self.cunsor.execute(f"SELECT * from Missions where missionDate = date('now') ORDER BY abs(strftime('%s','{formatted2}') - strftime('%s', MissionRemember)) LIMIT 1;")
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")       
    def OnlyRequest(self,id):
        try:  
            self.cunsor.execute(f"select * from Missions where MissionsId='{id}'")
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")
    def allrequest(self):
        try:
            #self.oldmission()   
            self.cunsor.execute(f"select MissionsId,MissionAdi,MissionTime FROM Missions WHERE MissionDate >= '{str(formatted)}' ORDER BY time(MissionTime) DESC;")
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")
    def todayrequest(self):
        try:
            self.cunsor.execute("SELECT MissionsId,MissionAdi,MissionTime FROM Missions where MissionDate = ? ORDER BY time(MissionTime) DESC;",(formatted,))
            kullanicibilgi = self.cunsor.fetchall()
            return kullanicibilgi
        except sqlite3.Error as e:
            print(f"Sorgu hatası: {e}")

    def addmission(self, ad, aciklama, gun, saat,hatirlatici,ses):
        self.connectionopen()
        try:
            self.cunsor.execute(
                "INSERT INTO Missions (MissionAdi, MissionExplanation, MissionDate,MissionTime,MissionRemember,MissionMusic) VALUES (?, ?, ?, ?, ?, ?)",
                (ad,aciklama,gun,saat,hatirlatici,ses)
            )
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            pass
    def DeleteMission(self, id):
        self.connectionopen()
        try:
            self.cunsor.execute(
            "DELETE FROM Missions WHERE MissionsId = ?",  
            (id,)  
            )
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            pass

    def connectionclose(self):
        try:
            if self.con:
                self.con.close()  # Bağlantıyı kapatıyoruz
        except sqlite3.Error as e:
            print(f"Bağlantı kapama hatası: {e}")
"""
# Örnek kullanım
a = veritabani()
for a in a.allrequest():
    print(f" lskmdklsamdsad {a}")
"""
if __name__ == "__main__":
    app = veritabani()
    a = app.index()
    print(a)
