import wmi

w = wmi.WMI(namespace="root\wmi")
# print(w.Win32_TemperatureProbe()[0].CurrentReading)

# temperature_info = w.MSAcpi_ThermalZoneTemperature()

# print(temperature_info.CurrentTemperature)

# Win32_processor


c = wmi.WMI()

wql = "select * from Win32_VideoController"
for item in c.query(wql):
    print(item)

wql = "SELECT * FROM MSAcpi_ThermalZoneTemperature"
for item in c.query(wql):
    print(item)
