#################################################
Use to fit specific component                   #
#################################################

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT
from array import array
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
import sys,os,argparse
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
import naked_party as nake
ROOT.gROOT.SetBatch(1)
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data')
parser.add_argument('-id','--ID', nargs='+',help='Cell ID', type=int)
parser.add_argument('-e','--E',nargs='+',help='Min E and Max E',type=int)
parser.add_argument('-type','--Type',nargs='?',help='gamma,lepton,hadron,nan or all')
args = parser.parse_args()

ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100

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
mcPDG = ROOT.RooRealVar("mcPDG", "",-1000,1000)

argSetFit = ROOT.RooArgSet(*[arg for arg in (__experiment__, __run__, clusterCellID, clusterHighestE, clusterTiming, clusterZernikeMVA, isSignal, eff20, minC2TDist, hlt_hadron, mcPDG)])
#clusterTiming.setBins(Bin_num)

Event_type ={'all':[''],'gamma':[' && isSignal==1'],'lepton':[' && (abs(mcPDG)==11 || abs(mcPDG)==13)'],'hadron':[' && (abs(mcPDG)==130 || abs(mcPDG)==211)'],'nan':[' && isSignal!=1 && isSignal!=0']}

Selection = f"hlt_hadron==1 && eff20==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}{Event_type[args.Type][0]}"
print(Selection)

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'

c1 = ROOT.TCanvas('c1', 'c1', 600,490)
#c1.Divide(2)
MC = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst00_{args.E[0]}_{args.E[1]}.root'
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
#file_names = ['MC15_prompt_charged_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)

h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,-200,200)
MC.Draw(f"clusterTiming>>h_mc",Selection)

#mc_sample = ROOT.RooDataHist("mc_s", "mc_s",clusterTiming,h_mc)

mc_sample = ROOT.RooDataSet("mc_s", "mc_s",MC,argSetFit,Selection)

mean = ROOT.RooRealVar("mean", "mean", 0, -100, 100)
sigma = ROOT.RooRealVar("sigma", "sigma", 0.1, 0., 1000)
Width = ROOT.RooRealVar("Width", "Width", 10,0., 1000)

#Gawr = ROOT.RooVoigtian("Gawr", "Gawr", clusterTiming, mean,sigma,Width)
Gawr = ROOT.RooBreitWigner("Gawr", "Gawr", clusterTiming, mean, sigma)
#Gawr = ROOT.RooLandau("Gawr", "Gawr", clusterTiming, mean, sigma)

MEAM = ROOT.RooRealVar("MEAM", "MEAM", 0)
Sigma = ROOT.RooRealVar("Sigma", "Sigma", 10, 0., 1000)
Sigmaa = ROOT.RooRealVar("Sigmaa", "Sigmaa", 10, 0., 1000)
Amelia = ROOT.RooBifurGauss("Amelia", "Amelia", clusterTiming, MEAM, Sigma,Sigmaa)
#Amelia = ROOT.RooGaussian("Amelia", "Amelia", clusterTiming, MEAM, Sigma)

AmeSame = ROOT.RooFFTConvPdf("AmeSame", "AmeSame", clusterTiming, Gawr, Amelia)

coe1 = ROOT.RooRealVar("coe1", "coe1", 0.0,10.,-10.)
coe2 = ROOT.RooRealVar("coe2", "coe2", 0.0,10.,-10.)
Gura = ROOT.RooPolynomial("Gura","Gura", clusterTiming,ROOT.RooArgList(coe1,coe2))

ns = ROOT.RooRealVar("ns", "ns", 500000, 1000, 10000000)
nb = ROOT.RooRealVar("nb", "nb", 500, 0., 10000000)
f = ROOT.RooRealVar("f", "f",0.9,0.,1.)
Shark = ROOT.RooAddPdf("Shark","Shark",ROOT.RooArgList(Gawr,Gura),ROOT.RooArgList(f))

ll = ROOT.RooLinkedList()

#EN = AmeSame.chi2FitTo(mc_sample,ll)
EN = AmeSame.fitTo(mc_sample,ROOT.RooFit.Minos(True),ROOT.RooFit.Save(True))

f = ROOT.TFile("fit_result_test", "RECREATE")
EN.Write("tree")
f.Close()

t_frame_mc = mc_sample.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('mc'))

AmeSame.plotOn(t_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark'))
#Shark.plotOn(t_frame_mc,ROOT.RooFit.Components("Gawr"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gawr'))
#Shark.plotOn(t_frame_mc,ROOT.RooFit.Components("Gura"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('gura'))

Pull_mc = t_frame_mc.pullHist()
pad = ROOT.TPad('pad','pad',0.,0.316,1.0,1.0)
pad.SetLogy()
pad.SetBottomMargin(0)
pad.Draw()
pad.cd()

t_frame_mc.Draw()

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
h_mc.Delete()
Cluster_E = ROOT.TLatex()
Cluster_E.SetTextFont(42)
Cluster_E.SetTextSize(0.045)
Cluster_E.SetTextColor(1)
Cluster_E.SetNDC()
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

#c1.SaveAs(f"./Fit_result/plot/MC/{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#c1.SaveAs(f"{Dataset}_CellID{ID}_{E_min}_{E_max}.png")
c1.SaveAs("test.png")
#input('Press ENTER to exit')
