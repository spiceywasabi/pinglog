import os
import sys
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
        response_time = -10 # instead of timeout, so we see the difference
    with csv_lock:
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, seq_num, status, response_time])
            if display_output:
                print(f"{timestamp} - ICMP PING to {target_host} timeout={timeout} ttl={ttl} psize={size} icmp_seq={seq_num} response_time={response_time} status={status}")


def main():
    parser = argparse.ArgumentParser(description="ICMP Ping Tool")
    parser.add_argument("--target", dest="target_host", nargs='+', required=False, default="8.8.8.8", help="Target host to ping (default: 8.8.8.8)")
    parser.add_argument("--targetfile", dest="target_file", type=argparse.FileType('r'), required=False, help="(Optional) New line separated file of target hosts.")
    parser.add_argument("--count", dest="num_pings", type=int, default=5, help="Number of pings to send (default: 5)")
    parser.add_argument("--timeout", dest="timeout", type=float, default=2, help="Timeout for each ping in seconds (default: 2)")
    parser.add_argument('--timeoutunit', dest="timeout_time_unit", required=False, default="s", choices=['s', 'ms'], help='Timeout unit ([s or ms] default: s)')
    parser.add_argument("--ttl", dest="ttl", type=float, default=64, help="Timeout for each ping in seconds (default: 64)")
    parser.add_argument("--size", dest="packet_size", type=float, default=56, help="Size of the ICMP Packet (default: 56)")
    parser.add_argument("--continuous", action="store_true", help="Ping continuously")
    parser.add_argument("--output", dest="output_file", default="ping_results.csv", help="Output CSV file (default: ping_results.csv) [@ip@ will be replaced by current target]")
    parser.add_argument("--print", dest="print_output", action="store_true", help="Print output of each ping")

    args = parser.parse_args()

    target_hosts = args.target_host
    num_pings = args.num_pings
    timeout = args.timeout
    timeout_unit = args.timeout_time_unit
    ttl = args.ttl
    packet_size = args.packet_size

    continuous = False
    if args.continuous:
        continuous = True
    display_output = False
    if args.print_output:
        display_output = True

    # ensure we always have some time of list
    # either from --target or from a file
    target_hosts = [args.target_host]  
    if isinstance(target_hosts, list):
        target_hosts = args.target_host 
    if args.target_file:
        try:
            lines = args.target_file.readlines()
            target_hosts = [line.strip().strip() for line in lines]
            print(f"Using target host list file {args.target_file.name} instead of --target arguments. Found {len(target_hosts)} hosts to ping.")
        except Exception as e:
                print(f"Error when reading target list file {args.target_file.name}, cannot continue: ", e)
                sys.exit(1)

    for ip_target in target_hosts:
        output_file = str(args.output_file).strip().replace("@ip@",ip_target)
        if continuous:
            print(f"Ping process started. Sending continuous requests to {ip_target} with timeout of {timeout}{timeout_unit} and ttl of {ttl}")
        else:
            print(f"Ping process started. Sending {num_pings} requests to {ip_target} with timeout of {timeout}{timeout_unit} and ttl of {ttl}")
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Sequence Number", "Ping Status", "Response Time (ms)"])
    
    if timeout_unit == "ms":
        timeout = float(timeout)/1000.0

    threads = []
    seq_num = 0

    try:
        while continuous or seq_num < num_pings:
            seq_num += 1
            for ip_target in target_hosts:
                output_file = str(args.output_file).strip().replace("@ip@",ip_target)
                thread = threading.Thread(target=ping_and_save_result, args=(seq_num, ip_target, output_file, timeout, ttl, packet_size, display_output))
                threads.append(thread)
                thread.start()
                # Wait for all threads to finish
                for thread in threads:
                    thread.join()
            time.sleep(timeout)

        print("Ping results saved to", output_file)
    except KeyboardInterrupt:
        print("Ping process interrupted. Exiting gracefully.")

if __name__ == "__main__":
    main()
