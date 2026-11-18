import csv
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

CSV_FILE = 'temperature_readings.csv'
GRAPH_FILE = 'temperature_graph.png'
WARNING_THRESHOLD = 35.0

def generate_simulated_data(filename, num_readings=50):
    print(f"[*] Generating {num_readings} simulated IoT temperature readings...")
    start_time = datetime.now() - timedelta(hours=num_readings)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Temperature_C'])
        for i in range(num_readings):
            timestamp = (start_time + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
            if i == 12:
                temp = "INVALID_READING"
            elif i == 28:
                temp = ""
            elif i == 42:
                temp = None
            else:
                temp = round(random.uniform(20.0, 42.0), 2)
            writer.writerow([timestamp, temp])
    print(f"[+] Data successfully saved to {filename}\n")

def process_temperature_data(filename):
    timestamps = []
    temperatures = []
    valid_temperatures = []
    print(f"[*] Reading data from {filename} and analyzing...")
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row_idx, row in enumerate(reader, start=1):
                if len(row) < 2:
                    continue
                timestamp, temp_str = row[0], row[1]
                timestamps.append(timestamp)
                try:
                    if temp_str == "" or temp_str is None or temp_str == "None":
                        raise ValueError("Missing value detected.")
                    temp_val = float(temp_str)
                    valid_temperatures.append(temp_val)
                    temperatures.append(temp_val)
                    if temp_val > WARNING_THRESHOLD:
                        print(f"⚠️ [WARNING] High Temp Alert! [{timestamp}] Temp: {temp_val}°C exceeds threshold!")
                except (ValueError, TypeError) as e:
                    print(f"❌ [HANDLED] Row {row_idx} ({timestamp}): Invalid data '{temp_str}' skipped.")
                    temperatures.append(None)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return [], []
    if valid_temperatures:
        avg_temp = sum(valid_temperatures) / len(valid_temperatures)
        print(f"\nAverage Temperature: {avg_temp:.2f}°C\n")
    return timestamps, temperatures

def plot_temperature_data(timestamps, temperatures, graph_filename):
    valid_data = [(ts, t) for ts, t in zip(timestamps, temperatures) if t is not None]
    if not valid_data:
        return
    plot_ts, plot_temp = zip(*valid_data)
    x_labels = [ts.split(' ')[1] for ts in plot_ts]
    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, plot_temp, marker='o', linestyle='-', color='teal', label='Sensor Temperature (°C)')
    plt.axhline(y=WARNING_THRESHOLD, color='crimson', linestyle='--', label=f'Warning Threshold ({WARNING_THRESHOLD}°C)')
    plt.title('Python-Based IoT Temperature Monitoring System')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(graph_filename)
    plt.show()

if __name__ == "__main__":
    generate_simulated_data(CSV_FILE, 50)
    ts, temps = process_temperature_data(CSV_FILE)
    plot_temperature_data(ts, temps, GRAPH_FILE)
