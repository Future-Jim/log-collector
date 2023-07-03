#!/usr/bin/env python3

import os
import subprocess
import sys
import time

def sshcmd(host, command, user = None):
    ''' Runs ssh command via subprocess. Requires .ssh/config to be configured
    Args:
        host: target host to send command to
        command: command to run on host
        user: (optional) if keys are not present, user may be required
        stdin: (optional) overrides sys.stdin
        check: (optional) checks return code and raises error if code != 0

    Returns
        subprocess.CompletedProcess object
    '''

    where = "%s" % host if user is None else "%s@%s" %(user, host)
    result = subprocess.run(["ssh", where, command],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    return result
    

def awkcmd(awk_input, command):
    ''' Runs awk command via subprocess. 
    Args:
        awk_input: input to be processed with awk
        command: command to run with awk (i.e. '{print $0}')

    Returns
        subprocess.CompletedProcess object
    '''

    result = subprocess.run(["awk", command],
                            input=awk_input,
                            capture_output=True,
                        text=True,
                            check=True)
    return result

def grepcmd(grep_input, command):
    ''' Runs grep command via subprocess. 
    Args:
        grep_input: input to be processed with grep
        command: command to run with grep (i.e. Regex)
    
    Returns
        subprocess.CompletedProcess object
    '''
    result = subprocess.run(["grep", "-E", command],
                            input=grep_input,
                            capture_output=True,
                            text=True,
                            check=True)
    return result

def file_write(file_input, filename, logs_path):
    ''' Writes to file with specified filename
    Args:
        file_input: data to be written to file
        filename: name of logfile
    Returns:
        None
     
    '''

    os.chdir(logs_path)
    with open(filename, "a") as o:
        o.write("LOGGING: " + time.strftime("%I:%M%p on %B %d, %Y\n"))
        o.write("HOST %s: " % i)
        o.writelines(file_input)
        o.write("\n")
        

def log_path():
    path = os.path.abspath("logs")
    if not os.path.exists(path):
        os.makedirs(path)
    return path
        
if __name__ == '__main__':
    logs_path = log_path()
    C1= ' cd /var/log && cat SSH.log'
    C2= '{print $0}'
    C3= '([0-9]{1,3}[\.]){3}(89)'
    LOGNAME="ssh-logs"
    filename = (LOGNAME+"-"+time.strftime("%B-%d-%Y-%H:%M-%Z"+".log\n"))

    with open("server_list.txt", "r") as f:
        lines = f.readlines()
        for i in lines:
          
            p1 = sshcmd(i.strip(), C1)
            p2 = awkcmd(p1.stdout, C2)
            p3 = grepcmd(p2.stdout, C3)
            p4 = file_write(p3.stdout, filename, logs_path)


