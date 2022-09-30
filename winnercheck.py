
import more_itertools as mit
import random
import itertools


class winner():

	def __init__(self,playercardsdic,boardcards):
		self.playercardsdic = playercardsdic
		self.boardcards = boardcards
		self.playercontdic={}
		self.higherwinnercheck={}
		self.winnerlist=[]
		self.controlelement=True
		self.resultcardsdic()
		self.royalflush()
		if self.controlelement==True:
			self.flushstraight()
		if self.controlelement==True:
			self.fourofakind()
		if self.controlelement==True:
			self.fullhouse()
		if self.controlelement==True:
			self.flushcheck()
		if self.controlelement==True:
			self.straight()
		if self.controlelement==True:
			self.threeofakind()
		if self.controlelement==True:
			self.twopair()
		if self.controlelement==True:
			self.onepair()
		if self.controlelement==True:
			self.highercard()
		print(self.winnerlist)

	def resultcardsdic(self):
		for i,j in self.playercardsdic.items():
				a=[]
				a.extend(j)
				a.extend(self.boardcards)
				self.playercontdic[i]=a

	def dublicatecheckdic(self):
		for e, i in self.playercontdic.items():
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
				try:
					a=int(a)
				except:
					pass
				kontroldublicate.append(a)		
			self.playercontdic[e]=kontroldublicate

		for d,i in self.playercontdic.items():
			e={k:i.count(k) for k in set(i)}
			self.playercontdic[d]=e

	def f_higher_winnercheck(self):
		
		b={}
		check=True
		while check:
			for i,j in self.higherwinnercheck.items():
				k=max(j)
				b[i]=k
			x=''
			try:
				c=max(b.values())
			except:
				pass
			d=[]
			for i,j in b.items():
				if j<c:
					d.append(i)
			try:
				for i in d:
					b.pop(i)
					self.higherwinnercheck.pop(i)
			except:
				pass
			for i,j in self.higherwinnercheck.items():        
				j.pop(0)
			groups = itertools.groupby(self.higherwinnercheck.values()) 
			next(groups, None)
			if next(groups, None) is None:     
				check=False 
			
			if len(self.higherwinnercheck)== 1:
				check=False   
		
		for i in self.higherwinnercheck.keys():
			self.winnerlist.append(i)



	def royalflush(self):	
		self.resultcardsdic()
			
		for i ,j in self.playercontdic.items():
			royalclubs=["AC","KC","QC","JC","10C"]
			a=[]
			a.extend(j)
			for element in royalclubs:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winnerlist.append(i)
				self.winnerlist.append('Royalflush')
				self.controlelement=False
		
		for i ,j in self.playercontdic.items():
			royaldiamonds=["AD","KD","QD","JD","10D"]
			a=[]
			a.extend(j)
			for element in royaldiamonds:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winnerlist.append(i)
				self.winnerlist.append('Royalflush')
				self.controlelement=False

		for i ,j in self.playercontdic.items():
			royalhearts=["AH","KH","QH","JH","10H"]
			a=[]
			a.extend(j)
			for element in royalhearts:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winnerlist.append(i)
				self.winnerlist.append('Royalflush')
				self.controlelement=False

		for i ,j in self.playercontdic.items():
			royalspades=["AS","KS","QS","JS","10S"]
			a=[]
			a.extend(j)
			for element in royalspades:
				if element in a:
					a.remove(element)
			x=len(a)
			if x==2:
				self.winnerlist.append(i)
				self.winnerlist.append('Royalflush')
				self.controlelement=False

	def flushstraight(self):
		resultdict={}
		self.resultcardsdic()
		e=0
		f=0
		g=0
		h=0	
		for j in self.boardcards:
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
		for i,j in self.playercontdic.items():
			b=[]
		
			for k in j:
				if k[-1]==symbol:
					b.append(k)
			self.playercontdic[i]=b	
								
		for e,i in self.playercontdic.items():
			kontroldublicate=[]
			for j in i:
				a= j[:-1]
				kontroldublicate.append(a)		
			self.playercontdic[e]=kontroldublicate

		for e,i in self.playercontdic.items():
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
				try:
					newliste.append(int(j))
				except:
					pass
			newliste.sort()
			grplist = [list(group) for group in mit.consecutive_groups(newliste)]

			for k in grplist:
				if len(k)>4:
					self.controlelement=False
					resultdict[e]=max(k)
		try:
			key = max(resultdict, key = lambda z: resultdict[z])
		except:
			pass
		winnercheck={}
		d=0
		for i,j in resultdict.items():
			if j==resultdict[key]:
				d+=1
				winnercheck[i]=self.playercontdic[i]
		if d==1:
			self.winnerlist.append(key)
			self.winnerlist.append('Flushstraiht')
			
		if d>1:
			a=[]
			for i in winnercheck.keys():
				a.append(i)
			self.winnerlist.extend(a)
			self.winnerlist.append('Flushstraiht')	
			
	def fourofakind(self):

		self.resultcardsdic()
		self.dublicatecheckdic()

		winnercheck={}
		for i,j in self.playercontdic.items():	
			for k,l in j.items():
				if l==4:
					self.controlelement=False
					winnercheck[i]=k
		try:			
			key = max(winnercheck, key = lambda z: winnercheck[z])
			self.winnerlist.append(key)
			self.winnerlist.append('Fourofakind')			
		except:
			pass

	def fullhouse(self):
		self.resultcardsdic()
		self.dublicatecheckdic()		
		list2={}
		for d,i in self.playercontdic.items():
			
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
					list2[d]=list1
		
		list3={}
		list6={}
		list7={}
		for i,j in list2.items():
			if len(j)>1:
				list4=[]
				list5=[]
				self.controlelement=False
				for k,l in j.items():
					if l==3:
						list4.append(k)
				for k,l in j.items():
					if l==2:
						list5.append(k)
				list5.sort(reverse=True)
				list4.extend(list5)
				if len(list4)>2:
					list4.pop()
				list3[i]=list4

		for i,j in list3.items():
			list6[i]=j[0]
			list7[i]=j[1]

		if len(list6)>0:
			key= max(list6, key=list6.get)
			list8=list6.copy()
			for i,j in list8.items():
				if j<list6[key]:
					list6.pop(i)
					list7.pop(i)
			
			key= max(list7, key=list7.get)
			list8=list7.copy()
			for i,j in list8.items():
				if j<list7[key]:
					list7.pop(i)
		
			groups = itertools.groupby(list6.values()) 
			next(groups, None)
			if next(groups, None) is None:
				groups1 = itertools.groupby(list7.values()) 
				next(groups1, None)
				if next(groups1, None) is None:
					for i in list7.keys():
						self.winnerlist.append(i)
					self.winnerlist.append('Fullhouse')
				else:
					key= max(list6, key=list7.get)
					self.winnerlist.append(key)
					self.winnerlist.append('Fullhouse')
			else:
				key= max(list6, key=list6.get)
				self.winnerlist.append(key)
				self.winnerlist.append('Fullhouse')

	def flushcheck(self):	
		controldict1={}
		self.resultcardsdic()
		for k,v in self.playercontdic.items():
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
				self.controlelement=False	
				self.higherwinnercheck[k]=self.playercontdic[k]
			elif f>4 :
				symbol='H'
				self.controlelement=False	
				self.higherwinnercheck[k]=self.playercontdic[k]
			if g>4 :
				symbol='S'
				self.controlelement=False	
				self.higherwinnercheck[k]=self.playercontdic[k]
			if h>4 :
				symbol='D'
				self.controlelement=False	
				self.higherwinnercheck[k]=self.playercontdic[k]
		
		for e, i in self.higherwinnercheck.items():
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
					try:
						a=int(a)
					except:
						pass
					kontroldublicate.append(a)
			kontroldublicate.sort(reverse=True)		
			self.higherwinnercheck[e]=kontroldublicate
		self.f_higher_winnercheck()
		if len(self.winnerlist)>0:
			self.winnerlist.append('Flush')
					
	def straight(self):	
		self.playercontdic={}
		resultdict={}
		d=0
		for i,j in self.playercardsdic.items():
			a=[]
			kontroldublicate=[]
			a.extend(j)
			a.extend(self.boardcards)
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
				try:
					newliste.append(int(j))
				except:
					pass
			newliste.sort()	
			grplist = [list(group) for group in mit.consecutive_groups(newliste)]		
			for j in grplist:
				if len(j)>4:
					self.controlelement=False
					self.playercontdic[i]=j
					resultdict[i]=max(j)

		try:
			key = max(resultdict, key = lambda z: resultdict[z])
		except:
			pass
		winnercheck={}

		for i,j in resultdict.items():
			if j==resultdict[key]:
				d+=1
				winnercheck[i]=self.playercontdic[i]
		if d==1:
			self.winnerlist.append(key)
			self.winnerlist.append('Straight')
			
		if d>1:
			a=[]
			for i in winnercheck.keys():
				a.append(i)
			self.winnerlist.extend(a)
			self.winnerlist.append('Straight')

	def threeofakind(self):	
		self.resultcardsdic()
		self.dublicatecheckdic()
		winnercheck={}
		for d,i in self.playercontdic.items():
			for j,k in i.items():
				
				list1=[]
				if k==3:
					self.controlelement=False
					list1.append(j)
					winnercheck[d]=j
		try:
			key = max(winnercheck, key = lambda z: winnercheck[z])
			key2=winnercheck[key]
		except:
			pass

		c=0
		for i,j in winnercheck.items():
			if j==key2:
				c+=1
		
		if c==1:
			try:
				key = max(winnercheck, key = lambda z: winnercheck[z])
				self.winnerlist.append(key)
				self.winnerlist.append('Three of a kind')			
			except:
				pass
		winnercheck2={}
		
		if c>1:
			for i,j in self.playercontdic.items():
				list7=[]
				for k,l in j.items():
					if l==3:
						winnercheck2[i]=j

			for i,j in winnercheck2.items():
				list7=[]
				for k,l in j.items():
					list7.append(k)
				list7.sort(reverse=False)
				self.higherwinnercheck[i]=list7
			self.f_higher_winnercheck()
			self.winnerlist.append('Three of a kind')
			
	def twopair(self):		
		self.resultcardsdic()
		self.dublicatecheckdic()
		for d,i in self.playercontdic.items():
			list1=[]

			for j,k in i.items():
				
				if k==2:
					list1.append(j)
		
			if len(list1)>1:
				self.controlelement=False
				try:
					list1.sort(reverse=True)
					self.higherwinnercheck[d]=list1
				except:
					pass
				
		try:
			self.f_higher_winnercheck()
			if len(self.higherwinnercheck)>0:
				self.winnerlist.append('Twopair')	
		except:
			pass

	def onepair(self):	
		self.resultcardsdic()
		self.dublicatecheckdic()			
		dictionary1={'player1':0}
		for d,i in self.playercontdic.items():
			for j,k in i.items():
				if k==2:
					self.controlelement=False
					try:
						key1= max(dictionary1, key = lambda z: dictionary1[z])
					except:
						pass
					try:
						if j>dictionary1[key1]:
							dictionary1.clear()
							dictionary1[d]=j
						if j==dictionary1[key1]:
							dictionary1[d]=j
					except:
						pass

		dictionary2={'player1':0}
		dictionary3={'player1':[],'player2':[],'player3':[],'player4':[],'player5':[],'player6':[],'player7':[]}		
		if len(dictionary1)==1:
			for i,j in dictionary1.items():
				if j>0:
					self.winnerlist.append(i)
					
		elif len(dictionary1)>1:
			for i,j in dictionary1.items():
				dictionary2[i]=self.playercontdic[i]
			for i,j in dictionary2.items():
				newlist3=[]				
				try:
					for k,l in j.items():
						newlist3.append(k)
					if len(newlist3)>0:
						newlist3.sort(reverse=True)
						self.higherwinnercheck[i]=newlist3						
				except:
					pass
		self.f_higher_winnercheck()
		if len(self.winnerlist)>0:
			self.winnerlist.append('Onepair')

	def highercard(self):
		self.resultcardsdic()
		self.dublicatecheckdic()		
		for i,j in self.playercontdic.items():
			liste=[]
			for k in j.keys():
				liste.append(k)
			liste.sort(reverse=True)
			self.higherwinnercheck[i]=liste
		self.f_higher_winnercheck()
		self.winnerlist.append('Highercard')
	
if __name__ == "__main__":
	symbol=["D","C","H","S"]
	counts=list(range(1,14))
	deck=[]
	for i in symbol:
		for j in counts:
			if j==1:
				j="A"
				deck.append(str(j)+i)
			elif j==11:
				j="J"
				deck.append(str(j)+i)
			elif j==12:
				j="Q"
				deck.append(str(j)+i)
			elif j==13:
				j="K"
				deck.append(str(j)+i)
			else:
				deck.append(str(j)+i)

	playerlist0=list(range (1,7))
	playerlist=[]
	for i in playerlist0:
		playername="player"+str(i)
		playerlist.append(playername)
	boardcards=[]
	
	def board(a):
		boardcards.extend(random.sample(deck,a))
		for j in boardcards:
			try:
				deck.remove(j)
			except:
				pass
		print("board:",boardcards)
		return boardcards

	playerhands=[]
	for i in playerlist:
		c= random.sample(deck, 2)
		playerhands.append(c)
		for j in c:
			deck.remove(j)
	playercardsdic= dict(zip(playerlist,playerhands))
	print(playercardsdic)
	board(5)
	win = winner(playercardsdic,boardcards)
	a = win.winnerlist
