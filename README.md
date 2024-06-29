# can_telemetry

![black-formatter](https://github.com/OntarioTechRacing/can_telemetry/actions/workflows/black-formatter.yml/badge.svg)

General purpose CAN telemetry tool written in Python 3.

---

<details markdown="1">
  <summary>Table of Contents</summary>

- [1 Background](#1-background)
- [2 Backend CANTelemetryApp](#2-backend-cantelemetryapp)
    - [2.1 Example Usage](#21-example-usage)
- [3 Reference Docs](#3-reference-docs)
    - [3.1 Designing a custom UI with QT Designer](#31-designing-a-custom-ui-with-qt-designer)

</details>

---

## 1 Background

The purpose of this software is to provide a desktop application for building
custom digital interfaces and scripting for physical CAN tools.

This application enables quick and easy development of tools for automating CAN
procedures. It also allows users with less in-depth knowledge of CAN to utilize
these tools without needing developer tools such as BusMaster or CANalyzer.

Python is the primary language used to support easy and rapid tool
development. [PyQt6](https://pypi.org/project/PyQt6/) was selected for its clean
interfaces and support from its native GUI pick-and-place
designer, [Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html).

---

## 2 Backend CANTelemetryApp

### 2.1 Example Usage

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

---

## 3 Reference Docs

### 3.1 Designing a custom UI with QT Designer

[QT Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html).
