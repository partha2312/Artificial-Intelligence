#!/usr/bin/python3

# Class:     CSCI 680-B3
# Program:   Assignment 5
# Author:    Parthasarathy Krishnamurthy
# Z-number:  z1729253
# Date Due:  04/02/15
# Purpose:   To implement BFS, DFS, DFID and A* search algorithms
# Execution: python3 hw5.py

import re
from collections import deque

franceRoadMap = 'france-roads1.txt'
franceLong = 'france-long1.txt'

regEx = r"[a-zA-Z]*$"

dictMap = {}
dictLong = {}

def populateLists():
    try:
        mainKey=''
        tempDict={}
        file = open(franceRoadMap, "r")
        for line in file:
            if re.match(regEx, line[0]) and line[0] != '\n':
                line = line.rstrip('\n')
                if ':' in line:
                    if mainKey != '':
                        dictMap[mainKey]=tempDict
                        tempDict={}
                    mainKey=line.replace(':','')
                else:
                    city,dist = line.split(' ')
                    tempDict[city]=dist
        dictMap[mainKey]=tempDict
    except(OSError, IOError):
        print("File",  franceRoadMap, " not found")
        exit()    
    try:
        file = open(franceLong, "r")
        for line in file:
            if re.match(regEx, line[0]) and line[0] != '\n':
                line = line.rstrip('\n')
                city, longi = line.split(' ')
                dictLong[city]=longi
    except(OSError, IOError):
        print("File",  franceLong, " not found")
        exit()

def check(city, stack):
    if [item for item in stack if item[0]==city]:
        return False
    return True

def getBestNode(openList):
    min = (float("inf"))
    bestNode=None
    for item in openList:
        if item[3] < min:
            min = item[3]
            bestNode=item
    return bestNode

def printPath(dictMap):
    flag=True
    city = toCity
    resList=[]
    while flag:
        if city == fromCity:
            resList.append(city)
            flag = False
            continue
        resList.append(city)
        city = dictMap[city]
    return resList

def BFS(fromCity, toCity):
    print('BFS:')
    count=0
    pathHistory={}
    pathList = []
    que = deque([])
    que.append(fromCity)
    while len(que) != 0:
        dest = que.popleft()
        print('Expanding ', dest)
        if dest == toCity:
            pathList.append(dest)
            return pathHistory,count
        tempList = dictMap[dest.upper()]
        tempList = sorted(tempList)
        print("Children are ", end=" ")
        print(tempList)
        for city in tempList:
            if city not in pathHistory.keys():
                pathHistory[city] = dest
        print("New children are ", end=" ")
        for city in tempList:
            if city not in que and city not in pathList:
                que.append(city)
                count+=1
                print(city, end=" ")
        print()
        print("Open list is ", end=" ")
        for qCity in list(que):
            print(qCity, end=" ")
        print()
        pathList.append(dest)
        print("Closed list is ", end=" ")
        print(pathList)
        print()

def DFS(fromCity, toCity):
    print('DFS')
    count=0
    pathHistory = {}
    pathList=[]
    stack=[]
    stack.append(fromCity)
    while len(stack) != 0:
        dest = stack.pop()
        print('Expanding ', dest)
        if dest == toCity:
            pathList.append(dest)
            return pathHistory,count
        tempList = dictMap[dest.upper()]
        tempList=sorted(tempList, reverse=True)
        print('Children are ',tempList)
        print("New children are ", end=" ")
        for city in tempList:
            if city not in pathHistory.keys():
                pathHistory[city] = dest
        for city in tempList:
            if city not in stack and city not in pathList:
                stack.append(city)
                count+=1
                print(city, end=" ")
        print('Open List is ',stack)
        pathList.append(dest)
        print('Closed List is ',pathList)
        print()

def DFSModified(fromCity, toCity,depth):
    count=0
    pathHistory = {}
    pathList=[]
    stack=[]
    stack.append((fromCity,0))
    while len(stack) != 0:
        tup = stack.pop()
        dest = tup[0]
        level = tup[1]
        print('Expanding ', dest)
        pathList.append(tup)
        if dest == toCity:
            pathList.append(tup)
            return pathHistory,count
        if level == depth:
            print("Depth Reached")
        else:
            tempList = dictMap[dest.upper()]
            tempList=sorted(tempList, reverse=True)
            print('Children are ',tempList)
            for city in tempList:
                if city not in pathHistory.keys():
                    pathHistory[city] = dest
            for city in tempList:
                if check(city, stack) and check(city, pathList):
                    stack.append((city, level+1))
                    count+=1
            print('Open List is ',stack)
            print('Closed List is ',pathList)
    return None, count

