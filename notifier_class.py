"""Notifier class and logic for handling custom dynamic Notifiers."""

import sched
import threading
import time
from typing import Callable

from can import Message


class CustomNotifier:
    """CustomNotifier of dynamic notifier with listener management."""

    def __init__(
        self, listeners: list[Callable[[Message], None]] | None = None
    ):
        """CustomNotifier initialization function.

        Args:
            listeners: List of listener functions, default to None.
        """
        self.__listeners = listeners if listeners is not None else []
        self.__lock = threading.Lock()

    def add_listener(self, new_listener: Callable[[Message], None]):
        """Add a listener Callable to listener list.

        Args:
            new_listener: A Callable object to add to listeners list.
        """
        with self.__lock:
            self.__listeners.append(new_listener)

    def remove_listener(self, rem_listener: Callable[[Message], None]):
        """Remove a listener Callable to listener list.

        Args:
            rem_listener: A Callable object to remove from listeners list.
        """
        with self.__lock:
            # Attempt to remove the listener if it exists in the list.
            try:
                self.__listeners.remove(rem_listener)
            except ValueError:
                print(f"Listener {rem_listener} not found.")

    def notify_listeners(self, msg: Message):
        """Notify all listeners of a message.

        Args:
            msg: Message to notify listeners of.
        """
        with self.__lock:
            for listener_func in self.__listeners:
                listener_func(msg)

    def simulate(self, messages: list[Message]):
        """Simulate dynamic Notifier with messages scheduled via timestamp.

        Args:
            messages: Messages to schedule to send.

        Examples:
            >>> my_notifier = CustomNotifier([printer_listener])
            >>> current_time = time.time()
            >>> message_list = [ \
                    Message( \
                        arbitration_id=0x123, \
                        data=b"\x01\x02\x03\x04", \
                        timestamp=current_time + 2, \
                    ), \
                    Message( \
                        arbitration_id=0x456, \
                        data=b"\x05\x06\x07\x08", \
                        timestamp=current_time + 4, \
                    ), \
                ]
            >>> my_notifier.simulate(message_list)
        """
        scheduler = sched.scheduler(time.time, time.sleep)

        for msg in messages:
            # Schedule each message for sending, considering its timestamp.
            delay = msg.timestamp - time.time()
            if delay < 0:
                delay = 0  # Immediate transmit if in the past.
            scheduler.enter(delay, 1, self.notify_listeners, (msg,))

        # Running the scheduler in a separate thread to allow dynamic listener.
        scheduler_thread = threading.Thread(target=scheduler.run)
        scheduler_thread.start()


def printer_listener(msg: Message):
    """Simple print message listener.

    Args:
        msg: Message to process.
    """
    print(str(msg))
