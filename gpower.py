import sys
import os
import time
import subprocess
import matplotlib.pyplot as plt

def measure_power_or_temp(executable_with_args):
    start_time = time.time()

    process = subprocess.Popen(executable_with_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_points = []
    measurements = []

    power_supported = False
    label = 'Temperature (C)'

    try:
        while process.poll() is None:
            result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw,temperature.gpu', '--format=csv,noheader,nounits'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8').strip().split(', ')
            power_draw = float(output[0])
            temperature = float(output[1])
            current_time = time.time() - start_time

            if not power_supported and power_draw > 0:
                power_supported = True
                label = 'Power Draw (W)'

            value = power_draw if power_supported else temperature
            time_points.append(current_time)
            measurements.append(value)

            print(f'Time: {current_time:.2f}s, {label}: {value:.2f}')
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()

    return time_points, measurements, label

def plot_measurements(time_points, measurements, label, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, measurements, label=label)
    plt.xlabel('Time (seconds)')
    plt.ylabel(label)
    plt.title(f'GPU {label} during CUDA Execution')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gpower.py <path_to_cuda_executable> [executable_flags]")
        sys.exit(1)

    cuda_executable = sys.argv[1]
    executable_flags = sys.argv[2:]

    if not os.path.isfile(cuda_executable):
        print(f"CUDA executable file not found: {cuda_executable}")
        sys.exit(1)

    executable_with_args = [cuda_executable] + executable_flags
    time_points, measurements, label = measure_power_or_temp(executable_with_args)
    
    output_filename = os.path.basename(cuda_executable).replace('.exe', '.jpeg')
    plot_measurements(time_points, measurements, label, output_filename)

    print(f"GPU {label.lower()} graph saved as: {output_filename}")

