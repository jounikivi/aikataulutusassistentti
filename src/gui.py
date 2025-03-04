import tkinter as tk
from tkinter import ttk, messagebox
from google_calendar_sync import sync_tasks_to_calendar
from google_auth import authenticate_google, logout_google
from task_manager import load_tasks, save_tasks
from smart_scheduler import suggest_schedule
import os

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tehtävien Hallinta")
        self.root.geometry("650x450")

        # Käyttäjätiedot
        self.user_label = tk.Label(root, text="Ei kirjautunut sisään")
        self.user_label.pack()

        # Kirjautumis- ja uloskirjautumispainikkeet
        btn_frame_top = tk.Frame(root)
        btn_frame_top.pack(pady=5)

        tk.Button(btn_frame_top, text="Kirjaudu sisään Googlella", command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame_top, text="Kirjaudu ulos", command=self.logout).grid(row=0, column=1, padx=5)

        # Tehtävälista
        self.tree = ttk.Treeview(root, columns=("Title", "Deadline", "Priority", "AI Time"), show="headings")
        self.tree.heading("Title", text="Tehtävän nimi")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Tärkeys")
        self.tree.heading("AI Time", text="AI-ajankohta")
        self.tree.pack(pady=10)

        # Painikkeet tehtävien hallintaan
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Lisää tehtävä", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Muokkaa tehtävää", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Poista tehtävä", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Synkronoi Googleen", command=self.sync_google).grid(row=0, column=3, padx=5)

        # AI-ajankohta
        self.ai_suggestion_label = tk.Label(root, text=f"Tekoäly ehdottaa seuraavaa ajankohtaa uusille tehtäville: {suggest_schedule()}")
        self.ai_suggestion_label.pack(pady=10)

        self.load_task_data()
        self.check_login_status()

    def check_login_status(self):
        """Tarkistaa, onko käyttäjä kirjautunut sisään"""
        if os.path.exists("token.json"):
            self.user_label.config(text="✅ Kirjautunut sisään")
        else:
            self.user_label.config(text="⚠️ Ei kirjautunut sisään")

    def login(self):
        """Käyttäjä kirjautuu sisään Google-tilillä"""
        authenticate_google()
        self.check_login_status()
        messagebox.showinfo("Kirjautuminen", "Olet nyt kirjautunut sisään!")

    def logout(self):
        """Käyttäjä kirjautuu ulos ja poistaa tiedot"""
        logout_google()
        self.check_login_status()
        messagebox.showinfo("Uloskirjautuminen", "Olet kirjautunut ulos!")

    def load_task_data(self):
        """Lataa tehtävät ja näyttää ne käyttöliittymässä"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        tasks = load_tasks()
        for task in tasks:
            ai_time = suggest_schedule()
            self.tree.insert("", "end", values=(task["title"], task["deadline"], task["priority"], ai_time))

    def add_task(self):
        """Lisää uusi tehtävä"""
        messagebox.showinfo("Lisää tehtävä", "Tämä ominaisuus lisätään myöhemmin!")

    def edit_task(self):
        """Muokkaa valittua tehtävää"""
        messagebox.showinfo("Muokkaa tehtävää", "Tämä ominaisuus lisätään myöhemmin!")

    def delete_task(self):
        """Poistaa valitun tehtävän"""
        messagebox.showinfo("Poista tehtävä", "Tämä ominaisuus lisätään myöhemmin!")

    def sync_google(self):
        """Synkronoi tehtävät Google Kalenteriin, jos käyttäjä on kirjautunut"""
        if os.path.exists("token.json"):
            sync_tasks_to_calendar()
            messagebox.showinfo("Synkronointi", "Tehtävät synkronoitu Google Kalenteriin onnistuneesti!")
        else:
            messagebox.showerror("Virhe", "Sinun täytyy kirjautua sisään ennen synkronointia!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
