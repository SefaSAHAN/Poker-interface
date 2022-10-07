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
        self.board_cards_list=[]
        self.symbol=["D","C","H","S"]
        self.turn_count=0
        self.count_bet=0
        self.bet_check_dict={}
        self.total_bet={}
        self.a='player6'
        self.deck_fonk()        
        self.player = "player1"        
        self.player_turn()
        self.budget_check_dict={}
        self.all_in_dict={}
        self.screen.btn_call.clicked.connect(self.call_btn)
        self.screen.btn_fold.clicked.connect(self.fold_btn)
        self.screen.btn_bet.clicked.connect(self.bet_btn)
        self.screen.slider.valueChanged.connect(self.slider_increase)
        self.player_list=[]  
        for i in range(6):
            self.player_list.append(f"player{i+1}")
        self.player_hand=[]
        for i in self.player_list:
            c= random.sample(self.deck, 2)
            self.player_hand.append(c)
            for j in c:
                self.deck.remove(j)
        self.player_card_disc= dict(zip(self.player_list,self.player_hand))
        self.player_card_disc2=self.player_card_disc.copy()        
        if self.player == 'player1':
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc[self.player][0]}.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc[self.player][1]}.png"))        
        self.player_budget_dic={}
        for i in self.player_list:
            self.player_budget_dic[i]=500
        self.player_budget_dic['player2']=300
        self.player_budget_dic['player3']=350
        self.player_budget_dic['player4']=850
        self.budget_copy=self.player_budget_dic.copy()   
        self.budget_assign()
        self.player_bet_dic={}
        for i in self.player_list:
            self.player_bet_dic[i]=10      
        self.screen.slider.setMaximum(self.player_budget_dic[self.player])
        self.screen.btn_bet.setText(str(self.player_bet_dic[self.player]))
        self.maxvalue_find()
        self.screen.slider.setMinimum(self.max_bet)
        self.screen.slider.setValue(self.max_bet)
        b=random.sample(self.deck,5)
        self.board_cards_list.extend(b)
        for j in b:
            self.deck.remove(j)        
        for i in self.player_list:
            self.total_bet[i]=0  
        self.final_winner=[]
         
        #  (to finish the game quickly use this code)
        # for i in range(23): 
        #     self.call_btn()

    def final_card_show_up(self):
        for i in self.player_list:            
            if i == 'player1':
                self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png"))
            elif i == 'player2':
                self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png"))           
            elif i == 'player3':
                self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png")) 
            elif i == 'player4':
                self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png"))
            elif i == 'player5':
                self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png"))           
            elif i== 'player6':
                self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][0]}.png"))
                self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[i][1]}.png"))

    def pop_up(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/AH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.messagebox=QtWidgets.QMessageBox()
        b=self.final_winner
        c=''
        d=''
        e=''
        f=''
        g=''
        h=''
        i=''
        try:
            if len(self.small_pot)>0:
                i=self.small_pot
        except:
            pass
        try:
            c=b[0]
            d=b[1]
            e=b[2]
            f=b[3]
            g=b[4]
            h=b[5]   
        except:
            pass            
        self.messagebox.setText(f"{c}\n{d}\n{e}\n{f}\n{g}\n{h}{i}\n\n{self.winner_pop_up_list[-1]}")
        self.messagebox.setWindowTitle('Winner            ')
        self.messagebox.setWindowIcon(icon)
        self.messagebox.exec_()

    def finish_turn(self):
        self.small_pot=''
        self.budget_assign()
        self.img_assign()
        self.final_card_show_up()    
        self.total_pot=sum(self.total_bet.values())
        self.screen.pot.setText(str(sum(self.total_bet.values())))

        q=self.all_in_dict.copy()

        for k,l in q.items():
            if l == max(self.total_bet.values()):
                self.all_in_dict.pop(k)


        while len(self.all_in_dict)>0:
            min_value = min(self.all_in_dict.values())
            a={key:value for key, value in self.all_in_dict.items() if value == min_value}
            win = winner(self.player_card_disc,self.board_cards_list)
            self.winner_pop_up_list = win.winner_list           
            for i,j in a.items():
                if i in self.winner_pop_up_list:
                    self.final_winner.append(i)
                else:
                    self.player_list.remove(i)
                    if i=='player1':
                        self.screen.label_p1bet.setText("OUT")
                    elif i=='player2':
                        self.screen.label_p2bet.setText("OUT")
                    elif i=='player3':
                        self.screen.label_p3bet.setText("OUT")
                    elif i=='player4':
                        self.screen.label_p4bet.setText("OUT")
                    elif i=='player5':
                        self.screen.label_p5bet.setText("OUT")
                    elif i=='player6':
                        self.screen.label_p6bet.setText("OUT")
                           
            self.winner_pot=0                  
            if len(self.final_winner)>0: 
                z= self.total_bet[self.final_winner[0]]      
                for l,k in self.total_bet.items():
                    if k<=z:
                        self.winner_pot+=k
                        self.total_bet[l]=0
                    else:
                        self.winner_pot+=z
                        self.total_bet[l]-=z
                b=len(self.final_winner)
                for i in self.winner_pop_up_list[:-1]:
                    if i not in self.final_winner:
                        self.final_winner.append(i)
                for i in self.final_winner:
                    self.player_budget_dic[i]+=int(self.winner_pot/b)            

            self.total_pot-=self.winner_pot  
            if self.winner_pot>0:
                self.small_pot='\nSmall pot is \n'+str(self.winner_pot)
                self.final_card_show_up()
                self.pop_up()
                self.budget_assign()
                self.screen.pot.setText(str(sum(self.total_bet.values())))
                                  
            for i,j in a.items():
                self.all_in_dict.pop(i)
                self.player_card_disc.pop(i)
                
            self.final_winner.clear()
        
        self.small_pot=''
            

        if self.total_pot>0:            
            win = winner(self.player_card_disc,self.board_cards_list)
            self.winner_pop_up_list = win.winner_list
            self.final_winner= self.winner_pop_up_list[:-1]
            self.final_card_show_up()
            self.pop_up()
            k=len(self.final_winner)
            for i in self.final_winner:
                self.player_budget_dic[i]+=int(self.total_pot/k)

        list=[]
        for i,j in self.player_budget_dic.items():
            if j==0:
                list.append(i)
        for i in list:
            try:
                self.player_list.remove(i)
                if i=='player1':
                        self.screen.label_p1bet.setText("OUT")
                elif i=='player2':
                    self.screen.label_p2bet.setText("OUT")
                elif i=='player3':
                    self.screen.label_p3bet.setText("OUT")
                elif i=='player4':
                    self.screen.label_p4bet.setText("OUT")
                elif i=='player5':
                    self.screen.label_p5bet.setText("OUT")
                elif i=='player6':
                    self.screen.label_p6bet.setText("OUT")
            except:
                pass
            self.player_budget_dic.pop(i)
       
        self.final_winner.clear()
        self.winner_pop_up_list.clear()
        self.total_pot=0
        self.turn_count=0
        self.count_bet=0
        self.deck=[]
        self.winner_list=[]
        self.deck_fonk()
        self.player_hand=[]
        for i in self.player_list:
            c= random.sample(self.deck, 2)
            self.player_hand.append(c)
            for j in c:
                self.deck.remove(j)
        self.player_card_disc={}
        self.player_card_disc= dict(zip(self.player_list,self.player_hand))
        self.player_card_disc2=self.player_card_disc.copy()
        self.player_bet_dic={}
        self.total_bet={}
        for i in self.player_list:       
            self.player_bet_dic[i]=10
            self.total_bet[i]=0
        self.board_cards_list=[]
        b=random.sample(self.deck,5)
        self.board_cards_list.extend(b)
        for j in b:
            self.deck.remove(j) 
        self.bet_check_dict={}
        for i in self.player_list:
            self.player=i
            self.resigned_image('10',15,'rgb(85, 255, 255)')
        self.player='player6'
        self.a='player6'
        while True:
            if self.a in self.player_bet_dic:
                break
            if self.a=='player1':
                self.a='player6'
            else:    
                self.a='player'+str(int(self.a[-1])-1)
        self.img_assign       
        self.screen.desk_card1.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.screen.desk_card2.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.screen.desk_card3.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))    
        self.screen.desk_card4.setPixmap(QtGui.QPixmap(f":/icon/1B.png")) 
        self.screen.desk_card5.setPixmap(QtGui.QPixmap(f":/icon/1B.png"))
        self.budget_check_dict=self.player_budget_dic.copy()
        self.screen.btn_bet.setEnabled(True)
        self.screen.slider.setEnabled(True)
        self.all_in_dict={}


        self.budget_copy=self.player_budget_dic.copy() 

        if len(self.player_list)==1:
            self.budget_assign()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icon/AH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.setText(f"Winer is\n{self.player_list[0]}")
            self.messagebox.setWindowTitle('Game is finished     ')
            self.messagebox.setWindowIcon(icon)
            self.messagebox.exec_()

    def bet_btn(self):     
        self.player_bet_dic[self.player]=self.slider_value
        self.total_bet[self.player]+=self.slider_value   
        self.player_budget_dic[self.player]-=self.slider_value
        self.maxvalue_find()
        if self.player == self.a:
            groups = itertools.groupby(self.player_bet_dic.values()) 
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
                    for i,j in self.player_bet_dic.items():
                        self.player_bet_dic[i]=0
                else:    
                    if self.turn_count==4:
                        self.finish_turn()
            else:        
                self.a=self.player
                while True:
                    if self.a in self.player_bet_dic:
                        break
                    if self.a=='player1':
                        self.a='player6'
                    else:    
                        self.a='player'+str(int(self.a[-1])-1)
                self.count_bet=1
                self.screen.btn_bet.setEnabled(False)
                self.screen.slider.setEnabled(False)
                for i,j in self.player_bet_dic.items():
                        if j<self.max_bet:
                            self.bet_check_dict[i]=self.max_bet-j
        if self.count_bet==0:
            if len(self.player_bet_dic)<=1 and min(self.total_bet.values())>0:
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()
        if self.count_bet==1:
            if len(self.player_bet_dic)<2:
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()            
        self.playercountincrease()
        self.budget_assign()
        self.player_turn()
        self.img_assign()
        
    def slider_increase(self,value):
        self.screen.btn_bet.setText(str(value))
        self.slider_value=value
    
    def board(self,a):           
        if a==3:
            self.screen.desk_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[0]}.png"))
            self.screen.desk_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[1]}.png"))
            self.screen.desk_card3.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[2]}.png"))
        elif a==4:
            self.screen.desk_card4.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[3]}.png"))
        elif a==5:
            self.screen.desk_card5.setPixmap(QtGui.QPixmap(f":/icon/{self.board_cards_list[4]}.png"))

    def maxvalue_find(self):
        try:
            self.max_bet=max(self.player_bet_dic.values())
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
        if self.player not in self.player_bet_dic.keys():
            self.playercountincrease()
            self.img_assign()
        self.screen.slider.setMaximum(self.player_budget_dic[self.player])
        self.screen.btn_bet.setText(str(self.max_bet))
        self.screen.slider.setMinimum(self.max_bet)
        self.screen.slider.setValue(self.max_bet)
        a=max(self.budget_copy.values())
        if self.budget_copy[self.player]>=a:
            max1 = max(self.budget_copy.values())
            max2 = 0
            list=[]
            for v in self.budget_copy.values():
                if v==max1:
                    list.append(v)
                if(v>max2 and v<max1):
                        max2 = v
                if len(list)>1:
                    max2=max1                   
            self.screen.slider.setMaximum(max2)
            if self.turn_count>0:
                self.screen.slider.setMaximum(max2-self.total_bet[self.player])

        if self.budget_copy[self.player]<=max(self.total_bet.values()):          
                self.screen.btn_bet.setEnabled(False)
                self.screen.slider.setEnabled(False)
                self.screen.btn_call.setText("ALL IN")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);\n"
