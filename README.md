# Phillips Somneo
This is a work in progress...

This library can do the following things:
Connect to Somneo with ip, or msearch, control audio, alarms, lights and other settings.
It can also fetch sensor and settings data.

Below are a few examples of what you can do with this library.
This is not all, but I will update the readme soon.


```
from pysomneoctrl import SomneoDevice
somneo = SomneoDevice(ip="1.1.1.1")
```

Play Audio:
```
somneo.audio(True, device="fmr")
```
Light:
```
somneo.bedlight(True, brightness=20, ctype=3)
somneo.nightlight(True)
```

Sensors:
```
print(somneo._data[WUSRD])
```
Other data:
```
somneo._data[ALARMS] -> Alarm data
somneo._data[WURLX] -> Relax Breathe data
somneo._data[WUDSK] -> Sunset data
somneo._data[WUPLY] -> Audio data
somneo._data[WUFMR] -> FM Radio data
somneo._data[PRESETS] -> FM Radio Presets

```
