<!-- # pyvisa-playground -->
<h1 align="center"> Mock laser controller</h1>

## Project Description
### A simple description
This is a project sets up a fake laser which is connected to my computer. I perform a voltage sweep, (set a starting voltage, increase it by small steps till i reach target voltage). Everytime i receive the current voltage, to simulate real conditions, I add some noise. I calculate the number of photons which could have been emitted with that voltage, and plot those. I try to extract the slope of the graph just from the data which I plotted. 

### More technical description

This project implements a modular, hardware driver(LaserController) to manage SCPI-based communication over a virtual serial port. The experimental sequence runs a continous parameter sweep while polling the instrument state. To emulate realistic hardware, the simulated detector response includes a threshold of 2 V, below only Gaussian noise is registered. Above the threshold, the number of photons scales linearly with the voltage set. Realtime visualization is handled using matplotlib and SciPy predicts the slope of the data(photons vs volt) above threshold. 


## Libraries used
1. pyVISA-sim: to mock an actual laser
2. pyVISA: to connect with the mock laser
3. NumPy: to generate values for voltage sweep and to insert some noise 
4. Pandas: to store the data in a proper way (i stored them in CSVs)
5. SciPy: to calculate the slope of the data from the stored data(voltage, number of photons observed)
6. Matplotlib: for real time visualization of the data generated. 


## Installation & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
and then run the main program.
```
python3 main.py
```

An example plot
<img src="examplePlot.png" alt="Simulated Laser Threshold Plot" width="600"/>