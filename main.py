import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.optimize import curve_fit    


def run_experiment():
    rm = pyvisa.ResourceManager('laser.yaml@sim')
    inst = rm.open_resource('ASRL1::INSTR')
    inst.write_termination = '\n'
    inst.read_termination = '\n'
    print(f"Connected to: {inst.query('*IDN?')}")   

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
        inst.write(f"VOLT {voltage:.3f}")

        # we simulate hardware delay, XD
        time.sleep(0.1)

        #now we read it back
        read_voltage = float(inst.query("VOLT?"))

        #simulate a real laser which is linear above a certain voltage. 
        if read_voltage < 2.0:
            #somebackground noise
            photons = np.random.normal(10,3)
        else:
            photons = ((read_voltage - 2.0)* 500) + np.random.normal(0,20)

        measured_photons.append(photons)

        line.set_xdata(voltages[:len(measured_photons)])
        line.set_ydata(measured_photons)
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    # plt.show()

    #now lets store the data in a csv file
    df = pd.DataFrame({
        "Voltage_V": voltages,
        "Photon_Counts": measured_photons
    })
    df.to_csv(f"experiment_log_{time.time()}.csv", index=False)
    print("\nData saved to experiment_log.csv")

    def linear_model(x, m, b):
        return m * x + b

    active_region = df[df['Voltage_V'] > 2.0]
    popt, _ = curve_fit(linear_model, active_region['Voltage_V'], active_region['Photon_Counts'])
    
    slope, intercept = popt
    print(f"Analysis Complete: Laser efficiency (slope) is {slope:.2f} photons/Volt")

    # Plot the SciPy fit over the raw data
    ax.plot(active_region['Voltage_V'], linear_model(active_region['Voltage_V'], slope, intercept), 
            'r--', linewidth=2, label=f'SciPy Fit (m={slope:.0f})')
    ax.legend()

    plt.show() # Keep the final plot window open

    return inst

instrument = run_experiment()

