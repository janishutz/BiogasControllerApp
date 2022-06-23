import os
import configparser
import serial

config = configparser.ConfigParser()
config.read('./config/settings.ini')
co = config['Dev Settings']['verbose']
if co == "True":
    pass
else:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

import threading
import platform
import webbrowser
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread, Clock
import bin.lib.lib
import bin.lib.communication
import bin.lib.comport_search
import bin.lib.csv_parsers
import logging
import datetime
import time

version_app = f"{config['Info']['version']}{config['Info']['subVersion']}"

################################################################
# LOGGER SETUP
##################
logging.basicConfig(level=logging.DEBUG, filename="./log/main_log.log", filemode="w")
logs = f"./log/{datetime.datetime.now()}-log-main.log"
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logs)
formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s: %(message)s -- %(lineno)d")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(config['Dev Settings']['log_level'])
logger.info(f"Logger initialized, app is running Version: {version_app}")
#################################################################

if config['Port Settings']['specificPort'] == "None" or "\"\"":
    special_port = ""
else:
    special_port = config['Port Settings']['specificPort']
cvr = bin.lib.csv_parsers.CsvRead()
cvw = bin.lib.csv_parsers.CsvWrite()
com = bin.lib.lib.Com()


#################################################################
# Settings Handler
#########################
class SettingsHandler:
    def __init__(self):
        self.ports = None
        self.window_sizeh = 600
        self.window_sizew = 800

    def settingshandler(self):
        self.ports = config['Port Settings']['specificPort']
        self.window_sizeh = config['UI Config']['sizeH']
        self.window_sizew = config['UI Config']['sizeW']
        Window.size = (int(self.window_sizew), int(self.window_sizeh))


#################################################################


logger.info("Started modules")


##################################################################
# Popups
##################################################################


class QuitPU(Popup):
    def quitapp(self):
        com.quitcom()
        logger.debug("App stopped")


class NoConnection(Popup):
    def details(self):
        self.detailsinfo = DetailInfo()
        self.detailsinfo.open()


class DetailInfo(Popup):
    update_details = ""
    def infos(self):
        self.err = ""
        try:
            com.connect(19200, special_port)
            com.quitcom()
        except Exception as err:
            self.err += "Errormessage:\n"
            self.err += str(err)
            self.err += "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        return str(self.err)

    def error_tips(self):
        self.err_tip = ""
        try:
            com.connect(19200, special_port)
            com.quitcom()
        except Exception as err:
            self.err_tip += "Possible way to resolve the issue: \n\n"
            if str(err)[0:10] == "[Errno 13]":
                if platform.system() == "Linux":
                    self.err_tip += f"Open a terminal and type in: sudo chmod 777 {bin.lib.comport_search.ComportService().get_comport(special_port)}"
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
            elif str(err)[0:26] == f"could not open port '{bin.lib.comport_search.ComportService().get_comport(special_port)}'":
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


class InfoPU(Popup):
    def notshowanymore(self):
        config.set("License", "show", "0")
        with open("./config/settings.ini", "w") as configfile:
            config.write(configfile)
        self.dismiss()


####################################################################
# SCREENS
####################################################################
class HomeScreen(Screen):
    def reset(self):
        logger.info("HomeScreen initialised")
        SettingsHandler().settingshandler()
        self.connected = 1
        self.info = f"You are currently running Version {version_app} - If you encounter a bug, please report it!"
        try:
            com.connect(19200, special_port)
            com.quitcom()
        except Exception as e:
            self.connected = 0
            logger.error(e)
        return self.info

    def openlicensepu(self):
        self.licensepu = InfoPU()
        self.licensepu.open()

    def tryconnection(self):
        if config["License"]["show"] == "1":
            self.openlicensepu()
            logger.info("Showing License info")
        else:
            pass
        try:
            com.connect(19200, special_port)
            com.quitcom()
            self.connected = 1
            self.manager.current = "Readout"
            self.manager.transition.direction = "right"
        except Exception as ex:
            if config['Dev Settings']['disableConnectionCheck'] == "True":
                self.connected = 1
                self.manager.current = "Readout"
                self.manager.transition.direction = "right"
            else:
                self.connected = 0
                logger.error(f"COM_error: {ex}")
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
        logger.info("Trying to start COM")

    def comstart(self, pu_on):
        try:
            com.connect(19200, special_port)
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.error(f"COM_error: {e}")

        if self.go == 1:
            logger.debug("COM start success")
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
        except Exception as e:
            logger.warning(f"COM_Close_Error: {e}")
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
        logger.info("Starting COM_Hook")
        while self.__x != "\n":
            if time.time() - self.__begin > 5:
                self.go = 0
                break
            else:
                self.__x = com.decode_ascii(com.receive(1))

        if self.go == 1:
            logger.info("COM_Hook 1 success")
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
            logger.info("COM_Hook successful")
            com.receive(5)
        else:
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
            self.com_ok = 1
            logger.info("Mode_Switch successful")
        except Exception as e:
            if e == serial.SerialException:
                logger.info("No running process found, continuing")
            else:
                logger.fatal(f"FATAL ERROR OCCURED, APP WILL LEAVE NOW: {e}")
            self.com_ok = 0

        if self.com_ok == 1:
            if text == "Normal Mode":
                bin.lib.communication.SwitchMode().disable_fastmode(special_port)
            else:
                bin.lib.communication.SwitchMode().enable_fastmode(special_port)
            logger.info("Switched mode, restarting COM")
            self.openpupups()
            self.comstart(0)
            logger.info("COM restarted successfully")
        else:
            self.check = 1
            self.ids.mode_sel.state = "normal"
            self.openconnectionfailpu()

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
            logger.error("COM_fail")
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
        logger.info("Stopping COM")
        self.stopcom(0)

    def resscreen(self):
        logger.info("Screen reset")
        self.ids.sonde1.text = ""
        self.ids.sonde2.text = ""
        self.ids.sonde3.text = ""
        self.ids.sonde4.text = ""
        self.ids.frequency.text = ""


