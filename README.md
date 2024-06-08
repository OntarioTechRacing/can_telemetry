# can_telemetry

General purpose CAN telemetry tool written in Python 3.

---

<details markdown="1">
  <summary>Table of Contents</summary>

</details>

---

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

---

## Designing a custom UI with QT Designer

https://doc.qt.io/qt-6/qtdesigner-manual.html


# To-Do for gui.py
For all tasks, try to use as much of daniel's code as possible.

- we want to read the json to know which specific .ui file to load, and in what way we should set up the CAN connection
> json will be the specific file type that will record the requirements of each department's  configuration
>   - it uses key-value pairs. so you read the values of specific (named) keys to know what to do.

1) make a sample ui file, it can be empty
2) read the key that specifies the ui file location (might just be the name).
3) *LATER* use this value in a method that will render this specific file.
For Now, just  do 1 and 2.
create a new file on qt creator, ctrl n, under qt select qt designer form, click main window.
copy file directory just paste into pycharm project 

- we want to read the dbc file so that we can tell the computer how to understand the incoming electrical signals.
> json will specify location in a key, we need to extract in our gui.
>   - it uses key-value pairs. so you read the values of specific (named) keys to know what to do.

1) make a sample dbc file, it can be empty
2) read the key that specifies the dbc file location (might just be the name).
3) *LATER* use this value in a method that will decode this specific file.
For Now, just  do 1 and 2.

- we want to set up the CAN connections as needed.
> json file will have keys for all the required parameters our loaded libraries need for a successful connection (requirements.txt)
1) read the specific keys that specify all needed parameters. (feel free to ask daniel or myself for clarification).
this is only one step, but may require communication with me and/or daniel

---

>"name":value <--you read this,
>^^^by calling this
>^^^ by storing the name in a variable, which you will use throughout your program