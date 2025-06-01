# Ilogger.py

from abc import ABC, abstractmethod
import tkinter as tk # Import tkinter for the widget type hint

class ILogger(ABC):
    """
    Abstract Base Class (ABC) defining the interface for a logging component.
    Any class implementing this interface must provide concrete
    implementations for the defined abstract methods.
    """

    @abstractmethod
    def get_widget(self) -> tk.Widget:
        """
        Abstract method to return the Tkinter widget used for displaying logs.

        Returns:
            tk.Widget: The Tkinter widget (e.g., ScrolledText) where logs are displayed.
        """
        pass

    @abstractmethod
    def append_log(self, message: str, tag: str = "info"):
        """
        Abstract method to append a timestamped message to the log display.

        Args:
            message (str): The log message to append.
            tag (str, optional): A tag for styling the message (e.g., "info", "warning", "stderr").
                                 Defaults to "info".
        """
        pass

    @abstractmethod
    def clear_log(self):
        """
        Abstract method to clear all content from the log display.
        """
        pass

    @abstractmethod
    def save_log_to_file(self):
        """
        Abstract method to save the current log display content to a timestamped file
        within a 'Logger' folder in the application's directory.
        """
        pass

