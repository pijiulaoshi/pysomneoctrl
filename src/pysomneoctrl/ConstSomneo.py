#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: @pijiulaoshi
"""

from .paths import *
#from paths import *

HTTP_REST = 0.6
TIMEOUT = float(HTTP_REST)
DEFAULT_LOAD_ALMS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
DEFAULT_LOAD_COMP = ["alarms", "audio", "winddown"]

# SETTINGS LABELS USED BY SOMNEO
# --- GENERAL --- #
ONOFF = "onoff"
DEMO = "tempy"
#LIGHT SETTINGS
CURVE = "curve"
DURAT = "durat"
CTYPE = "ctype"
# SOUND SETTINGS
SNDDV = "snddv"
SNDCH = "sndch"
SNDLV = "sndlv"
SDVOL = "sdvol"
SNDSS = "sndss"
# SOUND DEVICES
AUX = "aux"
FMR = "fmr"
WUS = "wus"
DUS = "dus"
OFF = "off"
# --- CUSTOM --- #
ALARM_DATA = "alarms"
PRESETS = "fm_presets"



# --- SPECIFIC ---#
# ALARMS
PRFNR = "prfnr"
PRFEN = "prfen"
PRFVS = "prfvs"
PNAME = "pname"
DAYNM = "daynm"
ALMHR = "almhr"
ALMMN = "almmn"
PWRSZ = "pwrsz"
PSZHR = "pszhr"
PSZMN = "pszmn"
PWRSV = "pwrsv"
AYEAR = "ayear"
AMNTH = "amnth"
ALDAY = "alday"



# FIXME: Replace use of constants below with the original somneo ones, to reduce variables
#POWERWAKE
PWEN = "pwrsz"
PWHR = "pszhr"
PWMIN = "pszmn"
PWRSV = "pwrsv"
#DATE
YEAR = "ayear"
MNTH = "amnth"
DAY = "alday"

# SETTINGS MENU
DSPON = "dspon"
DSPBR = "brght"


SOMNEO_DATA_DICT = {
    WUSRD:{}, 
    WULGT:{}, 
    WUSTS:{}, 
    WUNGT:{}, 
    ALARM_DATA:{},  
    }

SOMNEO_DATA_DICT2 = {
    WUSRD:{}, 
    WULGT:{}, 
    WUSTS:{}, 
    WUNGT:{}, 
    WURLX:{}, 
    WUDSK:{}, 
    ALARM_DATA:{},
    WUPLY:{},
    WUFMR:{},   
    }

WEEKDAYS_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAYS = {
    "Never":0,
    "Mon":2,
    "Tue":4,
    "Wed":8,
    "Thu":16,
    "Fri":32,
    "Sat":64,
    "Sun":128,
    "Everyday":254
    }

#FRONTEND
CTYPES_I2N = {
    0: "sunny_day", 
    1: "island_red", 
    2: "nordic_white"
    }
WUSCH = {
    1:"forrest_birds", 
    2:"summer_birds", 
    3:"buddha_wakeup", 
    4:"morning_alps", 
    5:"yoga_harmony", 
    6:"nepal_bowls", 
    7:"summer_lake", 
    8:"ocean_waves"
    }
SND_DEVICES = {
    WUS:"wakeup_sounds",
    DUS:"sunset_sounds",
    AUX:"audio_jack",
    FMR:"fm_radio",
    OFF:"no_sound",
    }

ALMON = "alarm_enabled"
ATIME = "alarm_time"
AWDAY = "week_days"
PWRON = "powerwake_enabled"
PTIME = "powerwake_time"
TRLT = {CURVE: "brightness", DURAT: "duration", PRFEN: ALMON}
#TRLT_VAL = {CTYPE:["light_type",CTYPES_I2N], SNDDV:["sound_device", SND_DEVICES]}
CP_LIST = {CURVE: "brightness", DURAT: "duration"}


# ---- MOVE? DELETE? ---- #
CTYPES_N2I = {
    "sunny_day": 0, 
    "island_red": 1, 
    "nordic_white": 2
    }



# ---- TRASH ----- #
# # LABELS
# STTS = "settings"
# SENS = "sensors"
# LGHT = "lights"
# DUSK = "sunset"
# BTIM = "bedtime"
# RLX = "relax"


# # LOCATION LABELS USED BY SOMNEO
# L = {
#      STTS: "wusts",
#      SENS: "wusrd",
#      LGHT: "wulgt",
#      DUSK: "wudsk",
#      BTIM: "wungt",
#      RLX: "wurlx",
#      }
