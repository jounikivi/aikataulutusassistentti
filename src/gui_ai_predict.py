from __future__ import annotations

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

try:
    from .google_auth import (
        GoogleAuthError,
        get_credentials,
        get_current_user_email,
        is_authenticated,
        load_user_session,
        logout_google,
    )
    from .google_calendar_sync import delete_task_event, sync_tasks_to_calendar
    from .smart_scheduler_ml import recommend_schedule
    from .task_manager import load_tasks, save_tasks
    from .task_utils import DEFAULT_DURATION_MINUTES, format_deadline, parse_deadline
except ImportError:
    from google_auth import (
        GoogleAuthError,
        get_credentials,
        get_current_user_email,
        is_authenticated,
        load_user_session,
        logout_google,
    )
    from google_calendar_sync import delete_task_event, sync_tasks_to_calendar
    from smart_scheduler_ml import recommend_schedule
    from task_manager import load_tasks, save_tasks
    from task_utils import DEFAULT_DURATION_MINUTES, format_deadline, parse_deadline


class TaskManagerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Älykäs Aikataulutusassistentti")
        self.root.geometry("980x560")
        self.root.configure(bg="#f4f6f8")
        self.tasks: list[dict] = []

        self.user_label = ttk.Label(root, text="Google ei ole yhdistetty", foreground="red")
        self.user_label.pack(pady=(12, 6))

        top_frame = ttk.Frame(root)
        top_frame.pack(pady=4)

        ttk.Button(top_frame, text="Kirjaudu Googleen", command=self.login).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(top_frame, text="Kirjaudu ulos", command=self.logout).grid(
            row=0, column=1, padx=6
        )

        self.ai_label = ttk.Label(
            root,
            text="AI-suositus: lisää tai valitse tehtävä nähdäksesi aloitusaikaehdotuksen.",
            justify="left",
            wraplength=900,
        )
        self.ai_label.pack(padx=16, pady=(10, 8), anchor="w")

        self.tree = ttk.Treeview(
            root,
            columns=("Title", "Deadline", "Priority", "Duration", "Status"),
            show="headings",
            height=14,
        )
        self.tree.heading("Title", text="Tehtävä", anchor="center")
        self.tree.heading("Deadline", text="Deadline", anchor="center")
        self.tree.heading("Priority", text="Tärkeys", anchor="center")
        self.tree.heading("Duration", text="Oma kestoarvio", anchor="center")
        self.tree.heading("Status", text="Tila", anchor="center")
        self.tree.column("Title", anchor="w", width=280)
        self.tree.column("Deadline", anchor="center", width=150)
        self.tree.column("Priority", anchor="center", width=80)
        self.tree.column("Duration", anchor="center", width=130)
        self.tree.column("Status", anchor="center", width=100)
        self.tree.pack(fill="both", expand=True, padx=16, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.update_ai_hint)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=(4, 14))

        ttk.Button(button_frame, text="Lisää tehtävä", command=self.add_task).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(button_frame, text="Muokkaa tehtävää", command=self.edit_task).grid(
            row=0, column=1, padx=6
        )
        ttk.Button(button_frame, text="Poista tehtävä", command=self.delete_task).grid(
            row=0, column=2, padx=6
        )
        self.sync_google_btn = ttk.Button(
            button_frame, text="Synkronoi Google Kalenteriin", command=self.sync_google
        )
        self.sync_google_btn.grid(row=0, column=3, padx=6)

        self.check_login_status()
        self.load_task_data()

    def check_login_status(self) -> None:
        if is_authenticated():
            session = load_user_session()
            email = session.get("email") or get_current_user_email()
            if email != "default_user":
                text = f"Google yhdistetty: {email}"
            else:
                text = "Google yhdistetty"
            self.user_label.config(text=text, foreground="green")
            self.sync_google_btn.config(state=tk.NORMAL)
        else:
            self.user_label.config(
                text="Google ei ole yhdistetty. Voit silti hallita tehtäviä paikallisesti.",
                foreground="red",
            )
            self.sync_google_btn.config(state=tk.DISABLED)

    def clear_task_list(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_task_data(self, select_index: int | None = None) -> None:
        self.tasks = load_tasks()
        self.clear_task_list()

        for index, task in enumerate(self.tasks):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task["title"],
                    task["deadline"],
                    task["priority"],
                    f"{task['estimated_duration']} min",
                    task["status"],
                ),
            )

        if select_index is not None and str(select_index) in self.tree.get_children():
            self.tree.selection_set(str(select_index))
            self.tree.focus(str(select_index))

        self.update_ai_hint()

    def get_selected_task(self) -> tuple[int | None, dict | None]:
        selection = self.tree.selection()
        if not selection:
            return None, None

        index = int(selection[0])
        if index >= len(self.tasks):
            return None, None

        return index, self.tasks[index]

    def update_ai_hint(self, _event=None) -> None:
        if not self.tasks:
            self.ai_label.config(
                text="AI-suositus: lisää tehtävä, niin sovellus arvioi sopivan aloitusajan."
            )
            return

        _, selected_task = self.get_selected_task()
        if selected_task is None:
            pending_tasks = [task for task in self.tasks if task["status"] != "completed"]
            selected_task = min(
                pending_tasks or self.tasks,
                key=lambda task: parse_deadline(task["deadline"]),
            )
            intro = f"Seuraavaksi kiireisin tehtävä on '{selected_task['title']}'."
        else:
            intro = f"Valittu tehtävä on '{selected_task['title']}'."

        recommendation = recommend_schedule(selected_task)
        self.ai_label.config(
            text=(
                f"AI-suositus: {intro} Aloita noin {recommendation['recommended_start']} "
                f"ja varaa tehtävälle noin {recommendation['predicted_duration']} minuuttia "
                f"ennen deadlinea {selected_task['deadline']}."
            )
        )

    def login(self) -> None:
        try:
            get_credentials()
        except (GoogleAuthError, FileNotFoundError) as exc:
            messagebox.showerror("Kirjautuminen epäonnistui", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Kirjautuminen epäonnistui", str(exc))
            return

        self.check_login_status()
        self.load_task_data()
        messagebox.showinfo("Kirjautuminen", "Google-yhteys muodostettiin onnistuneesti.")

    def logout(self) -> None:
        logout_google()
        self.check_login_status()
        self.load_task_data()
        messagebox.showinfo("Uloskirjautuminen", "Google-yhteys poistettiin.")

    def add_task(self) -> None:
        self.open_task_editor()

    def edit_task(self) -> None:
        index, task = self.get_selected_task()
        if task is None:
            messagebox.showerror("Muokkaus", "Valitse ensin muokattava tehtävä.")
            return

        self.open_task_editor(task=task, index=index)

    def open_task_editor(self, task: dict | None = None, index: int | None = None) -> None:
        existing_task = task or {
            "title": "",
            "deadline": format_deadline(
                (datetime.now() + timedelta(days=1)).replace(minute=0, second=0, microsecond=0)
            ),
            "priority": 3,
            "estimated_duration": DEFAULT_DURATION_MINUTES,
            "status": "pending",
        }

        editor = tk.Toplevel(self.root)
        editor.title("Muokkaa tehtävää" if task else "Lisää tehtävä")
        editor.resizable(False, False)

        title_var = tk.StringVar(value=existing_task["title"])
        deadline_var = tk.StringVar(value=existing_task["deadline"])
        priority_var = tk.StringVar(value=str(existing_task["priority"]))
        duration_var = tk.StringVar(value=str(existing_task["estimated_duration"]))
        status_var = tk.StringVar(value=existing_task.get("status", "pending"))

        fields = [
            ("Tehtävän nimi", ttk.Entry(editor, textvariable=title_var, width=36)),
            ("Deadline (YYYY-MM-DD HH:MM)", ttk.Entry(editor, textvariable=deadline_var, width=36)),
            (
                "Tärkeysaste (1-5)",
                ttk.Combobox(
                    editor,
                    textvariable=priority_var,
                    values=["1", "2", "3", "4", "5"],
                    state="readonly",
                    width=33,
                ),
            ),
            ("Oma kestoarvio (min)", ttk.Entry(editor, textvariable=duration_var, width=36)),
            (
                "Tila",
                ttk.Combobox(
                    editor,
                    textvariable=status_var,
                    values=["pending", "completed"],
                    state="readonly",
                    width=33,
                ),
            ),
        ]

        for row_index, (label_text, widget) in enumerate(fields):
            ttk.Label(editor, text=label_text).grid(
                row=row_index, column=0, sticky="w", padx=12, pady=6
            )
            widget.grid(row=row_index, column=1, padx=12, pady=6)

        def save_current_task() -> None:
            title = title_var.get().strip()
            if not title:
                messagebox.showerror("Tallennus", "Tehtävällä täytyy olla nimi.")
                return

            try:
                deadline = format_deadline(parse_deadline(deadline_var.get().strip()))
                priority = int(priority_var.get())
                estimated_duration = int(duration_var.get())
            except ValueError:
                messagebox.showerror(
                    "Tallennus",
                    "Tarkista deadline-muoto ja että tärkeys sekä kesto ovat numeroita.",
                )
                return

            task_data = {
                "title": title,
                "deadline": deadline,
                "priority": priority,
                "estimated_duration": estimated_duration,
                "difficulty": priority,
                "status": status_var.get(),
            }

            if existing_task.get("calendar_event_id"):
                task_data["calendar_event_id"] = existing_task["calendar_event_id"]

            tasks = load_tasks()
            if index is None:
                tasks.append(task_data)
                new_index = len(tasks) - 1
            else:
                tasks[index] = task_data
                new_index = index

            save_tasks(tasks)
            self.load_task_data(select_index=new_index)
            editor.destroy()

        ttk.Button(editor, text="Tallenna", command=save_current_task).grid(
            row=len(fields), column=1, sticky="e", padx=12, pady=(8, 12)
        )

    def delete_task(self) -> None:
        index, task = self.get_selected_task()
        if task is None:
            messagebox.showerror("Poisto", "Valitse ensin poistettava tehtävä.")
            return

        confirmed = messagebox.askyesno(
            "Poista tehtävä",
            f"Haluatko varmasti poistaa tehtävän '{task['title']}'?",
        )
        if not confirmed:
            return

        calendar_deleted = False
        if task.get("calendar_event_id"):
            calendar_deleted = delete_task_event(task)

        tasks = load_tasks()
        tasks.pop(index)
        save_tasks(tasks)
        self.load_task_data()

        if task.get("calendar_event_id") and not calendar_deleted:
            messagebox.showwarning(
                "Poistettu paikallisesti",
                "Tehtävä poistettiin paikallisesti, mutta vastaava Google Calendar -tapahtuma voi silti olla olemassa.",
            )
            return

        messagebox.showinfo("Poistettu", "Tehtävä poistettiin.")

    def sync_google(self) -> None:
        try:
            result = sync_tasks_to_calendar()
        except (GoogleAuthError, FileNotFoundError) as exc:
            messagebox.showerror("Synkronointi epäonnistui", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Synkronointi epäonnistui", str(exc))
            return

        self.load_task_data()
        messagebox.showinfo(
            "Synkronointi valmis",
            (
                f"Luotiin {result['created']} tapahtumaa, päivitettiin {result['updated']} "
                f"ja ohitettiin {result['skipped']} valmista tehtävää."
            ),
        )


def main() -> None:
    root = tk.Tk()
    TaskManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
