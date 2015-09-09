#!/usr/bin/python3

# Class:     CSCI 680-B3
# Program:   Assignment 4
# Author:    Parthasarathy Krishnamurthy
# Z-number:  z1729253
# Date Due:  03/15/15
# Purpose:   The purpose of this assignment is to implement recommender systems. 
#            The film takes a movie names as input and based on the ratings of other users, 
#            finds the 20 closest movies to the input movie
# Execution: python3 hw4.py

import operator

movieNamesFile = 'movie-names.txt'
movieMatrixFile = 'movie-matrix.txt'

movieNames = []
movieMatrix = []

def populateLists():
    try:
        file = open(movieNamesFile, "r", encoding="latin-1")
        for line in file:
            movieName = line.split('|')[1].rstrip('\n')
            movieNames.append(movieName)
    except(OSError, IOError):
        print("File",  movieNamesFile, " not found")

    try:
        file = open(movieMatrixFile, "r", encoding="latin-1")
        for line in file:
            temp = []
            temp.append(line.rstrip('\n').split(';'))
            movieMatrix.append(temp[0])
    except(OSError, IOError):
        print("File",  movieMatrixFile, " not found")

dictMovieLists={}

def calPearson(selList, dictMovieLists):
    dictPearson = {}
    list1 = selList
    list2 = []
    length = len(movieMatrix[0])
    for key, value in dictMovieLists.items():
        list2 = value
        i=0
        sum1=0
        sum2=0
        count=0
        while i < length:
            if list1[i] != '' and list2[i] != '':
                sum1 += float(list1[i])
                sum2 += float(list2[i])
                count+=1
            i+=1
        mean1 = sum1/count
        mean2 = sum2/count
        i=0
        std1=0
        std2=0
        count=0
        while i < length:
            if list1[i] != '' and list2[i] != '':
                std1 += pow((mean1 - float(list1[i])),2)
                std2 += pow((mean2 - float(list2[i])),2)
                count+=1
            i+=1
        std1 = pow(std1/(count-1), 0.5)
        std2 = pow(std2/(count-1), 0.5)
        i=0
        pearson=0
        count=0
        while i < length:
            if list1[i] != '' and list2[i] != '':
                try:
                    pearson+=((float(list1[i]) - mean1)/std1)*((float(list2[i]) - mean2)/std2)
                    count+=1
                except(ZeroDivisionError):
                    break
            i+=1
        pearson=pearson/(count-1)
        dictPearson[key] = pearson
    return dictPearson

def compareMovies(movieNumber):
    print("Fetching similar movies...")
    print()
    movieNumber-=1
    dictMovieLists.clear()
    selList = movieMatrix[movieNumber]
    length = len(selList)
    listNum = 0
    for lists in movieMatrix:
        i = 0
        personCount=0
        while i<length:
            if lists[i] != '' and selList[i] != '':
                personCount+=1
            i+=1
        if personCount >= 10:
            dictMovieLists[listNum]=lists
        listNum+=1
    dictPearson = calPearson(selList, dictMovieLists)
    compMoviesCount = len(dictPearson)
    if compMoviesCount >= 20:
        dictPearsonOrdered = dict(sorted(dictPearson.items(), key = lambda x : x[1], reverse=True)[:20])
        dictPearsonOrdered = sorted(dictPearsonOrdered.items(), key=operator.itemgetter(1), reverse=True)
        print("The movies similar to the selected movie are:")
        print()
        i = 1
        print("{:>3} {:<75} {:>7}".format("Sno", "Movie Name", "Pearson"))
        for key, value in dictPearsonOrdered:
            print("{:>3} {:<75} {:>7}".format(i, movieNames[key], round(float(value),4)))
            i+=1
        print()
    else:
        print("Insufficient comparison movies")
        print()

flag = True
populateLists()

while flag:
    movieNum = input('Enter a movie number, q or quit to exit: ')
    if movieNum.isalpha():
        if movieNum.lower() == 'q' or movieNum.lower() == 'quit':
            print('Thanks for using the recommender system')
            flag=False
    elif movieNum.isdigit():
        if int(movieNum) > 0 and int(movieNum) <= len(movieNames):
            print()
            print('You have chosen ',movieNum,' | ',movieNames[int(movieNum)-1])
            print()
            compareMovies(int(movieNum))
        else:
            print('Please enter a number from 1-', len(movieNames))
            print()
    else:
        print('Please enter a number from 1-', len(movieNames))
        print()