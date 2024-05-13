# can_telemetry

General purpose CAN telemetry tool written in Python 3.

## Backend CANTelemetryApp

### Example Usage

```python
import time

from can import Message

from app import CANTelemetryApp, CANInterface

current_time = time.time()
message_list = [
    Message(
        arbitration_id=0x001,
        data=b"\x01\x02\x03\x04",
        timestamp=current_time + 2,
    ),
    Message(
        arbitration_id=0x002,
        data=b"\x05\x06\x07\x08",
        timestamp=current_time + 4,
    ),
]

app = CANTelemetryApp(
    dbc_file_path="example.dbc",
    interface=CANInterface.SIM,
    bit_rate=500000,
    sim_messages=message_list,
    csv_logging=True,
    ascii_logging=True,
)
app.start()

time.sleep(0.5)

print(f"Last 3 messages: {app.sqlite_read_via(3)}")  # Last 3 messages.

app.stop()
app.join()
```

## Designing a custom UI with QT Designer

https://doc.qt.io/qt-6/qtdesigner-manual.html
