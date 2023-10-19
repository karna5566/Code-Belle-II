#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT
from array import array
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
import sys
import os
import argparse
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
import naked_party as nake
ROOT.gROOT.SetBatch(1)
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data')
parser.add_argument('-id','--ID', nargs='+',help='Cell ID', type=int)
parser.add_argument('-e','--E',nargs='+',help='Min E and Max E',type=int)
args = parser.parse_args()

if len(args.ID) == 1 : 
	ID_location = args.ID[0] 
	ID_text = f"CellID : {args.ID[0]}"
else : 
	ID_location = '_'.join([str(args.ID[0]),str(args.ID[-1])])
	ID_text = f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100

myfile = ROOT.TFile(f"./Fit_result/root_file/Resolution_{args.sample}_{ID_location}_{args.E[0]}_{args.E[1]}.root","recreate")

tree = ROOT.TTree("tree","Li Ling Si Han")
width = array('d', [ 0. ])
tree.Branch("width",width,"width/D")
width_err = array('d', [ 0. ])
tree.Branch("width_err",width_err,"width_err/D")
Mean = array('d', [ 0. ])
tree.Branch("Mean",Mean,"Mean/D")
Mean_err = array('d', [ 0. ])
tree.Branch("Mean_err",Mean_err,"Mean_err/D")
#Label = array('i', [ 0 ])
#tree.Branch("Label",Label,"Label/I")
ClusterE = array('d', [ 0. ])
tree.Branch("ClusterE",ClusterE,"ClusterE/D")
ClusterE_err = array('d', [ 0. ])
tree.Branch("ClusterE_err",ClusterE,"ClusterE_err/D")
CellID_lo = array('i', [ 0 ])
tree.Branch("CellID_lo",CellID_lo,"CellID_lo/I")
CellID_up = array('i', [ 0 ])
tree.Branch("CellID_up",CellID_up,"CellID_up/I")


#Label[0] = int(Dataset[-2:])
ClusterE[0] = (args.E[0]+args.E[1])/2.
ClusterE_err[0] = (args.E[1]-args.E[0])/2.
CellID_lo[0] = args.ID[0]
CellID_up[0] = args.ID[-1]

__experiment__ = ROOT.RooRealVar("__experiment__", "__experiment__", 20,0,50)
__run__ = ROOT.RooRealVar("__run__", "__run__",0,0,5000)
clusterCellID = ROOT.RooRealVar("clusterCellID", "clusterCellID", 0, 0, 10000)
clusterHighestE = ROOT.RooRealVar("clusterHighestE", "clusterHighestE", 0, 0, 5000)
clusterTiming = ROOT.RooRealVar("clusterTiming", "",-200,200)
clusterZernikeMVA = ROOT.RooRealVar("clusterZernikeMVA", "",0,1)
isSignal = ROOT.RooRealVar("isSignal", "",0,1)
eff20 = ROOT.RooRealVar("eff20", "",0,1)
minC2TDist = ROOT.RooRealVar("minC2TDist", "",0,1000)
hlt_hadron = ROOT.RooRealVar("hlt_hadron", "",0,1)

argSetFit = ROOT.RooArgSet(__experiment__)
argSetFit.add(__run__)
argSetFit.add(clusterCellID)
argSetFit.add(clusterHighestE)
argSetFit.add(clusterTiming)
argSetFit.add(clusterZernikeMVA)
argSetFit.add(isSignal)
argSetFit.add(eff20)
argSetFit.add(minC2TDist)
argSetFit.add(hlt_hadron)


Selection = f"hlt_hadron==1 && eff20==1 && clusterZernikeMVA>0.75 && minC2TDist>75 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"
#Selection = f"hlt_hadron==1 && eff20==1 && clusterZernikeMVA>0.25 && minC2TDist>50 && abs(clusterTiming)<200 && clusterCellID=={ID}"

Extra_selection = " && isSignal!=1 && isSignal!=0"

if args.E[0] == args.E[1] :
	Selection += f" && clusterHighestE > {args.E[0]/1000.}"
	text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]'
else :
	Selection += f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
	text = f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'
c1 = ROOT.TCanvas('c1', 'c1', 600,490)
#c1.Divide(2)
MC = ROOT.TChain('merged')
Data = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'

#MC.Add(pwd+'MC15_prompt_ss_g/Qdst00.root')
MC.Add(pwd+'MC15_prompt_mixed_g/*.root')
MC.Add(pwd+'MC15_prompt_charged_g/*.root')
MC.Add(pwd+'MC15_prompt_cc_g/*.root')
MC.Add(pwd+'MC15_prompt_dd_g/*.root')
MC.Add(pwd+'MC15_prompt_ss_g/*.root')
MC.Add(pwd+'MC15_prompt_uu_g/*.root')
MC.Add(pwd+'MC15_prompt_tt_g/*.root')

