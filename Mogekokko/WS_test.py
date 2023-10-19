#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT
import sys,os
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
ROOT.gROOT.SetBatch(1)
import naked_party as nake
import nude_pics as pic
f = ROOT.TFile("/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/MC_Model/gamma_Bucket26_CellID1000_1002_50_100.root")
 
args = nake.getInputOptions_service()

'''
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

c1 = ROOT.TCanvas('c1', 'c1', 600,490)
#c1.Divide(2)
MC = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst00_{args.E[0]}_{args.E[1]}.root'
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
#file_names = ['MC15_prompt_charged_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)

data_mc = ROOT.RooDataSet("mc_s", "mc_s",MC,argSetFit,Selection)
'''
ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'

w = f.Get("w")
clusterTiming = w.var("clusterTiming")
model = w.pdf("AmeSame_gamma")
data = w.data("mc_s")

# Fit model to data, plot model
# ---------------------------------------------------------
# Fit model to data
model.fitTo(data,ROOT.RooFit.Minos(True))
t_frame_mc = data.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('mc'))

model.plotOn(t_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark')) 
 
# Draw the frame on the canvas
c = ROOT.TCanvas("rf503_wspaceread", "rf503_wspaceread", 600, 600)
ROOT.gPad.SetLeftMargin(0.15)
t_frame_mc.GetYaxis().SetTitleOffset(1.4)
t_frame_mc.Draw()
 
c.SaveAs("rf503_wspaceread.png")
