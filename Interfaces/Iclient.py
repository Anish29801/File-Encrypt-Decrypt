# Iclient.py

from abc import ABC, abstractmethod

class IClient(ABC):
    """
    Abstract Base Class (ABC) defining the interface for a client.
    Any class implementing this interface must provide concrete
    implementations for the defined abstract methods.
    """

    @abstractmethod
    def send_file(self, file_path):
        """
        Abstract method to send a file to the server.

        Args:
            file_path (str): The path to the file to be sent.
        """
        pass

