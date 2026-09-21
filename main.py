import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.optimize import curve_fit    


class LaserController:
    """
        This is the class which handles all the access with the laser
    """

    def __init__(self, resource_string = 'ASRL1::INSTR', backend = "laser.yaml@sim", ):
        self.rm = pyvisa.ResourceManager(backend)
        self.inst = self.rm.open_resource(resource_string)
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'    

    def identify(self):
        return self.inst.query('*IDN?')
    
    def setVoltage(self, voltage: float):
        
        self.inst.write(f"VOLT {voltage:.3f}")

    def getVoltage(self):
        print(self.inst.query("VOLT?"))
        return float(self.inst.query("VOLT?"))

    def close(self):
        self.inst.close()


def readSimulatedDetector(voltage, threshold= 2.0, efficiency=500):
    '''
    simulates a photon detectors response with some added noise
    '''
    photons = 0
    if voltage < 2.0:
        #somebackground noise
        photons = np.random.normal(10,3)
    else:
        photons = ((voltage - 2.0)* 500) + np.random.normal(0,20)
    return photons



def linear_model(x, m, b):
    return m * x + b

def calculateEfficiency(df):

    active_region = df[df['Voltage_V'] > 2.0]
    popt, _ = curve_fit(linear_model, active_region['Voltage_V'], active_region['Photon_Counts'])
    
    slope, intercept = popt
    return slope, intercept


def main():
    laser = LaserController(
        resource_string ='ASRL1::INSTR',
        backend         ='laser.yaml@sim'
    )
    print(laser.identify())

    voltages = np.linspace(0.0, 5.0, 25)
    measured_photons = []

    plt.ion()
    fig, ax = plt.subplots(figsize = (8,5))
    line, = ax.plot([], [], 'bo-', label='Live Data')
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1600)
    ax.set_xlabel("Applied Voltage (V)")
    ax.set_ylabel("Simulated Photon Counts")
    ax.set_title("Real-Time Photonic Measurement")
    ax.grid(True, alpha=0.3)

    print("-"*60)
    print("Initiating voltage sweep")
    print("-"*60)

    # now we slowly set the voltage and read the voltage back(ik its dumb) and keep increasing. 
    # for everytime we read teh value back, we calculate the number of photons which could have been emitted + some noise. 
    
    for voltage in voltages:
        #set the voltage
        laser.setVoltage(voltage)
        print(type(voltage))

        # we simulate hardware delay, XD
        time.sleep(0.1)

        #now we read it back
        readVoltage = laser.getVoltage()

        #simulate a real laser which is linear above a certain voltage. 
        photons = readSimulatedDetector(voltage=readVoltage)    

        measured_photons.append(photons)

        line.set_xdata(voltages[:len(measured_photons)])
        line.set_ydata(measured_photons)
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    #we close the connection to laser
    laser.close()
        
    #now lets store the data in a csv file
    df = pd.DataFrame({
        "Voltage_V": voltages,
        "Photon_Counts": measured_photons
    })
    df.to_csv(f"experiment_log_{time.time()}.csv", index=False)
    print("\nData saved to experiment_log_<timestamp>.csv")    

    
    # analysis
    slope, intercept = calculateEfficiency(df)
    print(f"Analysis Complete: Laser efficiency (slope) is {slope:.2f} photons/Volt")

    # Plot the fit
    active_v = df[df['Voltage_V'] > 2.0]['Voltage_V']
    ax.plot(active_v, slope * active_v + intercept, 'r--', linewidth=2, label=f'SciPy Fit (m={slope:.0f})')
    ax.legend()
    plt.show()    


if __name__ == "__main__":
    main()