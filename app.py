"""Main application class for CAN Telemetry.

This module defines the primary application logic for the CAN Telemetry system,
including message serialization and deserialization, CAN interface configuration,
logging setup, and application lifecycle management.

Attributes:
    None.
"""

import json
import sqlite3
from datetime import datetime
from enum import Enum, auto
from threading import Thread

import can
from cantools import database
from cantools.database.namedsignalvalue import NamedSignalValue

from bus_manager_class import CANBusManager

# Message serialization functions


def message_serializer(msg):
    """Serialize a can.Message object to a JSON compatible dictionary."""
    if not isinstance(msg, can.Message):
        raise TypeError("msg must be an instance of can.Message")

    # Convert data bytes to a list of integers for JSON serialization.
    data = list(msg.data) if msg.data is not None else None

    # Construct the dictionary.
    return {
        "timestamp": msg.timestamp,
        "arbitration_id": msg.arbitration_id,
        "is_extended_id": msg.is_extended_id,
        "channel": msg.channel,
        "dlc": msg.dlc,
        "data": data,
        "is_error_frame": msg.is_error_frame,
        "is_remote_frame": msg.is_remote_frame,
        "is_fd": msg.is_fd,
        "bitrate_switch": msg.bitrate_switch,
        "error_state_indicator": msg.error_state_indicator,
    }


def message_deserializer(data):
    """Deserialize a dictionary to a can.Message object."""
    return can.Message(
        timestamp=data.get("timestamp"),
        arbitration_id=data.get("arbitration_id"),
        is_extended_id=data.get("is_extended_id"),
        channel=data.get("channel"),
        dlc=data.get("dlc"),
        data=data.get("data"),
        is_error_frame=data.get("is_error_frame"),
        is_remote_frame=data.get("is_remote_frame"),
        is_fd=data.get("is_fd"),
        bitrate_switch=data.get("bitrate_switch"),
        error_state_indicator=data.get("error_state_indicator"),
    )


class CANInterface(Enum):
    """
    Enum to define supported CAN bus interface types.

    This enum provides a set of constants representing different types of CAN bus interfaces.
    Each constant corresponds to a specific interface type, such as simulated, virtual, or PEAK.
    """

    SIM = auto()
    """Simulated CAN bus interface."""

    VIRTUAL = auto()
    """Virtual CAN bus interface."""

    PEAK = auto()
    """PEAK CAN bus interface."""