Data.Add(pwd+'Data_prompt_all_g/*.root')
#Data.Add(pwd+'Data_prompt_all_g/Qdst00.root')

mc_sample = ROOT.RooDataSet("mc_s", "mc_s",MC,argSetFit,Selection)
data_sample = ROOT.RooDataSet("data_s", "data_s",Data,argSetFit,Selection)

mean = ROOT.RooRealVar("mean", "mean", 0, -100, 100)
sigma = ROOT.RooRealVar("sigma", "sigma", 10, 0., 1000)

#Gawr = ROOT.RooKeysPdf("Gawr", "Gawr", clusterTiming, mc_sample)
Gawr = ROOT.RooBreitWigner("Gawr", "Gawr", clusterTiming, mean, sigma)
#Gawr = ROOT.RooGaussian("Gawr", "Gawr", clusterTiming, mean, sigma)

MEAM = ROOT.RooRealVar("MEAM", "MEAM", 0)
Sigma = ROOT.RooRealVar("Sigma", "Sigma", 10, 0., 1000)
Sigmaa = ROOT.RooRealVar("Sigmaa", "Sigmaa", 10, 0., 1000)
Amelia = ROOT.RooBifurGauss("Amelia", "Amelia", clusterTiming, MEAM, Sigma,Sigmaa)

AmeSame = ROOT.RooFFTConvPdf("AmeSame", "AmeSame", clusterTiming, Gawr, Amelia)

coe = ROOT.RooRealVar("s", "s", 0.3, -100, 100)
Gura = ROOT.RooPolynomial("Gura","Gura", clusterTiming,coe)
#Gura = ROOT.RooBreitWigner("Gawr", "Gawr", clusterTiming, MEAM, Sigma)
#Gura = ROOT.RooGaussian("Gura", "Gura", clusterTiming, MEAM, Sigma)

ns = ROOT.RooRealVar("ns", "ns", 500000, 1000, 10000000)
nb = ROOT.RooRealVar("nb", "nb", 500, 0., 10000000)
f = ROOT.RooRealVar("f", "f",0.9,0.,1.)
Shark = ROOT.RooAddPdf("Shark","Shark",ROOT.RooArgList(Gawr,Gura),ROOT.RooArgList(f))

EN = AmeSame.fitTo(mc_sample,ROOT.RooFit.Minos(True))

t_frame_mc = mc_sample.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('mc'))

AmeSame.plotOn(t_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark'))
#Shark.plotOn(t_frame_mc,ROOT.RooFit.Components("Gawr"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gawr'))
#Shark.plotOn(t_frame_mc,ROOT.RooFit.Components("Gura"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('gura'))
Pull_mc = t_frame_mc.pullHist()

class Fitting_plot:
	def __init__(self,draw_sample,draw_frame):
		self.draw_sample = draw_sample  
		self.draw_frame = draw_frame
	def draw(self):
		pad = ROOT.TPad('pad','pad',0.,0.316,1.0,1.0)
		pad.SetLogy()
		pad.SetBottomMargin(0)
		pad.Draw()
		pad.cd()
		self.draw_frame.Draw()




legend = ROOT.TLegend(0.65,0.93,0.95,0.63)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.045)
legend.SetTextFont(42)
legend.AddEntry(t_frame_mc.findObject("mc"), "MC", "p")
legend.AddEntry(t_frame_mc.findObject("shark"), "Total fit", "l")
#legend.AddEntry(t_frame.findObject("gawr"), "$\mathrm{\gamma}$", "l")
#legend.AddEntry(t_frame.findObject("gura"), "Background", "l")
legend.Draw()

Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
ROOT.BELLE2Label(0.2,0.89,"",(ROOT.kBlack))
Lumi.DrawLatex(0.3, 0.89,"(simulation)" )
Lumi.DrawLatex(0.2, 0.8, pic.Venezia[args.sample][1])
Lumi.DrawLatex(0.2, 0.7, f"MC15_rd ({pic.Venezia[args.sample][5]} data)")
Lumi.DrawLatex(0.2, 0.65, ID_text)
c1.cd()
Cluster_E = ROOT.TLatex()
Cluster_E.SetTextFont(42)
Cluster_E.SetTextSize(0.045)
Cluster_E.DrawLatex(0.1, 0.025, text)

pad_pull = ROOT.TPad('pad_pull','pad_pull',0.0,0.068,1.0,0.3)
#pad_pull.SetTopMargin(0)
pad_pull.Draw()
pad_pull.cd()

