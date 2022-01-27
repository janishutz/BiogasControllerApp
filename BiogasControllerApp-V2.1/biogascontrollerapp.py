print("""

=====================

BIOGASCONTROLLERAPP

----------
Version 2.1
Copyright 2022 J.Hutz""")
import time
import threading
import platform
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
import bin.lib.lib
import bin.lib.communication
import bin.lib.comport_search




com = bin.lib.lib.Com()

##################################################################
# Popups
##################################################################


class QuitPU(Popup):
    def quitapp(self):
        com.quitcom()


class NoConnection(Popup):
    def details(self):
        self.detailsinfo = DetailInfo()
        self.detailsinfo.open()


class DetailInfo(Popup):
    update_details = ""
    def infos(self):
        self.err = ""
        try:
            com.connect(19200, "")
            com.quitcom()
        except Exception as err:
            self.err += "Errormessage:\n"
            self.err += str(err)
            self.err += "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        return str(self.err)

    def error_tips(self):
        self.err_tip = ""
        try:
            com.connect(19200, "")
            com.quitcom()
        except Exception as err:
            self.err_tip += "Possible way to resolve the issue: \n\n"
            if str(err)[0:10] == "[Errno 13]":
                if platform.system() == "Linux":
                    self.err_tip += f"Open a terminal and type in: sudo chmod 777 {bin.lib.comport_search.ComportService().get_comport()}"
                elif platform.system() == "Macintosh":
                    self.err_tip += "Give permission to access the cable"
                elif platform.system() == "Windows":
                    self.err_tip += "Try a different cable or install another driver"
                else:
                    self.err_tip += "Unknown OS"
            elif str(err)[0:10] == "[Errno 2] ":
                if platform.system() == "Linux":
                    self.err_tip += "Connect a cable, open a terminal and type in: sudo chmod 777 /dev/ttyUSB0"
                elif platform.system() == "Macintosh":
                    self.err_tip += "Give permission to access the cable"
                elif platform.system() == "Windows":
                    self.err_tip += "Try a different cable or install another driver"
                else:
                    self.err_tip += "Unknown OS"
            elif str(err)[0:34] == "could not open port '/dev/ttyUSB0'":
                self.err_tip += "Please connect the PC with the microcontroller!"
            elif str(err)[0:26] == f"could not open port '{bin.lib.comport_search.ComportService().get_comport()}'":
                self.err_tip += "Try using a different cable or close all monitoring software (like MSI Afterburner)"
            else:
                self.err_tip += "Special Error, consult the manual of Serial"
        return str(self.err_tip)


class Modeswitch(Popup):
    pass


class Connecting_PU(Popup):
    pass


class Disconnecting_PU(Popup):
    pass


class MissingFieldsError(Popup):
    pass


class ConnectionFail(Popup):
    pass


class SaveConf(Popup):
    pass


####################################################################
# SCREENS
####################################################################

class HomeScreen(Screen):
    connected = 1
    try:
        com.connect(19200, "")
        com.quitcom()
    except:
        connected = 0

    def tryconnection(self):
        try:
            com.connect(19200, "")
            com.quitcom()
            self.connected = 1
            self.manager.current = "Readout"
            self.manager.transition.direction = "right"
        except:
            self.connected = 0
            self.open_popup()

    def open_popup(self):
        self.popups = NoConnection()
        self.popups.open()

    def exitapp(self):
        self.pup = QuitPU()
        self.pup.open()


