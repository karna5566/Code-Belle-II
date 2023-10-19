#################################################
# Draw Data & MC histogram                      #
#################################################
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT,sys,os,argparse
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
import naked_party as nake
ROOT.gROOT.SetBatch(1)
args = nake.getInputOptions_service()

ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 100
Extra_selection = " && clusterZernikeMVA>{pic.Merv[repr(args.E)][0]} && minC2TDist>{pic.Merv[repr(args.E)][1]}"

Selection = f"hlt_hadron==1 && tight==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'
print(Selection)
Max_value = pic.Jerusalem[args.Var][1]
Min_value = pic.Jerusalem[args.Var][0]

c1 = ROOT.TCanvas('c1', 'c1', 600, 400)
c1.SetLogy(pic.Jerusalem[args.Var][6])
pad = ROOT.TPad('pad','pad',0.,0.,1.0,1.)

MC = ROOT.TChain('merged')
Data = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst*_{args.E[0]}_{args.E[1]}.root'

file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)

#Data.Add(pwd+'Data_prompt_all_g/*.root')
Data.Add(pwd+'Data_prompt_all_g/'+ppwd)

h_mc = ROOT.TH1F('h_mc','h_mc',Bin_num,Min_value,Max_value)

h_data = ROOT.TH1F('h_data','h_data',Bin_num,Min_value,Max_value)
MC.Draw(f"{args.Var}>>h_mc",Selection)
Data.Draw(f"{args.Var}>>h_data",Selection)

h_mc.Scale(0.25)
h_mc.GetXaxis().SetTitle(pic.Jerusalem[args.Var][3])
h_mc.GetYaxis().SetTitle("Candidates per event")

if h_mc.GetMaximum()>h_data.GetMaximum() :
	h_mc.SetMaximum(h_mc.GetMaximum()+pic.Jerusalem[args.Var][6]*1000)
else :
	h_mc.SetMaximum(h_data.GetMaximum()+pic.Jerusalem[args.Var][6]*1000)
h_mc.Draw("Hist")
h_data.Draw("E1 SAME")
Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
#BELLE2Label(0.2,0.89,"(simulation)",(kBlack))
ROOT.BELLE2Label(pic.Jerusalem[args.Var][4],0.89,"(preliminary)",(ROOT.kBlack))
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.8, pic.Venezia[args.sample][0])
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.7, f"{pic.Venezia[args.sample][5]} MC15_rd")
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.65, f"{ID_text}")
Purity = round(MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection), 2)
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.6, f"Purity : {Purity}")
Lumi.SetTextSize(0.055)
if args.Var != 'clusterHighestE' : Lumi.DrawLatex(0.1, 0.03, text)


Lehend = ROOT.TLegend(pic.Jerusalem[args.Var][5],0.7,pic.Jerusalem[args.Var][5]+0.2,0.9)
Lehend.AddEntry(h_mc,"rd MC","l")
Lehend.AddEntry(h_data,"Data","p")
Lehend.SetFillStyle(0)
Lehend.SetBorderSize(0)
Lehend.Draw()
c1.SaveAs(f"./Plots/{args.sample}/{pic.Jerusalem[args.Var][3]}/{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#input('Press ENTER to exit')
