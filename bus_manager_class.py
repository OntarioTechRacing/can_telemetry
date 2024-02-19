"""Classes for managing can package Bus connections and Notifiers.

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

    @abstractmethod
    def connection(self, bit_rate: int) -> BusABC:
        """Get Bus connection of the selected CANBusManager.

        Args:
            bit_rate: Bit rate of requested bus connection.

        Returns:
            BusABC object of bus connection.
        """
        pass

    @abstractmethod
    def is_valid_connection(self, bit_rate: int) -> bool:
        """Test connection with error handling for connection status.

        Args:
            bit_rate: Bit rate of requested bus connection.

        Returns:
            True for valid connection, False for invalid connection.

        Notes:
            Use python's with statement to open the Bus connection. If you are
            developing on an edge case and cannot use one, make sure to call
            BusABC_object.shutdown().
        """
        # try:
        #     connection = self.connection(bit_rate)
        #     connection.shutdown()
        # except interfaces.x.x.SomeInterfaceInitializationError:
        #     return False
        # except Exception as e:
        #     raise e
        # return True
        pass

    @abstractmethod
    def run_notifier(
        self, bit_rate: int, listener_func: Callable[[Message], any]
    ):
        """Run non-blocking synchronous notifier and listener thread.

        Args:
            bit_rate: Bit rate of requested bus connection.
            listener_func: Listener functions utilized by notifier.

        Notes:
            Careful consideration of practice required to prevent infinite
            thread running due to improper listener to close the thread.

            Use python's with statement to open the Bus connection. If you are
            developing on an edge case and cannot use one, make sure to call
            BusABC_object.shutdown().

            Make sure to account time for the Notifier to run.
        """
        # with self.connection(bit_rate) as b:
        #     Notifier(b, [listener_func])
        #
        #     # ...
        #
        #     time.sleep(1.0)  # Allow time for Notifier to run.
        pass


class PeakCANBasic(BusManager):
    def connection(self, bit_rate: int) -> BusABC:
        return Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate=bit_rate)

    def is_valid_connection(self, bit_rate: int) -> bool:
        try:
            connection = self.connection(bit_rate)
            connection.shutdown()
        except interfaces.pcan.pcan.PcanCanInitializationError:
            return False
        except Exception as e:
            raise e
        return True

    def run_notifier(
        self, bit_rate: int, listener_func: Callable[[Message], any]
    ):
        with self.connection(bit_rate) as b:
            Notifier(b, [listener_func])

            time.sleep(1.0)  # Allow time for Notifier to run.
