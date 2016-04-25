from __future__ import division
import numpy as np
import scipy as sp
from numpy.random import random
class  SVD_PP:
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
		self.movie_user={}
		self.user_movie={}
                self.ratedmovie={}
		
		for i in range(self.X.shape[0]):
			uid=self.X[i][0]
			mid=self.X[i][1]
			rat=self.X[i][2]
			
			self.movie_user.setdefault(mid,{})
			self.user_movie.setdefault(uid,{})
			self.movie_user[mid][uid]=rat
			self.user_movie[uid][mid]=rat
			self.bi.setdefault(mid,0)
			self.bu.setdefault(uid,0)
			self.qi.setdefault(mid,np.zeros((self.k,1)))
			self.pu.setdefault(uid,np.zeros((self.k,1)))

                        self.ratedmovie.setdefault(uid,{})
                        self.ratedmovie[uid][mid]=np.zeros((20,1))
                        


	def pred(self,uid,mid):
		self.bi.setdefault(mid,0)
		self.bu.setdefault(uid,0)
		self.qi.setdefault(mid,np.zeros((self.k,1)))
		self.pu.setdefault(uid,np.zeros((self.k,1)))

                sumyj=np.zeros((self.k,1))
                self.ratedmovie.setdefault(uid,{})
		for yj in self.ratedmovie[uid]:
                        sumyj+=self.ratedmovie[uid][yj]
                sqrtRu=np.sqrt(len(self.ratedmovie[uid]))
		
		if (self.qi[mid]==None):
			self.qi[mid]=np.zeros((self.k,1))
		if (self.pu[uid]==None):
			self.pu[uid]=np.zeros((self.k,1))
		if sqrtRu==0:
                        ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*self.pu[uid])
                else:
        		ans=self.ave+self.bi[mid]+self.bu[uid]+np.sum(self.qi[mid]*(self.pu[uid]+sumyj/sqrtRu))
		if ans>5:
			return 5
		elif ans<1:
			return 1
		return ans
	def train(self,steps=20,gamma=0.05,Lambda=0.15):
		for step in range(steps):
			print 'the ',step,'-th  step is running'
			rmse_sum=0.0
			kk=np.random.permutation(self.X.shape[0])

                        #np.random.shuffle(self.X)

                        #randomLength=int(len(self.X))
                        #randomX=self.X[:randomLength,:]
			#print randomLength
			for j in range(self.X.shape[0]):
				i=kk[j]
				uid=self.X[i][0]
				mid=self.X[i][1]
				rat=self.X[i][2]
				#uid=randomX[j][0]
				#mid=randomX[j][1]
				#rat=
				eui=rat-self.pred(uid,mid)
				rmse_sum+=eui**2
				self.bu[uid]+=gamma*(eui-Lambda*self.bu[uid])
				self.bi[mid]+=gamma*(eui-Lambda*self.bi[mid])
				
				temp=self.qi[mid]

                                sqrtRu=np.sqrt(len(self.ratedmovie[uid]))
                                if sqrtRu==0:
                                        sqrtRu=1

                                
                                sumyj=np.zeros((self.k,1))
				for yj in self.ratedmovie[uid]:
                                        sumyj+=self.ratedmovie[uid][yj]
                                        
				self.qi[mid]+=gamma*(eui*(self.pu[uid]+sumyj/sqrtRu)-Lambda*self.qi[mid])

                                for yj in self.ratedmovie[uid]:
                                        self.ratedmovie[uid][yj]+=gamma*(eui*temp/sqrtRu-Lambda*self.ratedmovie[uid][yj])

				self.pu[uid]+=gamma*(eui*temp-Lambda*self.pu[uid])
				
			gamma=gamma*0.93
			print "the rmse of this step on train data is ",np.sqrt(rmse_sum/self.X.shape[0])
			#self.test(test_data)
	def test(self,test_X):
		output=[]
		sums=0.0
		test_X=np.array(test_X)
		length=len(test_X)
		print "the test data size is ",test_X.shape
		for i in range(test_X.shape[0]):
			pre=self.pred(test_X[i][0],test_X[i][1])
			output.append(pre)
			#print pre,test_X[i][2]
			sums+=(pre-test_X[i][2])**2
		rmse=np.sqrt(sums/length)
		print "the rmse on test data is ",rmse
		return output,sums

