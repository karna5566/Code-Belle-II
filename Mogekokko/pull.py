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
#ROOT.gROOT.SetBatch(ROOT.kTRUE)
Dataset = sys.argv[1]
ID = sys.argv[2]

Bin_num = 100
Max_value = 500
Min_value = -500

c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
c1.SetLogy()

MC = ROOT.TChain('merged')
Data = ROOT.TChain('merged')

MC.Add('/mnt/qnap_01/user/lch/MC15_B30_Extra/sub00/*.root')
#Data.Add('/mnt/qnap_01/user/lch/B30/sub00/*.root')
Data.Add('/mnt/qnap_01/user/lch/B30/sub00/Qdst_00001_job279435882_00.root')
h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,Min_value,Max_value)

h_data = ROOT.TH1F('h_data','h_data',Bin_num,Min_value,Max_value)

f_pull = ROOT.TH1F('f_pull','f_pull',Bin_num,Min_value,Max_value)

MC.Draw("clusterTiming>>h_mc",f"clusterCellID=={ID} && abs(clusterTiming)<500")
h_mc.Scale(0.25)
Data.Draw("clusterTiming>>h_data",f"clusterCellID=={ID} && abs(clusterTiming)<500")
for i in range(Bin_num):
#	f_pull.SetBinContent(i+1,(h_data.GetBinContent(i+1)-h_mc.GetBinContent(i+1))/h_data.GetBinError(i+1))
	f_pull.SetBinContent(i+1,(h_data.GetBinContent(i+1)-h_mc.GetBinContent(i+1)))
pad = ROOT.TPad('pad','pad',0.,0.33,1.0,1.0)
pad.SetLogy()
pad.SetBottomMargin(0)

pad.Draw()
pad.cd()

h_mc.Draw("Hist")
h_data.Draw("E1 SAME")

Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
#BELLE2Label(0.2,0.89,"(simulation)",(kBlack))
ROOT.BELLE2Label(0.2,0.89,"(preliminary)",(ROOT.kBlack))
Lumi.DrawLatex(0.2, 0.8, "#int #it{L} d#it{t} = 20.5 fb^{-1}")
Lumi.DrawLatex(0.2, 0.7, f"{Dataset[:-2]} {Dataset[-2:]} data")
Lumi.DrawLatex(0.2, 0.6, f"CellID : {ID}")

Lehend = ROOT.TLegend(0.75,0.7,0.95,0.9)
Lehend.AddEntry(h_mc,"rd MC","l")
Lehend.AddEntry(h_data,"Data","p")
Lehend.SetFillStyle(0)
Lehend.SetBorderSize(0)
Lehend.Draw()
c1.cd()
pad_pull = ROOT.TPad('pad_pull','pad_pull',0.0,0.1,1.0,0.33)

pad_pull.SetTopMargin(0)   
pad_pull.Draw()
pad_pull.cd()
f_pull.Draw("E1")
f_pull.GetXaxis().SetTitle("ClusterTiming [ns]")
f_pull.GetYaxis().SetTitle("#frac{Data-MC}{Data Err}")
#c1.SaveAs(f"./Plots/{Dataset}_CellID{ID}.png")
c1.SaveAs(f"test.png")
input('Press ENTER to exit')