class Program(Screen):
    def read_config(self):
        logger.debug("Reading config")
        self.config_imp = []
        self.__export = []
        self.config_imp = cvr.importing("./config/config.csv")
        self.__export = self.config_imp.pop(0)
        self.__extracted = self.__export.pop(0)
        logger.debug(f"config {self.__extracted}")
        if self.__extracted == "1":
            self.ids.prsel.state = "normal"
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
            self.__mode = 1
        else:
            self.ids.prsel.state = "down"
            Clock.schedule_once(self.read_data, 1)
            self.__mode = 2

    def change_mode(self):
        logger.info("Changing mode")
        logger.debug(f"mode was: {self.__mode}")
        if self.__mode == 1:
            logger.debug("Sending instruction to read info")
            Clock.schedule_once(self.read_data, 1)
            self.__mode = 2
        else:
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
            self.__mode = 1

    def read_data(self, dt):
        logger.debug("Starting to read data from the microcontroller")
        try:
            com.connect(19200, special_port)
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.error(f"COM_error: {e}")

        if self.go == 1:
            logger.info("Sending instructions")
            com.send("RD")
            self.__pos = 1
            self.__beginning = time.time()
            logger.info("Awaiting confirmation from the microcontroller for hook")
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
                                    logger.info("Hook successful")
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
                    logger.error("Microcontroller not available, stopping connection")
                    break
            if self.go == 1:
                for i in range(4):
                    self.__x = com.receive(28)
                    self.__a = str(com.decode_float(self.__x[0:6]))
                    self.__b = str(com.decode_float(self.__x[7:13]))
                    self.__c = str(com.decode_float(self.__x[14:20]))
                    self.__temp = str(com.decode_float(self.__x[21:27]))
                    if self.__pos == 1:
                        self.ids.s1_a.text = self.__a
                        self.ids.s1_b.text = self.__b
                        self.ids.s1_c.text = self.__c
                        self.ids.s1_t.text = self.__temp
                    elif self.__pos == 2:
                        self.ids.s2_a.text = self.__a
                        self.ids.s2_b.text = self.__b
                        self.ids.s2_c.text = self.__c
                        self.ids.s2_t.text = self.__temp
                    elif self.__pos == 3:
                        self.ids.s3_a.text = self.__a
                        self.ids.s3_b.text = self.__b
                        self.ids.s3_c.text = self.__c
                        self.ids.s3_t.text = self.__temp
                    elif self.__pos == 4:
                        self.ids.s4_a.text = self.__a
                        self.ids.s4_b.text = self.__b
                        self.ids.s4_c.text = self.__c
                        self.ids.s4_t.text = self.__temp
                    self.__pos += 1
                logger.info("Recieved info from microcontroller")
            else:
                self.open_confail_pu()
            com.quitcom()
        else:
            self.open_confail_pu()

    def create_com(self):
        self.coms = bin.lib.communication.Communication()

    def send_data(self):
        try:
            self.create_com()
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.critical(f"TRANSMISSION_Error: {e}")

        if self.go == 1:
            logger.info("Preparing data to be sent")
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
                logger.debug("trying to send...")
                try:
                    self.coms.change_all(self.__transmit, special_port)
                    logger.info("Transmission successful")
                    logger.debug("purging fields...")
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
                except Exception as e:
                    self.open_confail_pu()
                    logger.critical(f"TRANSMITION_Error: {e}")
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
    def read_config(self):
        logger.debug("Reading config")
        self.config_imp = []
        self.__export = []
        self.config_imp = cvr.importing("./config/config.csv")
        self.__export = self.config_imp.pop(0)
        self.__extracted = self.__export.pop(0)
        logger.debug(f"Mode set is: {self.__extracted}")
        if self.__extracted == "1":
            self.ids.prsel.state = "normal"
            self.ids.temp_s1.text = ""
            self.ids.temp_s2.text = ""
            self.ids.temp_s3.text = ""
            self.ids.temp_s4.text = ""
            self.__mode = 1
        else:
            self.ids.prsel.state = "down"
            Clock.schedule_once(self.read_data, 1)
            self.__mode = 2

    def change_mode(self):
        logger.info("Changing mode")
        logger.debug(f"Mode was: {self.__mode}")
        if self.__mode == 1:
            logger.info("starting sub-thread")
            Clock.schedule_once(self.read_data, 1)
            self.__mode = 2
        else:
            logger.info("clearing screen")
            self.ids.temp_s1.text = ""
            self.ids.temp_s2.text = ""
            self.ids.temp_s3.text = ""
            self.ids.temp_s4.text = ""
            self.__mode = 1

    def read_data(self, dt):
        logger.info("Trying to establish connection...")
        try:
            com.connect(19200, special_port)
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.error(f"COM_Error: {e}")

        if self.go == 1:
            logger.info("Sending instructions to microcontroller...")
            com.send("RD")
            self.__pos = 1
            self.__beginning = time.time()
            self.go = 1
            logger.info("Awaiting confirmation from the microcontroller for hook")
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
                                    logger.info("Hook successful")
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
                    logger.error("Microcontroller not available, stopping connection")
                    break
            if self.go == 1:
                logger.info("Receiving data...")
                for i in range(4):
                    self.__x = com.receive(28)
                    self.__output = str(com.decode_float(self.__x[21:27]))
                    if self.__pos == 1:
                        self.ids.temp_s1.text = self.__output
                    elif self.__pos == 2:
                        self.ids.temp_s2.text = self.__output
                    elif self.__pos == 3:
                        self.ids.temp_s3.text = self.__output
                    elif self.__pos == 4:
                        self.ids.temp_s4.text = self.__output
                    self.__pos += 1
                logger.info("Recieved data")
                com.quitcom()
            else:
                self.open_confail_pu()

    def create_com(self):
        self.coms = bin.lib.communication.Communication()

    def send_data(self):
        try:
            self.create_com()
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.critical(f"COM_Error: Microcontroller unavailable: {e}")

        if self.go == 1:
            logger.info("Preparing transmission...")
            self.__transmit = []
            if self.ids.temp_s1.text != "" and self.ids.temp_s2.text != "" and self.ids.temp_s3.text != "" and self.ids.temp_s4.text != "":
                self.__transmit.append(self.ids.temp_s1.text)
                self.__transmit.append(self.ids.temp_s2.text)
                self.__transmit.append(self.ids.temp_s3.text)
                self.__transmit.append(self.ids.temp_s4.text)
                logger.debug("Transmitting...")
                self.coms.change_temp(self.__transmit, special_port)
                self.ids.temp_s1.text = ""
                self.ids.temp_s2.text = ""
                self.ids.temp_s3.text = ""
                self.ids.temp_s4.text = ""
                self.openconfpu()
            else:
                self.openerrorpu()
                logger.debug("Missing fields")
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
        logger.info("Trying to connect to the microcontroller")
        try:
            com.connect(19200, special_port)
            self.go = 1
        except Exception as e:
            self.go = 0
            logger.error(f"COM_Error: {e}")

        if self.go == 1:
            logger.info("Sending instructions to the microcontroller...")
            com.send("RD")
            self.__pos = 1
            self.__beginning = time.time()
            self.go = 1
            logger.info("Awaiting confirmation from the microcontroller for hook")
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
                                    logger.info("Hook successful")
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
                    logger.error("Microcontroller not available, stopping connection")
                    break
            if self.go == 1:
                logger.info("Receiving data")
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
                logger.info("Received data")
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


