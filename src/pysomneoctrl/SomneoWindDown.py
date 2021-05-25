#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
"""
if __name__ != "__main__":
    from .ConstSomneo import *
    #from ConstSomneo import *
else:
    from ConstSomneo import *

class SomneoWindDown:
    
    def __init__(self, http):
        self._http = http
        self._get = self._http._get
        self._put = self._http._put
        self._data = {}
        self.rlx_data = None
        self.dsk_data = None
        
        self.update()
        
    def relax(self, to_state=None, rtype=None ,duration=None, volume=None, ltlvl=None, pace=None):
        """rtype: 0=light,1=sound; pace: 4-10bpm"""
        payload = {}
        if to_state != None:
            payload[ONOFF] = to_state
        if rtype:
            payload["rtype"] = rtype
        if duration:
            payload[DURAT] = duration
        if volume:
            payload[SNDLV] = volume
        if ltlvl:
            payload["intny"] = ltlvl
        if pace:
            payload["maxpr"] = pace
        self.send_cmd(WURLX, payload)

    def sunset(self, to_state=None, curve=None, duration=None, ctype=None, device=None, volume=None):
        payload = {}
        if to_state != None:
            payload[ONOFF] = to_state
        if curve:
            payload[CURVE] = curve
        if duration:
            payload[DURAT] = duration
        if ctype:
            payload[CTYPE] = ctype
        if device:
            payload[SNDDV] = device
        if volume:
            payload[SNDLV] = volume
        self.send_cmd(WUDSK, payload)

    def send_cmd(self, path, pl, rtrn_path=None):
        data = self._put(path, pl)
        if rtrn_path == None:
            rtrn_path = path
        self._data[rtrn_path].update(data)

    def update(self):
        self._data[WURLX] = self._get(WURLX)
        self._data[WUDSK] = self._get(WUDSK)

if __name__ == "__main__":
    from SomneoHttp import SomneoHttp
    s = SomneoWindDown(SomneoHttp())
