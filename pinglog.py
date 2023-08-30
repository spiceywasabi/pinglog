import csv
import time
import threading
import datetime
import argparse
from ping3 import ping

csv_lock = threading.Lock()

def ping_and_save_result(seq_num, target_host, output_file, timeout, ttl, size, display_output = False, unit="ms"):
    timestamp = datetime.datetime.now()
    status = "received"
    response_time = ping(target_host, timeout=timeout, ttl=ttl, size=size, unit=unit)
    if not response_time:
        status = "timeout"
        response_time = timeout
    with csv_lock:
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, seq_num, status, response_time])
            if display_output:
                print(f"{timestamp} - ICMP PING to {target_host} timeout={timeout}s ttl={ttl} psize={size} icmp_seq={seq_num} response_time={response_time}{unit} status={status}")

def main():
    parser = argparse.ArgumentParser(description="ICMP Ping Tool")
    parser.add_argument("--target", dest="target_host", default="8.8.8.8", help="Target host to ping (default: 8.8.8.8)")
    parser.add_argument("--pings", dest="num_pings", type=int, default=10, help="Number of pings to send (default: 10)")
    parser.add_argument("--timeout", dest="timeout", type=float, default=5, help="Timeout for each ping in seconds (default: 5)")
    parser.add_argument("--ttl", dest="ttl", type=int, default=64, help="Timeout for each ping in seconds (default: 64)")
    parser.add_argument("--size", dest="packet_size", type=int, default=56, help="Size of the ICMP Packet (default: 56)")
    parser.add_argument("--continuous", action="store_true", help="Ping continuously")
    parser.add_argument("--output", dest="output_file", default="ping_results.csv", help="Output CSV file (default: ping_results.csv)")
    parser.add_argument("--print", dest="print_output", action="store_true", help="Print output of each ping")

    args = parser.parse_args()

    target_host = args.target_host
    num_pings = args.num_pings
    output_file = args.output_file
    timeout = args.timeout
    ttl = args.ttl
    packet_size = args.packet_size

    continuous = False
    if args.continuous:
        continuous = True
    display_output = False
    if args.print_output:
        display_output = True

    # Create or overwrite the CSV file with headers
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Sequence Number", "Ping Status", "Response Time (ms)"])

    # Create threads for pinging
    threads = []
    seq_num = 0
 
    if continuous:
        print(f"Ping process started. Sending continuous requests to {target_host} with timeout of {timeout}s and ttl of {ttl}")
    else:
        print(f"Ping process started. Sending {num_pings} requests to {target_host} with timeout of {timeout}s and ttl of {ttl}")
    try:
        while continuous or seq_num < num_pings:
            seq_num += 1
            thread = threading.Thread(target=ping_and_save_result, args=(seq_num, target_host, output_file, timeout, ttl, packet_size, display_output))
            threads.append(thread)
            thread.start()
            time.sleep(timeout)
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        print("Ping results saved to", output_file)
    except KeyboardInterrupt:
        print("Ping process interrupted. Exiting...")

if __name__ == "__main__":
    main()
