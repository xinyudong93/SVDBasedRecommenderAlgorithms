from __future__ import division

import numpy as np
import scipy as sp
from numpy.random import random
class  SVD_C:
	def __init__(self,X,k=20):
		'''
			k  is the length of vector
		'''
		self.X=np.array(X)
		self.k=k
		self.ave=np.mean(self.X[:,2])
		print "the input data size is ",self.X.shape
		self.bi={}
		self.bu={}
		self.qi={}
		self.pu={}
		self.user_genres={}

                self.genres={}

                genres=[]
                self.gen2int={'Action':0,'Adventure':1,'Animation':2,
                            'Children':3,'Comedy':4,'Crime':5,
                            'Documentary':6,
                            'Drama':7,
                            'Fantasy':8,
                            'Film-Noir':9,
                            'Horror':10,
                            'Musical':11,
                            'Mystery':12,
                            'Romance':13,
                            'Sci-Fi':14,
                            'Thriller':15,
                            'War':16,
                            'Western':17,
                            'IMAX':18,
                            '(no genres listed)':19
                        }

		
		for i in range(self.X.shape[0]):
			uid=self.X[i][0]
			mid=self.X[i][1]
			rat=self.X[i][2]
			self.user_genres.setdefault(uid,{})
						
			self.bi.setdefault(mid,0)
			self.bu.setdefault(uid,0)
			self.qi.setdefault(mid,random((self.k,1))/10*(np.sqrt(self.k)))
			self.pu.setdefault(uid,random((self.k,1))/10*(np.sqrt(self.k)))
			
                for u in self.user_genres:
                    for g in range(20):
                        self.user_genres[u][g]=np.zeros((self.k,1))		
		pass

        def setGenres(self,movies):

            for m in movies:
                genretexts=m[2].split('|')
                genreints=set([])
                for t in genretexts:
                    genreints.add(self.gen2int[t])
                self.genres.setdefault(int(m[0]),genreints)
            pass                

            

	def pred(self,uid,mid):
		self.bi.setdefault(mid,0)
		self.bu.setdefault(uid,0)
		self.qi.setdefault(mid,np.zeros((self.k,1)))
		self.pu.setdefault(uid,np.zeros((self.k,1)))

                sumyj=np.zeros((self.k,1))
                self.user_genres.setdefault(uid,{})

                if uid not in self.user_genres:
                        self.user_genres[uid]={}
                        for i in range(20):
                                self.user_genres[uid][i]=np.zeros((self.k,1))

                
		for yj in self.genres[mid]:
                        self.user_genres[uid].setdefault(yj,np.zeros((self.k,1)))
                        sumyj+=self.user_genres[uid][yj]
                        
                sqrtRu=np.sqrt(len(self.genres[mid]))
		
		if (self.qi[mid] is None):
			self.qi[mid]=np.zeros((self.k,1))
		if (self.pu[uid] is None):
			self.pu[uid]=np.zeros((self.k,1))
			
		if sqrtRu==0:
                        ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*self.pu[uid])
                else:
        		ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*(self.pu[uid]+sumyj/sqrtRu))

		ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*self.pu[uid])
		if ans>5:
			return 5
		elif ans<1:
			return 1
		return ans
	    
	def train(self,steps=0,gamma=0.04,Lambda=0.15,e=0.01):
                rmse_sum,rmse_last=0.0,5.0
		while True:
			print 'the ',steps,'-th  step is running'
			steps+=1
			
			kk=np.random.permutation(self.X.shape[0])
			for j in range(self.X.shape[0]):
				i=kk[j]
				uid=self.X[i][0]
				mid=self.X[i][1]
				rat=self.X[i][2]
				eui=rat-self.pred(uid,mid)
				rmse_sum+=eui**2
				self.bu[uid]+=gamma*(eui-Lambda*self.bu[uid])
				self.bi[mid]+=gamma*(eui-Lambda*self.bi[mid])
				temp=self.qi[mid]
				
                                sqrtRu=np.sqrt(len(self.genres[mid]))
                                if sqrtRu==0:
                                        sqrtRu=1
                                
                                sumyj=np.zeros((self.k,1))
                                for yj in self.genres[mid]:
                                    sumyj+=self.user_genres[uid][yj]

				self.qi[mid]+=gamma*(eui*(self.pu[uid]+sumyj/sqrtRu)-Lambda*self.qi[mid])

				
                                for yj in self.genres[mid]:
                                        self.user_genres[uid][yj]+=gamma*(eui*temp/sqrtRu-Lambda*self.user_genres[uid][yj])

                                self.pu[uid]+=gamma*(eui*temp-Lambda*self.pu[uid])


			gamma=gamma*0.93
			print "the rmse of this step on train data is ",np.sqrt(rmse_sum/self.X.shape[0])
			rmse_sum=np.sqrt(rmse_sum/self.X.shape[0])

                        if rmse_last-rmse_sum<e and steps>5:
                                break
                        rmse_sum,rmse_last=0.0,rmse_sum
			
			#self.test(test_data)
	def test(self,test_X):
		output=[]
		sums=0
		test_X=np.array(test_X)
		#print "the test data size is ",test_X.shape
		for i in range(test_X.shape[0]):
			pre=self.pred(test_X[i][0],test_X[i][1])
			output.append(pre)
			#print pre,test_X[i][2]
			sums+=(pre-test_X[i][2])**2
		rmse=np.sqrt(sums/test_X.shape[0])
		print "the rmse on test data is ",rmse
		return output
