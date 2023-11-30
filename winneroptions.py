from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
from ui.winnercheck import winner
from ui.winnerscreen import Ui_MainWindow
import sys
import random



# (class_ui, class_base) = loadUiType("./ui/pokerwinner.ui")

class Game(QMainWindow):
	def __init__(self):
		super().__init__() 
		self.screen = Ui_MainWindow()
		self.screen.setupUi(self)
		self.winner_kind=''
		self.deck_mthd()
		self.player_list()
		self.board()
		self.playerhands_assign()
		win = winner(self.player_card_dic,self.board_cards_list)
		self.winner_list = win.winner_list
		self.show_winner()
		self.screen.Royalflush_btn.clicked.connect(self.Royal_flush)
		self.screen.flush_straight_btn.clicked.connect(self.flush_straight)
		self.screen.four_btn.clicked.connect(self.four_of_a_kind)
		self.screen.full_button.clicked.connect(self.full_house)
		self.screen.flush_btn.clicked.connect(self.flush)
		self.screen.straight_btn.clicked.connect(self.straight)
		self.screen.three_btn.clicked.connect(self.three_of_a_kind)
		self.screen.two_btn.clicked.connect(self.two_pair)
		self.screen.one_btn.clicked.connect(self.one_pair)
		self.screen.higher_btn.clicked.connect(self.higher_card)
		self.screen.two_winner_btn.clicked.connect(self.two_winner)
	
 
	def card_shuffle(self):
		self.deck_mthd()
		self.player_list()
		self.board()
		self.playerhands_assign()
		win = winner(self.player_card_dic,self.board_cards_list)
		self.winner_list = win.winner_list
		print(self.winner_list)
  	
	def winner_option(self):	
		while True:
			self.count+=1
			print(self.count)
			self.card_shuffle()
			if self.option in self.winner_list:
				self.show_winner()
				break

	def two_winner(self):
		self.count=0	
		self.card_shuffle()
		while True:
			self.count+=1
			print(self.count)
			self.card_shuffle()
			if len(self.winner_list)>2:
				self.show_winner()
				break

	def Royal_flush(self):
		self.count=0
		self.option='Royalflush'
		self.card_shuffle()
		self.winner_option()
  
	def flush_straight(self):
		self.count=0
		self.option='Flushstraight'
		self.card_shuffle()
		self.winner_option()
  
	def four_of_a_kind(self):
		self.count=0
		self.option='Four of a kind'
		self.card_shuffle()
		self.winner_option()
  
	def full_house(self):
		self.count=0
		self.option='Full house'
		self.card_shuffle()
		self.winner_option()

	def flush(self):
		self.count=0
		self.option='Flush'
		self.card_shuffle()
		self.winner_option()
  
	def straight(self):
		self.count=0
		self.option='Straight'
		self.card_shuffle()
		self.winner_option()
  
	def three_of_a_kind(self):
		self.count=0
		self.option='Three of a kind'
		self.card_shuffle()
		self.winner_option()
  
	def two_pair(self):
		self.count=0
		self.option='Two pair'
		self.card_shuffle()
		self.winner_option()
  
	def one_pair(self):
		self.count=0
		self.option='One pair'
		self.card_shuffle()
		self.winner_option()
  
	def higher_card(self):
		self.count=0
		self.option='Higher card'
		self.card_shuffle()
		self.winner_option()

	def deck_mthd(self):
		symbol=["D","C","H","S"]
		counts=list(range(1,14))
		self.deck=[]
		for i in symbol:
			for j in counts:
				if j==1:
					j="A"
					self.deck.append(str(j)+i)
				elif j==11:
					j="J"
					self.deck.append(str(j)+i)
				elif j==12:
					j="Q"
					self.deck.append(str(j)+i)
				elif j==13:
					j="K"
					self.deck.append(str(j)+i)
				else:
					self.deck.append(str(j)+i)
	 
	def player_list(self):
		playerlist0=list(range (1,7))
		self.playerlist=[]
		for i in playerlist0:
			playername="player"+str(i)
			self.playerlist.append(playername)
		self.board_cards_list=[]

	def board(self):
		self.board_cards_list=[]
		self.board_cards_list.extend(random.sample(self.deck,5))
		for j in self.board_cards_list:
			self.deck.remove(j)	
		print("board:",self.board_cards_list)
		return self.board_cards_list
	
	def playerhands_assign(self):
		self.player_card_dic=[]
		self.playerhands=[]
		for i in self.playerlist:
			c= random.sample(self.deck, 2)
			self.playerhands.append(c)
			for j in c:
				self.deck.remove(j)
		self.player_card_dic= dict(zip(self.playerlist,self.playerhands))
		print(self.player_card_dic)
			
	def show_winner(self):
		self.screen.label_p1bet.setText('')
		self.screen.label_p2bet.setText('')
		self.screen.label_p3bet.setText('')
		self.screen.label_p4bet.setText('')
		self.screen.label_p5bet.setText('')
		self.screen.label_p6bet.setText('')
		self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player1'][0]}.png"))
		self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player1'][1]}.png"))
		self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player2'][0]}.png"))           	
		self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player2'][1]}.png"))           	
		self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player3'][0]}.png"))
		self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player3'][1]}.png")) 	
		self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player4'][0]}.png"))
		self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player4'][1]}.png"))	
		self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player5'][0]}.png"))
		self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player5'][1]}.png"))           	
		self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player6'][0]}.png"))
		self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_dic['player6'][1]}.png"))
		self.screen.desk_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[0]}.png"))
		self.screen.desk_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[1]}.png"))
		self.screen.desk_card3.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[2]}.png"))	
		self.screen.desk_card4.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[3]}.png"))		
		self.screen.desk_card5.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[4]}.png"))
		if 'player1' in self.winner_list:
			self.screen.label_p1bet.setText('Winner')
		if 'player2' in self.winner_list:    
			self.screen.label_p2bet.setText('Winner')
		if 'player3' in self.winner_list:
			self.screen.label_p3bet.setText('Winner')
		if 'player4' in self.winner_list:
			self.screen.label_p4bet.setText('Winner')
		if 'player5' in self.winner_list:
			self.screen.label_p5bet.setText('Winner')
		if 'player6' in self.winner_list:
			self.screen.label_p6bet.setText('Winner')
		self.screen.label_playerturn.setText(self.winner_list[-1])
		print(self.winner_list)

app = QApplication(sys.argv)
mainwindow = Game()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("SEFA POKER GAME")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icon/AH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(785)
widget.setFixedWidth(1600)
widget.show()
sys.exit(app.exec())

