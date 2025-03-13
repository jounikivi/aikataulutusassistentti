import tkinter as tk
from tkinter import ttk, messagebox
import os
from google_calendar_sync import sync_tasks_to_calendar
from google_auth import authenticate_google, logout_google
from task_manager import load_tasks, save_tasks

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📅 Älykäs Aikataulutusassistentti")
        self.root.geometry("750x450")
        self.root.configure(bg="#f0f0f0")  

        # Otsikko (Kirjautumistila)
        self.user_label = ttk.Label(root, text="⚠️ Ei kirjautunut sisään", foreground="red", font=("Arial", 12, "bold"))
        self.user_label.pack(pady=5)

        # **Kirjautumis- ja uloskirjautumisnapit**
        self.login_frame = ttk.Frame(root)
        self.login_frame.pack(pady=5)

        self.login_btn = ttk.Button(self.login_frame, text="🔑 Kirjaudu sisään Googlella", command=self.login)
        self.login_btn.grid(row=0, column=0, padx=5)

        self.logout_btn = ttk.Button(self.login_frame, text="🚪 Kirjaudu ulos", command=self.logout)
        self.logout_btn.grid(row=0, column=1, padx=5)

        # Tehtävälista
        self.tree = ttk.Treeview(root, columns=("Title", "Deadline", "Priority"), show="headings", height=10)
        self.tree.heading("Title", text="Tehtävän nimi", anchor="center")
        self.tree.heading("Deadline", text="Deadline", anchor="center")
        self.tree.heading("Priority", text="Tärkeys", anchor="center")

        # Keskitetään sarakkeet ja lisätään leveydet
        self.tree.column("Title", anchor="w", width=250)
        self.tree.column("Deadline", anchor="center", width=120)
        self.tree.column("Priority", anchor="center", width=70)
        self.tree.pack(pady=10)

        # Painikkeet tehtävien hallintaan
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(pady=5)

        self.add_task_btn = ttk.Button(self.btn_frame, text="➕ Lisää tehtävä", command=self.add_task, state=tk.DISABLED)
        self.add_task_btn.grid(row=0, column=0, padx=5)

        self.edit_task_btn = ttk.Button(self.btn_frame, text="✏️ Muokkaa tehtävää", command=self.edit_task, state=tk.DISABLED)
        self.edit_task_btn.grid(row=0, column=1, padx=5)

        self.delete_task_btn = ttk.Button(self.btn_frame, text="🗑️ Poista tehtävä", command=self.delete_task, state=tk.DISABLED)
        self.delete_task_btn.grid(row=0, column=2, padx=5)

        self.sync_google_btn = ttk.Button(self.btn_frame, text="🔄 Synkronoi Googleen", command=self.sync_google, state=tk.DISABLED)
        self.sync_google_btn.grid(row=0, column=3, padx=5)

        self.load_task_data()
        self.check_login_status()

    def check_login_status(self):
        """Tarkistaa, onko käyttäjä kirjautunut sisään ja näyttää oikeat napit"""
        if os.path.exists("token.json"):
            self.user_label.config(text="✅ Kirjautunut sisään", foreground="green")
            self.enable_task_buttons()
            self.load_task_data()
            self.login_btn.grid_remove()  # Piilotetaan "Kirjaudu sisään" -nappi
            self.logout_btn.grid()  # Näytetään "Kirjaudu ulos" -nappi
        else:
            self.user_label.config(text="⚠️ Ei kirjautunut sisään", foreground="red")
            self.disable_task_buttons()
            self.clear_task_list()
            self.login_btn.grid()  # Näytetään "Kirjaudu sisään" -nappi
            self.logout_btn.grid_remove()  # Piilotetaan "Kirjaudu ulos" -nappi

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

    def load_task_data(self):
        """Lataa tehtävät ja näyttää ne käyttöliittymässä"""
        self.clear_task_list()
        tasks = load_tasks()

        for task in tasks:
            self.tree.insert("", "end", values=(task["title"], task["deadline"], task["priority"]))

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

    def add_task(self):
        """Lisää tehtävän"""
        new_task_window = tk.Toplevel(self.root)
        new_task_window.title("➕ Lisää tehtävä")

        ttk.Label(new_task_window, text="Tehtävän nimi:").grid(row=0, column=0)
        title_entry = ttk.Entry(new_task_window)
        title_entry.grid(row=0, column=1)

        ttk.Label(new_task_window, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=1, column=0)
        deadline_entry = ttk.Entry(new_task_window)
        deadline_entry.grid(row=1, column=1)

        ttk.Label(new_task_window, text="Tärkeysaste (1-5):").grid(row=2, column=0)
        priority_entry = ttk.Entry(new_task_window)
        priority_entry.grid(row=2, column=1)

        def save_new_task():
            title = title_entry.get()
            deadline = deadline_entry.get()
            priority = priority_entry.get()

            if title and deadline and priority:
                tasks = load_tasks()
                tasks.append({"title": title, "deadline": deadline, "priority": priority, "status": "pending"})
                save_tasks(tasks)
                self.load_task_data()
                new_task_window.destroy()
            else:
                messagebox.showerror("⚠️ Virhe", "Täytä kaikki kentät!")

        ttk.Button(new_task_window, text="💾 Tallenna", command=save_new_task).grid(row=3, column=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
