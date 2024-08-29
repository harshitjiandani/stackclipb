import customtkinter as ctk
from tkinter import messagebox
import pyperclip


class ClipboardStack(ctk.CTk):
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

    def ask_max_stack_size(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Clipboard Stack")
        dialog.geometry("300x150")
        dialog.grab_set()

        label = ctk.CTkLabel(dialog, text="Enter the maximum number of items the clipboard can hold:", wraplength=250)
        label.pack(pady=(20, 10))

        size_var = ctk.StringVar(value="10")
        size_entry = ctk.CTkEntry(dialog, textvariable=size_var, width=200)
        size_entry.pack(pady=10)

        def confirm():
            try:
                size = int(size_var.get())
                if size > 0:
                    dialog.destroy()
                    self.max_stack_size = size
                else:
                    messagebox.showwarning("Invalid Input", "Please enter a valid number greater than 0.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid integer.")

        ok_button = ctk.CTkButton(dialog, text="OK", command=confirm)
        ok_button.pack(pady=10)

        self.wait_window(dialog)  

        return self.max_stack_size

    def create_widgets(self):
        listbox_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        listbox_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = ctk.CTkTextbox(listbox_frame, fg_color="#2e2e2e", text_color="#d4d4d4", font=("Segoe UI", 12))
        self.listbox.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<Double-1>", self.paste_clipboard_item)

        button_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        button_frame.pack(fill=ctk.X, padx=10, pady=(0, 10))

        clear_button = ctk.CTkButton(
            button_frame, text="Clear History", command=self.clear_history, fg_color="#444444", text_color="#d4d4d4"
        )
        clear_button.pack(side=ctk.LEFT, expand=True, padx=5)

        exit_button = ctk.CTkButton(
            button_frame, text="Exit", command=self.quit, fg_color="#444444", text_color="#d4d4d4"
        )
        exit_button.pack(side=ctk.RIGHT, expand=True, padx=5)

    def update_clipboard(self):
        try:
            cliptext = pyperclip.paste()
            if cliptext:
                if cliptext in self.clipboard_stack:
                    self.clipboard_stack.remove(cliptext)
                else:
                    if len(self.clipboard_stack) >= self.max_stack_size:
                        self.clipboard_stack.pop(0)
                self.clipboard_stack.append(cliptext)
                self.refresh_listbox()
            self.after(1000, self.update_clipboard)
        except Exception as e:
            print(f"Error: {e}")

    def refresh_listbox(self):
        self.listbox.delete("1.0", ctk.END)
        for idx, item in enumerate(reversed(self.clipboard_stack), 1):
            self.listbox.insert(ctk.END, f"{idx}. {item}\n{' ' * 40}\n")
    

    def paste_clipboard_item(self, event=None):
        try:
            selected_item = self.listbox.get("insert linestart", "insert lineend")
            if selected_item.strip():
                pyperclip.copy(selected_item.split('. ', 1)[-1].strip())
                print(f"Copied item to clipboard: {selected_item}")
        except Exception as e:
            print(f"Error: {e}")

    def clear_history(self):
        self.clipboard_stack = []
        self.refresh_listbox()

    def on_close(self):
        # Close the application
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("dark-blue") 
    app = ClipboardStack()
    app.mainloop()
