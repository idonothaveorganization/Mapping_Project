# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:10:20 2020

@author: zheng
"""


import matplotlib.cm as cm
import math as mt
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
#########  Change this directory respectively
Dir = r'C:\Users\zheng\.spyder-py3\Population.xlsx'
#########
df = pd.read_excel (Dir)
ox.config(log_console=True, use_cache=True)
place = 'Champaign, Illinois, USA'
gdf = ox.gdf_from_place(place)
area = ox.projection.project_gdf(gdf).unary_union.area
G = ox.graph_from_place(place, network_type='drive_service',simplify = True)
Population_Score = {}   
#create a new dict for population score
node_id = list(G.nodes())
for i in node_id:
    x1 = G.nodes[i]['x']
    y1 = G.nodes[i]['y']
    p1 = [x1,y1]
    pop_score = 0
    for j in range(43):
        x2 = df.at[j,'Long']
        y2 = df.at[j,'Lat']
        p2 = [x2,y2]
        pop = df.at[j,'Population']
        dis = mt.dist(p1,p2)*1000+1
        pop_score = pop_score+pop/dis  
#Population score is population of each tract divided by distance between 
#the node and the population center of the tract
    Population_Score.update({i:pop_score})
# the new dict takes form of nodeID: population score
Pop_max = max(Population_Score.values())
for i in node_id:
    pop = Population_Score.pop(i)
    pop = pop/Pop_max
    Population_Score.update({i:pop})
# Normalize popuation score
