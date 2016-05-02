from numpy import *
import operator
import pickle
import os  

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines,4))
    classLabelVector = []
    fr = open(filename)
    index=0
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split(',')
          returnMat[index,:]=listFromLine[0:4]
          index+=1
    fr.close()
    return returnMat



    

    

def file2matrix2(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    fr = open(filename)
    index=0
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split('::')
          returnMat[index,:]=listFromLine[0:3]
          index+=1
    fr.close()
    return returnMat
            
                
