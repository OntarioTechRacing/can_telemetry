"""Classes for managing can package Bus connections.

All low level BusABC object calls and thread management should be handled here.
"""

import time
from abc import *
from collections.abc import Callable

from can import *


class BusManager(ABC):
    """CAN bus hardware manager super class.

    Defines general structure of all CAN managers.
    """

    def __init__(self, bit_rate: int):
        """Class initialization.

        Args:
            bit_rate: Bit rate of requested bus connection.
        """
        self.bit_rate = bit_rate

    @abstractmethod
    def connection(self) -> BusABC:
        """Get Bus connection of the selected CANBusManager.


        Returns:
            BusABC object of bus connection.
        """
        pass

    @abstractmethod
    def is_valid_connection(self) -> bool:
        """Test connection with error handling for connection status.

        Returns:
            True for valid connection, False for invalid connection.

        Notes:
            Use python's with statement to open the Bus connection. If you are
            developing on an edge case and cannot use one, make sure to call
            BusABC_object.shutdown().
        """
        # try:
        #     connection = self.connection()
        #     connection.shutdown()
        # except interfaces.x.x.SomeInterfaceInitializationError:
        #     return False
        # except Exception as e:
        #     raise e
        # return True
        pass


class Virtual(BusManager):
    """Virtual CAN bus manager (for local virtual simulation)."""

    def connection(self) -> BusABC:
        return Bus("virtual", bustype="virtual")

    def is_valid_connection(self) -> bool:
        try:
            connection = self.connection()
            connection.shutdown()
        except Exception as e:
            raise e
        return True


class PeakCANBasic(BusManager):
    """PEAK-CAN USB CAN bus manager."""

    def connection(self) -> BusABC:
        return Bus(
            bustype="pcan", channel="PCAN_USBBUS1", bitrate=self.bit_rate
        )

    def is_valid_connection(self) -> bool:
        try:
            connection = self.connection()
            connection.shutdown()
        except interfaces.pcan.pcan.PcanCanInitializationError:
            return False
        except Exception as e:
            raise e
        return True
