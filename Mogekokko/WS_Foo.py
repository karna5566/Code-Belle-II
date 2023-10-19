#################################################
# Use to fit data & MC to get smearing function #
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
args = parser.parse_args()

ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100

#Import PDF and fitting parameters
f_gamma = ROOT.TFile(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/MC_Model/gamma_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.root")
w_gamma = f_gamma.Get("w")
model_gamma = w_gamma.pdf("Com_model_gamma")
mean_gamma = w_gamma.var("mean")
sigma_gamma = w_gamma.var("sigma")
Amelia_gamma = w_gamma.pdf("AmeSame_gamma")
B_guass_mva_gamma = w_gamma.pdf("B_guass_mva_gamma")

mc_sample_gamma = w_gamma.data("mc_s")
f_gamma.Close()


f_nan = ROOT.TFile(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/MC_Model/nan_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.root")
w_nan = f_nan.Get("w")
model_nan = w_nan.pdf("Com_model_nan")
AmeSame_nan = w_nan.pdf("AmeSame_gamma")
Gura_nan = w_nan.pdf("Gura")
f1_nan = w_nan.var("f")
B_guass_mva_nan = w_nan.pdf("B_guass_mva_nan")
mc_sample_nan = w_nan.data("mc_s")
f_nan.Close()

f_l_h = ROOT.TFile(f"/home/belle2/lch/Mogege/Mogekokko/Fit_result/root_file/MC_Model/l_h_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.root")
w_l_h = f_l_h.Get("w")
model_l_h = w_l_h.pdf("Com_model_l_h")
mc_sample_l_h = w_l_h.data("mc_s")
f_l_h.Close()

myfile = ROOT.TFile(f"./Fit_result/root_file/Resolution_{args.sample}_{ID_location}_{args.E[0]}_{args.E[1]}.root","recreate")

fit_tree = ROOT.TTree("tree","Li Ling Si Han")
#nake.setup_tree_branches(tree)

width = array('d', [0.])
fit_tree.Branch("width", width, "width/D")
width_err = array('d', [0.])
fit_tree.Branch("width_err", width_err, "width_err/D")
Mean = array('d', [0.])
fit_tree.Branch("Mean", Mean, "Mean/D")
Mean_err = array('d', [0.])
fit_tree.Branch("Mean_err", Mean_err, "Mean_err/D")
ClusterE = array('d', [0.])
fit_tree.Branch("ClusterE", ClusterE, "ClusterE/D")
ClusterE_err = array('d', [0.])
fit_tree.Branch("ClusterE_err", ClusterE_err, "ClusterE_err/D")
CellID_lo = array('i', [0])
fit_tree.Branch("CellID_lo", CellID_lo, "CellID_lo/I")
CellID_up = array('i', [0])
fit_tree.Branch("CellID_up", CellID_up, "CellID_up/I")
Purity = array('d', [0.])
fit_tree.Branch("Purity", Purity, "Purity/D")    
Log_LH_mc = array('d', [0.])    
fit_tree.Branch("Log_LH_mc", Log_LH_mc, "Log_LH_mc/D")    
Log_LH_data = array('d', [0.])    
fit_tree.Branch("Log_LH_data", Log_LH_data, "Log_LH_data/D")
nevents = array('i', [0])
fit_tree.Branch("nevents", nevents, "nevents/I")
FWHM_MC = array('d', [0.])
fit_tree.Branch("FWHM_MC", FWHM_MC, "FWHM_MC/D")
FWHM_Data = array('d', [0.])
fit_tree.Branch("FWHM_Data", FWHM_Data, "FWHM_Data/D")
Mean_MC = array('d', [0.])
fit_tree.Branch("Mean_MC", Mean_MC, "Mean_MC/D")
Mean_MC_err = array('d', [0.])
fit_tree.Branch("Mean_MC_err", Mean_MC_err, "Mean_MC_err/D")
n_gamma = array('d', [0.])
fit_tree.Branch("n_gamma", n_gamma, "n_gamma/D")  
n_gamma_err = array('d', [0.])
fit_tree.Branch("n_gamma_err", n_gamma_err, "n_gamma_err/D")
n_gamma_pull = array('d', [0.])
fit_tree.Branch("n_gamma_pull", n_gamma_pull, "n_gamma_pull/D")


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
clusterZernikeMVA = ROOT.RooRealVar("clusterZernikeMVA", "",0.25,1)
isSignal = ROOT.RooRealVar("isSignal", "",0,1)
tight = ROOT.RooRealVar("tight", "",0,1)
minC2TDist = ROOT.RooRealVar("minC2TDist", "",0,1000)
hlt_hadron = ROOT.RooRealVar("hlt_hadron", "",0,1)

argSetFit = ROOT.RooArgSet(*[arg for arg in (__experiment__, __run__, clusterCellID, clusterHighestE, clusterTiming, clusterZernikeMVA, isSignal, tight, minC2TDist, hlt_hadron)])
clusterTiming.setBins(100)
clusterZernikeMVA.setBins(75)
#minC2TDist.setBins(100)
argSetHist = ROOT.RooArgSet(clusterTiming,clusterZernikeMVA)
clusterZernikeMVA.setRange("sigRegion",0.5,0.85)

#Selection = f"hlt_hadron==1 && eff20==1 && clusterZernikeMVA>{pic.Merv[repr(args.E)][0]} && minC2TDist>{pic.Merv[repr(args.E)][1]} && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"
Selection = f"hlt_hadron==1 && tight==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"
print(Selection)
Extra_selection = " && isSignal!=1 && isSignal!=0"

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'
c1 = ROOT.TCanvas('c1', 'c1', 600,490)
#c1.Divide(2)
MC = ROOT.TChain('merged')
Data = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst00_{args.E[0]}_{args.E[1]}.root'
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
#file_names = ['MC15_prompt_charged_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)

Data.Add(pwd+'Data_prompt_all_g/'+ppwd)
#Data.Add(pwd+'Data_prompt_all_g/Qdst00.root')

nevents[0] = Data.GetEntries(Selection)


h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,-200,200) if args.E[0] >= 200 else ROOT.TH2F('h_mc','h_mc',Bin_num,-200,200,75,0.25,1.0)
MC.Draw(f"clusterTiming>>h_mc",Selection) if args.E[0] >= 200 else MC.Draw(f"clusterZernikeMVA:clusterTiming>>h_mc",Selection)
#h_mc = ROOT.TH2F('h_mc','h_mc',Bin_num,-200,200,75,0.25,1.0)
#MC.Draw(f"clusterZernikeMVA:clusterTiming>>h_mc",Selection)

#h_data = ROOT.TH1F('h_data','h_data',Bin_num,-200,200)
#Data.Draw(f"clusterTiming>>h_data",Selection)
h_data = ROOT.TH2F('h_data','h_data',Bin_num,-200,200,75,0.25,1.0)
Data.Draw(f"clusterZernikeMVA:clusterTiming>>h_data",Selection)

mc_sample = ROOT.RooDataHist("mc_s", "mc_s",argSetHist,h_mc)
data_sample = ROOT.RooDataHist("data_s", "data_s",argSetHist,h_data)

#mc_sample = ROOT.RooDataSet("mc_s", "mc_s",MC,argSetFit,Selection)
#data_sample = ROOT.RooDataSet("data_s", "data_s",Data,argSetFit,Selection)

#n_gamma = 33611
#n_nan = 13153
#n_l_h = 2562


mc_sample_l_h.append(mc_sample_nan)
mc_sample_l_h.append(mc_sample_gamma)
rg_mc = ROOT.RooRealVar("rg_mc","rg_mc",30000,-1000000,1000000) if MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)<0.9 else ROOT.RooRealVar("rg_mc","rg_mc",MC.GetEntries(Selection))
rn_mc = ROOT.RooRealVar("rn_mc","rn_mc",1000,-1000000,1000000) if MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)<0.9 else ROOT.RooRealVar("rn_mc","rn_mc",0) 
rl_mc = ROOT.RooRealVar("rl_mc","rl_mc",2500,-10000,10000) if MC.GetEntries(Selection+" && isSignal==0")/MC.GetEntries(Selection) > 0.05  else ROOT.RooRealVar("rl_mc","rl_mc",0)

