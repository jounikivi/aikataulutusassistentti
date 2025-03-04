import tkinter as tk
from tkinter import ttk, messagebox
from google_calendar_sync import sync_tasks_to_calendar
from google_auth import authenticate_google, logout_google
from task_manager import load_tasks, save_tasks
import os

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tehtävien Hallinta")
        self.root.geometry("650x450")

        # Käyttäjätiedot
        self.user_label = tk.Label(root, text="⚠️ Ei kirjautunut sisään", fg="red")
        self.user_label.pack()

        # Kirjautumis- ja uloskirjautumispainikkeet
        btn_frame_top = tk.Frame(root)
        btn_frame_top.pack(pady=5)

        tk.Button(btn_frame_top, text="Kirjaudu sisään Googlella", command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame_top, text="Kirjaudu ulos", command=self.logout).grid(row=0, column=1, padx=5)

        # Tehtävälista
        self.tree = ttk.Treeview(root, columns=("Title", "Deadline", "Priority"), show="headings")
        self.tree.heading("Title", text="Tehtävän nimi")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Tärkeys")
        self.tree.pack(pady=10)

        # Painikkeet tehtävien hallintaan
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)

        self.add_task_btn = tk.Button(self.btn_frame, text="Lisää tehtävä", command=self.add_task, state=tk.DISABLED)
        self.add_task_btn.grid(row=0, column=0, padx=5)

        self.edit_task_btn = tk.Button(self.btn_frame, text="Muokkaa tehtävää", command=self.edit_task, state=tk.DISABLED)
        self.edit_task_btn.grid(row=0, column=1, padx=5)

        self.delete_task_btn = tk.Button(self.btn_frame, text="Poista tehtävä", command=self.delete_task, state=tk.DISABLED)
        self.delete_task_btn.grid(row=0, column=2, padx=5)

        self.sync_google_btn = tk.Button(self.btn_frame, text="Synkronoi Googleen", command=self.sync_google, state=tk.DISABLED)
        self.sync_google_btn.grid(row=0, column=3, padx=5)

        self.load_task_data()
        self.check_login_status()

    def check_login_status(self):
        """Tarkistaa, onko käyttäjä kirjautunut sisään"""
        if os.path.exists("token.json"):
            self.user_label.config(text="✅ Kirjautunut sisään", fg="green")
            self.enable_task_buttons()
            self.load_task_data()
        else:
            self.user_label.config(text="⚠️ Ei kirjautunut sisään", fg="red")
            self.disable_task_buttons()
            self.clear_task_list()

    def enable_task_buttons(self):
        """Aktivoi tehtävien hallintapainikkeet kirjautumisen jälkeen"""
        self.add_task_btn.config(state=tk.NORMAL)
        self.edit_task_btn.config(state=tk.NORMAL)
        self.delete_task_btn.config(state=tk.NORMAL)
        self.sync_google_btn.config(state=tk.NORMAL)

    def disable_task_buttons(self):
        """Poistaa käytöstä tehtävien hallintapainikkeet ennen kirjautumista"""
        self.add_task_btn.config(state=tk.DISABLED)
        self.edit_task_btn.config(state=tk.DISABLED)
        self.delete_task_btn.config(state=tk.DISABLED)
        self.sync_google_btn.config(state=tk.DISABLED)

    def clear_task_list(self):
        """Tyhjentää tehtävälistan käyttöliittymästä"""
        for item in self.tree.get_children():
            self.tree.delete(item)

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
        """Lataa tehtävät ja näyttää ne käyttöliittymässä vain kirjautuneelle käyttäjälle"""
        self.clear_task_list()
        tasks = load_tasks()
        for task in tasks:
            self.tree.insert("", "end", values=(task["title"], task["deadline"], task["priority"]))

    def add_task(self):
        """Lisää tehtävän (toiminnallisuus lisätään myöhemmin)"""
        messagebox.showinfo("Lisää tehtävä", "Tämä ominaisuus lisätään myöhemmin!")

    def edit_task(self):
        """Muokkaa tehtävää (toiminnallisuus lisätään myöhemmin)"""
        messagebox.showinfo("Muokkaa tehtävää", "Tämä ominaisuus lisätään myöhemmin!")

    def delete_task(self):
        """Poistaa tehtävän (toiminnallisuus lisätään myöhemmin)"""
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
