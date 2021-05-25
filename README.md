

```
from pysomneoctrl import SomneoDevice

somneo = SomneoDevice(ip="1.1.1.1")

# Play Audio:
somneo.audio(True, device="fmr")
# Light:
somneo.bedlight(True, brightness=20, ctype=3)
somneo.nightlight(True)

# Sensors:
print(somneo._data[WUSRD])
# Other data:
somneo._data[ALARMS] -> Alarm data
somneo._data[WURLX] -> Relax Breathe data
somneo._data[WUDSK] -> Sunset data
somneo._data[WUPLY] -> Audio data
somneo._data[WUFMR] -> FM Radio data
somneo._data[PRESETS] -> FM Radio Presets

```
