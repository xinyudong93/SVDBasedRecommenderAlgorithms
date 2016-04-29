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


def file2matClu(path):
    #returnMat = zeros((numberOfLines,3))
    files = os.listdir(path)
    numberOfLines=len(files)
    returnMat = zeros((numberOfLines,3))
    for fl in files:  
            allFileNum = allFileNum + 1  
    print allFileNum
    #return returnMat

    
def recMovieGenr2(filename):
    fr = open(filename)
    movieGenrDic={}
    genrDic={}
    genrSet=set()
    j=0
    
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split('::')
          lat=len(listFromLine)
          movieId=listFromLine[0]
          genr=listFromLine[lat-1]
          movieGenrDic[movieId]=set()
          
          if genr=="":
              movieGenrDic[movieId]=set()
          else:
              genrLst=genr.split("|")
              result=0
              for i in genrLst:
                  if i in genrSet:
                      movieGenrDic[movieId].add(genrDic[i])
                  else:
                      genrSet.add(i)
                      genrDic[i]=j
                      j+=1
                      movieGenrDic[movieId].add(genrDic[i])
    fr.close()
    return movieGenrDic,genrSet

    

    


def recMovieGenr(filename):
    fr = open(filename)
    movieGenrDic={}
    genrDic={}
    genrSet=set()
    j=0
    
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split(',')
          lat=len(listFromLine)
          movieId=listFromLine[0]
          genr=listFromLine[lat-1]
          movieGenrDic[movieId]=set()
          
          if genr=="":
              movieGenrDic[movieId]=set()
          else:
              genrLst=genr.split("|")
              result=0
              for i in genrLst:
                  if i in genrSet:
                      movieGenrDic[movieId].add(genrDic[i])
                  else:
                      #print i
                      genrSet.add(i)
                      genrDic[i]=j
                      j+=1
                      movieGenrDic[movieId].add(genrDic[i])
    fr.close()
    return movieGenrDic,genrSet

def getBigList(smallList,movieGener):
    numberOfLines=len(smallList)
    returnMat=zeros((numberOfLines,4))
    returnMat[:,0:3]=smallList
    for i in range(0,numberOfLines):
        mid=smallList[i,1]
        returnMat[i,3]=movieGener[str(int(mid))]
    return returnMat
    
def getBigList2(smallList,movieGenre):
    returnDic={}
    numberOfLines=len(smallList)
    for i in range(0,numberOfLines):
        returnDic[i]={}
        returnDic[i]["uid"]=smallList[i,0]
        returnDic[i]["mid"]=smallList[i,1]
        returnDic[i]["rat"]=smallList[i,2]
        mid=smallList[i,1]
        returnDic[i]["genre"]=movieGenre[str(int(mid))]
    return returnDic    
    



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

