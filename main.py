import pyvisa

rm = pyvisa.ResourceManager('@sim')
rm.list_resources()
