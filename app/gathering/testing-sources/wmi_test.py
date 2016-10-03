import wmi

w = wmi.WMI(namespace="root\wmi")
#print(w.Win32_TemperatureProbe()[0].CurrentReading)

#temperature_info = w.MSAcpi_ThermalZoneTemperature()

#print(temperature_info.CurrentTemperature)



c = wmi.WMI()
wql = "SELECT * FROM MSAcpi_ThermalZoneTemperature"
for item in c.query(wql):
    print(item)


wmic path win32_processor get CurrentClockSpeed, MaxClockSpeed, Name, NumberOfCores, NumberOfLogicalProcessors

