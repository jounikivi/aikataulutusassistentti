import tkinter as tk
from tkinter import ttk, messagebox
import json
from smart_scheduler import suggest_schedule
from google_calendar_sync import sync_tasks_to_calendar
from task_manager import load_tasks, save_tasks

TASKS_FILE = "tasks.json"

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tehtävien Hallinta")
        self.root.geometry("600x400")

        # Tehtävälista (taulukko)
        self.tree = ttk.Treeview(root, columns=("Title", "Deadline", "Priority", "AI Time"), show="headings")
        self.tree.heading("Title", text="Tehtävän nimi")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Tärkeys")
        self.tree.heading("AI Time", text="AI-ajankohta")
        self.tree.pack(pady=10)

        # Painikkeet
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Lisää tehtävä", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Muokkaa tehtävää", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Poista tehtävä", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Synkronoi Googleen", command=self.sync_google).grid(row=0, column=3, padx=5)

        # AI:n suosittelema ajankohta
        self.ai_suggestion_label = tk.Label(root, text=f"Tekoäly ehdottaa seuraavaa ajankohtaa uusille tehtäville: {suggest_schedule()}")
        self.ai_suggestion_label.pack(pady=10)

        self.load_task_data()

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
        new_task_window = tk.Toplevel(self.root)
        new_task_window.title("Lisää uusi tehtävä")

        tk.Label(new_task_window, text="Tehtävän nimi:").grid(row=0, column=0)
        title_entry = tk.Entry(new_task_window)
        title_entry.grid(row=0, column=1)

        tk.Label(new_task_window, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=1, column=0)
        deadline_entry = tk.Entry(new_task_window)
        deadline_entry.grid(row=1, column=1)

        tk.Label(new_task_window, text="Tärkeysaste (1-5):").grid(row=2, column=0)
        priority_entry = tk.Entry(new_task_window)
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
                messagebox.showerror("Virhe", "Täytä kaikki kentät!")

        tk.Button(new_task_window, text="Tallenna", command=save_new_task).grid(row=3, column=1)

    def edit_task(self):
        """Muokkaa valittua tehtävää"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Virhe", "Valitse muokattava tehtävä!")
            return

        item_values = self.tree.item(selected_item, "values")
        tasks = load_tasks()

        for task in tasks:
            if task["title"] == item_values[0]:
                edit_task_window = tk.Toplevel(self.root)
                edit_task_window.title("Muokkaa tehtävää")

                tk.Label(edit_task_window, text="Tehtävän nimi:").grid(row=0, column=0)
                title_entry = tk.Entry(edit_task_window)
                title_entry.grid(row=0, column=1)
                title_entry.insert(0, task["title"])

                tk.Label(edit_task_window, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=1, column=0)
                deadline_entry = tk.Entry(edit_task_window)
                deadline_entry.grid(row=1, column=1)
                deadline_entry.insert(0, task["deadline"])

                tk.Label(edit_task_window, text="Tärkeysaste (1-5):").grid(row=2, column=0)
                priority_entry = tk.Entry(edit_task_window)
                priority_entry.grid(row=2, column=1)
                priority_entry.insert(0, task["priority"])

                def save_edited_task():
                    task["title"] = title_entry.get()
                    task["deadline"] = deadline_entry.get()
                    task["priority"] = priority_entry.get()
                    save_tasks(tasks)
                    self.load_task_data()
                    edit_task_window.destroy()

                tk.Button(edit_task_window, text="Tallenna muutokset", command=save_edited_task).grid(row=3, column=1)
                break

    def delete_task(self):
        """Poistaa valitun tehtävän"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Virhe", "Valitse poistettava tehtävä!")
            return

        item_values = self.tree.item(selected_item, "values")
        tasks = load_tasks()
        tasks = [task for task in tasks if task["title"] != item_values[0]]
        save_tasks(tasks)
        self.load_task_data()

    def sync_google(self):
        """Synkronoi tehtävät Google Kalenteriin"""
        sync_tasks_to_calendar()
        messagebox.showinfo("Synkronointi", "Tehtävät synkronoitu Google Kalenteriin onnistuneesti!")

# Käynnistetään käyttöliittymä
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
