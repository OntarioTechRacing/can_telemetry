"""Module to suport CAN dbc parsing"""

import canmatrix


class DbcReader:
    """
    Helper class to parse CAN dbc file with helper function to allow
    user to dynamically filter incoming messages

    """

    def __init__(self, dbc_path: str):
        self.dbc = list(canmatrix.formats.loadp(dbc_path, flat_import=True).values())[0]
        # ensure we only take the network we want incase DBC defines multiple networks

    def add_filters(self, filters: list[int], msg: str):
        """
        Allows user to add filters based on message names within the dbc file

        Args:
            filters (list[int]): List of CAN ID's to filter incoming messages
            msg (str): Name of message within the dbc
        """

        filter_id = 0
        for message in self.dbc.frames:  # Loop over all defined messages in dbc
            if msg in message.name:
                filter_id = message.arbitration_id.id
                filters.append(
                    filter_id
                )  # add message to filers list based on requirements

    def clear_filters(self, filters: list):
        """
        Clears the filters list

        Args:
            filters (list): List of CAN ID's to filter incoming messages
        """

        filters.clear()
