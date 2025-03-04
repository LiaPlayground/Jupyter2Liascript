import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib.colors import SymLogNorm

def find_idx_of_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def d_n(Anteil,d_new,cum_m_new):
    #curve = sp.interpolate.interp1d(Kumulierte_Masseanteile*100,np.log(Siebdurchmesser[0:-1]))
    #d_new = np.linspace(np.min(np.log(Siebdurchmesser[0:-1])),np.max(np.log(Siebdurchmesser[0:-1])),1000)
    #cum_m_new = sp.interpolate.interp1d(np.log(Siebdurchmesser[0:-1]),Kumulierte_Masseanteile*100,kind='cubic')
    idx = find_idx_of_nearest(cum_m_new(d_new),Anteil)
    return np.exp(d_new[idx])
    #return np.exp(curve(Anteil))

def Masseanteile(Siebmassen):
    return Siebmassen/Siebmassen.sum()

def Siebdurchgang(Masseanteile):
    #Aufsteigend ordnen
    aufsteigend_m_i = np.flip(Masseanteile)
    #Rueckgabe in urspruenglicher Sortierung
    return np.flip(aufsteigend_m_i[0:-1].cumsum())


def plot_KVK_glob(Neuauswertung, Startwerte, Siebdurchmesser):
    global Massen
    m_i = Startwerte
    dm_i = Masseanteile(m_i)
    Kumulierte_Masseanteile = Siebdurchgang(dm_i)
    fig, ax = plt.subplots(figsize=(18,10))
    
    #interpolation
    d_new = np.linspace(np.min(np.log(Siebdurchmesser[0:-1])),np.max(np.log(Siebdurchmesser[0:-1])),10000)
    #cum_m_new = sp.interpolate.interp1d(np.log(Siebdurchmesser[0:-1]),Kumulierte_Masseanteile*100,kind='quadratic')
    cum_m_new = sp.interpolate.PchipInterpolator(np.flip(np.log(Siebdurchmesser[0:-1])),np.flip(Kumulierte_Masseanteile)*100)
    
    ax.plot(np.exp(d_new),cum_m_new(d_new),ls='-',color='black')    
    ax.plot(Siebdurchmesser[0:-1],Kumulierte_Masseanteile*100,ls='',marker='d',color='black')
    #
    ax.set_xlabel(r"Korndurchmesser $d$ in mm",fontsize=18)
    #ax.set_ylabel(r"Masseanteil der Körner in Prozent",fontsize=18)
    ax.set_xscale('log')
    ax.axvspan(0.001,0.002,alpha=0.2, color='grey')
    ax.text(0.0015,80,'Feinstes',rotation=90,fontsize=18)
    #
    ax.axvspan(0.002,0.0063,alpha=0.1, color='green')
    ax.text(0.0045,80,'Feinschluff',rotation=90,fontsize=18)
    ax.axvspan(0.0063,0.02,alpha=0.2, color='green')
    ax.text(0.015,80,'Mittelschluff',rotation=90,fontsize=18)
    ax.axvspan(0.02,0.063,alpha=0.3, color='green')
    ax.text(0.048,80,'Grobschluff',rotation=90,fontsize=18)
    #
    ax.axvspan(0.063,0.2,alpha=0.1, color='orange')
    ax.text(0.15,80,'Feinsand',rotation=90,fontsize=18)
    ax.axvspan(0.2,0.63,alpha=0.2, color='orange')
    ax.text(0.48,80,'Mittelsand',rotation=90,fontsize=18)
    ax.axvspan(0.63,2,alpha=0.3, color='orange')
    ax.text(1.5,80,'Grobsand',rotation=90,fontsize=18)
    #
    ax.axvspan(2,6.3,alpha=0.1, color='blue')
    ax.text(4.8,80,'Feinkies', rotation=90,fontsize=18)
    ax.axvspan(6.3,20,alpha=0.2, color='blue')
    ax.text(15,80,'Mittelkies',rotation=90,fontsize=18)
    ax.axvspan(20,63,alpha=0.3, color='blue')
    ax.text(48,80,'Grobkies',rotation=90,fontsize=18)
    #
    ax.axvspan(63,200,alpha=0.3, color='grey')
    ax.text(150,80,'Steine',rotation=90,fontsize=18)
            
    d_10 = d_n(10,d_new,cum_m_new)
    d_30 = d_n(30,d_new,cum_m_new)
    d_60 = d_n(60,d_new,cum_m_new)
    
    ax.plot(d_10,10,marker='o',color='red')
    ax.text(d_10*1.5,8,'$d_{10} = %.3f$ mm' %(d_10),fontsize=18)
    ax.plot(d_30,30,marker='o',color='red')
    ax.text(d_30*1.5,28,'$d_{30} = %.3f$ mm' %(d_30),fontsize=18)
    ax.plot(d_60,60,marker='o',color='red')
    ax.text(d_60*1.5,58,'$d_{60} = %.3f$ mm' %(d_60),fontsize=18)
    
    U = d_60/d_10
    U_res = 'ungleichförmig'
    if (U < 5):
        U_res = 'gleichförmig'
    if (U >= 15):
        U_res = 'sehr ungleichförmig'
    
    Cc = d_30*d_30/(d_60*d_10)
    Cc_res = 'kontinuierlich'
    if (Cc < 1 or Cc > 3):
        Cc_res = 'nicht kontinuierlich'
    
    if (Cc < 1):
        if (U < 3):
            U_res = 'gleichmäßig gestuft'
        elif (U < 6):
            U_res = 'eng gestuft'
        elif (U <= 15):
            U_res = 'mäßig gestuft'
    elif (Cc >=1 and Cc <=3 and U > 15):
        U_res = 'weit gestuft'
    elif (Cc < 0.5 and U > 15):
        U_res = 'intermittierend gestuft'
    else:
        U_res = 'Werte'
    
    ax.text(8,12,U_res+':',fontsize=18)
    ax.text(8,5,'$C_U = %.1f$, $C_C = %.1f$' %(U,Cc),fontsize=18)
    
    #ax.grid(which='both')
    ax.set_xlim(0.001,200)
    ax.set_ylim(0,100)
    
    major_ticks = np.arange(0, 101, 10)
    minor_ticks = np.arange(0, 101, 5)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    
    #ax.set_xticks([0.001,0.002,0.006,0.02,0.063,0.2,0.63,2.0,6.3,20,63])
    #ax.set_xticklabels([0.001,0.002,0.006,0.02,0.063,0.2,0.63,2.0,6.3,20,63])
    for i in [0.002,0.006,0.02,0.063,0.2,0.63,2.0,6.3,20,63]:
        ax.axvline(i,ls='--',lw=1)
        ax.text(i,101,str(i)+' mm',rotation=45)
    
    #minor_ticks_x = np.logspace()
    #ax.set_xticks(minor_ticks_x, minor=True)
    
    ax.grid(which='major', alpha=1.0)
    ax.grid(which='minor', alpha=0.8, ls=':')
    
    fig.tight_layout()
    #fig.savefig('KVK.pdf')