class Modify(Screen):
    def read_config(self):
        logger.debug("Reading config")
        self.config_imp = []
        self.__export = []
        self.config_imp = cvr.importing("./config/config.csv")
        self.__export = self.config_imp.pop(0)
        self.__extracted = self.__export.pop(0)
        logger.debug(f"Mode at: {self.__extracted}")
        if self.__extracted == "1":
            self.ids.prsel.state = "normal"
        else:
            self.ids.prsel.state = "down"

    def issue_reporting(self):
        logger.info("Clicked error reporting button")
        webbrowser.open("https://github.com/simplePCBuilding/BiogasControllerApp/issues", new=2)

    def change_programming(self):
        logger.info("Switching programming mode")
        self.csv_import = []
        self.csv_import = cvr.importing("./config/config.csv")
        self.csv_import.pop(0)
        if self.ids.prsel.text == "Full\nreprogramming":
            self.csv_import.insert(0, 1)
        else:
            self.csv_import.insert(0, 2)
        logger.debug(f"Mode now: {self.csv_import}")
        cvw.write_str("./config/config.csv", self.csv_import)


########################################################
# Screenmanager
########################################################


class RootScreen(ScreenManager):
    pass


class BiogasControllerApp(App):
    def build(self):
        self.icon = "./BiogasControllerAppLogo.png"
        self.title = "BiogasControllerApp"
        return Builder.load_file("./bin/gui/gui.kv")


logger.info("Init finished, starting UI")

try:
    if __name__ == "__main__":
        bga = BiogasControllerApp()
        bga.run()
except Exception as e:
    logger.critical(e)