class CANTelemetryApp(Thread):
    """Main application class for CAN Telemetry.

    This class manages the primary application logic for the CAN Telemetry system,
    including CAN interface configuration, message decoding, logging setup,
    and application lifecycle management.

    Args:
        dbc_file_path (str): File path of the DBC file.
        interface (CANInterface, optional): Interface CANInterface enum type. Defaults to CANInterface.VIRTUAL.
        bit_rate (int, optional): Bit rate of the CAN bus instance. Defaults to 500000.
        hardware_filters (list, optional): Hardware filters to specify. Defaults to None.
        base_log_file_path (str, optional): Base filepath of all log output files. Defaults to None.
        csv_logging (bool, optional): Boolean to enable CSV logging. Defaults to False.
        ascii_logging (bool, optional): Boolean to enable ASCII logging. Defaults to False.
        sim_messages (list, optional): Simulation messages for SIM interface. Defaults to None.
    """

    # Initialization method
    def __init__(
        self,
        dbc_file_path: str,
        interface: CANInterface = CANInterface.VIRTUAL,
        bit_rate: int = 500000,
        hardware_filters: list[dict[str, int | bool]] = None,
        base_log_file_path: str | None = None,
        csv_logging: bool = False,
        ascii_logging: bool = False,
        sim_messages: list[can.Message] = None,  # CANInterface.SIM messages.
    ):
        """CANTelemetryApp class initialization.

        Args:
            dbc_file_path: File path of DBC file.
            interface: Interface CANInterface enum type, default VIRTUAL.
            bit_rate: Bit rate of CAN bus instance, default 500000.
            hardware_filters: Hardware filters to specify.
            base_log_file_path: Base filepath of all log output files, defaults.
            csv_logging: Boolean to enable CSV logging, default False.
            ascii_logging: Boolean to enable ASCII logging, default False.
            sim_messages: Simulation messages, interface must be SIM enum.
        """
        # Initialize threading attributes.
        super().__init__()
        self.daemon = True
        self._stop_event = False

        # Initialize Telemetry attributes.
        self.__dbc_file_path = dbc_file_path
        self.__interface = interface
        self.__bit_rate = bit_rate
        self.__hardware_filters = hardware_filters
        self.__base_log_file_path = (
            base_log_file_path
            if base_log_file_path is not None
            else f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_log"
        )
        self.__csv_logging = csv_logging
        self.__ascii_logging = ascii_logging
        self.__sim_messages = sim_messages if sim_messages is not None else []

    @property
    def dbc_file_path(self) -> str:
        """Get DBC file path.

        Returns:
            CANInterface enum.
        """
        return self.__dbc_file_path

    @dbc_file_path.setter
    def dbc_file_path(self, dbc_file_path: str):
        """Set DBC file path.

        Args:
            dbc_file_path: DBC file path to set.
        """
        if not isinstance(dbc_file_path, str):
            raise TypeError("dbc_file_path expected type str.")
        self.__dbc_file_path = dbc_file_path

    @property
    def interface(self) -> CANInterface:
        """Get type of interface.

        Returns:
            CANInterface enum.
        """
        return self.__interface

    @property
    def bit_rate(self) -> int:
        """Get bit rate.

        Returns:
            Bit rate as int.
        """
        return self.__bit_rate

    @property
    def base_log_file_path(self) -> str:
        """Get base output log file path.

        Returns:
            Base log file path.
        """
        return self.__base_log_file_path

    @property
    def sqlite_log_file_path(self) -> str:
        """Get SQLite output log file path.

        Returns:
            SQLite log file path.
        """
        return f"{self.base_log_file_path}_sqlite.db"

    @property
    def csv_log_file_path(self) -> str:
        """Get CSV output log file path.

        Returns:
            CSV log file path.
        """
        return f"{self.base_log_file_path}_csv.csv"

    @property
    def ascii_log_file_path(self) -> str:
        """Get ASCII output log file path.

        Returns:
            ASCII log file path.
        """
        return f"{self.base_log_file_path}_ascii.log"

    # Methods for JSON serialization and deserialization

    def __to_json_dict(self) -> dict:
        return {
            "dbc_file_path": self.__dbc_file_path,
            "interface": self.__interface.name,  # Serialize enum to its name.
            "bit_rate": self.__bit_rate,
            "hardware_filters": self.__hardware_filters,
            "base_log_file_path": self.__base_log_file_path,
            "csv_logging": self.__csv_logging,
            "ascii_logging": self.__ascii_logging,
            "sim_messages": [
                message_serializer(msg) for msg in self.__sim_messages
            ],  # Serialize each CAN message.
        }

    def to_json_file(self, file_path: str, indent: bool = False):
        """Serialize the CANTelemetryApp object to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(self.__to_json_dict(), f, indent=(4 if indent else None))

    def to_json(self, indent: bool = False) -> str:
        """Serialize the CANTelemetryApp object to a JSON string."""
        return json.dumps(self.__to_json_dict(), indent=(4 if indent else None))

    @classmethod
    def __from_dict(cls, data: dict):
        """Create an instance of CANTelemetryApp from a dictionary."""
        return cls(
            dbc_file_path=data["dbc_file_path"],
            interface=CANInterface[
                data["interface"]
            ],  # Convert from name to enum
            bit_rate=data.get("bit_rate", 500000),
            hardware_filters=data.get("hardware_filters", []),
            base_log_file_path=data.get("base_log_file_path"),
            csv_logging=bool(data.get("csv_logging", False)),
            ascii_logging=bool(data.get("ascii_logging", False)),
            sim_messages=[
                message_deserializer(msg)
                for msg in data.get("sim_messages", [])
            ],  # Deserialize each CAN message
        )

    @classmethod
    def from_json_file(cls, file_path: str):
        """Deserialize JSON file to a CANTelemetryApp instance."""
        with open(file_path, "r") as f:
            data = json.load(f)
        return cls.__from_dict(data)

    @classmethod
    def from_json(cls, json_data: str):
        """Deserialize JSON string to a CANTelemetryApp instance."""
        data = json.loads(json_data)
        return cls.__from_dict(data)

    def sqlite_read_via(
        self,
        n: int,
        white_list_ids: list = None,
        black_list_ids: list = None,
        is_error_frame: bool = None,
    ) -> list[can.Message]:
        """General purpose CAN message query function from SQLite database.

        Args:
            n: Number of messages to fetch.
            white_list_ids: List of arbitration IDs to include.
            black_list_ids: List of arbitration IDs to exclude.
            is_error_frame: If messages should be filtered by error state.

        Returns:
            list: List of can.Message objects from SQLite cursor fetchall query.

        Notes:
            Database fields:
                timestamp       =   ts
                arbitration_id  =   arbitration_id
                is_extended_id  =   extended
                is_remote_frame =   remote
                is_error_frame  =   error
                dlc             =   dlc
                data            =   data
        """
        # Construct the query.
        query = (
            "SELECT ts, arbitration_id, extended, remote, error, dlc, data "
            "FROM messages"
        )
        conditions = []
        parameters = []

        # Setup database connector and cursor.
        connector = sqlite3.connect(self.sqlite_log_file_path)
        cursor = connector.cursor()

        # Filter by white list and black list of arbitration IDs.
        if white_list_ids:
            placeholders = ",".join("?" for _ in white_list_ids)
            conditions.append(f"arbitration_id IN ({placeholders})")
            parameters.extend(white_list_ids)
        if black_list_ids:
            placeholders = ",".join("?" for _ in black_list_ids)
            conditions.append(f"arbitration_id NOT IN ({placeholders})")
            parameters.extend(black_list_ids)

        # Filter by is_error_frame if specified.
        if is_error_frame is not None:
            conditions.append("is_error_frame = ?")
            parameters.append(is_error_frame)

        # Append conditions to query if any.
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Append ordering and limit.
        query += " ORDER BY ts DESC LIMIT ?"
        parameters.append(n)

        # Execute the query.
        cursor.execute(query, parameters)
        rows = cursor.fetchall()

        # Close cursor and connector.
        cursor.close()
        connector.close()

        # Convert rows to can.Message objects.
        messages = []
        for row in rows:
            message = can.Message(
                timestamp=row[0],
                arbitration_id=row[1],
                is_extended_id=row[2],
                is_remote_frame=row[3],
                is_error_frame=row[4],
                dlc=row[5],
                data=row[6],
            )
            # Augment the message object with attribute.
            messages.append(message)

        return messages

    # Method for decoding CAN bus messages with DBC
    def get_dbc_db(self) -> database.Database:
        """Get DBC database object from DBC file path.

        Returns:
            database.Database object of DBC.
        """
        # Load the DBC.
        return database.load_file(self.dbc_file_path)

    def decode(
        self, msg: can.Message
    ) -> dict[str, int | float | str | NamedSignalValue]:
        """Decode CAN bus Message with DBC.

        Args:
            msg: Message object to decode.

        Returns:
            Return the decoded message.
        """
        db = self.get_dbc_db()
        return db.decode_message(msg.arbitration_id, msg.data)

    # Primary logic execution method
    def run(self):
        """Start primary CANTelemetryApp logic."""
        # Initialize CANBusManager depending on the interface.
        manager = None

        # Virtual CAN bus.
        if (
            self.interface == CANInterface.SIM
            or self.interface == CANInterface.VIRTUAL
        ):
            manager = CANBusManager(filters=self.__hardware_filters)

        # PEAK CAN bus.
        elif self.interface == CANInterface.PEAK:
            try:
                # Init Bus Manager.
                manager = CANBusManager(
                    bus_type="pcan",
                    channel="PCAN_USBBUS1",
                    filters=self.__hardware_filters,
                )

                # Ensure manager is set.
                if manager is None:
                    raise RuntimeError(
                        f"Requested CANBusManager could not be made from "
                        f"{self.interface}."
                    )

                # Test connection.
                manager.start()
                manager.stop()

            except can.interfaces.pcan.pcan.PcanCanInitializationError:
                raise RuntimeWarning("Could not connect to PCAN.")

        # Initialize logging.
        sqlite_logger = can.SqliteWriter(self.sqlite_log_file_path)
        manager.add_listener(sqlite_logger)
        csv_logger = (
            can.CSVWriter(self.csv_log_file_path)
            if self.__csv_logging
            else None
        )
        ascii_logger = (
            can.Logger(self.ascii_log_file_path)
            if self.__ascii_logging
            else None
        )

        if csv_logger:
            manager.add_listener(csv_logger)
        if ascii_logger:
            manager.add_listener(ascii_logger)

        try:
            if self.interface == CANInterface.SIM:
                # Start CAN bus with simulated messaging.
                manager.simulate(messages=self.__sim_messages)
            else:
                # Start CAN bus.
                manager.start()

            # Implement a loop with a condition to check for a stop flag.
            while not getattr(self, "_stop_event", True):
                pass

        # Manual program stop.
        except KeyboardInterrupt:
            pass

        finally:
            sqlite_logger.stop()

            if self.__csv_logging:
                csv_logger.stop()
            if self.__ascii_logging:
                ascii_logger.stop()

            # Stop manager.
            manager.stop()

    # Method to stop the application
    def stop(self):
        """Stop the telemetry application."""
        setattr(self, "_stop_event", True)
