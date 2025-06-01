# logger.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
import datetime

# Custom class to redirect stdout/stderr to a Tkinter Text widget
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str_val):
        self.widget.configure(state='normal') # Enable editing
        self.widget.insert(tk.END, str_val, self.tag)
        self.widget.see(tk.END) # Scroll to the end
        self.widget.configure(state='disabled') # Disable editing
        self.widget.update_idletasks() # Force update

    def flush(self):
        pass # Required for file-like objects

class Logger:
    """
    A centralized logging class that redirects stdout/stderr to a Tkinter
    ScrolledText widget and provides functionality to save the log to a file.
    """
    def __init__(self, parent_frame):
        self.log_text = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, state='disabled',
                                                 font=("Consolas", 10), bg="#fcfcfc", fg="#333", bd=2, relief="sunken")

        # Configure tags for different message types (optional, for coloring)
        self.log_text.tag_config("stdout", foreground="#0056b3") # Darker blue for stdout
        self.log_text.tag_config("stderr", foreground="#cc0000") # Red for errors
        self.log_text.tag_config("info", foreground="#007bff") # Bright blue for general info
        self.log_text.tag_config("success", foreground="#28a745") # Green for success
        self.log_text.tag_config("warning", foreground="#ffc107") # Yellow for warnings

        # Redirect stdout and stderr to this logger's text widget
        sys.stdout = TextRedirector(self.log_text, "stdout")
        sys.stderr = TextRedirector(self.log_text, "stderr")

    def get_widget(self):
        """Returns the ScrolledText widget for placement in the GUI."""
        return self.log_text

    def append_log(self, message, tag="info"):
        """Appends a message to the log area with a specific tag and timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, formatted_message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        self.log_text.update_idletasks()

    def clear_log(self):
        """Clears the content of the log area."""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.append_log("Log display cleared.", "info")

    def save_log_to_file(self):
        """Saves the content of the log display to a timestamped file in a 'Logger' folder."""
        log_folder = "Logger"
        # Create the Logger folder if it doesn't exist
        try:
            os.makedirs(log_folder, exist_ok=True)
        except Exception as e:
            self.append_log(f"[!] Error creating Logger folder: {e}", "stderr")
            messagebox.showerror("Folder Creation Error", f"Failed to create 'Logger' folder: {e}")
            return

        # Generate a unique filename with a timestamp
        timestamp_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_log.txt")
        full_log_path = os.path.join(log_folder, timestamp_filename)

        try:
            log_content = self.log_text.get(1.0, tk.END) # Get all content from the log
            with open(full_log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            self.append_log(f"Log saved successfully to: {full_log_path}", "success")
            messagebox.showinfo("Log Saved", f"Log content saved to:\n{full_log_path}")
        except Exception as e:
            self.append_log(f"[!] Error saving log to file: {e}", "stderr")
            messagebox.showerror("Save Log Error", f"Failed to save log: {e}")