rgn_mc = ROOT.RooRealVar("rgn_mc","rgn_mc",0.8073,0.0,1.0)
rnl_mc = ROOT.RooRealVar("rnl_mc","rnl_mc",0.3,0.0,1.0)


#RooGaussian De_mean_shift_Gaus("De_mean_shift_Gaus","De_mean_shift_Gaus",De_mean_shift,RooConst(-1.69999e-02),RooConst(1.43010e-03))



AmeSame_com = ROOT.RooAddPdf("AmeSame_com","AmeSame_com",ROOT.RooArgList(model_gamma,model_nan,model_l_h),ROOT.RooArgList(rg_mc,rn_mc,rl_mc))

ll = ROOT.RooLinkedList()

EN = AmeSame_com.chi2FitTo(mc_sample,ll)
#EN = AmeSame_com.fitTo(mc_sample_l_h,ROOT.RooFit.Hesse(True),ROOT.RooFit.Save(True))

#Log_LH_mc[0] = EN.minNll()
#Mean_MC[0] = mean.getVal()
#Mean_MC_err[0] = mean.getError()

n_gamma[0] = rg_mc.getVal()
n_gamma_err[0] = rg_mc.getError() if MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)<0.9 else 0
n_gamma_pull[0] = abs((rg_mc.getVal()-MC.GetEntries(Selection+" && isSignal==1")))/rg_mc.getError() if MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)<0.9 else 0
Purity[0]=MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)
t_frame_mc = mc_sample_l_h.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('mc'))

AmeSame_com.plotOn(t_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark'))
AmeSame_com.plotOn(t_frame_mc,ROOT.RooFit.Components("Com_model_gamma"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gamma'))
AmeSame_com.plotOn(t_frame_mc,ROOT.RooFit.Components("Com_model_nan"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('nan'))
AmeSame_com.plotOn(t_frame_mc,ROOT.RooFit.Components("Com_model_l_h"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlack),ROOT.RooFit.Name('l_h'))
Curve_MC = t_frame_mc.getCurve('shark')
'''
MC_max_y = 0.
for i in range(-200,200) : 
	if Curve_MC.Eval(i*0.1)>MC_max_y : MC_max_y = Curve_MC.Eval(i*0.1) 
MC_left_x = 0
for i in range(-1000,0) : 
	if Curve_MC.Eval(i*0.1) > MC_max_y/2. : 
		MC_left_x = i*0.1 
		break
MC_right_x = 0
for i in range(0,1000) : 
	if Curve_MC.Eval(i*0.1) < MC_max_y/2.: 
		MC_right_x = i*0.1 
		break

FWHM_MC[0] = MC_right_x-MC_left_x
'''
Pull_mc = t_frame_mc.pullHist()
#Log_LH_mc[0] = t_frame_mc.chiSquare(4)
pad = ROOT.TPad('pad','pad',0.,0.316,1.0,1.0)
pad.SetLogy()
pad.SetBottomMargin(0)
pad.Draw()
pad.cd()

t_frame_mc.Draw()

legend = pic.Legend(0.65,0.93,0.95,0.63)
legend.add_entry(t_frame_mc.findObject("mc"), "MC", "p")
legend.add_entry(t_frame_mc.findObject("shark"), "Total fit", "l")
legend.add_entry(t_frame_mc.findObject("gamma"), "$\mathrm{\gamma}$", "l")
legend.add_entry(t_frame_mc.findObject("nan"), "isSignal = Nan", "l")
legend.add_entry(t_frame_mc.findObject("l_h"), "Other background", "l")
legend.draw()

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
#h_data.Delete()
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

#X_title = ROOT.TLatex().SetTextFont(42).SetTextColor(1).SetTextSize(0.05).DrawLatex(0.7, 0.02,"clusterTiming [ns]")
#X_title.SetNDC()
Y_title = ROOT.TLatex()
Y_title.SetTextFont(42)
Y_title.SetNDC()
Y_title.SetTextColor(1)
Y_title.SetTextSize(0.05)
Y_title.SetTextAngle(90)
Y_title.DrawLatex(0.07, 0.15,"Pull")

c1.SaveAs(f"./Fit_result/plot/Loose/MC/Timing_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#c1.SaveAs(f"{Dataset}_CellID{ID}_{E_min}_{E_max}.png")
#c1.SaveAs("test.png")
#input('Press ENTER to exit')

c2 = ROOT.TCanvas('c2', 'c2', 600,490)
mva_frame_mc = mc_sample_l_h.plotOn(clusterZernikeMVA.frame(100),ROOT.RooFit.Name('mc'))

AmeSame_com.plotOn(mva_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark'))
AmeSame_com.plotOn(mva_frame_mc,ROOT.RooFit.Components("Com_model_gamma"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gamma'))
AmeSame_com.plotOn(mva_frame_mc,ROOT.RooFit.Components("Com_model_nan"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('nan'))
AmeSame_com.plotOn(mva_frame_mc,ROOT.RooFit.Components("Com_model_l_h"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlack),ROOT.RooFit.Name('l_h'))
mva_Pull_mc = mva_frame_mc.pullHist()
pad.SetLogy(0)
pad.Draw()
pad.cd()

mva_frame_mc.Draw()
legend.clear()
legend.add_entry(mva_frame_mc.findObject("mc"), "MC", "p")
legend.add_entry(mva_frame_mc.findObject("shark"), "Total fit", "l")
legend.add_entry(mva_frame_mc.findObject("gamma"), "$\mathrm{\gamma}$", "l")
legend.add_entry(mva_frame_mc.findObject("nan"), "isSignal = Nan", "l")
legend.add_entry(mva_frame_mc.findObject("l_h"), "Background", "l")
legend.draw()

ROOT.BELLE2Label(0.2,0.89,"",(ROOT.kBlack))
Lumi.DrawLatex(0.3, 0.89,"(simulation)" )
Lumi.DrawLatex(0.2, 0.8, pic.Venezia[args.sample][1])
Lumi.DrawLatex(0.2, 0.7, f"MC15_rd ({pic.Venezia[args.sample][5]} data)")
Lumi.DrawLatex(0.2, 0.65, ID_text)
c2.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)
pad_pull.Draw()
pad_pull.cd()
mva_pull_frame = clusterZernikeMVA.frame(100)
mva_pull_frame.addPlotable(mva_Pull_mc, "P")
mva_pull_frame.GetYaxis().SetLabelFont(63)
mva_pull_frame.GetYaxis().SetLabelSize(12)
mva_pull_frame.GetXaxis().SetLabelFont(63)
mva_pull_frame.GetXaxis().SetLabelSize(12)
mva_pull_frame.Draw()
c2.cd()
X_title.DrawLatex(0.7, 0.02,"clusterZernikeMVA")
Y_title.DrawLatex(0.07, 0.15,"Pull")
#c2.SaveAs("ttest.png")
c2.SaveAs(f"./Fit_result/plot/Loose/MC/MVA_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")

'''
c3 = ROOT.TCanvas('c3', 'c3', 600,490)
TD_frame_mc = mc_sample_l_h.plotOn(minC2TDist.frame(100),ROOT.RooFit.Name('mc'))

AmeSame_com.plotOn(TD_frame_mc,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('shark'))
AmeSame_com.plotOn(TD_frame_mc,ROOT.RooFit.Components("Com_model_gamma"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gamma'))
AmeSame_com.plotOn(TD_frame_mc,ROOT.RooFit.Components("Com_model_nan"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('nan'))
AmeSame_com.plotOn(TD_frame_mc,ROOT.RooFit.Components("Com_model_l_h"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlack),ROOT.RooFit.Name('l_h'))
TD_Pull_mc = TD_frame_mc.pullHist()
pad.SetLogy(0)
pad.Draw()
pad.cd()

TD_frame_mc.Draw()
'''
'''
legend.Clear()
legend.AddEntry(TD_frame_mc.findObject("mc_td"), "MC", "p")
legend.AddEntry(TD_frame_mc.findObject("td_shark"), "Total fit", "l")
legend.AddEntry(TD_frame_mc.findObject("td_gamma"), "$\mathrm{\gamma}$", "l")
legend.AddEntry(TD_frame_mc.findObject("td_nan"), "isSignal = Nan", "l")
legend.AddEntry(TD_frame_mc.findObject("td_l_h"), "Background", "l")
legend.Draw()
'''
'''
legend.clear()
legend.add_entry(mva_frame_mc.findObject("mc"), "MC", "p")
legend.add_entry(mva_frame_mc.findObject("shark"), "Total fit", "l")
legend.add_entry(mva_frame_mc.findObject("gamma"), "$\mathrm{\gamma}$", "l")
legend.add_entry(mva_frame_mc.findObject("nan"), "isSignal = Nan", "l")
legend.add_entry(mva_frame_mc.findObject("l_h"), "Background", "l")
legend.draw()

Lumi.DrawLatex(0.3, 0.89,"(simulation)" )
Lumi.DrawLatex(0.3, 0.89,"(simulation)" )
Lumi.DrawLatex(0.2, 0.8, pic.Venezia[args.sample][1])
Lumi.DrawLatex(0.2, 0.7, f"MC15_rd ({pic.Venezia[args.sample][5]} data)")
Lumi.DrawLatex(0.2, 0.65, ID_text)
c3.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)
pad_pull.Draw()
pad_pull.cd()
TD_pull_frame = minC2TDist.frame(100)
TD_pull_frame.addPlotable(TD_Pull_mc, "P")
TD_pull_frame.GetYaxis().SetLabelFont(63)
TD_pull_frame.GetYaxis().SetLabelSize(12)
TD_pull_frame.GetXaxis().SetLabelFont(63)
TD_pull_frame.GetXaxis().SetLabelSize(12)
TD_pull_frame.Draw()
c3.cd()
X_title.DrawLatex(0.7, 0.02,"minC2TDist")
Y_title.DrawLatex(0.07, 0.15,"Pull")
c3.SaveAs("tttest.png")
'''

mean_shift = ROOT.RooRealVar("mean_shift", "mean_shift",0,-100,100)
mean_data = ROOT.RooFormulaVar("mean_data","@0+@1",ROOT.RooArgSet(mean_gamma,mean_shift))
Gawr_data = ROOT.RooBreitWigner("Gawr_data", "Gawr_data", clusterTiming, mean_data, sigma_gamma)
AmeSame_data = ROOT.RooFFTConvPdf("AmeSame_data", "AmeSame_data", clusterTiming, Gawr_data, Amelia_gamma)

MAEN = ROOT.RooRealVar("MAEN", "MAEN", 0)
sIgma = ROOT.RooRealVar("sIgma", "sIgma", 1., -10, 1000)
sIgmaa = ROOT.RooRealVar("sIgmaa", "sIgmaa", 10, 0., 1000)
f_test = ROOT.RooRealVar("f_test", "f_test",1.0)
#Ina = ROOT.RooBifurGauss("Ina","Ina",clusterTiming,MAEN,sIgma,sIgmaa)
Ina = ROOT.RooGaussian("Ina","Ina",clusterTiming,MAEN,sIgma)

InaAmeSame_gamma = ROOT.RooFFTConvPdf("InaAmeSame_gamma", "InaAmeSame_gamma", clusterTiming,model_gamma,Ina)
InaAmeSame_nan = ROOT.RooFFTConvPdf("InaAmeSame_nan", "InaAmeSame_nan", clusterTiming,AmeSame_nan,Ina)
model_nan_data = ROOT.RooAddPdf("model_nan_data","model_nan_data",ROOT.RooArgList(AmeSame_data,AmeSame_data),f1_nan)

Com_model_gamma_data = ROOT.RooProdPdf(f"Com_model_gamma_data","Com_model_gamma_data",ROOT.RooArgList(InaAmeSame_gamma,B_guass_mva_gamma))
Com_model_nan_data = ROOT.RooProdPdf(f"Com_model_nan_data","Com_model_nan_data",ROOT.RooArgList(model_nan_data,B_guass_mva_nan)) 


rg_data = ROOT.RooRealVar("rg_data","rg_data",30000,-1000000,1000000) if MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection)<0.9 else ROOT.RooRealVar("rg_data","rg_data",Data.GetEntries(Selection))
AmeSame_com_data = ROOT.RooAddPdf("AmeSame_com_data","AmeSame_com_data",ROOT.RooArgList(Com_model_gamma_data,Com_model_nan_data,model_l_h),ROOT.RooArgList(rg_data,rn_mc,rl_mc))


HoloEN = AmeSame_com_data.chi2FitTo(data_sample,ll)
#HoloEN = AmeSame_com_data.fitTo(data_sample,ROOT.RooFit.Minos(True),ROOT.RooFit.Save(True))
#Log_LH_data[0] = HoloEN.minNll()
Mean[0] = mean_shift.getVal()
Mean_err[0] = mean_shift.getError()

if sIgma.getError() > 1. : width[0] = width_err[0] = 0.
else : width[0], width_err[0] = sIgma.getVal(), sIgma.getError()

t_frame_data = data_sample.plotOn(clusterTiming.frame(100),ROOT.RooFit.Name('data'))
AmeSame_com_data.plotOn(t_frame_data,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('AmeSame_com_data'))
AmeSame_com_data.plotOn(t_frame_data,ROOT.RooFit.Components("Com_model_gamma_data"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gamma'))
AmeSame_com_data.plotOn(t_frame_data,ROOT.RooFit.Components("Com_model_nan_data"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('nan'))
AmeSame_com_data.plotOn(t_frame_data,ROOT.RooFit.Components("Com_model_l_h"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlack),ROOT.RooFit.Name('l_h'))
Curve_Data = t_frame_data.getCurve('AmeSame_com_data')
Data_max_y = 0.
for i in range(-200,200) : 
	if Curve_Data.Eval(i*0.1)>Data_max_y : Data_max_y = Curve_Data.Eval(i*0.1) 
Data_left_x = 0
for i in range(-1000,0) : 
	if Curve_Data.Eval(i*0.1) > Data_max_y/2. : 
		Data_left_x = i*0.1 
		break
Data_right_x = 0
for i in range(0,1000) : 
	if Curve_Data.Eval(i*0.1) < Data_max_y/2.: 
		Data_right_x = i*0.1 
		break

FWHM_Data[0] = Data_right_x-Data_left_x
Pull_data = t_frame_data.pullHist()
Log_LH_data[0] = t_frame_data.chiSquare(2)
pad.Draw()
pad.cd()

t_frame_data.Draw()
legend.clear()
legend.add_entry(t_frame_data.findObject("data"), "Data", "p")
legend.add_entry(t_frame_data.findObject("AmeSame_com_data"), "Total fit", "l")
legend.add_entry(t_frame_data.findObject("gamma"), "$\mathrm{\gamma}$", "l")
legend.add_entry(t_frame_data.findObject("nan"), "isSignal = Nan", "l")
legend.add_entry(t_frame_data.findObject("l_h"), "Other background", "l")
legend.draw()

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

c1.SaveAs(f"./Fit_result/plot/Loose/Data/{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")

c2 = ROOT.TCanvas('c2', 'c2', 600,490)
mva_frame_data = data_sample.plotOn(clusterZernikeMVA.frame(100),ROOT.RooFit.Name('data'))

AmeSame_com_data.plotOn(mva_frame_data,ROOT.RooFit.LineStyle(1),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('AmeSame_com_data'))
AmeSame_com_data.plotOn(mva_frame_data,ROOT.RooFit.Components("Com_model_gamma_data"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.Name('gamma'))
AmeSame_com_data.plotOn(mva_frame_data,ROOT.RooFit.Components("Com_model_nan_data"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.Name('nan'))
AmeSame_com_data.plotOn(mva_frame_data,ROOT.RooFit.Components("Com_model_l_h"),ROOT.RooFit.LineStyle(7),ROOT.RooFit.LineColor(ROOT.kBlack),ROOT.RooFit.Name('l_h'))
mva_Pull_data = mva_frame_data.pullHist()
pad.SetLogy(0)
pad.Draw()
pad.cd()

mva_frame_data.Draw()
legend.clear()
legend.add_entry(mva_frame_data.findObject("data"), "Data", "p")
legend.add_entry(mva_frame_data.findObject("AmeSame_com_data"), "Total fit", "l")
legend.add_entry(mva_frame_data.findObject("gamma"), "$\mathrm{\gamma}$", "l")
legend.add_entry(mva_frame_data.findObject("nan"), "isSignal = Nan", "l")
legend.add_entry(mva_frame_data.findObject("l_h"), "Background", "l")
legend.draw()

ROOT.BELLE2Label(0.2,0.89,"",(ROOT.kBlack))
Lumi.DrawLatex(0.3, 0.89,"(simulation)" )
Lumi.DrawLatex(0.2, 0.8, pic.Venezia[args.sample][1])
Lumi.DrawLatex(0.2, 0.7, f"({pic.Venezia[args.sample][5]} data)")
Lumi.DrawLatex(0.2, 0.65, ID_text)
c2.cd()
Cluster_E.DrawLatex(0.1, 0.025, text)
pad_pull.Draw()
pad_pull.cd()
mva_pull_frame = clusterZernikeMVA.frame(100)
mva_pull_frame.addPlotable(mva_Pull_mc, "P")
mva_pull_frame.GetYaxis().SetLabelFont(63)
mva_pull_frame.GetYaxis().SetLabelSize(12)
mva_pull_frame.GetXaxis().SetLabelFont(63)
mva_pull_frame.GetXaxis().SetLabelSize(12)
mva_pull_frame.Draw()
c2.cd()
X_title.DrawLatex(0.7, 0.02,"clusterZernikeMVA")
Y_title.DrawLatex(0.07, 0.15,"Pull")
#c2.SaveAs("ttest.png")
c2.SaveAs(f"./Fit_result/plot/Loose/Data/MVA_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")

fit_tree.Fill()
fit_tree.Write()
myfile.Close()
