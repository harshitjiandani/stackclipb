import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import pyperclip
from tkinter import *

class ClipboardStack(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Stack")
        self.geometry("400x400")
        self.max_stack_size = self.ask_max_stack_size()
        if self.max_stack_size is None:
            self.quit()
            return

        self.clipboard_stack = [] 

        self.create_widgets()
        self.update_clipboard()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.style()

    def ask_max_stack_size(self):
        while True:
            try:
                size = simpledialog.askinteger("Clipboard Stack", "Enter the maximum number of items the clipboard can hold:", minvalue=1, initialvalue=10)
                if size is not None and size > 0:
                    return size
                else:
                    messagebox.showwarning("Invalid Input", "Please enter a valid number greater than 0.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid integer.")

    def create_widgets(self):
        listbox_frame = tk.Frame(self, bg="#1e1e1e", bd=0)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, bg="#2e2e2e", fg="#d4d4d4", font=("Segoe UI", 12), bd=0, highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<Double-1>", self.paste_clipboard_item)

        menubar = Menu(self, bg="#333333", fg="#d4d4d4", activebackground="#555555")
        options_menu = Menu(menubar, tearoff=0, bg="#2e2e2e", fg="#d4d4d4", activebackground="#555555")
        options_menu.add_command(label="Clear History", command=self.clear_history, background="#444444", foreground="#d4d4d4")
        options_menu.add_command(label="Exit", command=self.quit, background="#444444", foreground="#d4d4d4")
        menubar.add_cascade(label="Options", menu=options_menu)
        self.config(menu=menubar, bg="#1e1e1e")

    def update_clipboard(self):
        try:
            cliptext = pyperclip.paste()
            if cliptext:
                if cliptext in self.clipboard_stack:
                    self.clipboard_stack.remove(cliptext)
                else:
                    if len(self.clipboard_stack) >= self.max_stack_size:
                        self.clipboard_stack.pop(0)
                # Add the item to the top of the stack
                self.clipboard_stack.append(cliptext)
                self.refresh_listbox()
            self.after(1000, self.update_clipboard)
        except Exception as e:
            print(f"Error: {e}")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in reversed(self.clipboard_stack):
            self.listbox.insert(tk.END, item)

    def paste_clipboard_item(self, event=None):
        try:
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_item = self.listbox.get(selected_index)
                pyperclip.copy(selected_item)
                print(f"Copied item to clipboard: {selected_item}")
        except Exception as e:
            print(f"Error: {e}")

    def paste_top_clipboard_item(self, event=None):
        try:
            if self.clipboard_stack:
                print("Clipboard stack is not empty.")
                top_item = self.clipboard_stack.pop()
                print("Top item:", top_item)
                pyperclip.copy(top_item)
                print("Copied top item to clipboard.")
                self.refresh_listbox()
            else:
                print("Clipboard stack is empty.")
        except Exception as e:
            print(f"Error: {e}")

    def clear_history(self):
        self.clipboard_stack = []
        self.refresh_listbox()

    def on_close(self):
        self.destroy()  

    def style(self):

        pass

if __name__ == "__main__":
    app = ClipboardStack()
    app.mainloop()
