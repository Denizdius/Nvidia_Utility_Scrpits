import sys
import os
import time
import subprocess
import matplotlib.pyplot as plt

def measure_sm_utilization(executable_with_args, cooldown_period=5):
    start_time = time.time()

    process = subprocess.Popen(executable_with_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_points = []
    sm_utilization_data = []

    try:
        while process.poll() is None:
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sm_utilization = float(result.stdout.decode('utf-8').strip())
            current_time = time.time() - start_time

            time_points.append(current_time)
            sm_utilization_data.append(sm_utilization)

            print(f'Time: {current_time:.2f}s, SM Utilization (%): {sm_utilization}')
            time.sleep(1)
        
        # Cooldown period after the process finishes
        end_time = time.time()
        while time.time() - end_time < cooldown_period:
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sm_utilization = float(result.stdout.decode('utf-8').strip())
            current_time = time.time() - start_time

            time_points.append(current_time)
            sm_utilization_data.append(sm_utilization)

            print(f'Time: {current_time:.2f}s, SM Utilization (%): {sm_utilization}')
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate()

    return time_points, sm_utilization_data

def plot_sm_utilization(time_points, sm_utilization_data, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, sm_utilization_data, label='SM Utilization (%)', marker='o')
    plt.xlabel('Time (seconds)')
    plt.ylabel('SM Utilization (%)')
    plt.title('SM Utilization Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sm_utilization.py <path_to_cuda_executable> [executable_flags]")
        sys.exit(1)

    cuda_executable = sys.argv[1]
    executable_flags = sys.argv[2:]

    if not os.path.isfile(cuda_executable):
        print(f"CUDA executable file not found: {cuda_executable}")
        sys.exit(1)

    executable_with_args = [cuda_executable] + executable_flags
    time_points, sm_utilization_data = measure_sm_utilization(executable_with_args)
    
    output_filename = os.path.basename(cuda_executable).replace('.exe', '_sm_utilization.jpeg')
    plot_sm_utilization(time_points, sm_utilization_data, output_filename)

    print(f"SM utilization graph saved as: {output_filename}")

