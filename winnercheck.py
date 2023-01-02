from pokerscreen import Ui_MainWindow
import more_itertools as mit
import random
import itertools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel,QPushButton,QMainWindow,QMessageBox
from PyQt5.QtWidgets import *
import sys


class winner():

	def __init__(self,player_card_disc,board_cards_list):
		self.player_card_disc = player_card_disc
		self.board_cards_list = board_cards_list
		self.player_control_dic={}
		self.higher_winner_check_dict={}
		self.winner_list=[]
		self.control_element=True
		self.result_card_dic()
		self.royalflush()
		if self.control_element==True:
			self.flush_straight()
		if self.control_element==True:
			self.four_of_a_kind()
		if self.control_element==True:
			self.full_house()
		if self.control_element==True:
			self.flush_check()
		if self.control_element==True:
			self.straight()
		if self.control_element==True:
			self.three_of_a_kind()
		if self.control_element==True:
			self.two_pair()
		if self.control_element==True:
			self.one_pair()
		if self.control_element==True:
			self.higher_card()
		print(self.winner_list)

	def result_card_dic(self):
		for i,j in self.player_card_disc.items():
				a=[]
				a.extend(j)
				a.extend(self.board_cards_list)
				self.player_control_dic[i]=a

	def dublicatecheckdic(self):
		for e, i in self.player_control_dic.items():
			kontroldublicate=[]
			for j in i:
				a= j[:-1]
				if a=="A":
					a=14
				elif a=="K":
					a=13
				elif a=="Q":
					a=12
				elif a=="J":
					a=11
				else:
					a=int(a)
				
				kontroldublicate.append(a)		
			self.player_control_dic[e]=kontroldublicate

		for d,i in self.player_control_dic.items():
			e={k:i.count(k) for k in set(i)}
			self.player_control_dic[d]=e

	def f_higher_winnercheck(self):		
		
		check=True
		while check:
			b={}
			for i,j in self.higher_winner_check_dict.items():
				k=max(j)
				b[i]=k
			x=''
			if len(b.values())>0:
				c=max(b.values())
		
			d=[]
			for i,j in b.items():
				if j<c:
					d.append(i)
			
			for i in d:
				b.pop(i)
				self.higher_winner_check_dict.pop(i)
			
			if len(self.higher_winner_check_dict)== 1:
				check=False
				break
			groups = itertools.groupby(self.higher_winner_check_dict.values()) 
			next(groups, None)
			if next(groups, None) is None:     
				check=False 
				break 
			y=[]
			for i,j in self.higher_winner_check_dict.items():        
				j.pop(0)
				if len(j)==0:
					y.append(i)
			for i in y:
				self.higher_winner_check_dict.pop(i)

			groups = itertools.groupby(self.higher_winner_check_dict.values()) 
			next(groups, None)
			if next(groups, None) is None:     
				check=False 
			
			if len(self.higher_winner_check_dict)== 1:
				check=False   
		
		for i in self.higher_winner_check_dict.keys():
			self.winner_list.append(i)

	def royalflush(self):	
		self.result_card_dic()			
		for i ,j in self.player_control_dic.items():
			royalclubs=["AC","KC","QC","JC","10C"]
			a=[]
			a.extend(j)
			for element in royalclubs:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winner_list.append(i)
				self.winner_list.append('Royalflush')
				self.control_element=False
		
		for i ,j in self.player_control_dic.items():
			royaldiamonds=["AD","KD","QD","JD","10D"]
			a=[]
			a.extend(j)
			for element in royaldiamonds:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winner_list.append(i)
				self.winner_list.append('Royalflush')
				self.control_element=False

		for i ,j in self.player_control_dic.items():
			royalhearts=["AH","KH","QH","JH","10H"]
			a=[]
			a.extend(j)
			for element in royalhearts:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winner_list.append(i)
				self.winner_list.append('Royalflush')
				self.control_element=False

		for i ,j in self.player_control_dic.items():
			royalspades=["AS","KS","QS","JS","10S"]
			a=[]
			a.extend(j)
			for element in royalspades:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winner_list.append(i)
				self.winner_list.append('Royalflush')
				self.control_element=False

	def flush_straight(self):
		resultdict={}
		self.result_card_dic()
		e=0
		f=0
		g=0
		h=0	
		for j in self.board_cards_list:
			i=j[-1]
			if i=="C":
				e+=1
			elif i=="H":
				f+=1
			elif i=="S":
				g+=1
			else:
				h+=1
		if e>=3:
			symbol="C"
		if f>=3:
			symbol="H"
		if g>=3:
			symbol="S"
		if h>=3:
			symbol="D"
		else:
			symbol='&'
		for i,j in self.player_control_dic.items():
			b=[]
		
			for k in j:
				if k[-1]==symbol:
					b.append(k)
			self.player_control_dic[i]=b	
								
		for e,i in self.player_control_dic.items():
			kontroldublicate=[]
			for j in i:
				a= j[:-1]
				kontroldublicate.append(a)		
			self.player_control_dic[e]=kontroldublicate

		for e,i in self.player_control_dic.items():
			newliste=[]
			for j in i:
				if j=="A":
					newliste.append(1)
					newliste.append(14)
				elif j=="K":
					newliste.append(13)
				elif j=="Q":
					newliste.append(12)
				elif j=="J":
					newliste.append(11)
				else:
					newliste.append(int(j))
				# except:
				# 	pass
			newliste.sort()
			grplist = [list(group) for group in mit.consecutive_groups(newliste)]

			for k in grplist:
				if len(k)>4:
					self.control_element=False
					resultdict[e]=max(k)
		
		if len(resultdict)>0:
			key = max(resultdict, key = lambda z: resultdict[z])
		
		winnercheck={}
		d=0
		for i,j in resultdict.items():
			if j==resultdict[key]:
				d+=1
				winnercheck[i]=self.player_control_dic[i]
		if d==1:
			self.winner_list.append(key)
			self.winner_list.append('Flushstraight')
			
		if d>1:
			a=[]
			for i in winnercheck.keys():
				a.append(i)
			self.winner_list.extend(a)
			self.winner_list.append('Flushstraight')	
			
	def four_of_a_kind(self):
		self.result_card_dic()
		self.dublicatecheckdic()
		winnercheck={}
		for i,j in self.player_control_dic.items():	
			for k,l in j.items():
				if l==4:
					self.control_element=False
					winnercheck[i]=k
		if len(winnercheck)>0:			
			key = max(winnercheck, key = lambda z: winnercheck[z])
			self.winner_list.append(key)
			self.winner_list.append('Four of a kind')			

	def full_house(self):
		self.result_card_dic()
		self.dublicatecheckdic()		
		dic2={}
		for d,i in self.player_control_dic.items():		
			for j,k in i.items():
				x=0
				list1={}
				
				if k==3:
					for l,m in i.items():
						if m==2:
							list1[l]=2	
						if m==3:
							list1[l]=3
							x+=1
					dic2[d]=list1	
		dic3={}
		dic6={}
		dic7={}
		for i,j in dic2.items():
			if len(j)>1:
				list4=[]
				list5=[]
				self.control_element=False
				for k,l in j.items():
					if l==3:
						list4.append(k)
				list4.sort(reverse=True)
				for k,l in j.items():
					if l==2:
						list5.append(k)
				list5.sort(reverse=True)
				list4.extend(list5)
				if len(list4)>2:
					list4.pop()
				dic3[i]=list4
		for i,j in dic3.items():
			dic6[i]=j[0]
			dic7[i]=j[1]
		if len(dic6)>0:
			key= max(dic6, key=dic6.get)
			list8=dic6.copy()
			for i,j in list8.items():
				if j<dic6[key]:
					dic6.pop(i)
					dic7.pop(i)			
			key= max(dic7, key=dic7.get)
			list8=dic7.copy()
			for i,j in list8.items():
				if j<dic7[key]:
					dic7.pop(i)
			groups = itertools.groupby(dic6.values()) 
			next(groups, None)
			if next(groups, None) is None:
				groups1 = itertools.groupby(dic7.values()) 
				next(groups1, None)
				if next(groups1, None) is None:
					for i in dic7.keys():
						self.winner_list.append(i)
					self.winner_list.append('Full house')
				else:
					key= max(dic6, key=dic7.get)
					self.winner_list.append(key)
					self.winner_list.append('Full house')
			else:
				key= max(dic6, key=dic6.get)
				self.winner_list.append(key)
				self.winner_list.append('Full house')

	def flush_check(self):	
		controldict1={}
		self.result_card_dic()
		for k,v in self.player_control_dic.items():
			kontrolflush=[]
			for j in v:
				a=j[-1]
				kontrolflush.append(a)
			controldict1[k]=kontrolflush	
		for k,v in controldict1.items():
			e=0
			f=0
			g=0
			h=0	
			for j in v:
				if j=="C":
					e+=1
				elif j=="H":
					f+=1
				elif j=="S":
					g+=1
				else:
					h+=1
			if e>4 :
				symbol='C'
				self.control_element=False	
				self.higher_winner_check_dict[k]=self.player_control_dic[k]
			elif f>4 :
				symbol='H'
				self.control_element=False	
				self.higher_winner_check_dict[k]=self.player_control_dic[k]
			if g>4 :
				symbol='S'
				self.control_element=False	
				self.higher_winner_check_dict[k]=self.player_control_dic[k]
			if h>4 :
				symbol='D'
				self.control_element=False	
				self.higher_winner_check_dict[k]=self.player_control_dic[k]
		
		for e, i in self.higher_winner_check_dict.items():
			kontroldublicate=[]
			for j in i:
				if j[-1]==symbol:
					a= j[:-1]	
					if a=="A":
						a=14
					elif a=="K":
						a=13
					elif a=="Q":
						a=12
					elif a=="J":
						a=11
					else:
						a=int(a)
					kontroldublicate.append(a)
			kontroldublicate.sort(reverse=True)
			while True:
				if len(kontroldublicate)==5:
					break
				if len(kontroldublicate)>5:
					kontroldublicate.pop()		
			self.higher_winner_check_dict[e]=kontroldublicate
		self.f_higher_winnercheck()
		if len(self.winner_list)>0:
			self.winner_list.append('Flush')
					
	def straight(self):	
		self.player_control_dic={}
		resultdict={}
		d=0
		for i,j in self.player_card_disc.items():
			a=[]
			kontroldublicate=[]
			a.extend(j)
			a.extend(self.board_cards_list)
			for j in a:
				b= j[:-1]
				kontroldublicate.append(b)
			my_finallist = [j for k, j in enumerate(kontroldublicate) if j not in kontroldublicate[:k]]
			newliste=[]
			for j in my_finallist:
				if j=="A":
					newliste.append(1)
					newliste.append(14)
				elif j=="K":
					newliste.append(13)
				elif j=="Q":
					newliste.append(12)
				elif j=="J":
					newliste.append(11)
				else:
					newliste.append(int(j))
				
			newliste.sort()	
			grplist = [list(group) for group in mit.consecutive_groups(newliste)]		
			for j in grplist:
				if len(j)>4:
					self.control_element=False
					self.player_control_dic[i]=j
					resultdict[i]=max(j)
		if len(resultdict)>0:
			key = max(resultdict, key = lambda z: resultdict[z])
		
		winnercheck={}

		for i,j in resultdict.items():
			if j==resultdict[key]:
				d+=1
				winnercheck[i]=self.player_control_dic[i]
		if d==1:
			self.winner_list.append(key)
			self.winner_list.append('Straight')			
		if d>1:
			a=[]
			for i in winnercheck.keys():
				a.append(i)
			self.winner_list.extend(a)
			self.winner_list.append('Straight')

	def three_of_a_kind(self):	
		self.result_card_dic()
		self.dublicatecheckdic()
		winnercheck={}
		for d,i in self.player_control_dic.items():
			for j,k in i.items():
				
				list1=[]
				if k==3:
					self.control_element=False
					list1.append(j)
					winnercheck[d]=j
		if len(winnercheck)>0:
			key = max(winnercheck, key = lambda z: winnercheck[z])
			key2=winnercheck[key]
		
		c=0
		for i,j in winnercheck.items():
			if j==key2:
				c+=1		
		if c==1:
			if len(winnercheck)>0:
				key = max(winnercheck, key = lambda z: winnercheck[z])
				self.winner_list.append(key)
				self.winner_list.append('Three of a kind')			
		
		winnercheck2={}		
		if c>1:
			for i,j in self.player_control_dic.items():
				list7=[]
				for k,l in j.items():
					if l==3:
						winnercheck2[i]=j
			for i,j in winnercheck2.items():
				list7=[]
				for k,l in j.items():
					list7.append(k)
				list7.sort(reverse=False)
				self.higher_winner_check_dict[i]=list7
			self.f_higher_winnercheck()
			self.winner_list.append('Three of a kind')

		if len(self.winner_list)>2:
			self.higher_winner_check_dict.clear()
			for i in self.winner_list[:-1]:
				a=[]
				for k ,l in self.player_control_dic.items():
					if k == i:
						a.extend(l.keys())
				a.sort(reverse=True)
				self.higher_winner_check_dict[i]=a
			self.winner_list.clear()
			self.f_higher_winnercheck()
			self.winner_list.append('Three of a kind')
			
	def two_pair(self):		
		self.result_card_dic()
		self.dublicatecheckdic()
		for d,i in self.player_control_dic.items():
			list1=[]
			for j,k in i.items():				
				if k==2:
					list1.append(j)		
			if len(list1)>1:
				self.control_element=False				
				list1.sort(reverse=True)
				if len(list1)>2:
					list1.pop(-1)
				self.higher_winner_check_dict[d]=list1
								
		if len(self.higher_winner_check_dict)>0:
			self.f_higher_winnercheck()
			if len(self.higher_winner_check_dict)>0:
				self.winner_list.append('Two pair')	

		if len(self.winner_list)>2:
			self.higher_winner_check_dict={}
			for i in self.winner_list[:-1]:
				a=[]
				for k ,l in self.player_control_dic.items():
					if k == i:
						a.extend(l.keys())
				a.sort(reverse=True)
				self.higher_winner_check_dict[i]=a
			self.winner_list.clear()
			self.f_higher_winnercheck()
			self.winner_list.append('Two pair')

	def one_pair(self):	
		self.result_card_dic()
		self.dublicatecheckdic()			
		dictionary1={'player1':0}
		for d,i in self.player_control_dic.items():
			for j,k in i.items():
				if k==2:
					self.control_element=False
					if len(dictionary1)>0:
						key1= max(dictionary1, key = lambda z: dictionary1[z])
					
					
						if j>dictionary1[key1]:
							dictionary1.clear()
							dictionary1[d]=j
						if key1 in dictionary1:
							if j==dictionary1[key1]:
								dictionary1[d]=j
					

		dictionary2={}		
		if len(dictionary1)==1:
			for i,j in dictionary1.items():
				if j>0:
					self.winner_list.append(i)
					
		elif len(dictionary1)>1:
			for i,j in dictionary1.items():
				dictionary2[i]=self.player_control_dic[i]		
			for i,j in dictionary2.items():
				newlist3=[]				
				for k,l in j.items():
					newlist3.append(k)
				if len(newlist3)>0:
					newlist3.sort(reverse=True)
					self.higher_winner_check_dict[i]=newlist3						
			
		self.f_higher_winnercheck()
		if len(self.winner_list)>0:
			self.winner_list.append('One pair')

	def higher_card(self):
		self.result_card_dic()
		self.dublicatecheckdic()		
		for i,j in self.player_control_dic.items():
			liste=[]
			for k in j.keys():
				liste.append(k)
			liste.sort(reverse=True)
			self.higher_winner_check_dict[i]=liste
		self.f_higher_winnercheck()
		self.winner_list.append('Higher card')
  


