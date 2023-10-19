#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%matplotlib inline
#from belle2PlotStyle import setBelle2PlotStyle
import numpy as np
import math
import ROOT
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.SetBelle2Style()
import sys
import os
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
ID = sys.argv[1]
E_min = int(sys.argv[2])
E_max = int(sys.argv[3])


#c1 = ROOT.TCanvas('c1', 'c1', 600, 400)

F1 = ROOT.TH1F("FOM","FOM",250,0,1)

gamma = ROOT.TChain("merged")
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra'
#gamma.Add(pwd+'/MC15_prompt_dd_g/Qdst00.root')
gamma.Add(pwd+'/MC15_prompt_dd_g/*.root')
gamma.Add(pwd+'/MC15_prompt_uu_g/*.root')
gamma.Add(pwd+'/MC15_prompt_ss_g/*.root')
gamma.Add(pwd+'/MC15_prompt_charged_g/*.root')
Selection = f"hlt_hadron==1 && eff20==1 && clusterCellID=={ID} && abs(clusterTiming)<200 && clusterHighestE > {E_min/1000.} && clusterHighestE < {E_max/1000.}"

t_s = gamma.GetEntries("isSignal==1 && "+Selection)
t_b = gamma.GetEntries("isSignal!=1 && "+Selection)
num_bin = 16
X = np.arange(0,80,80./num_bin)
Y = np.arange(0,0.8,0.8/num_bin)
Z = np.zeros((num_bin, num_bin))

FOM = 0.
Track_D = 0.
Z_mva = 0.

e_s = 0.
e_b = 0.
for i in np.linspace(0., 80., num=num_bin, endpoint=False):
	for j in np.linspace(0.0, 0.8, num=num_bin, endpoint=False):
		n_s = gamma.GetEntries(Selection+" && isSignal==1 && minC2TDist>%f && clusterZernikeMVA>%f" %(i,j))
		n_b = gamma.GetEntries(Selection+" && isSignal!=1 && minC2TDist>%f && clusterZernikeMVA>%f" %(i,j))
		fom = n_s/(n_s+n_b)
		#fom = n_s/math.sqrt(n_s+n_b)
		#Z[round(i*num_bin)][round(j*num_bin)]=fom
		#if (n_s+n_b)<10 : print(f"# of signal = {n_s} and # of bkg = {n_b} when i = {i} j = {j}")
		#print("FOM = %.4f, I = %d, J = %d, Z = %4f"%(fom,I,J,Z[I][J]))
		if (fom>FOM):
			FOM = fom
			Track_D = i
			Z_mva = j
			e_s = n_s
			e_b = n_b
'''
fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(1,1,1, projection='3d')
pi = np.pi

X,Y = np.meshgrid(np.array(X),np.array(Y))
#X = np.array(X)
#Y = np.array(Y)


ax.plot_surface(X, Y, Z, alpha=0.25,cmap="inferno")
#ax.contour(X, Y, Z,3, zdir='x', offset=0., cmap=plt.cm.coolwarm)
#ax.contour(X, Y, Z,0, zdir='y', offset=1., cmap=plt.cm.coolwarm)
#plot FOM line
ax.plot([Track_D,Track_D], [1.,1.],zs=[0.,FOM],color='blue')
ax.plot([0.,0.],[Z_mva,Z_mva],zs=[0.,FOM],color='red')
for i in range(num_bin):
	ax.plot(i/float(num_bin),1.,Z[round(Track_D*num_bin)][i],'.',color='blue',markersize=3)
	ax.plot(0.,i/float(num_bin),Z[i][round(Z_mva*num_bin)],'.',color='red',markersize=3)
ax.set(xlim=(0.,1.), ylim=(0.,1.), zlim=(0.,FOM+0.0005),xlabel='clusterZernikeMVA', ylabel='minC2TDist', zlabel='FOM')
plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
plt.show()
'''
#for i in range(50,60):print(Z[50][i])
#print(X)
print("FOM = %.4f, minC2TDist = %.d , clusterZernikeMVA = %.3f with %.2f signal %.2f BB ClusterID = %s  Emin = %s\n" % (FOM,Track_D,Z_mva,e_s,e_b,ID,E_min))


