#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
import sys,os,argparse
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
ROOT.gROOT.SetBatch(1)
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data',default='Prompt_data')
parser.add_argument('-id','--ID', nargs='+',help='Cell ID', type=int)
parser.add_argument('-e','--E',nargs='+',help='Min E and Max E',type=int)
parser.add_argument('-v','--Var',nargs='?',help='clusterTiming,clusterHighestE,clusterZernikeMVA,clusterTotalMCMatchWeight/clusterE,clusterLAT,minC2TDist',default='clusterTiming')
args = parser.parse_args()
ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"

Bin_num = 25

#Selection = f"hlt_hadron==1 && eff20==1 && abs(clusterTiming)<200 && clusterZernikeMVA>{pic.Merv[repr(args.E)][0]} && minC2TDist>{pic.Merv[repr(args.E)][1]} && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"
Selection = f"hlt_hadron==1 && tight==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}"

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'


c1 = ROOT.TCanvas('c1', 'c1', 600, 400)
c1.SetLogy(pic.Jerusalem[args.Var][6])
pad = ROOT.TPad('pad','pad',0.,0.,1.0,1.)
#pad.SetLogy()
MC = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst*_{args.E[0]}_{args.E[1]}.root'
#file_names = ['MC15_prompt_charged_g/']
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
for file_name in file_names:MC.Add(pwd+file_name+ppwd)


min_value = pic.Jerusalem[args.Var][0] if args.Var != 'clusterHighestE' else args.E[0]/1000.
max_value = pic.Jerusalem[args.Var][1] if args.Var != 'clusterHighestE' else args.E[1]/1000.

h_g = ROOT.TH1F('h_g','h_g',Bin_num,min_value,max_value)
h_l = h_g.Clone('h_l')
h_h = h_g.Clone('h_h')
#h_e = h_g.Clone('h_e')
#h_mu = h_g.Clone('h_mu')
#h_KL = h_g.Clone('h_KL')
#h_pi = h_g.Clone('h_pi')
h_nan = h_g.Clone('h_nan')

print(Selection)

h_g.GetXaxis().SetTitle(pic.Jerusalem[args.Var][2])
h_g.GetYaxis().SetTitle("Candidates per event")
#h_g.SetMinimum(0)
h_l.SetLineColor(2)
h_h.SetLineColor(4)
h_nan.SetLineStyle(7)
MC.Draw(f"{args.Var}>>h_g",Selection+' && isSignal==1','Hist')
MC.Draw(f"{args.Var}>>h_l",Selection+' && (abs(mcPDG)==11 || abs(mcPDG)==13)','Hist SAME')
MC.Draw(f"{args.Var}>>h_h",Selection+' && (abs(mcPDG)==130 || abs(mcPDG)==211)','Hist SAME')
MC.Draw(f"{args.Var}>>h_nan",Selection+' && isSignal!=1 && isSignal!=0','Hist SAME')
#h_g.Draw("Hist")
#h_l.Draw("Hist SAME")
#h_h.Draw("Hist SAME")
#h_nan.Draw("Hist SAME")

Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
ROOT.BELLE2Label(pic.Jerusalem[args.Var][4],0.89,"(simulation)",(ROOT.kBlack))
#Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.8, pic.Venezia[Dataset][0])
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.8,f"MC15_rd ({pic.Venezia[args.sample][5]})")
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.72,f"{ID_text}")
Purity = round(h_g.GetEntries()/(h_g.GetEntries()+h_h.GetEntries()+h_l.GetEntries()+h_nan.GetEntries()), 2)
Lumi.DrawLatex(pic.Jerusalem[args.Var][4], 0.65, f"Purity : {Purity}")
Lumi.SetTextSize(0.055)
if args.Var != 'clusterHighestE' : Lumi.DrawLatex(0.1, 0.03, text)

Lehend = ROOT.TLegend(0.6,0.7,1.,0.9)
Lehend.AddEntry(h_g,"$\mathrm{\gamma}$"+f",ratio:{round(h_g.GetEntries()/(h_g.GetEntries()+h_h.GetEntries()+h_l.GetEntries()+h_nan.GetEntries()),2)}","l")
Lehend.AddEntry(h_l,"$\mathrm{Lepton}$"+f",ratio:{round(h_l.GetEntries()/(h_g.GetEntries()+h_h.GetEntries()+h_l.GetEntries()+h_nan.GetEntries()),2)}","l")
Lehend.AddEntry(h_h,"$\mathrm{Hadron}$"+f",ratio:{round(h_h.GetEntries()/(h_g.GetEntries()+h_h.GetEntries()+h_l.GetEntries()+h_nan.GetEntries()),2)}","l")
#Lehend.AddEntry(h_mu,"$\mathrm{\mu^{\pm}}$","l")
#Lehend.AddEntry(h_e,"$\mathrm{e^{\pm}}$","l")
#Lehend.AddEntry(h_KL,"$\mathrm{K^0_L}$","l")
#Lehend.AddEntry(h_pi,"$\mathrm{\pi^{\pm}}$","l")
Lehend.AddEntry(h_nan,"$\mathrm{isSignal = Nan}$"+f",ratio:{round(h_nan.GetEntries()/(h_g.GetEntries()+h_h.GetEntries()+h_l.GetEntries()+h_nan.GetEntries()),2)}","l")
Lehend.SetFillStyle(0)
Lehend.SetBorderSize(0)
Lehend.SetTextSize(0.04)
Lehend.Draw()
c1.SaveAs(f"./Plots/OnlyMC/{pic.Jerusalem[args.Var][3]}_{args.sample}_CellID{ID_location}_{args.E[0]}_{args.E[1]}.png")
#print("Gamma: %2f ,nan: %2f ,lepton: %2f ,hadron: %2f" %(MC.GetEntries(Selection+" && isSignal==1")/MC.GetEntries(Selection),MC.GetEntries(Selection+" && isSignal!=1 && isSignal!=0")/MC.GetEntries(Selection),MC.GetEntries(Selection+" && (abs(mcPDG)==11 || abs(mcPDG)==13)")/MC.GetEntries(Selection),MC.GetEntries(Selection+" && (abs(mcPDG)==130 || abs(mcPDG)==211)")/MC.GetEntries(Selection)))

#c1.SaveAs("test.png")
#input('Press ENTER to exit')
print(f"# of gamma = {h_g.GetEntries()}, # of nan = {h_nan.GetEntries()} and # of l_h = {h_h.GetEntries()+h_l.GetEntries()}")
