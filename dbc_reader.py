"""Module to suport CAN dbc parsing"""

import canmatrix

class DbcReader:

    """dbcReader class to help filter CAN messages based on an existing CAN 
    database with pre-defined message structures"""

    def __init__(self, dbc_path: str):
        self.dbc = list(canmatrix.formats.loadp(dbc_path, flat_import=True).values())[0]
        #ensure we only take the network we want incase DBC defines multiple networks

    def add_filters(self, filters: list, msg: str):

        """"Takes in a filter string and filters array, adds CAN ID's to the filter 
        array based on filter string allowing those message to be graphed/viewed"""

        filter_id=0
        for message in self.dbc.frames: #Loop over all defined messages in dbc
            if msg in message.name:
                filter_id = message.arbitration_id.id
                filters.append(filter_id) #add message to filers list based on requirements

    def clear_filters(self, filters: list):

        """Clears the filters list for reuse"""

        filters.clear()
