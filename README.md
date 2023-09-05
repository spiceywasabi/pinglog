
# pinglog
A very simple ICMP Ping tool to log results to CSV and accompanying tool to generate graph data from the collected data. *Useful when you need to provide a log of issues with your ISP.* 

The only dependency is `ping3` which you can install via `pip`

**Note: You may need to run this as `root`.**

<hr>

## Command Arguments

```
ICMP Ping Tool
options:
  -h, --help            show this help message and exit
  --target TARGET_HOST [TARGET_HOST ...]
                        Target host to ping (default: 8.8.8.8)
  --targetfile TARGET_FILE
                        (Optional) New line separated file of target hosts.
  --count NUM_PINGS     Number of pings to send (default: 5)
  --timeout TIMEOUT     Timeout for each ping in seconds (default: 2)
  --timeoutunit {s,ms}  Timeout unit ([s or ms] default: s)
  --ttl TTL             Timeout for each ping in seconds (default: 64)
  --size PACKET_SIZE    Size of the ICMP Packet (default: 56)
  --continuous          Ping continuously
  --output OUTPUT_FILE  Output CSV file (default: ping_results.csv) [@ip@ will be replaced by current target]
  --print               Print output of each ping
```

## Examples


- `pinglog.py --target 1.2.3.4` - Pings to 1.2.3.4 with defaults of 2 second timeout and a total of 5 ICMP ping requests and write to the file `ping_results.csv` all the results 
- `pinglog.py --target 1.2.3.4 4.5.6.7 --print` would print out the ping results with defaults of 2 second timeout and a total of 5 ICMP ping requests and write to the file `ping_results.csv` all the results of both `1.2.3.4` and `4.5.6.7`.
- `pinglog.py --target 192.168.1.2 192.168.3.4 192.168.5.6 --print --output 'ping_results-@ip@.csv' --size 128 --continuous` - This would print out the ping results with defaults of 2 second timeout and continuous ping requests. It would also create an ICMP packet of 128 bytes. It would create a unique file for each IP based on the template provided. 
 
# pinglog

Tool to generate graphs from the results. This tool needs `pandas` and `matplotlib`. 

<hr>

## Command Arguments

This command takes a single required argument `--srcdir`. This is the path to the CSV files generated by `pinglog.py`.

## Example Output

![image](https://github.com/spiceywasabi/pinglog/assets/69662763/6a61fc97-7e69-43de-bf6e-c1fc6b4cf5a4)
