import tkinter as tk
from tkinter import messagebox

def show_message(text):
    root = tk.Tk()
    root.title("Scalable MessageBox")

    text_widget = tk.Text(root, wrap=tk.WORD, width=100, height=10)  # Adjusted width and height
    text_widget.pack(padx=10, pady=10)

    text_widget.insert(tk.END, text)

    def close_window():
        root.destroy()

    ok_button = tk.Button(root, text="OK", command=close_window)
    ok_button.pack(pady=10)

    root.mainloop()

# Example usage:
message_text = "        08:30-10:30     10:30-12:30     12:30-14:30     14:30-16:30     16:30-18:30\n" + \
               "Pzt             113             113             -               -               -\n" + \
               "Sali            113             -               -               -               -\n" + \
               "Crs             -               -               -               -               -\n" + \
               "Prs             -               -               -               -               -\n" + \
               "Cuma            -               -               -               -               -"

show_message(message_text)
