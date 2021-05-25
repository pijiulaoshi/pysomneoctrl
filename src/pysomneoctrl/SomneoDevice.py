#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
"""
import logging
import time
if __name__ != "__main__":
    from .ConstSomneo import *
    from .SomneoHttp import SomneoHttp
    from .SomneoAlarmManager import SomneoAlarmManager
    from .SomneoAudioManager import SomneoAudioManager
    from .SomneoWindDown import SomneoWindDown 
else:   
    from ConstSomneo import *
    from SomneoHttp import SomneoHttp
    from SomneoAlarmManager import SomneoAlarmManager
    from SomneoAudioManager import SomneoAudioManager
    from SomneoWindDown import SomneoWindDown

_LOGGER = logging.getLogger('pysomneoctrl_device')

class SomneoDevice:
    """Setup Somneo Device"""
    def __init__(self, ip=None, load_comp=None, load_alms=None, http_cd=TIMEOUT):

        # ---------------SETTINGS--------------#
        self._data = SOMNEO_DATA_DICT
        self.sensor_data = None
        self.hr_data = {}
        # --------------CONNECTION-------------#
        self._http = SomneoHttp(ip, http_cd)
        self._get = self._http._get
        self._put = self._http._put        
        # -----------LOAD_COMPONENTS-----------#
        self.load_comp = load_comp if load_comp else DEFAULT_LOAD_COMP
        self.debug(f"Components to load: {self.load_comp}")
        if "audio" in self.load_comp:
            self.audio = SomneoAudioManager(self._http)
            self._data.update(self.audio._data)
            self.debug("Audio Loaded")
        if "winddown" in self.load_comp: 
            self.winddown = SomneoWindDown(self._http)
            self._data.update(self.winddown._data)
            self.debug("Wind Down Loaded")
        if "alarms" in self.load_comp:
            self.load_alms = load_alms if load_alms else DEFAULT_LOAD_ALMS
            self.alarms = SomneoAlarmManager(self._http, self.load_alms)
            self.debug("Alarms Loaded")
        # ----------- FETCH DATA --------------#    
        self.fetch_inital_data()
        # -----------DEBUG-------------------- #
        self.debug(f' Somneo Setup Done. IP: {self._http._ip}')

    # --------------SWITCHES-------------------#
    def bedlight(self, to_state=None, brightness=None, ctype=None):
        payload = {DEMO: False}
        if to_state != None:
            payload[ONOFF] = to_state
        if brightness:
            payload['ltlvl'] = int(brightness)
        if ctype:
            payload[CTYPE] = int(ctype)
        self.send_cmd(WULGT, payload)

    def nightlight(self, to_state=None):
        payload = {"ngtlt": to_state}
        self.send_cmd(WULGT, payload)

    def bedtime(self, to_state):
        payload = {"night": to_state}
        self.send_cmd(WUNGT, payload)

    def display(self, to_state=None, brightness=None):
        payload = {}
        if to_state != None:
            payload[DSPON] = to_state
        if brightness:
            payload[DSPBR] = int(brightness)
        self.send_cmd_update(WUSTS, payload)

    def powerwake(self, to_state):
        payload = {"pwrsz": to_state}
        self.send_cmd(WUSTS, payload)

    # -----------------------------------------#
    def update_sensors(self):
        self.sensor_data = self._get(WUSRD)
    
    def fetch_inital_data(self):
        self._data[WUNGT] = self._get(WUNGT)
        self._data[WULGT] = self._get(WULGT)
        self._data[WUSTS] = self._get(WUSTS)
        self.update()

    def update(self):
        """Get the latest update from Somneo."""
        self.update_sensors()
        self._data[WUSRD] = self.sensor_data
        if "alarms" in self.load_comp:
            self._data[ALARM_DATA] = self.alarms._data
        if "audio" in self.load_comp:
            self._data[WUPLY] = self.audio._data[WUPLY]
            self._data[WUFMR] = self.audio._data[WUFMR]
            self._data[PRESETS] = self.audio._data[PRESETS]
        if "winddown" in self.load_comp:
            self._data[WURLX] = self.winddown._data[WURLX]
            self._data[WUDSK] = self.winddown._data[WUDSK]
        
# ------------------------ HTTP FUNCTIONS ------------------------- #
    def send_cmd(self, path, pl, rtrn_path=None):
        data = self._put(path, pl)
        if rtrn_path == None:
            rtrn_path = path
        self._data[rtrn_path].update(data)

# ----------------- TESTING/DEBUGGING ----------------------------- #
    def debug(self, msg):
        _LOGGER.error(f"DBG:{msg}")
    def error(self, msg):
        _LOGGER.error(f"ERR:{msg}")
# ------------------------ RUN MODULE ------------------------- #
if __name__ == "__main__":
    s = SomneoDevice()

        

