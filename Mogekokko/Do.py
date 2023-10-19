#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %matplotlib inline
# +
import ROOT,sys,os
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Style.C')
ROOT.gROOT.LoadMacro('/home/belle2/lch/belle2style/root/Belle2Labels.C')
ROOT.SetBelle2Style()
sys.path.append('./')
sys.path.append(os.environ['Mogedule'])
import nude_pics as pic
ROOT.gROOT.SetBatch(1)
import naked_party as nake
args = nake.getInputOptions_service()
Bin_num = 100

ID_location = args.ID[0] if len(args.ID) == 1 else '_'.join([str(args.ID[0]), str(args.ID[-1])])
ID_text = f"CellID : {args.ID[0]}" if len(args.ID) == 1 else f"CellID : {'~'.join([str(args.ID[0]),str(args.ID[-1])])}"
Event_type ={'all':[''],'gamma':[' && isSignal==1'],'lepton':[' && (abs(mcPDG)==11 || abs(mcPDG)==13)'],'hadron':[' && (abs(mcPDG)==130 || abs(mcPDG)==211)'],'l_h':[' && (abs(mcPDG)==11 || abs(mcPDG)==13 || abs(mcPDG)==130 || abs(mcPDG)==211)'],'nan':[' && isSignal!=1 && isSignal!=0']}
Selection = f"hlt_hadron==1 && eff20==1 && abs(clusterTiming)<200 && __experiment__{pic.Venezia[args.sample][2]} && __run__>={pic.Venezia[args.sample][3]} && __run__<={pic.Venezia[args.sample][4]} && clusterCellID>={args.ID[0]} && clusterCellID<={args.ID[len(args.ID)-1]}{Event_type[args.Type][0]}"
print(Selection)

Selection += f" && clusterHighestE > {args.E[0]/1000.}" if args.E[0] == args.E[1] else f" && clusterHighestE > {args.E[0]/1000.} && clusterHighestE < {args.E[1]/1000.}"
text = f'ClusterHighestE > {args.E[0]/1000.} [GeV]' if args.E[0] == args.E[1] else f'ClusterHighestE in [{args.E[0]},{args.E[1]}] [MeV]'

c1 = ROOT.TCanvas('c1', 'c1', 600, 400)
c1.SetLogz()
MC = ROOT.TChain('merged')
pwd = '/mnt/qnap_01/user/lch/M2023_prompt_g_extra/'
ppwd = f'skim/Qdst00_{args.E[0]}_{args.E[1]}.root'
file_names = ['MC15_prompt_charged_g/', 'MC15_prompt_mixed_g/', 'MC15_prompt_cc_g/', 'MC15_prompt_dd_g/', 'MC15_prompt_ss_g/', 'MC15_prompt_uu_g/', 'MC15_prompt_tt_g/']
#file_names = ['MC15_prompt_charged_g/']
for file_name in file_names:MC.Add(pwd + file_name + ppwd)
#Data = ROOT.TChain('merged')

h_mc = ROOT.TH2F('h_mc','h_mc',Bin_num,pic.Constantinople[args.Var2][0],pic.Constantinople[args.Var2][1],Bin_num,pic.Constantinople[args.Var][0],pic.Constantinople[args.Var][1])

#h_data = ROOT.TH2F('h_data','h_data',Bin_num,pic.Constantinople[args.Var2][0],pic.Constantinople[args.Var2][1],Bin_num,pic.Constantinople[args.Var][0],pic.Constantinople[args.Var][1])

MC.Draw(f"{args.Var}:{args.Var2}>>h_mc",Selection)
#Data.Draw(f"{args.Var}:{args.Var2}>>h_data",Selection)

#h_mc.Scale(0.25)
h_mc.GetXaxis().SetTitle(pic.Constantinople[args.Var2][2])
h_mc.GetYaxis().SetTitle(pic.Constantinople[args.Var][2])
#h_data.GetXaxis().SetTitle(pic.Constantinople[args.Var2][2])
#h_data.GetYaxis().SetTitle(pic.Constantinople[args.Var][2])

pad = ROOT.TPad('pad','pad',0.,0.,1.,1.)
pad.SetLogz()
pad.Draw()
pad.cd()
h_mc.Draw("colz")
Cor_mc = ROOT.TLatex()
Cor_mc.SetTextFont(42)
Cor_mc.SetNDC()
Cor_mc.SetTextColor(1)
Cor_mc.SetTextSize(0.06)
Cor_mc.DrawLatex(0.1, 0.03,f"Correlation = {round(h_mc.GetCorrelationFactor(2,1), 3)}")
Cor_mc.DrawLatex(0.2, 0.85,ID_text)
Cor_mc.DrawLatex(0.2, 0.78,f"MC15_rd ({pic.Venezia[args.sample][5]} data)")
c1.cd()
Cluster_E = ROOT.TLatex()
Cluster_E.SetTextFont(42)
Cluster_E.SetTextSize(0.045)
Cluster_E.SetTextColor(1)
Cluster_E.SetNDC()
#Cluster_E.DrawLatex(0.1, 0.025, text)
'''
c1.cd()
padd = ROOT.TPad('padd','padd',0.5,0.,1.0,1.)
pad.SetLogz()
padd.Draw()
padd.cd()
h_data.Draw("colz")
Cor_data = ROOT.TLatex()
Cor_data.SetTextFont(42)
Cor_data.SetNDC()
Cor_data.SetTextColor(1)
Cor_data.SetTextSize(0.06)
Cor_data.DrawLatex(0.1, 0.03,f"Correlation = {round(h_data.GetCorrelationFactor(2,1), 3)}")
'''

'''
Lumi = ROOT.TLatex()
Lumi.SetTextFont(42)
Lumi.SetNDC()
Lumi.SetTextColor(1)
Lumi.SetTextSize(0.045)
#BELLE2Label(0.2,0.89,"(simulation)",(kBlack))
ROOT.BELLE2Label(pic.Jerusalem[Var][4],0.89,"(preliminary)",(ROOT.kBlack))
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.8, pic.Venezia[Dataset][0])
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.7, f"{Dataset[:-2]} {Dataset[-2:]} data")
Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.65, f"CellID : {ID}")
if Var != 'clusterHighestE' : Lumi.DrawLatex(pic.Jerusalem[Var][4], 0.6, text)

Lehend = ROOT.TLegend(pic.Jerusalem[Var][5],0.7,pic.Jerusalem[Var][5]+0.2,0.9)
Lehend.AddEntry(h_mc,"rd MC","l")
Lehend.AddEntry(h_data,"Data","p")
Lehend.SetFillStyle(0)
Lehend.SetBorderSize(0)
Lehend.Draw()
'''
c1.SaveAs(f"./Plots/{args.sample}/2D/{args.Type}_{args.sample}_CellID{ID_location}_{pic.Constantinople[args.Var][3]}_{pic.Constantinople[args.Var2][3]}_{args.E[0]}_{args.E[1]}.png")
#c1.SaveAs("./test.png")
#input('Press ENTER to exit')
