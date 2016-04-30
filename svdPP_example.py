import random

from  algo import svdPP
from algo import timeSVDPP
from reader import readMat
#test on svd++ model
lates=readMat.file2matrix("data/ml-latest-small/ratings.csv")
random.shuffle(lates)
train1m,test1m=lates[:80000,],lates[80000:,]
svdcc=svdPP.SVD_PP(train1m)
svdcc.train()
a,b=svdcc.test(test1m)


#test on timeSVD++ model

ml1m=readMat.file2matrix2("DataSets/ml-1m/ratings.dat")
tr1m,ts1m=ml1m[:800000,:],ml1m[800000:,:]
tvp=timeSVDPP.SVD_PP(tr1m)
tvp.train()
a,b=tvp.test(ts1m)