"border-radius:20px;\n"
"background-color: rgb(255, 255, 0);\n""\n""")
        elif self.count_bet==0 and self.budget_copy[self.player]>max(self.total_bet.values()):
                self.screen.btn_bet.setEnabled(True)
                self.screen.slider.setEnabled(True)
                self.screen.btn_call.setText("CALL")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"background-color: rgb(0, 0, 255);\n""\n""")
        else:
                self.screen.btn_call.setText("CALL")
                self.screen.btn_call.setStyleSheet("border:none;\n"
"font: 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"background-color: rgb(0, 0, 255);\n""\n""")
            
    def budget_assign(self):
        try:
            self.screen.label_p1budget.setText(str(self.player_budget_dic['player1']))
        except:
            pass
        try:
            self.screen.label_p2budget.setText(str(self.player_budget_dic['player2']))
        except:
            pass
        try:
            self.screen.label_p3budget.setText(str(self.player_budget_dic['player3']))
        except:
            pass
        try:
            self.screen.label_p4budget.setText(str(self.player_budget_dic['player4']))
        except:
            pass
        try:
            self.screen.label_p5budget.setText(str(self.player_budget_dic['player5']))
        except:
            pass
        try:
            self.screen.label_p6budget.setText(str(self.player_budget_dic['player6']))
        except:
            pass

    def img_assign(self):
        self.screen.pot.setText(str(sum(self.total_bet.values())))
        if 'player1' in self.player_bet_dic.keys():
            self.screen.label_p1bet.setText(str(self.player_bet_dic['player1']))
        if 'player2' in self.player_bet_dic.keys():    
            self.screen.label_p2bet.setText(str(self.player_bet_dic['player2']))
        if 'player3' in self.player_bet_dic.keys():
            self.screen.label_p3bet.setText(str(self.player_bet_dic['player3']))
        if 'player4' in self.player_bet_dic.keys():
            self.screen.label_p4bet.setText(str(self.player_bet_dic['player4']))
        if 'player5' in self.player_bet_dic.keys():
            self.screen.label_p5bet.setText(str(self.player_bet_dic['player5']))
        if 'player6' in self.player_bet_dic.keys():
            self.screen.label_p6bet.setText(str(self.player_bet_dic['player6']))
        if self.player == 'player1':
            self.screen.p1_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p1_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.screen.p2_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p2_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.screen.p3_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p3_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.screen.p4_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p4_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.screen.p5_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p5_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.screen.p6_card1.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][0]}.png"))
            self.screen.p6_card2.setPixmap(QtGui.QPixmap(f":/icon/{self.player_card_disc2[self.player][1]}.png"))
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
            self.all_in_dict[self.player]= self.budget_copy[self.player]
            self.player_bet_dic.pop(self.player)
            self.player_budget_dic[self.player]=0
            self.total_bet[self.player]=self.budget_copy[self.player]
            self.resigned_image('ALL IN',14,'rgb(255,255,0)')
            try:
                self.bet_check_dict.pop(self.player)
            except:
                pass
       
        if self.count_bet==0:
            self.screen.slider.setValue(self.max_bet)
            if self.player not in self.all_in_dict.keys():
                self.player_budget_dic[self.player]-=self.max_bet                
                self.total_bet[self.player]+=self.slider_value
                self.player_bet_dic[self.player]=self.max_bet

            if self.player == self.a:
                for i,j in self.player_budget_dic.items():
                    if j==0:
                        
                        if i not in self.all_in_dict.keys():
                            self.player_bet_dic.pop(i)
                            self.all_in_dict[i]= self.budget_copy[i]
                            if i=='player1':
                                self.screen.label_p1bet.setText("ALL IN")
                                self.screen.label_p1bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                            elif i=='player2':
                                self.screen.label_p2bet.setText("ALL IN")
                                self.screen.label_p2bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                                
                            elif i=='player3':
                                self.screen.label_p3bet.setText("ALL IN")
                                self.screen.label_p3bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                            elif i=='player4':
                                self.screen.label_p4bet.setText("ALL IN")
                                self.screen.label_p4bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                            elif i=='player5':
                                self.screen.label_p5bet.setText("ALL IN")
                                self.screen.label_p5bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                            elif i=='player6':
                                self.screen.label_p6bet.setText("ALL IN")
                                self.screen.label_p6bet.setStyleSheet("background-color: rgb(255,255,0);\n"
"border-radius:20px;\n""")
                        try:
                            self.bet_check_dict.pop(self.player)
                        except:
                            pass

                groups = itertools.groupby(self.player_bet_dic.values()) 
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
                        for i,j in self.player_bet_dic.items():
                            self.player_bet_dic[i]=0
                    else:    
                        if self.turn_count==4:
                            self.finish_turn()                                                    
                else:
                    self.count_bet=1
                    self.screen.btn_bet.setEnabled(False)
                    self.screen.slider.setEnabled(False)
                    for i,j in self.player_bet_dic.items():
                            if j<self.max_bet:
                                self.bet_check_dict[i]=self.max_bet-j
    
        if self.count_bet==1:        
            try:
                if self.player not in self.all_in_dict.keys():
                    self.player_budget_dic[self.player]-=self.bet_check_dict[self.player]
                    
                    self.bet_check_dict.pop(self.player)
                    if self.player_bet_dic[self.player]>0:
                        self.total_bet[self.player]+=self.slider_value-self.player_bet_dic[self.player]
                    else:
                        self.total_bet[self.player]+=self.slider_value
                    self.player_bet_dic[self.player]=self.max_bet
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
                    for i,j in self.player_bet_dic.items():
                        self.player_bet_dic[i]=0
                    self.screen.btn_bet.setEnabled(True)
                    self.screen.slider.setEnabled(True)
                    self.a=self.player
                    while True:
                        if self.a in self.player_bet_dic:
                            break
                        if self.a=='player1':
                            self.a='player6'
                        else:    
                            self.a='player'+str(int(self.a[-1])-1)
                    self.count_bet=0
                else:    
                    if self.turn_count==4:
                        self.finish_turn() 
        if self.count_bet==0:
            if len(self.player_bet_dic)<=1 and min(self.total_bet.values())>0:
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()
        if self.count_bet==1:
            if len(self.player_bet_dic)<2:
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()
        self.playercountincrease()
        self.budget_assign()
        self.player_turn()
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
                self.player_budget_dic[self.player]-=10
                self.total_bet[self.player]=10  
            self.player_bet_dic.pop(self.player)
            self.player_card_disc.pop(self.player)
            self.resigned_image('Resigned',10,'rgb(255,0,0)')
                    
        if self.player == self.a:            
            groups = itertools.groupby(self.player_bet_dic.values()) 
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
                    for i,j in self.player_bet_dic.items():
                        self.player_bet_dic[i]=0
                    self.a=self.player
                    while True:
                        if self.a in self.player_bet_dic:
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
                for i,j in self.player_bet_dic.items():
                        if j<self.max_bet:
                            self.bet_check_dict[i]=self.max_bet-j
        
        if self.count_bet==1:
            try:
                self.player_bet_dic.pop(self.player)
                self.bet_check_dict.pop(self.player)
                self.player_card_disc.pop(self.player)
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
                    for i,j in self.player_bet_dic.items():
                        self.player_bet_dic[i]=0
                    self.screen.btn_bet.setEnabled(True)
                    self.screen.slider.setEnabled(True)
                    self.a=self.player
                    while True:
                        if self.a in self.player_bet_dic:
                            break
                        if self.a=='player1':
                            self.a='player6'
                        else:    
                            self.a='player'+str(int(self.a[-1])-1)
                    self.count_bet=0                                    
                elif self.turn_count==4:
                    self.finish_turn()
                
        if self.count_bet==0:
            if len(self.player_bet_dic)<=1 :
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()
        if self.count_bet==1:
            if len(self.player_bet_dic)<2:
                self.board(3)
                self.board(4)
                self.board(5)
                self.finish_turn()
        self.playercountincrease()
        self.budget_assign()
        self.player_turn()       
        self.img_assign()

    def player_turn(self) :
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