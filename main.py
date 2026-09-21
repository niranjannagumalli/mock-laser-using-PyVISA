import pyvisa
import streamlit as st


# st.set_page_config(layout="wide")
# st.title("Fake Laser: Demonstration")

#initiliazing the simulator using the laser.yaml file
# @st.cache_resource
def connect_instrument():
    rm = pyvisa.ResourceManager('laser.yaml@sim')
    inst = rm.open_resource('ASRL1::INSTR')
    inst.write_termination = '\n'
    inst.read_termination = '\n'
    
    return inst

instrument = connect_instrument()

# st.success(f"Connected to: {instrument.query('*IDN?')}")
print(f"Connected to: {instrument.query('*IDN?')}")

readVoltage = float(instrument.query("VOLT?"))
print(readVoltage)