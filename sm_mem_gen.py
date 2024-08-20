import matplotlib.pyplot as plt

def create_graphic(kernel_name, block_names, sm_throughputs, memory_throughputs):
    # Set the bar width
    bar_width = 0.4

    # Function to add labels inside the bars
    def add_labels(bars, labels):
        for bar, label in zip(bars, labels):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, height / 2, label, ha='center', va='center', color='white', fontsize=8, fontweight='bold', rotation=90)

    # SM Throughput Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    sm_bars = ax.bar(block_names, sm_throughputs, color='blue', width=bar_width)
    ax.set_title(f'SM Throughput for {kernel_name}')
    ax.set_xlabel('Blocks')
    ax.set_ylabel('SM Throughput (%)')
    ax.set_ylim(0, 100)  # Set y-axis from 0 to 100%
    
    # Add block names inside the columns
    add_labels(sm_bars, block_names)
    
    plt.tight_layout()
    plt.savefig(f'{kernel_name}_sm_throughput.png')
    plt.close()

    # Memory Throughput Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    memory_bars = ax.bar(block_names, memory_throughputs, color='green', width=bar_width)
    ax.set_title(f'Memory Throughput for {kernel_name}')
    ax.set_xlabel('Blocks')
    ax.set_ylabel('Memory Throughput (%)')
    ax.set_ylim(0, 100)  # Set y-axis from 0 to 100%
    
    # Add block names inside the columns
    #add_labels(memory_bars, block_names)
    
    plt.tight_layout()
    plt.savefig(f'{kernel_name}_memory_throughput.png')
    plt.close()

def main():
    kernel_name = input("Enter kernel name: ")
    block_variations = int(input("Enter number of block variations: "))
    
    block_names = []
    sm_throughputs = []
    memory_throughputs = []
    
    for i in range(block_variations):
        block_name = input(f"Enter name for block {i+1}: ")
        sm_throughput = float(input(f"Enter SM throughput for {block_name} (%): "))
        memory_throughput = float(input(f"Enter memory throughput for {block_name} (%): "))
        
        block_names.append(block_name)
        sm_throughputs.append(sm_throughput)
        memory_throughputs.append(memory_throughput)
    
    create_graphic(kernel_name, block_names, sm_throughputs, memory_throughputs)
    print("Graphs have been saved successfully!")

if __name__ == "__main__":
    main()

