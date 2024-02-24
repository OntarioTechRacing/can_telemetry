"""CAN bus connection class for bus management."""

import threading

import can

from notifier_class import CustomNotifier


class CANBusManager:
    def __init__(
        self,
        channel: str = "virtual",
        bus_type: str = "virtual",
        filters: list[dict[str, int | bool]] = None,
    ):
        """General CANBusManager initialization.

        Args:
            channel: python.can.Bus() channel parameter.
            bus_type: python.can.Bus() bus type parameter.
            filters: python.can.Bus() filters parameter.
        """
        self.__channel = channel
        self.__bus_type = bus_type
        self.__filters = filters  # List of CAN filter dictionaries
        self.__notifier = CustomNotifier()
        self.__running = False
        self.__reader_thread = None  # Initialized later.
        self.__bus = None  # Initialized later.

    def is_running(self) -> bool:
        """Get state of CAN bus.

        Returns:
            True for running, False for not running.
        """
        return self.__running

    def start(self):
        """Start the CAN bus."""
        filter_print = (
            "no filters"
            if self.__filters is None
            else f"filters {self.__filters}"
        )
        print(f"CANBusManager starting on {self.__bus} with {filter_print}.")

        # Initialize the CAN bus.
        self.__bus = can.interface.Bus(
            channel=self.__channel,
            bustype=self.__bus_type,
            can_filters=self.__filters,
        )

        # Start the CAN reader in a daemon thread.
        self.__reader_thread = threading.Thread(
            target=self.can_reader, daemon=True
        )
        self.__reader_thread.start()
        self.__running = True

    def stop(self):
        """Stop the CAN bus."""
        if self.__running:
            self.__running = False
            self.__bus.shutdown()
            print("CANBusManager stopped.")

    def simulate(self, messages: list[can.Message]):
        """Start the CAN bus and run simulated CAN bus messages.

        Args:
            messages: Messages to simulate Rx.

        Notes:
            Messages are scheduled via timestamp.
        """
        # Start standard bus.
        self.start()
        print(f"CANBusManager Notifier simulation starting...")

        # Begin (threaded) notifier scheduled message simulation function.
        self.__notifier.simulate(messages=messages)

    def add_listener(self, listener):
        """Add a listener Callable to Notifier.

        Args:
            listener: Listener to add to Notifier.
        """
        self.__notifier.add_listener(listener)

    def can_reader(self):
        """Read messages from the CAN bus and notify listeners."""
        while self.__running:
            msg = self.__bus.recv(timeout=1.0)
            # TODO: A minium timeout is hardcoded here. A better solution might
            #  be possible.
            if msg:
                self.__notifier.notify_listeners(msg)
