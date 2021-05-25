#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi

TODO:
    - Test Aux
    - WUSND = "wusnd" (what is this for???)
        # {"sdvol":25,"softst":0,"chifn":0,"softst":false}
"""
import logging
_LOGGER = logging.getLogger('pysomneoctrl_audio')

if __name__ != "__main__":
    from .ConstSomneo import *
    #from ConstSomneo import *
else:
    from ConstSomneo import *

# SETTING LIMITS
MIN = "min"
MAX = "max"
FRQ = {MIN:87.5, MAX:108.0}
CHFM = {MIN:1, MAX:5}
CHWU = {MIN:1, MAX:8}
CHDU = {MIN:1, MAX:4}
CHNL = {FMR:CHFM, WUS:CHWU, DUS:CHDU}

class SomneoAudioManager:
    
    def __init__(self, http):
        self._http = http
        self._get = self._http._get
        self._put = self._http._put
        self._state = None
        self._vol = None
        self._data = {WUFMR:{}, WUPLY:{}, PRESETS:{},}
        
        self.update()       
# --------------------------- WUPLY ----------------------------- #
    def play(self, to_state=None, volume=None, device=None, channel=None, sndss=None):
        payload = {}
        if device != None:
            payload[SNDDV] = device
            if device == FMR or device == AUX:
                payload[DEMO] = False
            else:
                payload[DEMO] = True
        if to_state != None:
            payload[ONOFF] = to_state
        if volume:
            payload["sdvol"] = volume
        if channel != None:
            payload[SNDCH] = str(channel)
        if sndss:
            payload[SNDSS] = sndss
        self.send_cmd(WUPLY, payload)
        
    def switch_channel(self, ch):
        dev = self._data[WUPLY][SNDDV]
        chl = CHNL[dev]
        if ch >= chl[MIN] and ch <= chl[MAX]:
            self.play(channel=ch)
        else:
            self.error("Invalid channel number")
            
    def aux(self, to_state):
        self.play(to_state, False, device=AUX)

# ------------------------- WUFMR/WUFMP ---------------------------- #
    def edit_fm_preset(self, ch, freq):
        path = FM_PRES
        if ch < CHFM[MIN] or ch > CHFM[MAX]:
            self.error("Invalid channel number")
            pass
        if freq == "" or float(freq) > FRQ[MAX] or float(freq) < FRQ[MIN]:
            self.error("Invalid frequency")
            pass          
        else:
            payload = {str(ch):freq}
            self.send_cmd(FM_PRES, payload, PRESETS)

    def radio_seek(self, direction):
        if direction == "up" or direction == "down":
            payload = {"fmcmd":f"seek{direction}"}
            self._put(WUFMR, payload)
            self._data[WUFMR] = self._get(WUFMR)
        else:
            self.error("Invalid command")

# ------------------------ SEND/GET DATA ------------------------- #
    def update(self):
        self._data[WUPLY].update(self._get(WUPLY))
        self._data[WUFMR].update(self._get(WUFMR))
        pres = self._get(FM_PRES)
        for i in range(1, 6):
            pr = str(i)
            self._data[PRESETS][pr] = pres[pr]

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

# No Idea how this works. Seems to have to do with starting soft start/fade in of sound?
    # def test_wusnd(self, sdvol=None, softst=None,chifn=None, softst2=None):
    #     payload = {}
    #     if sdvol:
    #         payload["sdvol"] = sdvol
    #     if softst:
    #         payload["softst"] = softst
    #     if chifn:
    #         payload["chifn"] = chifn
    #     if softst2:
    #         payload["softst"] = softst2
    #     self._put(WUSND, payload)
        
        
# ----------------- RUN MODULE INDEPENDENTLY ---------------------- #
if __name__ == "__main__":
    from SomneoHttp import SomneoHttp
    s = SomneoAudioManager(SomneoHttp())
