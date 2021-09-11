# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 19:12:18 2021

@author: jonat
"""

"""
This version of the game lets the player type the entirety of the text displayed and then tells him how much time he took
"""

from requests import get
from bs4 import BeautifulSoup
import tkinter as tk
from time import time

started = False

#Window in which the game is played
window = tk.Tk()

#StringVar of the text to type
randomTextStringVar = tk.StringVar(window)

#Label for the text to type
textLabel = tk.Label(window,textvariable = randomTextStringVar, wraplength = 800)

#Entry where the player types
entry = tk.Entry(window, justify = "center")

#StringVar of the statistics of the player
statsStringVar = tk.StringVar(window)

#Label for the statistics of the player
statsLabel = tk.Label(window, textvariable = statsStringVar)


def newGame():
    #Function launching a new game
    global errorsCounter, randomText, randomTextStringVar, entry, t1, started
    url = "http://www.randomtextgenerator.com"
    html = get(url)
    soup = BeautifulSoup(html.text,"html.parser")
    
    randomText = soup.find('textarea').get_text().replace('\n','').replace('\r','') #This variable holds the text generated by the site
    
    #The next lines allows us to limit the size of the text, while keeping the last sentence complete
    n = 50
    char = randomText[n]
    
    while char != '.':
        char = randomText[n]
        n += 1
        
    randomText = randomText[:n]
    
    #Changing the text in the window
    randomTextStringVar.set(randomText)
    
    #Emptying the entry and the statistics display
    entry.bind('<KeyRelease>', compare)
    entry['state'] = 'normal'
    entry.delete(0, 'end')
    
    statsStringVar.set('\n\n\n\n\n\n\n')
    
    started = False
    
    #Resetting the errors counter
    errorsCounter = 0

def compare(event):
    #This function compares the content of the entry to the text in order to indicate errors
    global errorsCounter, started, t1
    
    txt = entry.get()
    
    if started == False:
        #As long as the player hasn't begun typing, the chronometer doesn't start
        if txt != '':
            t1 = time()
            started = True
            entry.after(2, compare) #Here using the .after method on the compare function, which needs an event, raises an exception in the terminal but it doesn't impact the game, so I leave it as is
        else:
            entry.after(2, compare)
    else:
        l = len(txt)
        
        if txt != randomText[:l]:
            if entry['bg'] != 'red':
                errorsCounter += 1
            entry['bg'] = 'red'
        else:
            entry['bg'] = 'white'
       
        if l == len(randomText) and entry['bg'] != 'red':
            #If the player finishes the recopy, we display their average characters/s and the number of errors
            entry.unbind('<KeyRelease>')
            entry['state'] = 'disabled'
            t2 = time()
            
            score = round(l/(t2-t1),4)
            
            #Getting the top 3 highscores from the file holding them
            scoreFile = open('highscore.txt','r')
            
            scores = scoreFile.readlines()
            
            scoreFile.close()
            
            for i in range(len(scores)):
                scores[i].replace('\n','')
                scores[i] = float(scores[i]) 
                
            if len(scores) == 0 or score > scores[-1] or len(scores) < 3:
                #If the new score is at least better that the worst score of the top, we put it in
                scores.append(score)
                scores.sort(reverse = True)
                
                if len(scores)>3:
                    #Checking whether 3 scores or less were saved as only 3 can be saved
                    del(scores[-1])
                
                scoreFile = open('highscore.txt','w')
                scoreFile.truncate(0)
                
                for scr in scores:
                    #Writing the new top
                    scoreFile.write(str(scr) + '\n')
                    
                scoreFile.close()
            
            #Displaying the top and statistics of the player
            string = ''
            for i in range(len(scores)):
                string += str(i+1) + '. ' + str(scores[i]) + '\n'
            if score in scores:
                statsStringVar.set('Average characters/s = ' + str(score) + '\nErrors : ' + str(errorsCounter) + '\n\nNew highscore !\n\n' + string)
            else:
                statsStringVar.set('Average characters/s = ' + str(score) + '\nErrors : ' + str(errorsCounter) + '\n\n' + string)
                            
    
newGame()        

#Placing the different elements
window.geometry('1200x400')
window.resizable(False,False)
window.grid_columnconfigure(0, weight=1)

textLabel.grid(pady = 20)

entry.grid(pady = 20, sticky = tk.EW)

entry.bind('<KeyRelease>',compare)

statsLabel.grid(pady = 20)

retryButton = tk.Button(window,text = 'Retry',command = newGame)
retryButton.grid(ipadx = 10,pady = 20)

window.mainloop()