from __future__ import division
import numpy as np
import scipy as sp
from numpy.random import random
import time
import pickle
import datetime
class  SVD_PP:
	def __init__(self,X,k=20,beta=0.4):
		'''
			k  is the length of vector
		'''
		self.filename='timesvdpp.pkl'
		self.beta=0.4
		
		self.X=np.array(X)
		self.k=k
		self.beta=beta
		self.ave=np.mean(self.X[:,2])
		print "the input data size is ",self.X.shape
		self.bi={}
                self.bibin={}
                self.biper={}
                #self.bip={}
		
		self.bu={}
                self.alphau={}
                self.bubin={}
                
		self.qi={}
		self.pu={}
		
		self.movie_user={}
		self.user_movie={}
                self.ratedmovie={}
                
                self.tu={}

		
		for i in range(self.X.shape[0]):
			uid=self.X[i][0]
			mid=self.X[i][1]
			rat=self.X[i][2]
			time=self.X[i][3]
			
			self.movie_user.setdefault(mid,{})
			self.user_movie.setdefault(uid,{})
			self.movie_user[mid][uid]=rat
			self.user_movie[uid][mid]=rat
			
			self.bibin.setdefault(mid,[0 for i in range(30)])
			self.biper.setdefault(mid,[0 for i in range(4)])
                        self.bi.setdefault(mid,0)
			
			self.bubin.setdefault(uid,[0 for i in range(30)])
			self.bu.setdefault(uid,0)
			self.alphau.setdefault(uid,0)

                        self.tu.setdefault(uid,[])
                        self.tu[uid].append(time)
			
			self.qi.setdefault(mid,random((self.k,1))/10*(np.sqrt(self.k)))
			self.pu.setdefault(uid,random((self.k,1))/10*(np.sqrt(self.k)))

                        self.ratedmovie.setdefault(uid,{})
                        self.ratedmovie[uid][mid]=np.zeros((20,1))

                for k in self.tu:
                        self.tu[k]=self.tbin(sum(self.tu[k])/len(self.tu[k]))



        #def tperiod(self,time):
        def tper(self,time):
                dateArray = datetime.datetime.utcfromtimestamp(time)
                m=dateArray.month
                if (m>=3)&(m<=5):
                        return 0
                if (m>=6)&(m<=8):
                        return 1
                if (m>=9)&(m<=11):
                        return 2
                return 3
                
        
        def tbin(self,time):
            return int((int(time)-828504918)/20000000)

        def devu(self,u,time):
                self.tu.setdefault(u,0)

                if time-self.tu[u]>0:
                        return abs(time-self.tu[u])**self.beta
                else:
                        return -abs(time-self.tu[u])**self.beta


	def pred(self,uid,mid,time):
		self.bi.setdefault(mid,0)
		self.bu.setdefault(uid,0)
		self.qi.setdefault(mid,np.zeros((self.k,1)))
		self.pu.setdefault(uid,np.zeros((self.k,1)))
		self.bibin.setdefault(mid,[0 for i in range(30)])
		self.biper.setdefault(mid,[0 for i in range(4)])
		self.bubin.setdefault(uid,[0 for i in range(30)])
		self.alphau.setdefault(uid,0)

                tbin=self.tbin(time)

                tper=self.tper(time)

                but=self.bu[uid]+self.alphau[uid]*self.devu(uid,tbin)+self.bubin[uid][tbin]

                bit=self.bi[mid]+self.bibin[mid][tbin]+self.biper[mid][tper]
                

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
                        ans=self.ave+bit+but+np.sum(self.qi[mid]*self.pu[uid])
                else:
        		ans=self.ave+bit+but+np.sum(self.qi[mid]*(self.pu[uid]+sumyj/sqrtRu))
		if ans>5:
			return 5
		elif ans<1:
			return 1
		return ans

	
	def train(self,steps=20,gamma=0.04,Lambda=0.15):
		for step in range(steps):
			print 'the ',step,'-th  step is running'
			rmse_sum=0.0
			kk=np.random.permutation(self.X.shape[0])

                        #np.random.shuffle(self.X)

                        randomLength=int(len(self.X))
                        #randomX=self.X[:randomLength,:]
			
			for j in range(randomLength):
				i=kk[j]
				uid=self.X[i][0]
				mid=self.X[i][1]
				rat=self.X[i][2]
				time=self.X[i][3]
				tbin=self.tbin(time)
				tper=self.tper(time)

				eui=rat-self.pred(uid,mid,time)
				rmse_sum+=eui**2
				self.bu[uid]+=gamma*(eui-Lambda*self.bu[uid])
				self.bi[mid]+=gamma*(eui-Lambda*self.bi[mid])

				self.bubin[uid][tbin]+=gamma*(eui-Lambda*self.bubin[uid][tbin])
				self.bibin[mid][tbin]+=gamma*(eui-Lambda*self.bibin[mid][tbin])
				self.biper[mid][tper]+=gamma*(eui-0.5*self.biper[mid][tper])

                                self.alphau[uid]+=gamma*(eui*self.devu(uid,tbin)-Lambda*self.alphau[uid])
				
				temp=self.qi[mid]

                                sqrtRu=np.sqrt(len(self.ratedmovie[uid]))
                                
                                sumyj=np.zeros((self.k,1))
				for yj in self.ratedmovie[uid]:
                                        sumyj+=self.ratedmovie[uid][yj]
                                        
				
				self.qi[mid]+=gamma*(eui*(self.pu[uid]+sumyj/sqrtRu)-Lambda*self.qi[mid])

                                for yj in self.ratedmovie[uid]:
                                        self.ratedmovie[uid][yj]+=gamma*(eui*temp/sqrtRu-Lambda*self.ratedmovie[uid][yj])

				self.pu[uid]+=gamma*(eui*temp-Lambda*self.pu[uid])
				
				
			gamma=gamma*0.93
			print "the rmse of this step on train data is ",np.sqrt(rmse_sum/randomLength)
			#self.test(test_data)
	def test(self,test_X):
		output=[]
		sums=0.0
		test_X=np.array(test_X)
		print "the test data size is ",test_X.shape
		for i in range(test_X.shape[0]):
		    pre=self.pred(test_X[i][0],test_X[i][1],test_X[i][3])
		    output.append(pre)
		    #print pre,test_X[i][2]
		    sums+=(pre-test_X[i][2])**2
		rmse=np.sqrt(sums/test_X.shape[0])
		print "the rmse on test data is ",rmse
		return output,sums