def file2matrix3(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = []
    classLabelVector = []
    fr = open(filename)
    index=0
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split('::')
          returnMat.append(listFromLine[0:3])
          index+=1
    fr.close()
    return returnMat

def file2MoveilensMat(filename):
    fr=open(filename)
    returnMat=zeros((943,1682))
    for line in fr.readlines():
        line=line.strip()
        listFromLine=line.split('::')
        userNo=int(listFromLine[0])
        itemNo=int(listFromLine[1])
        returnMat[userNo-1,itemNo-1]=listFromLine[2]
    fr.close()
    return returnMat

def listToMat(mat1,movieDic,uLen,iLen):
    mat2=zeros((uLen,iLen))
    for line in mat1:
        uid=int(line[0])-1
        mid=movieDic[int(line[1])]
        rat=line[2]
        mat2[uid][mid]=rat
    return mat2

def listToGenMat(filename,mLen,gLen):
    fr = open(filename)
    genrDic={}
    genrSet=set()
    j=0
    mat2=zeros((mLen,gLen))
    movieId=0
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split(',')
          lat=len(listFromLine)
          genr=listFromLine[lat-1]
          if genr=="":
              movieGenrDic[movieId]=set()
          else:
              genrLst=genr.split("|")
              result=0
              for i in genrLst:
                  if i in genrSet:
                      mat2[movieId][genrDic[i]]=1
                  else:
                      genrSet.add(i)
                      genrDic[i]=j
                      mat2[movieId][genrDic[i]]=1
                      j+=1
          movieId+=1
    fr.close()
    return mat2

def listToGenMat2(filename,mLen,gLen):
    fr = open(filename)
    genrDic={}
    genrSet=set()
    j=0
    mat2=zeros((mLen,gLen))
    movieId=0
    for line in fr.readlines():
          line=line.strip()
          listFromLine=line.split('::')
          lat=len(listFromLine)
          genr=listFromLine[lat-1]
          if genr=="":
              movieGenrDic[movieId]=set()
          else:
              genrLst=genr.split("|")
              result=0
              for i in genrLst:
                  if i in genrSet:
                      mat2[movieId][genrDic[i]]=1
                  else:
                      genrSet.add(i)
                      genrDic[i]=j
                      mat2[movieId][genrDic[i]]=1
                      j+=1
          movieId+=1
    fr.close()
    return mat2

def getYingShe(filename):
    movieDic={}
    reverseDic={}
    fr = open(filename)
    i=0
    for line in fr.readlines():
        line=line.strip()
        listFromLine=line.split('::')
        movieNo=int(listFromLine[0])
        movieDic[movieNo]=i
        reverseDic[i]=movieNo
        i+=1
    fr.close()
    return movieDic,reverseDic
    
def getYingShe2(filename):
    movieDic={}
    reverseDic={}
    fr = open(filename)
    i=0
    for line in fr.readlines():
        line=line.strip()
        listFromLine=line.split(',')
        movieNo=int(listFromLine[0])
        movieDic[movieNo]=i
        reverseDic[i]=movieNo
        i+=1
    fr.close()
    return movieDic,reverseDic


def recordHighRatings(ratMat):
    highRateItem={}
    index=0
    for line in ratMat:
        rating=line[2]
        if rating>3:
            if index<line[0]:
                index=line[0]
                highRateItem[index]=[]
                highRateItem[index].append(line[1])
            else:
                highRateItem[index].append(line[1])
    return highRateItem

def changeToList(rateDic):
    rateList=[]
    for i in rateDic:
        singleDic={}
        singleDic['user']=i
        singleDic['item']=set(rateDic[i])
        rateList.append(singleDic)
    return rateList

def splitMatrixByTime(start,end,RMatrix):
    lst=[]
    for row in RMatrix:
        if row[3]>=start and row[3]<end:
            lst.append(row)
    return lst
        


def patternMining(rateDic):
    rateList=[]
    for k in rateDic:
        tempDic={}
        tempDic['user']=k
        tempDic['item']=rateDic[k]
        rateList.append(tempDic)
    numberOfLine=len(rateList)
    patternList=[]
    userList=[]
    index=0
    for i in range(0,numberOfLine):
        for j in range(i+1,numberOfLine):
            intersec=rateList[i]['item'].intersection(rateList[j]['item'])
            if intersec!=set():
                patternList.append(intersec)
                userSet=([rateList[i]['user'],rateList[j]['user']])
                userList.append(userSet)
                index=index+1
                if index>=10000:
                    print index
                    index=0
    return patternList,userList

def selectPatter(ptl,usl):
    ptll=[]
    usll=[]
    numberOfLine=len(ptl)
    for i in range(0,numberOfLine):
        if len(ptl[i])>1:
            ptll.append(ptl[i])
            usll.append(usl[i])
    return ptll,usll

def mergeUserAndPattern(ptl,usl):
    mergel=[]
    numberOfLine=len(ptl)
    for i in range(0,numberOfLine):
        dic={}
        dic["pattern"]=ptl[i]
        dic["user"]=usl[i]
        mergel.append(dic)
    return mergel




                
def readFromDic(ratings):
    dic={}
    for lin in ratings:
	if dic.has_key(int(lin[0])):
		dic[int(lin[0])].add(lin[1])
	else:
		dic[int(lin[0])]=set()
		dic[int(lin[0])].add(lin[1])
    return dic

    
def removeRedundant(mergel):
    numberOfLine=len(mergel)
    for i in range(0,numberOfLine):
        if mergel[i]==set():continue
        if i%1000==0:print i
        for j in range(i+1,numberOfLine):
            if mergel[j]==set():continue
            if mergel[i]["pattern"].issubset(mergel[j]["pattern"]):
                mergel[j]["user"]=mergel[j]["user"].union(mergel[i]["user"])
                mergel[i]=set()
                break
    return mergel
                    

            


def statTag(filename):
    fr=open(filename)
    tag_dict={}
    tag_lst=[]
    index=0
    for line in fr.readlines():
        line=line.strip()
        listFromLine=line.split(',')
        tag_lst.append(listFromLine[2])
    for tag in tag_lst:
        if tag not in tag_dict:
            tag_dict[tag]=1
        else:
            tag_dict[tag]+=1
    tag_dict=sorted(tag_dict.items(),key=lambda d:d[1],reverse=True)
    tagFile=open("tagFile.txt","wb")
    pickle.dump(tag_dict,tagFile)
    tagFile.close()
    return tag_dict,tag_lst



            
                
