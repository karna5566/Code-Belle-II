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
Dataset = sys.argv[1]
ID = sys.argv[2]
Var = sys.argv[3] 

E_min = int(sys.argv[4])
E_max = int(sys.argv[5])

Bin_num = 100
Max_value = pic.Jerusalem[Var][1]
Min_value = pic.Jerusalem[Var][0]


c1 = ROOT.TCanvas('c1', 'c1', 600, 400)
c1.SetLogy(pic.Jerusalem[Var][6])

MC = ROOT.TChain('merged')
Data = ROOT.TChain('merged')

MC.Add('/mnt/qnap_01/user/lch/MC15_B30_Extra/sub00/*.root')
h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,Min_value,Max_value)

h_data = ROOT.TH1F('h_data','h_data',Bin_num,Min_value,Max_value)
if E_min == E_max :
	Selection = f"clusterCellID=={ID} && abs(clusterTiming)<500 && clusterHighestE > {E_min/1000.}"
	text = f'ClusterHighestE > {E_min/1000.} [GeV]'
else :
	Selection = f"clusterCellID=={ID} && abs(clusterTiming)<500 && clusterHighestE > {E_min/1000.} && clusterHighestE < {E_max/1000.}"
	text = f'ClusterHighestE in\n [{E_min},{E_max}] [MeV]'
print(Selection)
MC.Draw(f"{Var}>>h_mc",Selection)

h_mc.Scale(0.25)
h_mc.GetXaxis().SetTitle(pic.Jerusalem[Var][3])
h_mc.GetYaxis().SetTitle("Candidates per event")
h_mc.Draw("Hist")

Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
ROOT.BELLE2Label(pic.Jerusalem[Var][4],0.89,"(simulation)",(ROOT.kBlack))
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.8, pic.Venezia[Dataset][0])
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.72, f"CellID : {ID}")
if Var != 'clusterHighestE' : Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.67, text)
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.62, f"Mean : {round(h_mc.GetMean(), 2)}")

c1.SaveAs(f"./Plots/{pic.Jerusalem[Var][3]}/{Dataset}_CellID{ID}_{E_min}_{E_max}.png")
#input('Press ENTER to exit')
