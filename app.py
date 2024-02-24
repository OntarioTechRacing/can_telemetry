"""Main application class for CAN Telemetry."""

import sqlite3
import time
from datetime import datetime
from enum import Enum, auto

import can
from cantools import database
from cantools.database.namedsignalvalue import NamedSignalValue

from bus_manager_class import CANBusManager


class CANInterface(Enum):
    """Enum to define supported CAN bus interface types."""

    SIM = auto()
    VIRTUAL = auto()
    PEAK = auto()


class CANTelemetryApp:
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
        run_gui: bool = True,
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
            run_gui: Boolean to enable GUI, default True.
        """
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
        self.__run_gui = run_gui

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

    def start(self):
        """Start primary CANTelemetryApp logic.

        Raises:
            RuntimeError: CANBusManager object was not instanced from interface.
            RuntimeWarning: Hardware CAN bus connection failure.
        """
        # Create CANBusManager instance.
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
                manager = CANBusManager(
                    bus_type="pcan",
                    channel="PCAN_USBBUS1",
                    filters=self.__hardware_filters,
                )
            except can.interfaces.pcan.pcan.PcanCanInitializationError:
                raise RuntimeWarning("Could not connect to PCAN.")

        # Ensure manager is set.
        if manager is None:
            raise RuntimeError(
                f"Requested CANBusManager could not be made from "
                f"{self.interface}."
            )

        # Add SQLite logger.
        sqlite_logger = can.SqliteWriter(self.sqlite_log_file_path)
        manager.add_listener(sqlite_logger)

        # Add any additional loggers specified.
        csv_logger = None
        ascii_logger = None

        if self.__csv_logging:
            csv_logger = can.CSVWriter(self.csv_log_file_path)
            manager.add_listener(csv_logger)
        if self.__ascii_logging:
            ascii_logger = can.Logger(self.ascii_log_file_path)
            manager.add_listener(ascii_logger)

        if self.interface == CANInterface.SIM:
            # Start CAN bus with simulated messaging.
            manager.simulate(messages=self.__sim_messages)
        else:
            # Start CAN bus.
            manager.start()

        # Run bus.
        try:
            while True:
                time.sleep(1)

        # Manual program stop.
        except KeyboardInterrupt:
            # Stop loggers.
            sqlite_logger.stop()

            if self.__csv_logging:
                csv_logger.stop()
            if self.__ascii_logging:
                ascii_logger.stop()

            # Stop manager.
            manager.stop()

    def start_gui(self):
        # TODO: FUTURE WIP.
        pass
