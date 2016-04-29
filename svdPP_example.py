import random

from  algo import svdPP
from reader import readMat
lates=readMat.file2matrix("data/ml-latest-small/ratings.csv")
random.shuffle(lates)
train1m,test1m=lates[:80000,],lates[80000:,]
svdcc=svdPP.SVD_PP(train1m)
svdcc.train()
a,b=svdcc.test(test1m)
