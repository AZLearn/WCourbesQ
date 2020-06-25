# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:44:12 2020

@author: vanPC2015
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import time

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


#path_Dropbox = 'C:/Users/btvan/Dropbox'
#dir_data = path_Dropbox + '/' + 'dossiers VAN/Fichiers/EDF'

fname = "Enedis_Conso_Heure_20200513-20200618.csv" #à partir du 13/05 
df = pd.read_csv(fname, sep=';')

def valkWh_jour(mois, jour, df):
    j_str = '2020-' + mois + '-' + jour + 'T00:30:00+02:00'
    j_encoded = datetime.strptime(j_str, "%Y-%m-%dT%H:%M:%S+02:00")
    jplus1_encoded = j_encoded + timedelta(hours=23, minutes=30)
    jplus1_str = jplus1_encoded.strftime("%Y-%m-%dT%H:%M:%S+02:00")
    
    mask = (df.iloc[:, 0]>= j_str) & (df.iloc[:, 0]<= jplus1_str)
    df_j48demih = df.loc[mask]

    time_48demih = list(df_j48demih.iloc[:, 0].values)
    time_48demih_encoded = [datetime.strptime(elem, "%Y-%m-%dT%H:%M:%S+02:00") for elem in time_48demih]
    time_48demih_compatEDF = [elem - timedelta(minutes=30) for elem in time_48demih_encoded]
    t_48demiheures = [datetime.strftime(elem,"%H:%M") for elem in time_48demih_compatEDF]
     
    val = df_j48demih.iloc[:, 1].values
    val_kWh = val.astype(np.float)/2000.
    date_courbe = time_48demih[0][0:10]
    
    return t_48demiheures, val_kWh, date_courbe

def input_date_streamlit():
	import datetime

	d = st.date_input( "Entrer date : ",datetime.date(2020, 6, 6))
	st.write('Jour examiné', d)
	
	return(d)

date_entree = input_date_streamlit()
mois = date_entree.strftime("%m") #'06'
jour = date_entree.strftime("%d") #'07'

t_48demiheures, val_kWh, d_YMD = valkWh_jour(mois, jour, df)

fig = plt.figure(figsize=(10, 6), dpi=80)
ax = fig.add_subplot(211)
ax.set_title(d_YMD)
#fig, ax = plt.subplots() 

#plt.ylim(0, 4.0)
ax.set_ylim(0,5.0)
ax.set_yticks(np.linspace(0., 5., 10, endpoint= False))
plt.grid(color='black', which='major', axis='y', linestyle='-', alpha=0.2)
#plt.grid(True)

bar_width = 0.35
ax.bar(t_48demiheures, val_kWh, bar_width)

#plt.bar(t_demiheures, val_kWh, bar_width)

for label in ax.xaxis.get_ticklabels(): 
    label.set_color('black') 
    label.set_rotation(90) 
    #label.set_fontsize(4) 

st.pyplot()