class ReadoutScreen(Screen):
    go = 1
    def start_com(self):
        self.comstart(1)

    def comstart(self, pu_on):
        try:
            com.connect(19200, "")
            self.go = 1
        except:
            self.go = 0

        if self.go == 1:
            self.parent.current = "Readout"
            if pu_on == 1:
                self.openstartpu()
            else:
                pass
            self.communication = threading.Thread(name="communication", target=self.start_coms)
            self.communication.start()
        else:
            self.openconnectionfailpu()

    def end_com(self):
        self.stopcom(1)

    def stopcom(self, pu_on):
        self.go = 0
        try:
            self.communication.join()
        except:
            pass
        if pu_on == 1:
            self.openendpu()
        else:
            pass

    def start_coms(self):
        self.check = 1
        self.__level = 0
        self.__distance = 0
        self.__x = ""
        self.__begin = time.time()
        self.go = 1
        while self.__x != "\n":
            if time.time() - self.__begin > 5:
                self.go = 0
                break
            else:
                self.__x = com.decode_ascii(com.receive(1))

        if self.go == 1:
            while self.__level < 3:
                self.__x = com.decode_ascii(com.receive(1))
                if self.__x == " ":
                    if self.__distance == 4:
                        self.__level += 1
                    else:
                        pass
                    self.__distance = 0
                else:
                    if self.__distance > 4:
                        self.__level = 0
                        self.__distance = 0
                    else:
                        self.__distance += 1
            self.check = 1
            com.receive(5)
        else:
            self.go = 0
            self.check = 0

        while self.go == 1:
            self.__starttime = time.time()
            self.__output = ""
            self.__data_recieve = com.receive(68)
            self.__output += "Tadc: "
            self.__output += str(com.decode_int(self.__data_recieve[0:4]))
            self.__output += "\nTemperatur: "
            self.__output += com.decode_float(self.__data_recieve[5:11])
            self.__output += f"\nDuty-Cycle: {(float(com.decode_float_2(self.__data_recieve[48:52])) / 65535) * 100}%"
            self.change_screen(1, self.__output)
            self.__output = "Tadc: "
            self.__output += str(com.decode_int(self.__data_recieve[12:16]))
            self.__output += "\nTemperatur: "
            self.__output += com.decode_float(self.__data_recieve[17:23])
            self.__output += f"\nDuty-Cycle: {(float(com.decode_float_2(self.__data_recieve[53:57])) / 65535) * 100}%"
            self.change_screen(2, self.__output)
            self.__output = "Tadc: "
            self.__output += str(com.decode_int(self.__data_recieve[24:28]))
            self.__output += "\nTemperatur: "
            self.__output += com.decode_float(self.__data_recieve[29:35])
            self.__output += f"\nDuty-Cycle: {(float(com.decode_float_2(self.__data_recieve[58:62])) / 65535) * 100}%"
            self.change_screen(3, self.__output)
            self.__output = "Tadc: "
            self.__output += str(com.decode_int(self.__data_recieve[36:40]))
            self.__output += "\nTemperatur: "
            self.__output += com.decode_float(self.__data_recieve[41:47])
            self.__output += "\nDuty-Cycle: "
            self.__output += f"\nDuty-Cycle: {(float(com.decode_float_2(self.__data_recieve[63:67])) / 65535) * 100}%"
            self.change_screen(4, self.__output)
            self.change_screen(5, f"F={1 / (time.time() - self.__starttime)}")
        self.change_screen(6, "")
        com.quitcom()

    def switch_mode(self, text):
        self.go = 0
        try:
            self.communication.join()
            com.quitcom()
        except:
            pass
        if text == "Normal Mode":
            bin.lib.communication.SwitchMode().disable_fastmode()
        else:
            bin.lib.communication.SwitchMode().enable_fastmode()
        self.openpupups()
        self.comstart(0)

    @mainthread
    def change_screen(self, pos, value):
        if pos == 1:
            self.ids.sonde1.text = value
        elif pos == 2:
            self.ids.sonde2.text = value
        elif pos == 3:
            self.ids.sonde3.text = value
        elif pos == 4:
            self.ids.sonde4.text = value
        elif pos == 6:
            self.openconnectionfailpu()
        else:
            self.ids.frequency.text = value

    def openpupups(self):
        self.popup = Modeswitch()
        self.popup.open()

    def openendpu(self):
        self.pu = Disconnecting_PU()
        self.pu.open()

    def openstartpu(self):
        self.pup = Connecting_PU()
        self.pup.open()

    def openconnectionfailpu(self):
        if self.check == 0:
            self.cfpu = ConnectionFail()
            self.cfpu.open()
        else:
            pass

    def leave_screen(self):
        self.stopcom(0)

    def resscreen(self):
        self.ids.sonde1.text = ""
        self.ids.sonde2.text = ""
        self.ids.sonde3.text = ""
        self.ids.sonde4.text = ""
        self.ids.frequency.text = ""


