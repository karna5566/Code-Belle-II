#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
import sys
import os
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
ROOT.gROOT.SetBatch(1)
import numpy as np
import matplotlib.pyplot as plt
Bin_num = 100
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data')
parser.add_argument('-v','--Var',nargs='?',help='width,Mean,Purity,nevents,log_lh_mc/data and FWHM_mc/data and n_gamma_pull',default='width')
args = parser.parse_args()
Sample = ROOT.TChain('tree')
pwd = '/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/'
Sample.Add(pwd+f'*{args.sample}_*000_*004_*.root')
#Sample.Add(pwd+f'*{args.sample}_6769_6912*.root')
#Sample.Add(pwd+f'*{args.sample}_6000_6029*.root')
#Sample.Add(pwd+f'*{args.sample}_7000_7029*.root')

ID_list = [1000,4000,8000]
marker = ['bo','ro','rD','go','gD']
data = {var: [[] for _ in range(len(ID_list))] for var in ["E", "width", "width_e", "Mean", "Mean_e", "Purity","Purity_e","log_lh_mc","log_lh_mc_e","log_lh_data","log_lh_data_e","nevents","nevents_e","FWHM_mc","FWHM_mc_e","FWHM_data","FWHM_data_e","n_gamma","n_gamma_e","n_gamma_pull","n_gamma_pull_e"]}
YLable = {'width':['Width of smearing Gaussian [ns]',1,9],'Purity':['%',60,100],'Mean':['Mean shift [ns]',-4,7],'log_lh_mc':['-log(LH)',0.,40],'log_lh_data':['-log(LH)',0.,40],'nevents':['# of events',0,40000],'FWHM_mc':['FWHM [ns]',0.,60],'FWHM_data':['FWHM [ns]',0.,60],'n_gamma_pull':['Pull',0.,3],'n_gamma':['# of gamma',0,50000]}
for i in Sample:
	ID = Sample.CellID_lo
	j = ID_list.index(ID)
	data["E"][j].append(Sample.ClusterE)
	data["width"][j].append(Sample.width)
	data["width_e"][j].append(Sample.width_err)
	data["Mean"][j].append(Sample.Mean)
	data["Mean_e"][j].append(Sample.Mean_err)
	data["Purity"][j].append(Sample.Purity*100.)
	data["Purity_e"][j].append(0.)
	data["log_lh_mc"][j].append(Sample.Log_LH_mc)
	data["log_lh_mc_e"][j].append(0.)
	data["log_lh_data"][j].append(Sample.Log_LH_data)
	data["log_lh_data_e"][j].append(0.)
	data["nevents"][j].append(Sample.nevents)
	data["nevents_e"][j].append(0.)
	data["FWHM_mc"][j].append(Sample.FWHM_MC)
	data["FWHM_mc_e"][j].append(0.)
	data["FWHM_data"][j].append(Sample.FWHM_Data)
	data["FWHM_data_e"][j].append(0.)
	data["n_gamma_pull"][j].append(Sample.n_gamma_pull)
	data["n_gamma_pull_e"][j].append(0.)
	data["n_gamma"][j].append(Sample.n_gamma)
	data["n_gamma_e"][j].append(Sample.n_gamma_err)

plt.figure()
for i in range(len(ID_list)):plt.errorbar(data['E'][i], data[args.Var][i], yerr=data[f'{args.Var}_e'][i],fmt=marker[i],label=f'CellID = {ID_list[i]}')

#plt.errorbar(E[0],Purity[0],fmt="o",label='CellID = 1000')
#plt.errorbar(E[1],Purity[1],fmt="o",label='CellID = 4000')
plt.vlines(x=[100,200,400,1000],ymin=[YLable[args.Var][1]],ymax=[YLable[args.Var][2]], colors='c', linestyles='dotted', lw=1)
plt.xlim([0, 1050])
plt.legend(loc='best')
plt.xlabel("ClusterHighestE [MeV]")
#plt.ylabel("Purity [%]")
plt.ylabel(YLable[args.Var][0])
#plt.ylabel("Mean shift")

#c1.SaveAs(f"./Plots/{Dataset}/2D/{Dataset}_CellID{ID}_{pic.Constantinople[Var1][3]}_{pic.Constantinople[Var2][3]}.png")
plt.savefig(f'./Matplot/{args.sample}_{args.Var}.png', bbox_inches='tight')
#input('Press ENTER to exit')
