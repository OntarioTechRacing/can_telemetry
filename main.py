"""Main application module."""

if __name__ == "__main__":
    # TODO: DEV TEST CODE.
    # import time
    # from can import Message
    # from app import CANTelemetryApp, CANInterface
    #
    # current_time = time.time()
    # message_list = [
    #     Message(
    #         arbitration_id=0x001,
    #         data=b"\x01\x02\x03\x04",
    #         timestamp=current_time + 2,
    #     ),
    #     Message(
    #         arbitration_id=0x002,
    #         data=b"\x05\x06\x07\x08",
    #         timestamp=current_time + 4,
    #     ),
    # ]
    #
    # app = CANTelemetryApp(
    #     dbc_file_path="example.dbc",
    #     interface=CANInterface.SIM,
    #     bit_rate=500000,
    #     sim_messages=message_list,
    #     csv_logging=True,
    #     ascii_logging=True,
    # )
    # app.start()
    # print(f"Last 3 messages: {app.sqlite_read_via(3)}")  # Last 3 messages.
    pass
