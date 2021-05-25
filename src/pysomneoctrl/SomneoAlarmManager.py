#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
"""
import datetime
import time

if __name__ != "__main__":
    from .ConstSomneo import *
    #from ConstSomneo import *
else:
    from ConstSomneo import *

# DEFAULT PAYLOADS
DELETE = {"prfen":False,"prfvs":False,"almhr":7,"almmn":30,"pwrsz":0,"pszhr":0,"pszmn":0,"ctype":0,"curve":20,"durat":30,"daynm":254, "snddv":"wus", "snztm":0}
CREATE = {"prfen":False,"prfvs":True,"almhr":7,"almmn":30,"pwrsz":0,"pszhr":0,"pszmn":0,"ctype":1,"curve":20,"durat":15,"daynm":0, "snddv":"wus", "snztm":0}


class SomneoAlarmManager:

    def __init__(self, http, load_alarms):
        self.load_alarms = load_alarms
        self.ro_data = {}
        self._data = {}
        self._http = http
        self._get = self._http._get
        self._put = self._http._put
        self._alarms = {}
        self.setup_alarms()
    
# ----------------- CHANGE ALARM SETTINGS ------------------------#
    def delete_alarm(self, al_id):
        c_settings = DELETE
        self.change_settings(al_id, c_settings)
        
    def change_state(self, al_id, to_state: bool):
        c_settings = {PRFEN:to_state}
        self.change_settings(al_id, c_settings)
        
    def change_time(self, al_id, chour, cminute, weekday=None):
        c_settings = {ALMHR:chour, ALMMN: cminute}
        if weekday:
            wkdayint = weekday
            c_settings[DAYNM] = wkdayint      
        self.change_settings(al_id, c_settings)
    
    def change_pwr_wake(self, al_id, minutes=None):
        c_settings = {}
        if type(minutes) == int:
            pwhour = self._data[ALMHR]
            pwminute = int(self._data[ALMMN]) + int(minutes)
            if pwminute > 59:
                pwminute = pwminute - 60
                pwhour += 1
            c_settings = {PWHR:pwhour, PWMIN:pwminute, PWEN:255}
        else:
            c_settings[PWEN] = 0
        self.change_settings(al_id, c_settings)
    
    def change_light(self, al_id, curve=None, duration=None, ctype=None):
        c_settings = {}
        if curve:
            c_settings[CURVE] = curve
        if duration:
            c_settings[DURAT] = duration
        if ctype:
            c_settings[CTYPE] = ctype
        self.change_settings(al_id, c_settings)
    
    def change_sound(self, al_id, device=None, channel=None, level=None, sndss=None):
        c_settings = {}
        if device:
            c_settings[SNDDV] = device
        if channel:
            c_settings[SNDCH] = channel
        if level:
            c_settings[SNDLV] = level
        if sndss:
            c_settings[SNDSS] = sndss
        self.change_settings(al_id, c_settings)
        
# ----------------- SEND UPDATES TO SOMNEO -----------------------#
    def change_settings(self, al_id: int, c_settings: dict):
        payload = {PRFNR: al_id, PRFVS:True}
        payload.update(c_settings)
        alarm = self._put(SET_ALARMS, payload=payload)
        # FIXME: Make sleeptime easier to change??
        time.sleep(HTTP_REST)
        self.fetch_single_alarm(al_id)
  
# ----------------- FETCH DATA AND UPDATE -----------------------#           
    def setup_alarms(self):
        self.fetch_ro_data()
        for alarm, data in self.ro_data.items():
            self._data[alarm] = data

    def fetch_single_alarm(self, al_id):
        payload = {PRFNR: al_id}
        alarm = self._put(ALARMS, payload=payload)
        self._data[al_id].update(alarm)

    def fetch_ro_data(self):
        alarm_status = self._get(path=STATUS)
        alarm_time = self._get(path=TIMES)
        for alarm, enabled in enumerate(alarm_status[PRFEN]):
            alarm_id = alarm + 1
            if alarm_id in self.load_alarms:
                self.ro_data[alarm_id] = dict()
                self.ro_data[alarm_id][PRFVS] = bool(alarm_status[PRFVS][alarm])
                self.ro_data[alarm_id][PRFEN] = bool(enabled)
                self.ro_data[alarm_id][PNAME] = f"alm_{alarm_id}"
                self.ro_data[alarm_id][ALMHR] = alarm_time[ALMHR][alarm]
                self.ro_data[alarm_id][ALMMN] = alarm_time[ALMMN][alarm]
                self.ro_data[alarm_id][DAYNM] = int(alarm_time[DAYNM][alarm])
                self.ro_data[alarm_id][PWEN] = alarm_status[PWRSV][int(alarm*3)]
                self.ro_data[alarm_id][PWHR] = int(alarm_status[PWRSV][int(alarm*3)+1])
                self.ro_data[alarm_id][PWMIN] = int(alarm_status[PWRSV][int(alarm*3)+2])
    
    def update(self):
        self.fetch_ro_data()
        self._data.update(self.ro_data)
        
# ----------------- TESTING IMPROVEMENTS -----------------------#  
    # def change_date(self, al_id):
    #     """This does not seem to be an official option yet"""
    #     pass
            
if __name__ == "__main__":
    from SomneoHttp import SomneoHttp
    http = SomneoHttp()
    a = SomneoAlarmManager(http, [1,2])    


