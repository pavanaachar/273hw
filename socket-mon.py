# Socket-mon.py
#
# Using psutil to implement a network socket monitoring tool that
# can check how many TCP connections are made by a web application.
#
# Author: Pavana Achar
# 
# For CMPE-273, Spring 2017, SJSU

import psutil

PidEntryMap = {}

def KeyFuncNumConn(pid):
    return len(PidEntryMap[pid].connections)

class PidEntry:
    def printConnections(self):
        for conn in self.connections:
            print '"{0}","{1}@{2}","{3}@{4}","{5}"'.format(conn[0], \
                                                           conn[1][0], \
                                                           conn[1][1], \
                                                           conn[2][0], \
                                                           conn[2][1], \
                                                           conn[3])
    def __init__(self, pid):
        self.pid = pid
        self.connections = []

for conn in psutil.net_connections(kind='tcp'):
    pid = conn[6]
    laddr = conn[3]
    raddr = conn[4]
    status = conn[5]

    if laddr and raddr and pid != None:
        if pid not in PidEntryMap.keys():
            PidEntryMap[pid] = PidEntry(pid)
        PidEntryMap[pid].connections.append([pid, laddr, raddr, status])

keys = PidEntryMap.keys()
sortedPids = sorted(keys, key=KeyFuncNumConn, reverse=True)

# Print entries

print '"pid","laddr","raddr","status"'
for pid in sortedPids:
    PidEntryMap[pid].printConnections()

