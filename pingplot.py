# Ping Plot Tool (PPT)import os
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import matplotlib.dates as mdates

parser = argparse.ArgumentParser(description='Ping Plotting Tool')
parser.add_argument('--srcdir', type=str, required=True, help='Directory containing CSV files')
parser.add_argument('--datefmt', type=str, default="%Y-%m-%d %H:%M:%S", required=False, help='The Date Format')
args = parser.parse_args()

if not os.path.exists(args.srcdir):
	print(f"Error, the dir {args.srcdir} does not exist")
	sys.exit(1)

csv_files = [file for file in os.listdir(args.srcdir) if file.endswith('.csv')]
plt.figure(figsize=(16, 8))
combined_chart_data = []

for csv_file in csv_files:
    file_path = os.path.join(args.srcdir, csv_file)
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    plt.subplot(len(csv_files) + 1, 1, csv_files.index(csv_file) + 1)
    plt.plot(df['Timestamp'], df['Response Time (ms)'])
    plt.xlabel('Timestamp')
    plt.ylabel('Response Time (ms)')
    plt.title(f'Response Time Over Time - {csv_file}')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(args.datefmt))
    
    combined_chart_data.append((csv_file, df['Timestamp'], df['Response Time (ms)']))

plt.subplot(len(csv_files) + 1, 1, len(csv_files) + 1)

for csv_file, timestamp, response_time in combined_chart_data:
    plt.plot(timestamp, response_time, label=csv_file)

plt.xlabel('Timestamp')
plt.ylabel('Response Time (ms)')
plt.title('Combined Response Time Over Time')
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(args.datefmt))
plt.legend()

combined_chart_path = os.path.join(args.srcdir, 'combined_chart.png')
plt.tight_layout()
plt.savefig(combined_chart_path)

plt.show()
