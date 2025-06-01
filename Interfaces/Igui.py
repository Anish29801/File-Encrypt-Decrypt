# Igui.py

from abc import ABC, abstractmethod
import tkinter as tk # For type hinting Tkinter widgets

class IGUI(ABC):
    """
    Abstract Base Class (ABC) defining the interface for the Secure File Transfer GUI.
    Any concrete GUI class implementing this interface must provide
    implementations for the defined abstract methods.
    """

    @abstractmethod
    def _update_button_states(self):
        """
        Abstract method to update the enabled/disabled state of GUI buttons
        based on the application's current state (e.g., server running status,
        presence of crypto keys).
        """
        pass

    @abstractmethod
    def _check_initial_setup(self):
        """
        Abstract method to perform initial checks at application startup,
        such as verifying the presence of necessary cryptographic utility files
        and server keys.
        """
        pass

    @abstractmethod
    def clear_log(self):
        """
        Abstract method to clear all messages from the log display area.
        """
        pass

    @abstractmethod
    def save_log_to_file(self):
        """
        Abstract method to save the current content of the log display
        to a timestamped file in a designated 'Logger' folder.
        """
        pass

    @abstractmethod
    def select_server_save_directory(self):
        """
        Abstract method to open a file dialog, allowing the user to select
        a directory where the server will save received files.
        """
        pass

    @abstractmethod
    def set_client_download_directory(self):
        """
        Abstract method to open a file dialog, allowing the user to select
        a directory where the client would save received files (if client
        had receiving functionality).
        """
        pass

    @abstractmethod
    def _auto_start_server(self):
        """
        Abstract method to automatically start the server component
        in a separate thread when the GUI application initializes.
        """
        pass

    @abstractmethod
    def _check_server_status_after_start(self):
        """
        Abstract method to check the server's status shortly after
        an attempt to start it, and update the GUI accordingly.
        """
        pass

    @abstractmethod
    def send_file_via_client(self):
        """
        Abstract method to initiate the process of selecting a file
        and sending it to the server using the client component.
        """
        pass

    @abstractmethod
    def _perform_send_file(self, filepath: str):
        """
        Abstract method to encapsulate the actual file sending logic
        to be executed in a separate thread, preventing GUI freezes.

        Args:
            filepath (str): The path to the file to be sent.
        """
        pass

    @abstractmethod
    def _on_closing(self):
        """
        Abstract method to handle the application's window close event,
        ensuring a graceful shutdown of background processes like the server.
        """
        pass