class Program(Screen):
    def create_com(self):
        self.coms = bin.lib.communication.Communication()

    def send_data(self):
        try:
            self.create_com()
            self.go = 1
        except:
            self.go = 0

        if self.go == 1:
            self.__transmit = []
            if self.ids.s1_a.text != "" and self.ids.s1_b.text != "" and self.ids.s1_c.text != "" and self.ids.s1_t.text != "" and self.ids.s2_a.text != "" and self.ids.s2_b.text != "" and self.ids.s2_c.text != "" and self.ids.s2_t.text != "" and self.ids.s3_a.text != "" and self.ids.s3_b.text != "" and self.ids.s3_c.text != "" and self.ids.s3_t.text != "" and self.ids.s4_a.text != "" and self.ids.s4_b.text != "" and self.ids.s4_c.text != "" and self.ids.s4_t.text != "":
                self.__transmit.append(self.ids.s1_a.text)
                self.__transmit.append(self.ids.s1_b.text)
                self.__transmit.append(self.ids.s1_c.text)
                self.__transmit.append(self.ids.s1_t.text)
                self.__transmit.append(self.ids.s2_a.text)
                self.__transmit.append(self.ids.s2_b.text)
                self.__transmit.append(self.ids.s2_c.text)
                self.__transmit.append(self.ids.s2_t.text)
                self.__transmit.append(self.ids.s3_a.text)
                self.__transmit.append(self.ids.s3_b.text)
                self.__transmit.append(self.ids.s3_c.text)
                self.__transmit.append(self.ids.s3_t.text)
                self.__transmit.append(self.ids.s4_a.text)
                self.__transmit.append(self.ids.s4_b.text)
                self.__transmit.append(self.ids.s4_c.text)
                self.__transmit.append(self.ids.s4_t.text)
                self.coms.change_all(self.__transmit,"")
                self.ids.s1_a.text = ""
                self.ids.s1_b.text = ""
                self.ids.s1_c.text = ""
                self.ids.s1_t.text = ""
                self.ids.s2_a.text = ""
                self.ids.s2_b.text = ""
                self.ids.s2_c.text = ""
                self.ids.s2_t.text = ""
                self.ids.s3_a.text = ""
                self.ids.s3_b.text = ""
                self.ids.s3_c.text = ""
                self.ids.s3_t.text = ""
                self.ids.s4_a.text = ""
                self.ids.s4_b.text = ""
                self.ids.s4_c.text = ""
                self.ids.s4_t.text = ""
                self.openconfpu()
            else:
                self.openerrorpu()
        else:
            self.open_confail_pu()

    def openerrorpu(self):
        self.pu = MissingFieldsError()
        self.pu.open()

    def open_confail_pu(self):
        self.cfpu = ConnectionFail()
        self.cfpu.open()

    def openconfpu(self):
        self.confpus = SaveConf()
        self.confpus.open()


class ProgramTemp(Screen):
    def create_com(self):
        self.coms = bin.lib.communication.Communication()

    def send_data(self):
        try:
            self.create_com()
            self.go = 1
        except:
            self.go = 0

        if self.go == 1:
            self.__transmit = []
            if self.ids.temp_s1.text != "" and self.ids.temp_s2.text != "" and self.ids.temp_s3.text != "" and self.ids.temp_s4.text != "":
                self.__transmit.append(self.ids.temp_s1.text)
                self.__transmit.append(self.ids.temp_s2.text)
                self.__transmit.append(self.ids.temp_s3.text)
                self.__transmit.append(self.ids.temp_s4.text)
                self.coms.change_temp(self.__transmit, "")
                self.ids.temp_s1.text = ""
                self.ids.temp_s2.text = ""
                self.ids.temp_s3.text = ""
                self.ids.temp_s4.text = ""
                self.openconfpu()
            else:
                self.openerrorpu()
        else:
            self.open_confail_pu()

    def openerrorpu(self):
        self.pu = MissingFieldsError()
        self.pu.open()

    def openconfpu(self):
        self.confpu = SaveConf()
        self.confpu.open()

    def open_confail_pu(self):
        self.cfpu = ConnectionFail()
        self.cfpu.open()


class ReadData(Screen):
    def read_data(self):
        try:
            com.connect(19200, "")
            self.go = 1
        except:
            self.go = 0

        if self.go == 1:
            com.send("RD")
            self.__pos = 1
            self.__beginning = time.time()
            self.go = 1
            while True:
                if time.time() - self.__beginning < 5:
                    self.__data_recieve = com.decode_ascii(com.receive(1))
                    if self.__data_recieve == "\n":
                        self.__data_recieve = com.decode_ascii(com.receive(1))
                        if self.__data_recieve == "R":
                            self.__data_recieve = com.decode_ascii(com.receive(1))
                            if self.__data_recieve == "D":
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
                else:
                    self.go = 0
                    break
            if self.go == 1:
                for i in range(4):
                    self.__x = com.receive(28)
                    self.__output = "a: "
                    self.__output += str(com.decode_float(self.__x[0:6]))
                    self.__output += f"\nb: {str(com.decode_float(self.__x[7:13]))}"
                    self.__output += f"\nc: {str(com.decode_float(self.__x[14:20]))}"
                    self.__output += f"\nTemp: {str(com.decode_float(self.__x[21:27]))}"
                    if self.__pos == 1:
                        self.ids.inf_sonde1.text = self.__output
                    elif self.__pos == 2:
                        self.ids.inf_sonde2.text = self.__output
                    elif self.__pos == 3:
                        self.ids.inf_sonde3.text = self.__output
                    elif self.__pos == 4:
                        self.ids.inf_sonde4.text = self.__output
                    self.__pos += 1
            else:
                self.open_confail_pu()
            com.quitcom()
        else:
            self.open_confail_pu()

    def open_confail_pu(self):
        self.cfpu = ConnectionFail()
        self.cfpu.open()


class Credits(Screen):
    pass


########################################################
# Screenmanager
########################################################


class RootScreen(ScreenManager):
    pass


kv = Builder.load_file("./bin/gui/gui.kv")


class BiogasControllerApp(App):
    def build(self):
        self.icon = "./BiogasControllerAppLogo.png"
        return kv


if __name__ == "__main__":
    BiogasControllerApp().run()
