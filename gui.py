import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import time

# Assuming server.py, client.py, and logger.py are in the same directory
import server
import client
from logger import Logger

class FileTransferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Transfer Application")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        button_style = {
            "font": ("Inter", 10),
            "fg": "#333333",
            "bg": "#e1e1e1",
            "activebackground": "#c0c0c0",
            "width": 35,
            "height": 1,
            "relief": "raised",
            "bd": 1,
            "cursor": "hand2"
        }
        button_grid_options = {"pady": 5, "padx": 5}

        self.server_save_directory = None
        self.client_download_directory = None
        self.server_thread = None

        # --- GUI Layout using Grid ---
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=0) # Heading row
        self.root.rowconfigure(1, weight=0) # Buttons row
        self.root.rowconfigure(2, weight=1) # Log area row

        # --- Heading Label ---
        self.heading_label = tk.Label(self.root,
                                      text="Secure File Transfer", # Your desired heading text
                                      font=("Inter", 16, "bold"), # Larger, bold font for the heading
                                      bg="#f0f0f0", # Match root background
                                      fg="#2c3e50") # Darker text for contrast
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=15, padx=10, sticky="ew") # Placed at row 0

        # --- Buttons Frame ---
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.grid(row=1, column=0, columnspan=2, pady=5) # Moved to row 1

        # Row 0 (within button_frame, now effectively row 1 in root)
        self.select_server_dir_button = tk.Button(button_frame, text="1. Choose Folder for Received Files",
                                                 command=self.select_server_save_directory,
                                                 **button_style)
        self.select_server_dir_button.grid(row=0, column=0, **button_grid_options)

        self.client_download_dir_button = tk.Button(button_frame, text="2. Choose Client Download Folder",
                                                 command=self.set_client_download_directory,
                                                 **button_style)
        self.client_download_dir_button.grid(row=0, column=1, **button_grid_options)

        # Row 1 (within button_frame, now effectively row 2 in root)
        self.send_file_button = tk.Button(button_frame, text="3. Send File to Server",
                                          command=self.send_file_via_client,
                                          **button_style)
        self.send_file_button.grid(row=1, column=0, **button_grid_options)

        self.clear_log_button = tk.Button(button_frame, text="Clear Log Display",
                                          command=self.clear_log,
                                          **button_style)
        self.clear_log_button.grid(row=1, column=1, **button_grid_options)

        # Row 2 (within button_frame, now effectively row 3 in root)
        self.save_log_button = tk.Button(button_frame, text="Save Log (to Logger Folder)",
                                         command=self.save_log_to_file,
                                         **button_style)
        self.save_log_button.grid(row=2, column=0, columnspan=2, **button_grid_options)

        # --- Log Area ---
        self.logger = Logger(self.root)
        self.log_text = self.logger.get_widget()
        self.log_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew") # Moved to row 2

        # Initial setup and auto-start server
        self._check_initial_setup()
        self._auto_start_server()

    def _update_button_states(self):
        """Updates the enabled/disabled state of buttons based on server_running flag."""
        if os.path.exists(server.PUBLIC_KEY_FILE):
            self.send_file_button.config(state=tk.NORMAL)
        else:
            self.send_file_button.config(state=tk.DISABLED)

        self.client_download_dir_button.config(state=tk.NORMAL)
        self.save_log_button.config(state=tk.NORMAL)
        self.select_server_dir_button.config(state=tk.NORMAL)

    def _check_initial_setup(self):
        """Checks for crypto_utils and key files at startup."""
        self.logger.append_log("Performing initial setup checks...", "info")
        try:
            import crypto_utils
            self.logger.append_log("crypto_utils.py found.", "success")
        except ImportError:
            self.logger.append_log("[CRITICAL] 'crypto_utils.py' not found. Please ensure it's in the same directory.", "stderr")
            messagebox.showerror("Setup Error", "'crypto_utils.py' not found. Cannot proceed. Please place 'crypto_utils.py' in the same folder as this application.")
            self.send_file_button.config(state=tk.DISABLED)
            self.select_server_dir_button.config(state=tk.DISABLED)
            self.client_download_dir_button.config(state=tk.DISABLED)
            self.save_log_button.config(state=tk.DISABLED)
            return

        if not os.path.exists(server.PUBLIC_KEY_FILE):
            self.logger.append_log(f"'{server.PUBLIC_KEY_FILE}' not found. The server will generate keys on its first start.", "warning")
            self.send_file_button.config(state=tk.DISABLED)
            messagebox.showwarning("Key Warning", f"'{server.PUBLIC_KEY_FILE}' not found. The server will generate necessary encryption keys automatically when the application starts. You can then send files.")
        else:
            self.logger.append_log(f"'{server.PUBLIC_KEY_FILE}' found. Client can send files.", "success")
            self.send_file_button.config(state=tk.NORMAL)

        self.logger.append_log("Initial setup complete.", "info")
        self._update_button_states()

    def clear_log(self):
        """Clears the content of the log area using the Logger instance."""
        self.logger.clear_log()

    def save_log_to_file(self):
        """Saves the content of the log display to a timestamped file in a 'Logger' folder using the Logger instance."""
        self.logger.save_log_to_file()

    def select_server_save_directory(self):
        """Opens a dialog for the user to select a directory for the server to save received files."""
        directory = filedialog.askdirectory(title="Choose a folder for Server to save received files")
        if directory:
            self.server_save_directory = directory
            self.logger.append_log(f"Server save folder set to: {directory}", "info")
            messagebox.showinfo("Server Save Folder", f"Server will save received files in:\n{directory}")
        else:
            self.logger.append_log("Server save folder selection cancelled.", "warning")

    def set_client_download_directory(self):
        """
        Opens a dialog for the user to select a directory where the client
        would save received files (if client had receiving functionality).
        """
        directory = filedialog.askdirectory(title="Choose a folder for Client to download files")
        if directory:
            self.client_download_directory = directory
            self.logger.append_log(f"Client download folder set to: {directory}", "info")
            messagebox.showinfo("Client Download Folder",
                                f"Client would download files to (if receiving): \n{directory}\n\n"
                                "Note: The current client only SENDS files and does not have built-in receiving functionality.")
        else:
            self.logger.append_log("Client download folder selection cancelled.", "warning")

    def _auto_start_server(self):
        """Automatically starts the server when the GUI initializes."""
        self.logger.append_log("Automatically starting server in the background...", "info")
        self.server_thread = threading.Thread(target=server.start_server, args=(self.server_save_directory,), daemon=True)
        self.server_thread.start()
        self.root.after(500, self._check_server_status_after_start)

    def _check_server_status_after_start(self):
        """Checks server status after attempting to start it."""
        if server.server_running:
            self.logger.append_log("Server started successfully and is listening for incoming files.", "success")
            self._update_button_states()
        else:
            self.logger.append_log("[!] Server failed to start or stopped unexpectedly. Please check the log for errors.", "stderr")
            self._update_button_states()

    def send_file_via_client(self):
        """Prompts user to select a file and initiates file transfer via client."""
        if not os.path.exists(server.PUBLIC_KEY_FILE):
            self.logger.append_log(f"[!] Cannot send file: '{server.PUBLIC_KEY_FILE}' is missing. Please start the server first.", "stderr")
            messagebox.showerror("Error", "Server's public key is missing. Please start the server first to generate necessary encryption keys.")
            return

        self.logger.append_log("Opening file selection dialog...", "info")
        filepath = filedialog.askopenfilename(
            title="Select a file to send to the server",
            filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("PDF files", "*.pdf"), ("Image files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filepath:
            self.logger.append_log(f"Preparing to send file: {os.path.basename(filepath)}...", "info")
            self.send_file_button.config(state=tk.DISABLED)
            threading.Thread(target=self._perform_send_file, args=(filepath,), daemon=True).start()
        else:
            self.logger.append_log("File selection cancelled by user.", "warning")

    def _perform_send_file(self, filepath):
        """Internal function to be run in a thread for sending the file."""
        try:
            client.send_file(filepath)
            self.root.after(0, lambda: self.logger.append_log(f"File '{os.path.basename(filepath)}' transfer process initiated. Check log for server's confirmation.", "success"))
        except ConnectionRefusedError:
            self.root.after(0, lambda: self.logger.append_log(f"[!] Connection refused. Is the server running?", "stderr"))
            self.root.after(0, lambda: messagebox.showerror("Connection Error", "Could not connect to the server. Please ensure the server is running."))
        except Exception as e:
            self.root.after(0, lambda: self.logger.append_log(f"[!] Failed to send file '{os.path.basename(filepath)}': {e}", "stderr"))
            self.root.after(0, lambda: messagebox.showerror("File Send Error", f"An error occurred while sending the file: {e}"))
        finally:
            self.root.after(0, self._update_button_states)

    def _on_closing(self):
        """Handler for the window close event."""
        if server.server_running:
            self.logger.append_log("Stopping server before exiting application...", "info")
            server.stop_server()
            self.root.after(1000, self.root.destroy)
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferGUI(root)
    root.mainloop()