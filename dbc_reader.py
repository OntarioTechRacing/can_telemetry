import canmatrix  # Import cantools for DBC file handling

class dbcReader:
    def __init__(self, dbc_path):
        self.dbc = list(canmatrix.formats.loadp(dbc_path, flat_import=True).values())[0] #ensure we only take the network we want incase DBC defines multiple networks
    
    def add_filters(self, filters, msg):
        filter=0
        for message in self.dbc.frames: #Loop over all defined messages in dbc
            if msg in message.name:
                filter = message.arbitration_id.id
                filters.append(filter) #add message to filers list based on requirements