import bin.lib.lib
com = bin.lib.lib.Com()


class Communication:
    def __init__(self):
        self.__x = 0
        self.__data_recieve = 0
        self.__output = ""

    def change_temp(self, data, special_port):
        com.connect(19200, special_port)
        com.send("PT")
        self.go = 0
        while True:
            self.__data_recieve = com.decode_ascii(com.receive(1))
            if self.__data_recieve == "\n":
                self.__data_recieve = com.decode_ascii(com.receive(1))
                if self.__data_recieve == "P":
                    self.__data_recieve = com.decode_ascii(com.receive(1))
                    if self.__data_recieve == "T":
                        self.__data_recieve = com.decode_ascii(com.receive(1))
                        if self.__data_recieve == "\n":
                            self.go = 1
                            break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        if self.go == 1:
            self.data = data
            while len(self.data) > 0:
                self.__data_recieve = com.receive(3)
                if self.__data_recieve != "":
                    com.send_float(float(self.data.pop(0)))
                else:
                    print("error")
                    break
        else:
            print("Error")
        com.quitcom()

    def change_all(self, data, special_port):
        com.connect(19200, special_port)
        com.send("PR")
        self.go = 0
        while True:
            self.__data_recieve = com.decode_ascii(com.receive(1))
            if self.__data_recieve == "\n":
                self.__data_recieve = com.decode_ascii(com.receive(1))
                if self.__data_recieve == "P":
                    self.__data_recieve = com.decode_ascii(com.receive(1))
                    if self.__data_recieve == "R":
                        self.__data_recieve = com.decode_ascii(com.receive(1))
                        if self.__data_recieve == "\n":
                            self.go = 1
                            break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        if self.go == 1:
            self.data = data
            while len(self.data) > 0:
                self.__data_recieve = com.receive(3)
                if self.__data_recieve != "":
                    com.send_float(float(self.data.pop(0)))
                else:
                    print("error")
                    break
        else:
            print("Error")
        com.quitcom()


class SwitchMode:
    def __init__(self):
        pass

    def enable_fastmode(self, special_port):
        com.connect(19200, special_port)
        com.send("FM")
        com.quitcom()

    def disable_fastmode(self, special_port):
        com.connect(19200, special_port)
        com.send("NM")
        com.quitcom()
