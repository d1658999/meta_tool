from connection_interface.connection_serial import ModemComport

class Test:
    def __init__(self):
        self.ser = ModemComport()

t = Test()
t.ser.readlines()
