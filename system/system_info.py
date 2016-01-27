#!/usr/bin/python

import platform
import subprocess
import os
import pprint
import glob
import re
import pwd

"""
/proc/cpuinfo as a Python dict
"""
# from __future__ import print_function
from collections import OrderedDict
from collections import namedtuple

# Add any other device pattern to read from
dev_pattern = ['sd.*','mmcblk*']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	

def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

def detect_devs():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print '\t\t\t' + ('Device: {0}, Size: {1} GiB'.format(device, size(device)))

def cpu_info():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    '''

    cpuinfo=OrderedDict()
    procinfo=OrderedDict();

    nprocs = 0;
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo;
                nprocs=nprocs+1;
                # Reset
                procinfo=OrderedDict();
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip();
                else:
                    procinfo[line.split(':')[0].strip()] = '';
            
    return cpuinfo;

def mem_info():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def net_devs():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                float(line[1].split()[8])/(1024.0*1024.0))
    
    return device_data

def process_list():

	pids = []
	for subdir in os.listdir('/proc'):
		if subdir.isdigit():
			pids.append(subdir)
	
	return pids

# Get the users from /etc/passwd
def get_users():
    users = pwd.getpwall()
    for user in users:
        print '\t\t\t' + ('{0}:{1}'.format(user.pw_name, user.pw_shell))
	
def system_info(): 
	print bcolors.OKBLUE + ('-' * 100) + bcolors.ENDC;
	print bcolors.OKGREEN + "Architecture type: \t" + bcolors.ENDC + platform.machine();
	print bcolors.OKGREEN + "Platform system: \t" + bcolors.ENDC + platform.system();
	print bcolors.OKGREEN + "Platform version: \t" + bcolors.ENDC + platform.version();
	print bcolors.OKGREEN + "Distribution name: \t" + bcolors.ENDC + " ".join(platform.linux_distribution());
	print bcolors.OKBLUE + ('-' * 100) + bcolors.ENDC;
	print bcolors.OKGREEN + "Processors: "  + bcolors.ENDC;
	
	cpuinfo = cpu_info();
	
	for processor in cpuinfo.keys():
		print bcolors.OKGREEN + '\t\t\t' + processor + bcolors.ENDC + ': \t' + (cpuinfo[processor]['model name']);
	print '\n';
	
	print bcolors.OKGREEN + "Memory information: " + bcolors.ENDC;
	
	meminfo = mem_info();
	print bcolors.OKGREEN + '\t\t\t' + ('Total memory' + bcolors.ENDC + ': {0}'.format(meminfo['MemTotal'])) + bcolors.ENDC;
	print bcolors.OKGREEN + '\t\t\t' + ('Free memory' + bcolors.ENDC + ': {0}'.format(meminfo['MemFree'])) + bcolors.ENDC;
	print '\n';
	
	
	print bcolors.OKGREEN + "Network information: " + bcolors.ENDC;
	netdevs = net_devs()
	for dev in netdevs.keys():
		print bcolors.OKGREEN + '\t\t\t' + ('{0}'.format(dev) + bcolors.ENDC + ': {0} MiB/received {1} MiB/sent'.format(netdevs[dev].rx, netdevs[dev].tx))
	print '\n';
	
	pids = process_list()
	print bcolors.OKGREEN + "Running processes: " + bcolors.ENDC + '\t' + ('{0}'.format(len(pids))) + '\n';
	for pid in pids:
		command = 'ps -fp ' + str(pid) + ' -o cmd=';
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		(salida, err) = p.communicate()
		print '\t\t\t' + ('{0}'.format(str(pid))) + '\t' + salida[:len(salida)-1] # Ignore last character in the output, line ending
	print '\n';
	
	print bcolors.OKGREEN + "Devices: " + bcolors.ENDC;
	detect_devs();
	print '\n';
	
	print bcolors.OKGREEN + "Users & shells: " + bcolors.ENDC;
	get_users();
	
	print bcolors.OKBLUE + ('-' * 100) + bcolors.ENDC;

if __name__=='__main__':
	os.system("clear");
	system_info();
	print '\n' * 10;