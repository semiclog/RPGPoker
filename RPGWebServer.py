# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 20:23:42 2019
https://code.tutsplus.com/tutorials/charting-using-plotly-in-python--cms-30286
@author: semiclog
"""
from flask import Flask, render_template
import json
import plotly
import plotly.graph_objs as go
import RPGGame
import json

def Game():
    #When the function is called, the Game is Created and the Combat takes place
    Game1=RPGGame.Game()
    RPGGame.Combat(Game1.PlayerList[0].PlayerCardList, Game1.PlayerList[0].EnemyCardList)
    
    # PRINTING the STATS
    PrintPlayerStats = RPGGame.CardOutput(Game1.PlayerList[0].PlayerCardList)
    PrintEnemyStats = RPGGame.CardOutput(Game1.PlayerList[0].EnemyCardList)    

    # GRAPHING the STATS
    xaxis=["Power","Speed","Endurance","HitPpoints","ArmorClass","Luck","Rating"]
    markertype=['circle','square','diamond', 'triangle-up', 'star', 'cross-thin']
    markercolor=['red','blue','yellow','purple','orange']
    markersize=[18, 16, 14, 12, 10]       
    
    statsdataPlayer = []
    for i, Card in enumerate(Game1.PlayerList[0].PlayerCardList):
        statsdataPlayer.append(
            go.Scatter(x=xaxis, y=RPGGame.ExtractStats(Card), name=Card.name,
            opacity=0.75,
            mode='markers',
            #visible='legendonly', this sort of works but not what I want
            marker=dict(
                symbol=markertype[i],
                color=markercolor[i],
                size=markersize[i]),
            ))
    statsdataEnemy = []
    for i, Card in enumerate(Game1.PlayerList[0].EnemyCardList):
        statsdataEnemy.append(
            go.Scatter(x=xaxis, y=RPGGame.ExtractStats(Card), name=Card.name,
            opacity=0.75,
            mode='markers',
            marker=dict(
                symbol=markertype[i],
                color=markercolor[i],
                size=markersize[i]),
            ))
    # Edit the layout
    # I think I will eventually be forced to use this reference
        #https://stackoverflow.com/questions/51010402/html-css-plotly-plot-size
    statslayout = go.Layout(
        #title=ListName,
        #plot_bgcolor = '#ff0000',
        #paper_bgcolor = '#aacccc',
        paper_bgcolor = 'rgb(136, 185, 229)',
        autosize=True,
        #width=600,
        height=300,
        #xaxis_title='Stats',
        #yaxis_title='Value',
        yaxis=dict(dtick=1,range=[2,19]),
        scene = dict(
            yaxis=dict(range=[2,19])),
        grid = dict(columns=2, rows=1),
        legend=dict(x=0.5,y=1, orientation='v'),
        margin= dict(l= 30,r= 30,b= 60,t= 30,pad= 0))
    
    statsfig1 = dict(data=statsdataPlayer, layout=statslayout)
    statsfig2 = dict(data=statsdataEnemy, layout=statslayout)
    #I could create graphJSON variables with 2,3,4,5 characters and send them all in a list
    #then I could just set a button to change which dataset to plot
    #this is definitely the wrong way to do it.
    #I should be able to send all of it and then parse it on the javascript side
    graphJSON1 = json.dumps(statsfig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(statsfig2, cls=plotly.utils.PlotlyJSONEncoder)
    #print(graphJSON1)

    # GRAPHING the COMBAT
    xcombataxis=list(range(len(Game1.PlayerList[0].PlayerCardList[0].hitpointsList[0])))
    
    combathitpointdataPlayer = []
    for i, Card in enumerate(Game1.PlayerList[0].PlayerCardList):
        combathitpointdataPlayer.append(
            go.Scatter(x=xcombataxis, y=Card.hitpointsList[0], name=Card.name,
            mode='lines',
            line=dict(
                color='blue',
                width=2
            )))
    combathitpointdataEnemy = []
    for i, Card in enumerate(Game1.PlayerList[0].EnemyCardList):
        combathitpointdataEnemy.append(
            go.Scatter(x=xcombataxis, y=Card.hitpointsList[0], name=Card.name,
            mode='lines',
            line=dict(
                color='red',
                width=2
            )))
    
    combatendurancedataPlayer = []
    for i, Card in enumerate(Game1.PlayerList[0].PlayerCardList):
        combatendurancedataPlayer.append(
            go.Scatter(x=xcombataxis, y=Card.enduranceList[0], name=Card.name,
            mode='lines',
            line=dict(
                color='blue',
                width=2
            )))
    combatendurancedataEnemy = []
    for i, Card in enumerate(Game1.PlayerList[0].EnemyCardList):
        combatendurancedataEnemy.append(
            go.Scatter(x=xcombataxis, y=Card.enduranceList[0], name=Card.name,
            mode='lines',
            line=dict(
                color='red',
                width=2
            )))
    # Edit the layout
    # I think I will eventually be forced to use this reference
        #https://stackoverflow.com/questions/51010402/html-css-plotly-plot-size
    combatlayout = go.Layout(
        #title=ListName,
        #plot_bgcolor = '#ff0000',
        #paper_bgcolor = '#aacccc',
        paper_bgcolor = 'rgb(136, 185, 229)',
        autosize=True,
        #width=600,
        height=300,
        #xaxis_title='Stats',
        #yaxis_title='Value',
        yaxis=dict(dtick=1,range=[0,19]),
        scene = dict(
            yaxis=dict(range=[0,19])),
        grid = dict(columns=2, rows=1),
        legend=dict(x=0.5,y=1, orientation='v'),
        margin= dict(l= 30,r= 30,b= 60,t= 30,pad= 0))

    combathitpointfig = dict(
            data=combathitpointdataPlayer+combathitpointdataEnemy, 
            layout=combatlayout)
    combatendurancefig = dict(
            data=combatendurancedataPlayer+combatendurancedataEnemy, 
            layout=combatlayout)
    #I could create graphJSON variables with 2,3,4,5 characters and send them all in a list
    #then I could just set a button to change which dataset to plot
    #this is definitely the wrong way to do it.
    #I should be able to send all of it and then parse it on the javascript side
    graphJSONcombathitpoints = json.dumps(combathitpointfig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSONcombatendurance = json.dumps(combatendurancefig, cls=plotly.utils.PlotlyJSONEncoder)
    
    #Sending the Raw Lists instead of the formatted graphs and text
    PlayerHitPointsList=[x.hitpointsList[0] for x in Game1.PlayerList[0].PlayerCardList]
    PlayerEnduranceList=[x.enduranceList for x in Game1.PlayerList[0].PlayerCardList]
    EnemyHitPointsList=[x.hitpointsList[0] for x in Game1.PlayerList[0].EnemyCardList]
    EnemyEnduranceList=[x.enduranceList for x in Game1.PlayerList[0].EnemyCardList]
    HitPointsList = PlayerHitPointsList + EnemyHitPointsList
    EnduranceList=PlayerEnduranceList + EnemyEnduranceList

 
    return [statsdataPlayer, statsdataEnemy, statslayout, 
            graphJSON1, graphJSON2, 
            graphJSONcombathitpoints,graphJSONcombatendurance,
            PrintPlayerStats, PrintEnemyStats,
            HitPointsList, EnduranceList,
            xcombataxis]

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('RPGhome.html')
 
@app.route('/RPGgame')
def RPGgame():
    (statsdataPlayer,statsdataEnemy,statslayout,
    graphJSON1,graphJSON2,
    graphJSONcombathitpoints,graphJSONcombatendurance,
    PrintPlayerStats, PrintEnemyStats,
    HitPointsList, EnduranceList,
    xcombataxis) = Game()
    return render_template('RPGgame.html', 
                               statsdataPlayer=statsdataPlayer,
                               statsdataEnemy=statsdataEnemy,
                               statslayout=statslayout,
                               graphJSON1=graphJSON1, 
                               graphJSON2=graphJSON2,
                               graphJSONcombathitpoints=graphJSONcombathitpoints,
                               graphJSONcombatendurance=graphJSONcombatendurance,
                               PrintPlayerStats=PrintPlayerStats,
                               PrintEnemyStats=PrintEnemyStats,
                               HitPointsList=HitPointsList,
                               EnduranceList=EnduranceList,
                               xcombataxis=xcombataxis)     

if __name__ == '__main__':
#Or disable the reloader if you want to call app.run from Jupyter.
    app.run()