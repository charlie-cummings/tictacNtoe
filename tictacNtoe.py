#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import re
import textwrap as tr
from IPython.display import clear_output


# In[3]:


def board(n=2):
    return np.zeros_like([],shape=[9]*n)


# In[4]:


def print_game(game=[]):
    n=game.ndim
    game=np.reshape(np.array(game,dtype=str),[3]*2*game.ndim)
    game=np.char.replace(game,'0.0',' ')
    game=np.char.replace(game,'1.0','X')
    game=np.char.replace(game,'3.0','X')
    game=np.char.replace(game,'5.0','X')
    game=np.char.replace(game,'2.0','O')
    game=np.char.replace(game,'4.0','O')
    game=np.char.replace(game,'6.0','O')
    if n==1:
        wid=11
        gs=game
    elif n==2:
        wid=41
        gs=np.einsum('ijkl->ikjl',game)
    elif n==3:
        print('still wip')
        wid=147
        gs=np.einsum('abcdef->acebdf',game)
    else:
        return 0
    lists=tr.wrap(str(gs).replace('[','').replace(']','').replace("\'    \'","'  \|  '"),width=wid)
    
    count=0
    for ii in lists:
        if count % 3 == 0:
            print('-'*wid)
        print(ii)
        count+=1
    print('-'*wid)
    return 0


# In[5]:


def win_list(num):
    win_condition=[f'{num}{num}{num}......',f'...{num}{num}{num}...',f'......{num}{num}{num}',f'{num}..{num}..{num}..',f'.{num}..{num}..{num}.',f'..{num}..{num}..{num}',f'{num}...{num}...{num}',f'..{num}.{num}.{num}..']
    return re.compile(r'|'.join(win_condition))

def battle_check(battle,jj=0):
    check=''
    for ii in battle:
        check=check+str(int(ii))
    
    xx=re.match(win_list(1+2*jj),check)
    oo=re.match(win_list(2+2*jj),check)
    
    if xx:
        return 3
    elif oo:
        return 4
    else:
        return 0


# In[6]:


n=2              #choose the dimensionality of the game
var=[-1]*n         #initialize the moves
var_prev=var
game=board(n)     #build a blank board
pieces=['X','O']
big_pieces=[['X',' ','X',' ','X',' ','X',' ','X'],[' ','O',' ','O',' ','O',' ','O',' ']]
name=['wip']*(n-3)+['front','battle','move']
move,win=0,0
error=''

#### dictionary:
# 0 = blank
# 1 = X
# 2 = O
# 3 = X won the battle
# 4 = O won the battle
###

###choose who goes first###
flag=1
while flag==1:
    first=input("Who will go first? ")
    if first in ['x','X']:
        token=0
        flag=0
    elif first in ['o','O']:
        token=1
        flag=0
    else:
        print('Please enter a valid player, either X or O.')
        
###main game###
while move!='q' and win==0:
    ##clear the screen and show game##
    clear_output(wait=False)
    if not -1 in var[:-1]:print(f"Previous Move: {pieces[not token]} at {np.ones(n)+var}.")
    
    ##list any errors##
    if error=='wild': print("Error: Wildcard. Please go anywhere else.")
    error=''
    
    print_game(game)
    var=np.roll(var,-1)
    var[-1]=-1
    for ii in np.arange(len(var)): 
        #if a move is needed, there should be a -1 in that spot.
        if np.ceil(game[tuple(var)]/2)==n-ii or var[ii]==-1:
            #get the move
            flag=1
            while flag:
                move = input(f"{pieces[token]}'s Move (Select a {name[ii-n]}): ")
                #and check its valid
                if move in ('1','2','3','4','5','6','7','8','9'):
                    if game[tuple(list(var[:ii])+[int(move)-1]+list(var[ii+1:]))] in [1,2]: 
                        print("Error: There is already a piece there.")
                    else:
                        flag=0
                        var[ii] = int(move)-1
                #or if they want to quit
                elif move=='q': flag=0
                #elif game[tuple(list(var[:ii])+[move]+list(var[ii+1:]))]
                elif move=='print': print(game)
                #and let them know if they made a typo otherwise
                else: print('Please enter a valid move (an integer 1-9)')
        if move=='q': break
    
    ##placing a piece##
    #check if the space is empty first
    if game[tuple(var)]==0:
        #place the piece if it is
        game[tuple(var)]= token+1
        #and check if that made them win the battle
        for ii in np.arange(n):
            #did they win?
            check=battle_check(game[tuple(list(var[:n-ii-1])+[np.s_[::]]+list(var[n-ii:]))],ii)
            #if so, (going deeper unless its a total win)
            if check:
                #mark the game where they won
                game[tuple(list(var[:n-ii-1])+[...])]=check+2*ii
                #and check if that made them win the whole game
                if ii==n-1:
                    clear_output(wait=False)
                    print_game(game)
                    print(f"{pieces[(check+1) % 2]} Wins!")
                    win=1
            else:
                break

    token+=1;token%=2 #update the player

#add random commands
#make game visualization better (matplotlib?)


# In[ ]:




