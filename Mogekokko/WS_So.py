#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT,math
from ROOT import TMath
from array import array
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
import sys,os
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
import naked_party as nake
ROOT.gROOT.SetBatch(1)
args = nake.getInputOptions_service()
print(args.sample)
print(args.E)
print(args.ID)

ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100

__experiment__ = ROOT.RooRealVar("__experiment__", "__experiment__", 20,0,50)
__run__ = ROOT.RooRealVar("__run__", "__run__",0,0,5000)
clusterCellID = ROOT.RooRealVar("clusterCellID", "clusterCellID", 0, 0, 10000)
clusterHighestE = ROOT.RooRealVar("clusterHighestE", "clusterHighestE", 0, 0, 5000)
clusterTiming = ROOT.RooRealVar("clusterTiming", "clusterTiming",-200,200)
clusterZernikeMVA = ROOT.RooRealVar("clusterZernikeMVA", "",0.25,1)
isSignal = ROOT.RooRealVar("isSignal", "",0,1)
eff20 = ROOT.RooRealVar("eff20", "",0,1)
tight = ROOT.RooRealVar("tight", "",0,1)
minC2TDist = ROOT.RooRealVar("minC2TDist", "",0,1000)
hlt_hadron = ROOT.RooRealVar("hlt_hadron", "",0,1)
mcPDG = ROOT.RooRealVar("mcPDG", "",-1000,1000)

argSetFit = ROOT.RooArgSet(*[arg for arg in (__experiment__, __run__, clusterCellID, clusterHighestE, clusterTiming, clusterZernikeMVA, isSignal, eff20,tight, minC2TDist, hlt_hadron, mcPDG)])
#clusterTiming.setBins(Bin_num)
#clusterZernikeMVA.setBins(75)
#argSetHist = ROOT.RooArgSet(clusterTiming,clusterZernikeMVA)

Event_type ={'all':[''],'gamma':[' && isSignal==1'],'lepton':[' && (abs(mcPDG)==11 || abs(mcPDG)==13)'],'hadron':[' && (abs(mcPDG)==130 || abs(mcPDG)==211)'],'l_h':[' && (abs(mcPDG)==11 || abs(mcPDG)==13 || abs(mcPDG)==130 || abs(mcPDG)==211)'],'nan':[' && isSignal!=1 && isSignal!=0']}

Selection = f"hlt_hadron==1 && tight==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}{Event_type[args.Type][0]}"
print(Selection)

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'

c1 = ROOT.TCanvas('c1', 'c1', 600,490)
#c1.Divide(2)
MC = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst*_{args.E[0]}_{args.E[1]}.root'
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
#file_names = ['MC15_prompt_charged_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)

#h_mc = ROOT.TH2F('h_mc','h_mc',Bin_num,75,-200,200,0.25,1.0)
h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,-200,200)
#MC.Draw(f"clusterZernikeMVA:clusterTiming>>h_mc",Selection)
MC.Draw(f"clusterTiming>>h_mc",Selection)

#mc_sample = ROOT.RooDataHist("mc_s", "mc_s",argSetHist,h_mc)
mc_sample = ROOT.RooDataSet("mc_s", "mc_s",MC,argSetFit,Selection)

#Timing

mean = ROOT.RooRealVar("mean", "mean", 0, -100, 100)
sigma = ROOT.RooRealVar("sigma", "sigma", 0.1, 0., 1000)
ssigma = ROOT.RooRealVar("ssigma", "ssigma", 0.1, 0., 1000)
Width = ROOT.RooRealVar("Width", "Width", 10,0., 1000)

#Gawr = ROOT.RooVoigtian("Gawr", "Gawr", clusterTiming, mean,sigma,Width)
Gawr = ROOT.RooBreitWigner("Gawr", "Gawr", clusterTiming, mean, sigma)
#Gawr = ROOT.RooBifurGauss("Gawr", "Gawr", clusterTiming, mean, sigma,ssigma)
#Gawr = ROOT.RooLandau("Gawr", "Gawr", clusterTiming, mean, sigma)

MEAM = ROOT.RooRealVar("MEAM", "MEAM", 0)
Sigma = ROOT.RooRealVar("Sigma", "Sigma", 10, 0., 10000)
Sigmaa = ROOT.RooRealVar("Sigmaa", "Sigmaa", 10, 0., 10000)
Amelia = ROOT.RooBifurGauss("Amelia", "Amelia", clusterTiming, MEAM, Sigma,Sigmaa)
#Amelia = ROOT.RooGaussian("Amelia", "Amelia", clusterTiming, MEAM, Sigma)

AmeSame_gamma = ROOT.RooFFTConvPdf(f"AmeSame_gamma", "AmeSame", clusterTiming, Gawr, Amelia)

c1_t = ROOT.RooRealVar("c1_t", "",10,-100,100)
c2_t = ROOT.RooRealVar("c2_t", "",0.5,-100,100)
Function_mva = ROOT.RooGenericPdf("Function_mva","1/(1+exp(@0*(@1-@2)))",ROOT.RooArgList(c1_t,clusterTiming,c2_t))

f = ROOT.RooRealVar("f", "f",0.9,0.,1.)
AmeSame_l_h = ROOT.RooAddPdf("AmeSame_l_h","",ROOT.RooArgList(AmeSame_gamma,Function_mva),ROOT.RooArgList(f)) 

coe1 = ROOT.RooRealVar("coe1", "coe1", 0.0,100.,-100.)
coe2 = ROOT.RooRealVar("coe2", "coe2", 0.0,100.,-100.)
Gura = ROOT.RooPolynomial("Gura","Gura", clusterTiming,ROOT.RooArgList(coe1,coe2))
AmeSame_nan = ROOT.RooAddPdf("AmeSame_nan","",ROOT.RooArgList(AmeSame_gamma,Gura),ROOT.RooArgList(f))


ns = ROOT.RooRealVar("ns", "ns", 500000, 1000, 10000000)
nb = ROOT.RooRealVar("nb", "nb", 500, 0., 10000000)
Shark = ROOT.RooAddPdf("Shark","Shark",ROOT.RooArgList(Gawr,Gura),ROOT.RooArgList(f))

Argus_coe1 = ROOT.RooRealVar("Argus_coe1","",0.9,0.3,1.)
Argus_coe2 = ROOT.RooRealVar("Argus_coe2","",0.,-100,100)
Argus = ROOT.RooArgusBG(f"Argus_{args.Type}","",clusterZernikeMVA,Argus_coe1,Argus_coe2)

mean_mva = ROOT.RooRealVar("mean_mva", "mean_mva",0.9,0.,1.0)
sigma_mva = ROOT.RooRealVar("sigma_mva", "sigma_mva",1.,0.,50)
a_mva = ROOT.RooRealVar("a_mva", "a_mva",0.,0.,500)
n_mva = ROOT.RooRealVar("n_mva", "n_mva",0.,0.,500)
sigmaa_mva = ROOT.RooRealVar("sigmaa_mva", "sigmaa_mva",10,0.,50)
B_guass_mva = ROOT.RooBifurGauss(f"B_guass_mva_{args.Type}", "", clusterZernikeMVA,mean_mva,sigma_mva,sigmaa_mva)
B_Crystal_mva = ROOT.RooCrystalBall (f"B_Crystal_mva_{args.Type}", "", clusterZernikeMVA,mean_mva,sigma_mva,a_mva,n_mva)

#minus_x = ROOT.RooRealVar("minus_x", "@0*(-1)",ROOT.RooArgList(clusterZernikeMVA))

mean_TD = ROOT.RooRealVar("mean_TD", "mean_TD",50,25,200)
sigma_TD = ROOT.RooRealVar("sigma_TD", "sigma_TD",5,0.,200)
sigmaa_TD = ROOT.RooRealVar("sigmaa_TD", "sigmaa_TD",50,0.,200)
B_guass_TD = ROOT.RooBifurGauss(f"B_guass_TD_{args.Type}", "",minC2TDist,mean_TD,sigma_TD,sigmaa_TD)
Landau_TD = ROOT.RooLandau(f"Landau_TD_{args.Type}","",minC2TDist,mean_TD,sigma_TD)


parameters = [mean,sigma,Sigma, Sigmaa]
#parameters = = [mean_mva,sigma_mva,sigmaa_mva]
if args.Type == 'l_h' : 
	#Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_l_h,B_guass_mva))
	Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_l_h))
	parameters += [c1_t,c2_t,f]
elif args.Type == 'nan':
	#Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_nan,B_guass_mva))
	Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_nan))
	parameters += [coe1,coe2,f]
elif args.Type == 'gamma':
	#Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_gamma,B_guass_mva)) 
	Com_model = ROOT.RooProdPdf(f"Com_model_{args.Type}","",ROOT.RooArgList(AmeSame_gamma)) 

#ll = ROOT.RooLinkedList()

#EN = Com_model.chi2FitTo(mc_sample,ll)
EN = Com_model.fitTo(mc_sample,ROOT.RooFit.Hesse(True),ROOT.RooFit.Save(True))

for param in parameters:param.setConstant(True)

#f = ROOT.TFile("fit_result_test", "RECREATE")
#EN.Write("tree")
#f.Close()

t_frame_mc = mc_sample.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('mc'))

Com_model.plotOn(t_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark_t'))
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
#h_mc.Delete()
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

c1.SaveAs(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/plot/MC_Model/clusterTiming/{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#c1.SaveAs(f"./{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#c1.Clear()
'''
c2 = ROOT.TCanvas('c2', 'c2', 600,490)
mva_frame_mc = mc_sample.plotOn(clusterZernikeMVA.frame(75),ROOT.RooFit.Name('mc'))

Com_model.plotOn(mva_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark_mva'))

mva_Pull_mc = mva_frame_mc.pullHist()
pad.SetLogy(0)
pad.Draw()
pad.cd()
mva_frame_mc.Draw()
c2.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)

pad_pull_mva = ROOT.TPad('pad_pull_mva','pad_pull_mva',0.0,0.068,1.0,0.3)
pad_pull.Draw()
pad_pull.cd()
pull_frame_mva = clusterZernikeMVA.frame(75)
pull_frame_mva.addPlotable(mva_Pull_mc, "P")
pull_frame_mva.GetYaxis().SetLabelFont(63)
pull_frame_mva.GetYaxis().SetLabelSize(12)
pull_frame_mva.GetXaxis().SetLabelFont(63)
pull_frame_mva.GetXaxis().SetLabelSize(12)
pull_frame_mva.Draw()
c2.cd()
X_title.DrawLatex(0.7, 0.02,"clusterZernikeMVA")
Y_title.DrawLatex(0.07, 0.15,"Pull")

c2.SaveAs(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/plot/MC_Model/clusterZernikeMVA/{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
'''
'''
c3 = ROOT.TCanvas('c3', 'c3', 600,490)
TD_frame_mc = mc_sample.plotOn(minC2TDist.frame(100),ROOT.RooFit.Name('mc'))

Com_model.plotOn(TD_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark_mva'))

TD_Pull_mc = TD_frame_mc.pullHist()
pad.SetLogy(0)
pad.Draw()
pad.cd()
TD_frame_mc.Draw()
c3.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)

pad_pull_TD = ROOT.TPad('pad_pull_TD','pad_pull_TD',0.0,0.068,1.0,0.3)
pad_pull.Draw()
pad_pull.cd()
pull_frame_TD = minC2TDist.frame(100)
pull_frame_TD.addPlotable(TD_Pull_mc, "P")
pull_frame_TD.GetYaxis().SetLabelFont(63)
pull_frame_TD.GetYaxis().SetLabelSize(12)
pull_frame_TD.GetXaxis().SetLabelFont(63)
pull_frame_TD.GetXaxis().SetLabelSize(12)
pull_frame_TD.Draw()
c3.cd()
X_title.DrawLatex(0.7, 0.02,"minC2TDist")
Y_title.DrawLatex(0.07, 0.15,"Pull")

c3.SaveAs(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/plot/MC_Model/minC2TDist/{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
'''
#input('Press ENTER to exit')

w = ROOT.RooWorkspace("w", "workspace")

getattr(w,'import')(Com_model) 
getattr(w,'import')(AmeSame_gamma) 
getattr(w,'import')(B_guass_mva) 
if args.Type == 'l_h' : 
	getattr(w,'import')(Function_mva)
	getattr(w,'import')(AmeSame_l_h)
elif args.Type == 'nan':
	getattr(w,'import')(Gura)
	getattr(w,'import')(AmeSame_nan)
getattr(w,'import')(mc_sample) 

w.Print()
 
# Save workspace in file
# -------------------------------------------
 
# Save the workspace into a ROOT file
w.writeToFile(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/MC_Model/{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.root")
#w.writeToFile(f"./3D_{args.Type}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.root")
