import json
import os
import tkinter as tk
import customtkinter as ctk

# -----------------------------
# Basic configuration
# -----------------------------

APP_TITLE = "Modern To-Do List"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500

# Color variables (easy to change later)
PRIMARY_COLOR = "#8B5CF6"
ACCENT_COLOR = "#7C3AED"
DELETE_RED = "#E74C3C"
DELETE_RED_HOVER = "#C0392B"
COMPLETED_TEXT_COLOR = "#A0A0A0"

# Path to tasks.json in same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

# Will store all task objects (one dict per task)
tasks = []  # Each item: {"frame", "var", "checkbox", "delete_btn", "text"}


# -----------------------------
# Utility functions
# -----------------------------

def center_window(window, width, height):
    """Center the main window on the screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


def save_tasks():
    """Save all tasks (text + completed state) to tasks.json."""
    data = []
    for task in tasks:
        data.append({
            "text": task["text"],
            "completed": bool(task["var"].get())
        })

    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving tasks: {e}")


def load_tasks():
    """
    Load tasks from tasks.json (if it exists).
    Creates task widgets for each loaded task.
    """
    if not os.path.exists(TASKS_FILE):
        return

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return

    if not isinstance(data, list):
        return

    for item in data:
        text = item.get("text", "")
        completed = item.get("completed", False)
        if text.strip():
            create_task_widget(text, completed)


def update_task_appearance(task_dict):
    """
    Visually update a task based on whether it's completed or not:
    - Apply strikethrough
    - Change text color
    """
    completed = bool(task_dict["var"].get())
    checkbox = task_dict["checkbox"]

    # Always use a CustomTkinter font object for CTk widgets
    font_obj = ctk.CTkFont(size=14)

    # Apply or remove strikethrough using the CTkFont
    if completed:
        font_obj.configure(overstrike=True)
        checkbox.configure(text_color=COMPLETED_TEXT_COLOR, font=font_obj)
    else:
        font_obj.configure(overstrike=False)
        # None lets CustomTkinter handle the default text color for the theme
        checkbox.configure(text_color=("black", "white"))


def toggle_complete(task_dict):
    """Called when a task checkbox is clicked."""
    update_task_appearance(task_dict)
    save_tasks()


def delete_task(task_dict):
    """Delete a task from the UI and from memory, then save."""
    task_dict["frame"].destroy()
    if task_dict in tasks:
        tasks.remove(task_dict)
    save_tasks()


def create_task_widget(text, completed=False):
    """
    Create a visual row for a single task.
    Each row contains:
    - A checkbox with the task text
    - A 'Delete' button
    """
    # This frame holds the checkbox and delete button
    row = ctk.CTkFrame(task_list_frame, fg_color="transparent")
    row.pack(fill="x", pady=4, padx=4)

    # BooleanVar stores whether the task is completed or not
    var = tk.BooleanVar(value=completed)

    # Task dictionary is created here so callbacks can reference it
    task_dict = {}

    # Checkbox for completion
    checkbox = ctk.CTkCheckBox(
        row,
        text=text,
        variable=var,
        command=lambda: toggle_complete(task_dict),
        fg_color=PRIMARY_COLOR,
        hover_color=ACCENT_COLOR,
        border_width=2
    )
    checkbox.pack(side="left", fill="x", expand=True)

    # Delete button
    delete_btn = ctk.CTkButton(
        row,
        text="Delete",
        width=60,
        fg_color=DELETE_RED,
        hover_color=DELETE_RED_HOVER,
        command=lambda: delete_task(task_dict)
    )
    delete_btn.pack(side="right", padx=(8, 0))

    # Store everything in the task dict
    task_dict.update({
        "frame": row,
        "var": var,
        "checkbox": checkbox,
        "delete_btn": delete_btn,
        "text": text
    })

    # Keep track in the global list
    tasks.append(task_dict)

    # Apply initial appearance (handles completed tasks on load)
    update_task_appearance(task_dict)


def add_task(event=None):
    """
    Add a new task using the text from the entry.
    This function is called by the Add button and the Enter key.
    """
    text = task_entry.get().strip()
    if not text:
        return

    create_task_widget(text, completed=False)
    task_entry.delete(0, "end")
    save_tasks()


def toggle_theme():
    """
    Switch between Light Mode and Dark Mode.
    Also update the button text accordingly.
    """
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        theme_button.configure(text="Dark Mode")
    else:
        ctk.set_appearance_mode("Dark")
        theme_button.configure(text="Light Mode")


# -----------------------------
# Main application
# -----------------------------

if __name__ == "__main__":
    # Initial appearance and color theme
    ctk.set_appearance_mode("Dark")        # Start in Dark mode
    ctk.set_default_color_theme("blue")    # Built-in theme

    # Create main window
    root = ctk.CTk()
    root.title(APP_TITLE)
    root.resizable(False, False)
    center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Main outer frame for overall padding
    main_frame = ctk.CTkFrame(root, corner_radius=12)
    main_frame.pack(fill="both", expand=True, padx=12, pady=12)

    # ---------- Top Section: Title + Theme Toggle ----------
    top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    top_frame.pack(fill="x", pady=(4, 12))

    title_label = ctk.CTkLabel(
        top_frame,
        text=APP_TITLE,
        font=ctk.CTkFont(size=22, weight="bold")
    )
    title_label.pack(side="left", padx=(4, 0))

    theme_button = ctk.CTkButton(
        top_frame,
        text="Light Mode",  # Clicking switches to light, so label is current "action"
        width=90,
        fg_color=PRIMARY_COLOR,
        hover_color=ACCENT_COLOR,
        command=toggle_theme
    )
    theme_button.pack(side="right", padx=(0, 4))

    # ---------- Middle Section: Task Entry + Add Button ----------
    middle_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    middle_frame.pack(fill="x", pady=(0, 12))

    task_entry = ctk.CTkEntry(
        middle_frame,
        placeholder_text="Type a new task...",
        height=32
    )
    task_entry.pack(side="left", fill="x", expand=True, padx=(4, 6))

    add_button = ctk.CTkButton(
        middle_frame,
        text="Add Task",
        width=80,
        fg_color=PRIMARY_COLOR,
        hover_color=ACCENT_COLOR,
        command=add_task
    )
    add_button.pack(side="right", padx=(0, 4))

    # Pressing Enter in the entry will add the task
    task_entry.bind("<Return>", add_task)

    # ---------- Task Section: Scrollable List ----------
    task_list_frame = ctk.CTkScrollableFrame(
        main_frame,
        label_text="Tasks",
        height=330   # Roughly fits inside 400x500 window
    )
    task_list_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))

    # Load tasks from JSON (if any)
    load_tasks()

    # Start the GUI event loop
    root.mainloop()

