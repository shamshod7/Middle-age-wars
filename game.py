import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import units


games={}
count=0

class Game:
    
    def start(self):
        self.turn()
        
        
    def turn(self):
        maxspeed=0
        for ids in self.players:
            player=self.players[ids]
            if player.speed>maxspeed:
                maxspeed=player.speed
                
        spisok=[]
        for ids in self.players:
            player=self.players[ids]
            if player.speed==maxspeed:
                spisok.append(player)
                
        self.currentplayer=random.choice(spisok)
        self.currentplayer.turn(self)
        self.timer=threading.Timer(60, self.endturn)
        self.timer.start()
        
    def endturn(self):
        pass
        
    
    def __init__(self, fighters):   #{'fighter':ids,  'team':ct}
        global count
        count+=1
        self.players={}
        self.timer=None
        for ids in fighters:
            self.players.update(self.createunit(fighters[ids])) 
        self.turn=1
        self.currentplayer=None
        games.update({count:self})
        self.start()
    
    
    def createunit(self, unit):
        try:
            unit['fighter']+=''
            if unit['fighter']=='bear':
                x=units.Bear()
                x.controller='ai'
        except:
            if unit['fighter']['class']=='basic':
                x=units.Basic()
            elif unit['fighter']['class']=='warrior':
                x=units.Warrior()
            x.controller='player'
            x.id=unit['fighter']['id']
                
        x.team=unit['team']
            
        return {unit['id']:x}
        