def DFID(fromCity, toCity, depth):
    print("Depth First Iterative Deepening")
    depth+=1
    for i in range(depth):
        print("DFID Level ", i)
        pathListDFID,count = DFSModified(fromCity, toCity, i)
        if pathListDFID is None:
            print(count, ' nodes expanded. Destination not reached')
        else:
            resBFS = printPath(pathListDFID)
            print("Depth-first-Iterative deepening solution: ", end=" ")
            for DFIDcity in reversed(resBFS):
                print(DFIDcity, end=" ")
            print()
            print(count, ' nodes expanded')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
def aStar(fromCity, toCity, flag):
    print("A*")
    count=0
    openList=[]
    closedList=[]
    pathHistory={}
    h=0
    if flag != 0:
        h = abs(int(dictLong[fromCity])-int(dictLong[toCity]))
        h*=8
    g=0
    f=g+h
    openList.append((fromCity, g, h, f))
    while len(openList) != 0:
        bestNode = getBestNode(openList)
        openList.remove(bestNode)
        print('Expanding ', bestNode[0], 'f=', bestNode[3], 'g=', bestNode[1],'h=', bestNode[2])
        if bestNode[0] == toCity:
            return pathHistory,count
        tempList = dictMap[bestNode[0].upper()]
        print('Children ',tempList)
        for city,dist in tempList.items():
            
            if city not in pathHistory.keys():
                pathHistory[city] = bestNode[0]
            
            g=bestNode[1]+int(dist)
            
            if flag != 0:
                h = abs(int(dictLong[toCity])-int(dictLong[city]))
                h*=8
            f=g+h
            
            if check(city, openList) and check(city, closedList):
                openList.append((city, g, h, f))
                count+=1
            elif not check(city, openList) and check(city, closedList):
                tempTuple=()
                for tup in openList:
                    if tup[0] == city:
                        tempTuple=tup
                if tempTuple[3] > int(f):
                    openList.remove(tempTuple)
                    openList.append((city, g, h, f))
        closedList.append(bestNode)
        print('Open List ', openList)
        print('Closed List', closedList)
        print()
     
def findPaths(fromCity, toCity):
    pathListBFS,count = BFS(fromCity, toCity)
    resBFS = printPath(pathListBFS)
    print("Breadth-first-search solution: ", end=" ")
    for BFScity in reversed(resBFS):
        print(BFScity, end=" ")
    print()
    print(count, ' nodes expanded')
    print('--------------------------------------------------------------------------------------------------------------------')
    pathListDFS,count = DFS(fromCity, toCity)
    resDFS = printPath(pathListDFS)
    print("Depth-first-search solution: ", end=" ")
    for DFScity in reversed(resDFS):
        print(DFScity, end=" ")
    print()
    print(count, ' nodes expanded')
    print('--------------------------------------------------------------------------------------------------------------------')
    DFID(fromCity, toCity, 3)
    print('--------------------------------------------------------------------------------------------------------------------')
    pathListAStar,count = aStar(fromCity, toCity, 0)
    resAStar = printPath(pathListAStar)
    print("A Star with h=0 ", end=" ")
    for aStarcity in reversed(resAStar):
        print(aStarcity, end=" ")
    print()
    print(count, ' nodes expanded')
    print()
    print('--------------------------------------------------------------------------------------------------------------------')
    pathListAStar,count = aStar(fromCity, toCity, 1)
    resAStar = printPath(pathListAStar)
    print("A Star with h=0 ", end=" ")
    for aStarcity in reversed(resAStar):
        print(aStarcity, end=" ")
    print()
    print(count, ' nodes expanded')
    print()
    print('--------------------------------------------------------------------------------------------------------------------')

populateLists()

print("City choices")
tempList=[]
for k,v in dictLong.items():
    tempList.append(k)
i=0
j=0
leng = len(tempList)
while j < leng:
    if i < 6:
        print(j+1,'. ', tempList[j], ' ', end=' ')
        i+=1
        j+=1
    else:
        print()
        i=0
print()
flag = True

while flag:
    fromCity = input("Enter city name from which distance is to be calculated ")
    toCity = input("Enter city name to which distance is to be calculated ")
    if fromCity == toCity:
        print("Please enter different cities")
        print()
    elif fromCity not in dictLong.keys():
        print("From City not valid")
        print()
    elif toCity not in dictLong.keys():
        print("To City not valid")
        print()
    else:
        print('Inputs valid')
        findPaths(fromCity, toCity)
        flag=False