# README

## English

### Overview

This set of programs is designed to calibrate sensors embedded in shoe insoles. Each sensor measures changes in resistance corresponding to applied force, but their raw outputs need to be converted into meaningful force (pressure) values. By using known weights (masses) as references, the system can establish a mathematical relationship between the raw sensor signals and the actual force, enabling accurate calibration and subsequent force measurements.

### Calibration Principle

1. **Data Acquisition (with Known Loads):**  
   To calibrate each sensor, we begin by recording data from the shoe insole sensors under known loads. Typically, two sets of masses are used (e.g., ~500g and ~1kg). By placing these known weights on the insole sensors, we can measure how the sensor voltages change with different applied forces.

2. **Signal Processing:**  
   The raw voltage data collected from the sensors are first filtered and processed to identify a stable “activation” period. During this period, the sensor readings have stabilized under the applied load. The processed data extracts a characteristic voltage (or resistance) value representing the sensor’s response to that specific load.

3. **Regression and Model Fitting:**  
   Using pairs of (Force, Resistance) data points (collected from the two known weights), a mathematical model is fitted to each sensor. Typically, a power-law (F = k * R^α or R = k * F^α) or similar regression model is determined for each sensor. This model transforms a raw sensor reading into a calibrated force measurement.

4. **Application to Experimental Data:**  
   Once the model parameters (k and α) are known, any new data recorded by the sensors can be instantly converted from voltage/resistance to force. This allows subsequent experiments, conducted without known calibration masses, to yield accurate force measurements from the sensors.

### Program Usage Workflow

1. **Record Sensor Data with Known Weights (receive/visualization.py):**  
   Before calibration, you must record sensor output data while applying known reference loads:
   - Use `receive/visualization.py` to log sensor data as you apply two distinct known weights to each sensor.
   - Ensure that you have recorded multiple trials (e.g., `500g-1.csv`, `500g-2.csv`, `1kg-1.csv`, `1kg-2.csv`) for more reliable results.

2. **Run the Calibration Procedure (cali_auto.py):**  
   After collecting the raw data:
   - Use the `cali_auto` program to process these CSV files.
   - The program will automatically apply filtering, identify stable activation periods, average the results for each known load, and then perform regression to determine the calibration parameters (k and α) for each sensor.
   - At the end of this process, `cali_auto` generates a regression parameter file (e.g., `recur_results.csv`) which holds the calibration coefficients for each sensor.

3. **Prepare Experimental Data for Conversion:**  
   Once the sensors are calibrated, place the experimental data (recorded without the known masses, but under real test conditions) into the appropriate folder. Ensure that the folder structure and file naming conventions match those expected by the program (e.g., left or right insole data placed in corresponding directories).

4. **Convert Experimental Voltage Data to Force (v2f.py):**  
   Finally, run the `v2f.py` script. This script:
   - Loads the previously determined calibration parameters.
   - Reads your new, uncalibrated sensor data.
   - Converts the voltage/resistance values into force values using the fitted model.
   - Outputs the calibrated force measurements to a CSV file.

### Summary of Steps

1. **Record reference data:**  
   `receive/visualization.py` → Generate CSV files with known loads (e.g., 500g, 1000g).

2. **Calibrate sensors:**  
   `cali_auto.py` → Reads the CSV files with known loads, computes calibration parameters (k, α).

3. **Apply calibration to experimental data:**  
   Place your test data (from the correct shoe insole) into the proper folder.

4. **Convert voltage to force:**  
   `v2f.py` → Uses the calibration parameters to convert sensor readings in your experimental data into force.

By following this sequence, you ensure that all future measurements from the insoles are accurately translated into meaningful force values, making your experiments and analyses more reliable and reproducible.

---
