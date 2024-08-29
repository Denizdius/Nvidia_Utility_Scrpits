import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file with tab-separated values
file_path = '~/Documents/power_log.csv'
df = pd.read_csv(file_path, sep='\t')

# Extracting the relevant columns (Milliseconds, Max Power, Power Draw)
df_cleaned = df.iloc[:, [0, 2, 4]]

# Renaming the columns for clarity
df_cleaned.columns = ['Milliseconds', 'Max Power', 'Power Draw']

# Converting the data to numeric, if not already
df_cleaned['Milliseconds'] = pd.to_numeric(df_cleaned['Milliseconds'], errors='coerce')
df_cleaned['Max Power'] = pd.to_numeric(df_cleaned['Max Power'], errors='coerce')
df_cleaned['Power Draw'] = pd.to_numeric(df_cleaned['Power Draw'], errors='coerce')

# Dropping rows with any NaN values (if present)
df_cleaned = df_cleaned.dropna()

# Plotting the power draw against milliseconds
plt.figure(figsize=(10, 6))
plt.plot(df_cleaned['Milliseconds'], df_cleaned['Power Draw'], label='Power Draw', color='blue')
plt.xlabel('Time (Milliseconds)')
plt.ylabel('Power Draw (W)')
plt.title('Power Draw Over Time')
plt.grid(True)
plt.legend()
plt.show()
