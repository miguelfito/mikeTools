#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

class terminalColors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
try:
    remoteServer    = raw_input("Enter a remote host to scan: " + terminalColors.BLUE)
    remoteServerIP  = socket.gethostbyname(remoteServer)
except socket.gaierror:
    print terminalColors.END, 'Hostname could not be resolved. Exiting'
    sys.exit(1)

# Print a nice banner with information on which host we are about to scan
print terminalColors.END + "-" * 60
print "Please wait, scanning remote host", terminalColors.YELLOW + remoteServerIP + terminalColors.END
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

try:
    for port in range(1,1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print("Port {0}: \t".format(port) + terminalColors.GREEN + " Open" + terminalColors.END)
        # else:
        # 	print("Port {0}: \t Closed".format(port))
        sock.close()

except KeyboardInterrupt:
    print terminalColors.END, "You pressed Ctrl+C"
    sys.exit(0)

except socket.gaierror:
    print terminalColors.END, 'Hostname could not be resolved. Exiting'
    sys.exit(1)

except socket.error:
    print terminalColors.END, "Couldn't connect to server"
    sys.exit(1)

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

print "-" * 60
# Printing the information to screen
print 'Scanning Completed in: ', terminalColors.MAGENTA + str(total) + terminalColors.END
print "-" * 60
