import cantools  # Import cantools for DBC file handling

class dbcReader:
    def __init__(self, dbc_path):
        self.dbc = cantools.database.load_file(dbc_path)
    
    def add_filters(self, filters):
        filter=0
        filters["M1"] = []
        filters["M2"] = []
        filters["M3"] = []
        filters["M4"] = []
        for message in self.dbc.messages:
            if "M1_CellVoltages" in message.name:
                filter = message.frame_id
                filters["M1"].append(filter)
            if "M2_CellVoltages" in message.name:
                filter = message.frame_id
                filters["M2"].append(filter)
            if "M3_CellVoltages" in message.name:
                filter = message.frame_id
                filters["M3"].append(filter)
            if "M4_CellVoltages" in message.name:
                filter = message.frame_id
                filters["M4"].append(filter)