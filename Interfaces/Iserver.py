# Iserver.py

from abc import ABC, abstractmethod

class IServer(ABC):
    """
    Abstract Base Class (ABC) defining the interface for a server.
    Any class implementing this interface must provide concrete
    implementations for the defined abstract methods.
    """

    @abstractmethod
    def start_server(self, save_directory=None):
        """
        Abstract method to start the server.

        Args:
            save_directory (str, optional): The directory where received files will be saved.
                                            If None, a default location should be used.
        """
        pass

    @abstractmethod
    def stop_server(self):
        """
        Abstract method to stop the server.
        """
        pass

