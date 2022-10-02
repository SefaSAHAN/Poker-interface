import sys
import os
import more_itertools as mit
import random
import itertools
from winnercheck import winner
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pokerscreen import Ui_MainWindow

class Game(QMainWindow):
    def __init__(self):
        super(Game,self).__init__()
        self.screen = Ui_MainWindow()
        self.screen.setupUi(self)
        self.deck=[]
        self.boardcards=[]
        self.symbol=["D","C","H","S"]
        self.turn_count=0
        self.count_bet=0
        self.bet_check_dict={}
        self.total_bet={}
        self.a='player6'
        self.deck_fonk()        
        self.player = "player1"        
        self.playerturn()
        self.budget_check_dict={}
        self.all_in_list=[]
        self.screen.btn_call.clicked.connect(self.call_btn)
        self.screen.btn_fold.clicked.connect(self.fold_btn)
        self.screen.btn_bet.clicked.connect(self.bet_btn)
        self.screen.slider.valueChanged.connect(self.slider_increase)
        self.playerlist=[]
        self.second_pot=[]    
        for i in range(6):
            self.playerlist.append(f"player{i+1}")
        self.playerhands=[]
        for i in self.playerlist:
            c= random.sample(self.deck, 2)
            self.playerhands.append(c)
            for j in c:
                self.deck.remove(j)
        self.playercardsdic= dict(zip(self.playerlist,self.playerhands))
        self.playercardsdic2=self.playercardsdic.copy()        
        if self.player == 'player1':
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))        
        self.playerbudgetsdic={}
        for i in self.playerlist:
            self.playerbudgetsdic[i]=500
        self.playerbudgetsdic['player2']=300
        self.playerbudgetsdic['player3']=350
        self.playerbudgetsdic['player4']=850

        self.budget_copy=self.playerbudgetsdic.copy()   
        self.budgetassign()
        self.playerbetdic={}
        for i in self.playerlist:
            self.playerbetdic[i]=10      
        self.screen.slider.setMaximum(self.playerbudgetsdic[self.player])
        self.screen.btn_bet.setText(str(self.playerbetdic[self.player]))
        self.maxvalue_find()
        self.screen.slider.setMinimum(self.max_bet)
        self.screen.slider.setValue(self.max_bet)
        b=random.sample(self.deck,5)
        self.boardcards.extend(b)
        for j in b:
            self.deck.remove(j)
        
        for i in self.playerlist:
            self.total_bet[i]=0  
         
        #  (to finish the game quickly use this code)
        # for i in range(23): 
        #     self.call_btn()

    def finish_turn(self):
        self.img_assign()
        win = winner(self.playercardsdic,self.boardcards)
        a = win.winnerlist
        for i in self.playerlist:            
            if i == 'player1':
                self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png"))
            elif i == 'player2':
                self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png"))           
            elif i == 'player3':
                self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png")) 
            elif i == 'player4':
                self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png"))
            elif i == 'player5':
                self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png"))           
            elif i== 'player6':
                self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][0]}.png"))
                self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic2[i][1]}.png"))
        
        self.screen.label.setText(str(a[-1]))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/AH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.messagebox=QtWidgets.QMessageBox()
        b=a[:-1]
        c=''
        d=''
        e=''
        f=''
        g=''
        h=''
        try:
            c=b[0]
            d=b[1]
            e=b[2]
            f=b[3]
            g=b[4]
            h=b[5]
        except:
            pass            
        self.messagebox.setText(f"{c}\n{d}\n{e}\n{f}\n{g}\n{h}\n\n{a[-1]}")
        self.messagebox.setWindowTitle('Winner            ')
        self.messagebox.setWindowIcon(icon)
        self.messagebox.exec_()
        c=self.playerbudgetsdic.copy()
        b=int(3000-sum(c.values()))
        for i in a[:-1]:
            self.playerbudgetsdic[i]+=int(b/len(a[:-1]))
        self.turn_count=0
        self.count_bet=0
        self.deck=[]
        self.winnerlist=[]
        self.deck_fonk()
        self.playerlist=[]
        for i in range(6):
            self.playerlist.append(f"player{i+1}")
        self.playerhands=[]
        for i in self.playerlist:
            c= random.sample(self.deck, 2)
            self.playerhands.append(c)
            for j in c:
                self.deck.remove(j)
        self.playercardsdic={}
        self.playercardsdic= dict(zip(self.playerlist,self.playerhands))
        self.playercardsdic2=self.playercardsdic.copy()
        self.playerbetdic={}
        for i in self.playerlist:
            x=10
            self.playerbetdic[i]=x 
        self.boardcards=[]
        b=random.sample(self.deck,5)
        self.boardcards.extend(b)
        for j in b:
            self.deck.remove(j) 
        self.bet_check_dict={}
        for i in self.playerlist:
            self.player=i
            self.resigned_image('10',15,'rgb(85, 255, 255)')
        self.player='player6'
        self.a='player6'
        self.img_assign       
        self.screen.desk_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.screen.desk_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.screen.desk_card3.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))    
        self.screen.desk_card4.setPixmap(QtGui.QPixmap(f":/icon/1B.png")) 
        self.screen.desk_card5.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.budget_check_dict=self.playerbudgetsdic.copy()
        self.screen.btn_bet.setEnabled(True)
        self.screen.slider.setEnabled(True)
        self.all_in_list.clear()

    def bet_btn(self):     
        self.playerbetdic[self.player]=self.slider_value
        self.total_bet[self.player]+=self.slider_value   
        self.playerbudgetsdic[self.player]-=self.slider_value
        self.maxvalue_find()
        if self.player == self.a:
            groups = itertools.groupby(self.playerbetdic.values()) 
            next(groups, None)
            if next(groups, None) is None:
                self.count_bet=0
                self.turn_count+=1
                if self.turn_count==1 or self.turn_count==2 or self.turn_count==3:
                    if self.turn_count==1:
                        self.board(3)
                    elif self.turn_count==2:
                        self.board(4)
                    elif self.turn_count==3:
                        self.board(5)
                    for i,j in self.playerbetdic.items():
                        self.playerbetdic[i]=0
                else:    
                    if self.turn_count==4:
                        self.finish_turn()
            else:        
                self.a=self.player
                while True:
                    if self.a in self.playerbetdic:
                        break
                    if self.a=='player1':
                        self.a='player6'
                    else:    
                        self.a='player'+str(int(self.a[-1])-1)
                self.count_bet=1
                self.screen.btn_bet.setEnabled(False)
                self.screen.slider.setEnabled(False)
                for i,j in self.playerbetdic.items():
                        if j<self.max_bet:
                            self.bet_check_dict[i]=self.max_bet-j
         
        self.playercountincrease()
        self.budgetassign()
        self.playerturn()
        self.img_assign()

    def slider_increase(self,value):
        self.screen.btn_bet.setText(str(value))
        self.slider_value=value
    
    def board(self,a):           
        if a==3:
            self.screen.desk_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.boardcards[0]}.png"))
            self.screen.desk_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.boardcards[1]}.png"))
            self.screen.desk_card3.setPixmap(QtGui.QPixmap(f":/icon/{self.boardcards[2]}.png"))
        elif a==4:
            self.screen.desk_card4.setPixmap(QtGui.QPixmap(f":/icon/{self.boardcards[3]}.png"))
        elif a==5:
            self.screen.desk_card5.setPixmap(QtGui.QPixmap(f":/icon/{self.boardcards[4]}.png"))

    def maxvalue_find(self):
        try:
            self.max_bet=max(self.playerbetdic.values())
        except:
            pass

    def playercountincrease(self):
        self.maxvalue_find()
        if self.player[-1]=='6':
            self.player='player1'
        else:
            b=int(self.player[-1])+1
            c='player'+str(b)
            self.player=c
        self.screen.slider.setMaximum(self.playerbudgetsdic[self.player])
        self.screen.btn_bet.setText(str(self.max_bet))
        self.screen.slider.setMinimum(self.max_bet)
        self.screen.slider.setValue(self.max_bet)
        if self.player not in self.playerbetdic.keys():
            self.playercountincrease()
            self.img_assign()
        if self.budget_copy[self.player]<=max(self.total_bet.values()):
          
                self.screen.btn_bet.setEnabled(False)
                self.screen.slider.setEnabled(False)
                self.screen.btn_call.setText("ALL IN")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);\n"
