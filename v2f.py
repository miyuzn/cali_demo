import os
import pandas as pd
from sensor import read_sensor_data_from_csv, save_sensor_data_to_csv

date = './exp/1113'

# Load fitting parameters for sensors
def load_fitting_parameters(true_recur):
    """
    Load the regression parameters (k, alpha) for each sensor from a CSV file.
    """
    df = pd.read_csv(true_recur)
    params = {row['Sensor']: (row['k'], row['alpha']) for _, row in df.iterrows()}
    return params

# Main function: Batch process CSV files in a directory
def batch_process_csv_files(date):
    """
    Process CSV files in multiple directories, apply transformations (voltage to resistance, resistance to force),
    and save the results to the specified output directory.
    """
    # Define the subdirectories to process
    exps = [f'{date}/23', f'{date}/25', f'{date}/26']
    for i in exps:
        left_recur_results_csv = f"{i}/left.csv"  # Path to left sensor's fitting parameters
        right_recur_results_csv = f"{i}/right.csv"  # Path to right sensor's fitting parameters
        output_dir = f"{i}/force_output"  # Directory for saving output files
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

        # Iterate through CSV files in the current directory and its subdirectories
        for root, _, files in os.walk(i):
            # Skip the output directory to avoid re-processing
            root = os.path.normpath(root)
            if root.startswith(os.path.normpath(output_dir)):
                continue

            for file in files:
                # Process only CSV files, excluding fitting parameter files
                if file.endswith(".csv") and file not in ["left.csv", "right.csv"]:
                    if "left" in file:
                        recur_results_csv = left_recur_results_csv
                    elif "right" in file:
                        recur_results_csv = right_recur_results_csv
                    else:
                        continue
                    
                    # Load fitting parameters
                    params = load_fitting_parameters(recur_results_csv)
                    
                    # Handle file paths
                    sensor_input_path = os.path.join(root, file)
                    relative_path = os.path.relpath(sensor_input_path, ".")
                    relative_path = os.path.relpath(relative_path, start=os.path.commonpath([output_dir, relative_path]))
                    output_path = os.path.join(output_dir, relative_path)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    # Read sensor data from the input file
                    sensor_data_list = read_sensor_data_from_csv(sensor_input_path)
                    
                    # Use methods in the sensor module to transform data
                    for sensor_data in sensor_data_list:
                        sensor_data.sensor_v_to_r()  # Convert voltage to resistance
                        sensor_data.sensor_r_to_f(params)  # Convert resistance to force

                    # Save the transformed data to the output file
                    save_sensor_data_to_csv(sensor_data_list, output_path)
                    print(f"Processed {file} and saved to {output_path}")

# Execute batch processing
if __name__ == "__main__":
    batch_process_csv_files(date)
