#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import random

def read_driver_file(file):

    fpin = open(file, 'r')
    header = fpin.readline()
    vars = header.split(',')
    dNames = []
    dPoints = []
    dCost = []
    tNames = []
    tPoints = []
    tCost = []
    
    for line in fpin:
        aline = line.split(',')
        if (aline[0] == 'd'):
            dNames.append(aline[1])
            dPoints.append(float(aline[2]))
            dCost.append(float(aline[3]))
        else:
            tNames.append(aline[1])
            tPoints.append(float(aline[2]))
            tCost.append(float(aline[3]))
    drivers = {
        'Names': dNames,
        'Points': np.array(dPoints),
        'Cost': np.array(dCost),
        'Left': range(len(dNames))}
    teams = {
        'Names': tNames,
        'Points': np.array(tPoints),
        'Cost': np.array(tCost),
        'Left': range(len(tNames))}
    fpin.close()
    
    return drivers, teams

def pick_one(allThings, cap):

    # Use the Left array to figure out who is left
    nThings = len(allThings['Left'])

    iAvail_ = []
    for i in allThings['Left']:
        if (allThings['Cost'][i] <= cap):
            iAvail_.append(i)
    nAvail = len(iAvail_)
    print('Number still available : ', nAvail)
    iChoose = -1
    if (nAvail > 0):
        if (nAvail == 1):
            iChoose = iAvail_[0]
        else:
            iChoose = random.choice(iAvail_)
    print('Choice : ', iChoose)
    return iChoose

def pick_n(allThings, cap, nPick):

    iList = []
    for iPick in range(nPick):
        iChoose = pick_one(allThings, cap)
        if (iChoose > -1):
            print('Pick : ', iChoose, allThings['Names'][iChoose])
            cap = cap - allThings['Cost'][iChoose]
            print('  -> New Cap : ', cap)
            j = 0
            left = np.zeros(len(allThings['Left'])-1)
            for i in allThings['Left']:
                if (i != iChoose):
                    left[j] = i
                    j += 1
            allThings['Left'] = left.astype(int)
            print(allThings['Left'])
        iList.append(iChoose)
    return iList, cap
    
            
file = 'drivers.csv'
allDrivers, allTeams = read_driver_file(file)

cap = 100.0
nTeams = 2
nDrivers = 5

validChoice = False
while (not validChoice):
    iDrivers, newCap = pick_n(allDrivers, cap, nDrivers)
    iTeams, leftCap = pick_n(allTeams, newCap, nTeams)

    print(iTeams)
    if ((np.min(iDrivers) > -1) and \
        (np.min(iTeams) > -1)):
        validChoice = True