pull_frame = clusterTiming.frame(100)
pull_frame.addPlotable(Pull_mc, "P")
pull_frame.GetYaxis().SetLabelFont(63)
pull_frame.GetYaxis().SetLabelSize(12)
pull_frame.GetXaxis().SetLabelFont(63)
pull_frame.GetXaxis().SetLabelSize(12)
pull_frame.Draw()
c1.cd()
X_title = ROOT.TLatex()
X_title.SetTextFont(42)
X_title.SetNDC()
X_title.SetTextColor(1)
X_title.SetTextSize(0.05)
X_title.DrawLatex(0.7, 0.02,"clusterTiming [ns]")

Y_title = ROOT.TLatex()
Y_title.SetTextFont(42)
Y_title.SetNDC()
Y_title.SetTextColor(1)
Y_title.SetTextSize(0.05)
Y_title.SetTextAngle(90)
Y_title.DrawLatex(0.07, 0.15,"Pull")

c1.SaveAs(f"./Fit_result/plot/MC/{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#c1.SaveAs(f"{Dataset}_CellID{ID}_{E_min}_{E_max}.png")
#c1.SaveAs("test.png")
#input('Press ENTER to exit')

mean.setConstant(True)
sigma.setConstant(True)
Sigma.setConstant(True)
Sigmaa.setConstant(True)

mean_shift = ROOT.RooRealVar("mean_shift", "mean_shift",0,-100,100)
mean_data = ROOT.RooFormulaVar("mean_data","@0+@1",ROOT.RooArgSet(mean,mean_shift))
Gawr_data = ROOT.RooBreitWigner("Gawr_data", "Gawr_data", clusterTiming, mean_data, sigma)
AmeSame_data = ROOT.RooFFTConvPdf("AmeSame_data", "AmeSame_data", clusterTiming, Gawr_data, Amelia)



Mass = ROOT.RooRealVar("Mass", "Mass", 0, -100, 100)
Mu = ROOT.RooRealVar("Mu", "Mu", 0, -100, 100)
Lamda = ROOT.RooRealVar("Lamda", "Lamda", 0, -100, 100)
Gamma = ROOT.RooRealVar("Gamma", "Gamma", 0, -100, 100)
Delta = ROOT.RooRealVar("Delta", "Delta", 0, -100, 100)
MAEN = ROOT.RooRealVar("MAEN", "MAEN", 0)
sIgma = ROOT.RooRealVar("sIgma", "sIgma", 10, 0., 1000)
sIgmaa = ROOT.RooRealVar("sIgmaa", "sIgmaa", 10, 0., 1000)

#Ina = ROOT.RooBifurGauss("Ina","Ina",clusterTiming,MAEN,sIgma,sIgmaa)
Ina = ROOT.RooGaussian("Ina","Ina",clusterTiming,MAEN,sIgma)
#Ina = ROOT.RooJohnson("Ina","Ina",clusterTiming,Mu,Lamda,Gamma,Delta)

InaAmeSame = ROOT.RooFFTConvPdf("InaAmeSame", "InaAmeSame", clusterTiming,AmeSame_data,Ina)
HoloEN = InaAmeSame.fitTo(data_sample,ROOT.RooFit.Minos(True))

Mean[0] = mean_shift.getVal()
Mean_err[0] = mean_shift.getError()
width[0] = sIgma.getVal()
width_err[0] = sIgma.getError()

t_frame_data = data_sample.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('data'))
InaAmeSame.plotOn(t_frame_data,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('InaAmeSame'))
Pull_data = t_frame_data.pullHist()
pad.Draw()
pad.cd()

t_frame_data.Draw()
legend.Clear()
legend.AddEntry(t_frame_data.findObject("data"), "Data", "p")
legend.AddEntry(t_frame_data.findObject("InaAmeSame"), "Total fit", "l")
legend.Draw()

ROOT.BELLE2Label(0.2,0.89,"",(ROOT.kBlack))
Lumi.DrawLatex(0.3, 0.89,"(preliminary)" )
Lumi.DrawLatex(0.2, 0.8, pic.Venezia[args.sample][0])
Lumi.DrawLatex(0.2, 0.7, f"{pic.Venezia[args.sample][5]} data")
Lumi.DrawLatex(0.2, 0.65, ID_text)
c1.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)
pad_pull.Draw()
pad_pull.cd()
pull_frame.remove()
pull_frame.addPlotable(Pull_data, "P")
pull_frame.Draw()
c1.cd()
X_title.DrawLatex(0.7, 0.02,"clusterTiming [ns]")
Y_title.DrawLatex(0.07, 0.15,"Pull")

c1.SaveAs(f"./Fit_result/plot/Data/{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
tree.Fill()
tree.Write()
myfile.Close()

