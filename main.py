import dbc_reader

filters={}

if __name__ == "__main__":
    dbc_path = "F24_AMS_CANDB.dbc"
    dbc_support = dbc_reader.dbcReader(dbc_path)
    dbc_support.add_filters(filters)
    print(filters)
    # TODO: TEST CODE for #1.
    # import time
    #
    # from bus_manager_class import CANBusManager
    #
    # def print_message(msg):
    #     print(f"Received message: {msg}")
    #
    # filters = [{"can_id": 0x123, "can_mask": 0x7FF, "extended": False}]
    # manager = CANBusManager(filters=filters)
    #
    # manager.add_listener(print_message)
    # manager.start()
    #
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     manager.stop()

    pass