"border-radius:20px;\n"
"background-color: rgb(255, 255, 0);\n"
"\n"
"")
        elif self.count_bet==0 and self.budget_copy[self.player]>max(self.total_bet.values()):
                self.screen.btn_bet.setEnabled(True)
                self.screen.slider.setEnabled(True)
                self.screen.btn_call.setText("CALL")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"background-color: rgb(0, 0, 255);\n"
"\n"
"")
        else:
                self.screen.btn_call.setText("CALL")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"background-color: rgb(0, 0, 255);\n"
"\n"
"")
            
        
            

            


    def budgetassign(self):
        self.screen.label_p1budget.setText(str(self.playerbudgetsdic['player1']))
        self.screen.label_p2budget.setText(str(self.playerbudgetsdic['player2']))
        self.screen.label_p3budget.setText(str(self.playerbudgetsdic['player3']))
        self.screen.label_p4budget.setText(str(self.playerbudgetsdic['player4']))
        self.screen.label_p5budget.setText(str(self.playerbudgetsdic['player5']))
        self.screen.label_p6budget.setText(str(self.playerbudgetsdic['player6']))

    def img_assign(self):
        self.screen.pot.setText(str(3000-sum(self.playerbudgetsdic.values())))
        if 'player1' in self.playerbetdic.keys():
            self.screen.label_p1bet.setText(str(self.playerbetdic['player1']))
        if 'player2' in self.playerbetdic.keys():    
            self.screen.label_p2bet.setText(str(self.playerbetdic['player2']))
        if 'player3' in self.playerbetdic.keys():
            self.screen.label_p3bet.setText(str(self.playerbetdic['player3']))
        if 'player4' in self.playerbetdic.keys():
            self.screen.label_p4bet.setText(str(self.playerbetdic['player4']))
        if 'player5' in self.playerbetdic.keys():
            self.screen.label_p5bet.setText(str(self.playerbetdic['player5']))
        if 'player6' in self.playerbetdic.keys():
            self.screen.label_p6bet.setText(str(self.playerbetdic['player6']))

        if self.player == 'player1':
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        elif self.player == 'player2':
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))            
        elif self.player == 'player3':
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        elif self.player == 'player4':
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        elif self.player == 'player5':
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))            
        elif self.player == 'player6':
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][0]}.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.playercardsdic[self.player][1]}.png"))
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
    
 
    def call_btn(self):    
        self.maxvalue_find()
        if self.budget_copy[self.player]<=max(self.total_bet.values()):
            self.all_in_list.append(self.player)  
            self.playerbetdic.pop(self.player)
            self.playerbudgetsdic[self.player]=0
            self.resigned_image('ALL IN',14,'rgb(255,255,0)')
            try:
                self.bet_check_dict.pop(self.player)
            except:
                pass
       
        if self.count_bet==0:
            self.screen.slider.setValue(self.max_bet)
            if self.player not in self.all_in_list:
                self.playerbudgetsdic[self.player]-=self.max_bet                
                self.total_bet[self.player]+=self.slider_value
                self.playerbetdic[self.player]=self.max_bet

            if self.player == self.a:            
                groups = itertools.groupby(self.playerbetdic.values()) 
                next(groups, None)
                if next(groups, None) is None:
                    self.count_bet=0
                    self.turn_count+=1
                    if self.turn_count==1 or self.turn_count==2 or self.turn_count==3:
                        if self.turn_count==1:
                            self.board(3)
                        elif self.turn_count==2:
                            self.board(4)
                        elif self.turn_count==3:
                            self.board(5)
                        for i,j in self.playerbetdic.items():
                            self.playerbetdic[i]=0
                    else:    
                        if self.turn_count==4:
                            self.finish_turn()                                                    
                else:
                    self.count_bet=1
                    self.screen.btn_bet.setEnabled(False)
                    self.screen.slider.setEnabled(False)
                    for i,j in self.playerbetdic.items():
                            if j<self.max_bet:
                                self.bet_check_dict[i]=self.max_bet-j
    
        if self.count_bet==1:        
            try:
                if self.player not in self.all_in_list:
                    self.playerbudgetsdic[self.player]-=self.bet_check_dict[self.player]
                    
                    self.bet_check_dict.pop(self.player)
                    if self.playerbetdic[self.player]>0:
                        self.total_bet[self.player]+=self.slider_value-self.playerbetdic[self.player]
                    else:
                        self.total_bet[self.player]+=self.slider_value
                    self.playerbetdic[self.player]=self.max_bet
            except:
                pass
            if len(self.bet_check_dict)<=0:
                self.count_bet=0
                self.turn_count+=1
                if self.turn_count==1 or self.turn_count==2 or self.turn_count==3:
                    if self.turn_count==1:
                        self.board(3)
                    elif self.turn_count==2:
                        self.board(4)
                    elif self.turn_count==3:
                        self.board(5)
                    for i,j in self.playerbetdic.items():
                        self.playerbetdic[i]=0
                    self.screen.btn_bet.setEnabled(True)
                    self.screen.slider.setEnabled(True)
                    self.a=self.player
                    while True:
                        if self.a in self.playerbetdic:
                            break
                        if self.a=='player1':
                            self.a='player6'
                        else:    
                            self.a='player'+str(int(self.a[-1])-1)
                    self.count_bet=0
                else:    
                    if self.turn_count==4:
                        self.finish_turn()                                                       
        self.playercountincrease()
        self.budgetassign()
        self.playerturn()
        self.img_assign() 

    def resigned_image(self,a,b,c):

        if self.player=='player1':
            self.screen.label_p1bet.setText(a)
            self.screen.label_p1bet.setFont(QFont('Arial', b))
            self.screen.label_p1bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")
        if self.player=='player2':
            self.screen.label_p2bet.setText(a)
            self.screen.label_p2bet.setFont(QFont('Arial', b))
            self.screen.label_p2bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")
        if self.player=='player3':
            self.screen.label_p3bet.setText(a)
            self.screen.label_p3bet.setFont(QFont('Arial', b))
            self.screen.label_p3bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")
        if self.player=='player4':
            self.screen.label_p4bet.setText(a)
            self.screen.label_p4bet.setFont(QFont('Arial', b))
            self.screen.label_p4bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")
        if self.player=='player5':
            self.screen.label_p5bet.setText(a)
            self.screen.label_p5bet.setFont(QFont('Arial', b))
            self.screen.label_p5bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")
        if self.player=='player6':
            self.screen.label_p6bet.setText(a)
            self.screen.label_p6bet.setFont(QFont('Arial', b))
            self.screen.label_p6bet.setStyleSheet(f" border-radius: 20px; background-color: {c};")

    def fold_btn(self):
        self.screen.slider.setValue(self.max_bet) 
        if self.count_bet==0:
            if self.turn_count==0:
                self.playerbudgetsdic[self.player]-=10  
            self.playerbetdic.pop(self.player)
            self.playercardsdic.pop(self.player)
            self.resigned_image('Resigned',10,'rgb(255,0,0)')
            
        
        if self.player == self.a:            
            groups = itertools.groupby(self.playerbetdic.values()) 
            next(groups, None)
            if next(groups, None) is None:
                self.count_bet=0
                self.turn_count+=1
                if self.turn_count==1 or self.turn_count==2 or self.turn_count==3:
                    if self.turn_count==1:
                        self.board(3)
                    elif self.turn_count==2:
                        self.board(4)
                    elif self.turn_count==3:
                        self.board(5)
                    for i,j in self.playerbetdic.items():
                        self.playerbetdic[i]=0
                    self.a=self.player
                    while True:
                        if self.a in self.playerbetdic:
                            break
                        if self.a=='player1':
                            self.a='player6'
                        else:    
                            self.a='player'+str(int(self.a[-1])-1)

                else:    
                    if self.turn_count==4:
                        self.finish_turn()
                                                
            else:
                self.count_bet=1
                self.screen.btn_bet.setEnabled(False)
                self.screen.slider.setEnabled(False)
                for i,j in self.playerbetdic.items():
                        if j<self.max_bet:
                            self.bet_check_dict[i]=self.max_bet-j
        
        if self.count_bet==1:
            try:
                self.playerbetdic.pop(self.player)
                self.bet_check_dict.pop(self.player)
                self.playercardsdic.pop(self.player)
                self.resigned_image('Resigned',10,'rgb(255,0,0)')            
            except:
                pass
            
            if len(self.bet_check_dict)<=0:
                self.count_bet=0
                self.turn_count+=1
                if self.turn_count==1 or self.turn_count==2 or self.turn_count==3:
                    if self.turn_count==1:
                        self.board(3)
                    elif self.turn_count==2:
                        self.board(4)
                    elif self.turn_count==3:
                        self.board(5)
                    for i,j in self.playerbetdic.items():
                        self.playerbetdic[i]=0
                    self.screen.btn_bet.setEnabled(True)
                    self.screen.slider.setEnabled(True)
                    self.a=self.player
                    while True:
                        if self.a in self.playerbetdic:
                            break
                        if self.a=='player1':
                            self.a='player6'
                        else:    
                            self.a='player'+str(int(self.a[-1])-1)
                    self.count_bet=0
                                    
                elif self.turn_count==4:
                    self.finish_turn()
                
        if len(self.playerbetdic)<2:
            self.board(3)
            self.board(4)
            self.board(5)
            self.finish_turn()
        self.playercountincrease()
        self.budgetassign()
        self.playerturn()       
        self.img_assign()

    def playerturn(self) :
        self.screen.label_playerturn.setText(self.player)
        
    def deck_fonk(self):
        counts=list(range(1,14))       
        for i in self.symbol:
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