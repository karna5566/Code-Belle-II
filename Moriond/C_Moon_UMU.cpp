#ifndef __CINT__
#include "RooGlobalFunc.h"
#else
class Roo2DKeysPdf;
#endif
#include "RooGaussian.h"
#include "RooArgusBG.h"
#include "RooBifurGauss.h"
#include "RooCBShape.h"
#include "RooAddPdf.h"
#include "RooDataSet.h"
#include "RooArgSet.h"
#include "RooRealVar.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TMath.h"
#include "TF1.h"
#include "Math/DistFunc.h"
#ifndef __CINT__
#include "RooCFunction1Binding.h" 
#include "RooCFunction3Binding.h"
#endif
#include "RooTFnBinding.h" 
using namespace RooFit ;

int BiN=20;
//Some selection
double EEEEEFG = -0.3;
double EEEEElephant = 0.3;
double MMMMMM = 5.2;
double Bird = 0.5;
double DE_shift = -0.01699;//-0.0176433
void C_Moon_UMU()
{
RooRealVar mbc("mbc", "mbc ",5.2, 5.29,"GeV/c^{2}");
RooRealVar deltae("deltae", "deltae ",-0.3,0.3,"GeV");

//Set Range
deltae.setRange("signal_box_mbc",-0.14,0.06);//,-0.14,0.06

mbc.setRange("signal_box_de",5.27,5.29);//5.27,5.29

TChain *Ichika_BB = new TChain("tree");

//Ichika_BB->Add("/mnt/d/kekcc/rootfile/MC13/BB/*.root");
Ichika_BB->Add("/mnt/d/kekcc/Enson/C_Moon/Ichika/*charge*.root");
Ichika_BB->Add("/mnt/d/kekcc/Enson/C_Moon/Ichika/*mix*.root");

double DELTA_E_Ichika_BB,Mbc_Ichika_BB;
Ichika_BB->SetBranchAddress("Ichika_deltae",&DELTA_E_Ichika_BB);
Ichika_BB->SetBranchAddress("Ichika_mbc",&Mbc_Ichika_BB);

RooDataSet Ichika_BBB("Ichika_BBB", "Ichika_BBB",RooArgSet(mbc,deltae));

int no_of_events_Ichika_BB = (int) Ichika_BB->GetEntries();
for(int idx_Ichika_BB=0;idx_Ichika_BB<no_of_events_Ichika_BB;idx_Ichika_BB++)
{
double mbc_Ichika_BB = Mbc_Ichika_BB;
double de_Ichika_BB = DELTA_E_Ichika_BB+DE_shift;
Ichika_BB->GetEntry(idx_Ichika_BB);
mbc = mbc_Ichika_BB;
deltae = de_Ichika_BB;
if(de_Ichika_BB>-0.3)
Ichika_BBB.add(RooArgSet(mbc,deltae));
}

TChain *Nino_BB = new TChain("tree");

//Nino_BB->Add("/mnt/d/kekcc/Nakano_Nino/MC13/BB/*.root");
Nino_BB->Add("/mnt/d/kekcc/Enson/C_Moon/Nino/*charge*.root");
Nino_BB->Add("/mnt/d/kekcc/Enson/C_Moon/Nino/*mix*.root");

double DELTA_E_Nino_BB,Mbc_Nino_BB;
Nino_BB->SetBranchAddress("Nino_deltae",&DELTA_E_Nino_BB);
Nino_BB->SetBranchAddress("Nino_mbc",&Mbc_Nino_BB);

RooDataSet Nino_BBB("Nino_BBB", "Nino_BBB",RooArgSet(mbc,deltae));

int no_of_events_Nino_BB = (int) Nino_BB->GetEntries();
for(int idx_Nino_BB=0;idx_Nino_BB<no_of_events_Nino_BB;idx_Nino_BB++)
{
double mbc_Nino_BB = Mbc_Nino_BB;
double de_Nino_BB = DELTA_E_Nino_BB+DE_shift;
Nino_BB->GetEntry(idx_Nino_BB);
mbc = mbc_Nino_BB;
deltae = de_Nino_BB;
if (de_Nino_BB>-0.3)
Nino_BBB.add(RooArgSet(mbc,deltae));
}
//----------------classical period----------------//
RooRealVar mbc_mean_shift("mbc_mean_shift", "mbc_mean_shift",0.0,-0.03,0.03);//
RooRealVar mbc_ratio_sigma("mbc_ratio_sigma", "mbc_ratio_sigma",1.0,0.5,1.5);//,0.5,1.5
RooGaussian mbc_mean_shift_Gaus("mbc_mean_shift_Gaus","mbc_mean_shift_Gaus",mbc_mean_shift,RooConst(-1.16292e-04),RooConst(9.78058e-05)); 
RooGaussian mbc_ratio_sigma_Gaus("mbc_ratio_sigma_Gaus","mbc_ratio_sigma_Gaus",mbc_ratio_sigma,RooConst(1.02152),RooConst(3.32858e-02)); 

RooRealVar De_mean_shift("De_mean_shift", "De_mean_shift",0.0,-0.3,0.3);//
RooRealVar De_ratio_sigma("De_ratio_sigma", "De_ratio_sigma",1.0,0.1,1.9);//,0.5,1.5
RooGaussian De_mean_shift_Gaus("De_mean_shift_Gaus","De_mean_shift_Gaus",De_mean_shift,RooConst(-1.69999e-02),RooConst(1.43010e-03)); 
RooGaussian De_ratio_sigma_Gaus("De_ratio_sigma_Gaus","De_ratio_sigma_Gaus",De_ratio_sigma,RooConst(1.08431),RooConst(4.75068e-02));
RooArgSet Classic(mbc_mean_shift_Gaus,mbc_ratio_sigma_Gaus,De_mean_shift_Gaus,De_ratio_sigma_Gaus);
//Ichika PDF
//----------------signal pdf----------------//
//Mbc
RooRealVar F_Ichika_mean("F_Ichika_mean", "F_Ichika_mean",5.27921);
RooFormulaVar F_Ichika_mean_Data("F_Ichika_mean_Data","@0+@1",RooArgSet(F_Ichika_mean,mbc_mean_shift));

RooRealVar F_Ichika_sigma("F_Ichika_sigma", "F_Ichika_sigma",2.63018e-03);
RooProduct F_Ichika_sigma_Data("F_Ichika_sigma_Data", "F_Ichika_sigma_Data",RooArgSet(F_Ichika_sigma,mbc_ratio_sigma));

RooRealVar F_Ichika_ssigma("F_Ichika_ssigma", "F_Ichika_ssigma",1.42355e-02);
RooProduct F_Ichika_ssigma_Data("F_Ichika_ssigma_Data", "F_Ichika_ssigma_Data",RooArgSet(F_Ichika_ssigma,mbc_ratio_sigma));

RooGaussian F_Ichika_G("F_Ichika_G", "F_Ichika_G",mbc,F_Ichika_mean_Data,F_Ichika_sigma_Data);
RooGaussian F_Ichika_GG("F_Ichika_GG", "F_Ichika_GG",mbc,F_Ichika_mean_Data,F_Ichika_ssigma_Data);

RooRealVar F_Ichika_f1("F_Ichika_f1","F_Ichika_f1",9.88105e-01);

RooAddPdf F_Ichika_Sig("F_Ichika_Sig","F_Ichika_Sig",RooArgList(F_Ichika_G,F_Ichika_GG),RooArgList(F_Ichika_f1));

//deltaE
RooRealVar I_Ichika_mean_sig("I_Ichika_mean_sig", "I_Ichika_mean_sig",-8.48716e-03);
RooFormulaVar I_Ichika_mean_sig_Data("I_Ichika_mean_sig_Data","@0+@1",RooArgSet(I_Ichika_mean_sig,De_mean_shift));

RooRealVar I_Ichika_sigmaR_sig("I_Ichika_sigmaR_sig", "I_Ichika_sigmaR_sig",1.18767e-01);
RooProduct I_Ichika_sigmaR_sig_Data("I_Ichika_sigmaR_sig_Data", "I_Ichika_sigmaR_sig_Data",RooArgSet(I_Ichika_sigmaR_sig,De_ratio_sigma));

RooRealVar I_Ichika_sigmaM_sig("I_Ichika_sigmaM_sig", "I_Ichika_sigmaM_sig",3.32619e-02);
RooProduct I_Ichika_sigmaM_sig_Data("I_Ichika_sigmaM_sig_Data", "I_Ichika_sigmaM_sig_Data",RooArgSet(I_Ichika_sigmaM_sig,De_ratio_sigma));

RooRealVar I_Ichika_a_sig("I_Ichika_a_sig", "I_Ichika_aa_sig",6.36282e-01);

RooRealVar I_Ichika_n_sig("I_Ichika_n_sig", "I_Ichika_nn_sig",6.06065);

RooCBShape I_Ichika_CB_sig("I_Ichika_ball_sig", "I_Ichika_signal_sig",deltae,I_Ichika_mean_sig_Data,I_Ichika_sigmaM_sig_Data,I_Ichika_a_sig,I_Ichika_n_sig);

RooGaussian I_Ichika_G2_sig("gaus2_sig", "I_Ichika_gaus_sig", deltae,I_Ichika_mean_sig_Data,I_Ichika_sigmaR_sig_Data);

RooRealVar I_Ichika_f1_sig("I_Ichika_f1_sig","I_Ichika_frac1_sig",9.68612e-01);

RooAddPdf I_Ichika_sig("I_Ichika_m_sig","I_Ichika_mm_sig",RooArgList(I_Ichika_CB_sig,I_Ichika_G2_sig),RooArgList(I_Ichika_f1_sig));

RooProdPdf UMU_Ichika_sig("UMU_Ichika_sig","UMUUMU_Ichika_sig", RooArgList(F_Ichika_Sig,I_Ichika_sig));

//----------------BB pdf----------------//
//Mbc
RooRealVar F_Ichika_mean_BB("F_Ichika_mean_BB", "F_Ichika_mean_BB",5.2784);
RooFormulaVar F_Ichika_mean_BB_Data("F_Ichika_mean_BB_Data","@0+@1",RooArgSet(F_Ichika_mean_BB,mbc_mean_shift));

RooRealVar F_Ichika_sigma_BB("F_Ichika_sigma_BB", "F_Ichika_sigma_BB",7.12735e-03);
RooProduct F_Ichika_sigma_BB_Data("F_Ichika_sigma_BB_Data", "F_Ichika_sigma_BB_Data",RooArgSet(F_Ichika_sigma_BB,mbc_ratio_sigma));

RooRealVar F_Ichika_a_BB("F_Ichika_a_BB", "F_Ichika_aa_BB",5.78820e-01);

RooRealVar F_Ichika_n_BB("F_Ichika_n_BB", "F_Ichika_nn_BB",4.22033);

RooCBShape F_Ichika_CB_BB("F_Ichika_CB_BB", "F_Ichika_CB_BB",mbc,F_Ichika_mean_BB,F_Ichika_sigma_BB,F_Ichika_a_BB,F_Ichika_n_BB);

//deltaE
RooKeysPdf I_Ichika_background_BB("I_Ichika_background_BB","I_Ichika_background_BB",deltae,Ichika_BBB,RooKeysPdf::MirrorBoth);

//I_Ichika_background_BB.fitTo(Ichika_BBB,Minos(true));

//
RooNDKeysPdf UMU_Ichika_BB_2D("UMU_Ichika_BB_2D","UMUUMU_Ichika_BB_2D",RooArgSet(mbc,deltae),Ichika_BBB,"am");
UMU_Ichika_BB_2D.fitTo(Ichika_BBB,Minos(true));
RooProdPdf UMU_Ichika_BB("UMU_Ichika_BB","UMUUMU_Ichika_BB", RooArgList(UMU_Ichika_BB_2D));
//----------------Nino pdf----------------//
//Mbc
RooRealVar F_Ichika_mean_Nino("F_Ichika_mean_Nino","F_Ichika_mean_Nino",5.27931);
RooFormulaVar F_Ichika_mean_Nino_Data("F_Ichika_mean_Nino_Data","@0+@1",RooArgSet(F_Ichika_mean_Nino,mbc_mean_shift));

RooRealVar F_Ichika_sigma_Nino("F_Ichika_sigma_Nino","F_Ichika_sigma_Nino",2.94025e-03);
RooProduct F_Ichika_sigma_Nino_Data("F_Ichika_sigma_Nino_Data", "F_Ichika_sigma_Nino_Data",RooArgSet(F_Ichika_sigma_Nino,mbc_ratio_sigma));

RooRealVar F_Ichika_a_Nino("F_Ichika_a_Nino", "F_Ichika_aa_Nino",1.52077);

RooRealVar F_Ichika_n_Nino("F_Ichika_n_Nino", "F_Ichika_nn_Nino",9.67646);

RooRealVar F_Ichika_ssigma_Nino("F_Ichika_ssigma_Nino","F_Ichika_ssigma_Ninoo",0.00307848);

RooCBShape F_Ichika_G_Nino("F_Ichika_G_Nino","F_Ichika_G_Nino",mbc,F_Ichika_mean_Nino_Data,F_Ichika_sigma_Nino_Data,F_Ichika_a_Nino,F_Ichika_n_Nino);

//deltaE
RooRealVar I_Ichika_mean_Nino("I_Ichika_mean_Nino", "I_Ichika_mean_Nino",3.3936e-02);
RooFormulaVar I_Ichika_mean_Nino_Data("I_Ichika_mean_Nino_Data","@0+@1",RooArgSet(I_Ichika_mean_Nino,De_mean_shift));

RooRealVar I_Ichika_sigmaR_Nino("I_Ichika_sigmaR_Nino", "I_Ichika_sigmaR_Nino",1.06094e-01);
RooProduct I_Ichika_sigmaR_Nino_Data("I_Ichika_sigmaR_Nino_Data", "I_Ichika_sigmaR_Nino_Data",RooArgSet(I_Ichika_sigmaR_Nino,De_ratio_sigma));

RooRealVar I_Ichika_sigmaM_Nino("I_Ichika_sigmaM_Nino", "I_Ichika_sigmaM_Nino",3.47489e-02);
RooProduct I_Ichika_sigmaM_Nino_Data("I_Ichika_sigmaM_Nino_Data", "I_Ichika_sigmaM_Nino_Data",RooArgSet(I_Ichika_sigmaM_Nino,De_ratio_sigma));

RooRealVar I_Ichika_a_Nino("I_Ichika_a_Nino", "I_Ichika_aa_Nino",6.28381e-01);

RooRealVar I_Ichika_n_Nino("I_Ichika_n_Nino", "I_Ichika_nn_Nino",6.68713);

RooCBShape I_Ichika_CB_Nino("I_Ichika_CB_Nino", "I_Ichika_CB_Nino",deltae,I_Ichika_mean_Nino_Data,I_Ichika_sigmaM_Nino_Data,I_Ichika_a_Nino,I_Ichika_n_Nino);

RooGaussian I_Ichika_G2_Nino("I_Ichika_G2_Nino", "I_Ichika_G2_Nino", deltae,I_Ichika_mean_Nino_Data,I_Ichika_sigmaR_Nino_Data);

RooRealVar I_Ichika_f1_Nino("I_Ichika_f1_Nino","I_Ichika_frac1_Nino",9.65157e-01);

RooAddPdf I_Ichika_Nino("I_Ichika_m_Nino","I_Ichika_mm_Nino",RooArgList(I_Ichika_CB_Nino,I_Ichika_G2_Nino),RooArgList(I_Ichika_f1_Nino));

RooProdPdf UMU_Ichika_Nino("UMU_Ichika_Nino","UMUUMU_Ichika_Nino", RooArgList(F_Ichika_G_Nino,I_Ichika_Nino));
//----------------qq pdf----------------//
//Mbc
RooRealVar F_Ichika_argpar_qq("F_Ichika_argpar_qq","F_Ichika_argpar_qq",-2.00694e+01,-30.,100.);//,-50,50
RooArgusBG F_Ichika_background_qq("F_Ichika_background_qq","F_Ichika_background_qq",mbc,RooConst(5.2899),F_Ichika_argpar_qq);
//deltae
//RooRealVar I_Ichika_coef1_qq("I_Ichika_coef1_qq","I_Ichika_coef1_qq",-1.3474);//,-5.,5.

RooRealVar I_Ichika_coef1_qq("I_Ichika_coef1_qq","I_Ichika_coef1_qq",-1.43286,-5.,5.);//

RooRealVar I_Ichika_coef2_qq("I_Ichika_coef2_qq","I_Ichika_coef2_qq",1.16612,-5.,5.);//

RooPolynomial I_Ichika_background_qq("I_Ichika_bg_qq","I_Ichika_bbg_qq",deltae,RooArgList(I_Ichika_coef1_qq,I_Ichika_coef2_qq));

RooProdPdf UMU_Ichika_qq("UMU_Ichika_qq","UMUUMU_Ichika_qq", RooArgList(F_Ichika_background_qq,I_Ichika_background_qq));

//Ichika PDF
//----------------signal pdf----------------//
//Mbc
RooRealVar F_Nino_mean("F_Nino_mean", "F_Nino_mean",5.27921);
RooFormulaVar F_Nino_mean_Data("F_Nino_mean_Data","@0+@1",RooArgSet(F_Nino_mean,mbc_mean_shift));

RooRealVar F_Nino_sigma("F_Nino_sigma", "F_Nino_sigma",2.64172e-03);
RooProduct F_Nino_sigma_Data("F_Nino_sigma_Data", "F_Nino_sigma_Data",RooArgSet(F_Nino_sigma,mbc_ratio_sigma));

RooRealVar F_Nino_ssigma("F_Nino_ssigma", "F_Nino_ssigma",1.37575e-02);
RooProduct F_Nino_ssigma_Data("F_Nino_ssigma_Data", "F_Nino_ssigma_Data",RooArgSet(F_Nino_ssigma,mbc_ratio_sigma));

RooGaussian F_Nino_G("F_Nino_G", "F_Nino_G",mbc,F_Nino_mean_Data,F_Nino_sigma_Data);
RooGaussian F_Nino_GG("F_Nino_GG", "F_Nino_GG",mbc,F_Nino_mean_Data,F_Nino_ssigma_Data);

RooRealVar F_Nino_f1("F_Nino_f1","F_Nino_f1",9.81600e-01);

RooAddPdf F_Nino_Sig("F_Nino_Sig","F_Nino_Sig",RooArgList(F_Nino_G,F_Nino_GG),RooArgList(F_Nino_f1));

//deltaE
RooRealVar I_Nino_mean_sig("I_Nino_mean_sig", "I_Nino_mean_sig",-7.19116e-03);
RooFormulaVar I_Nino_mean_sig_Data("I_Nino_mean_sig_Data","@0+@1",RooArgSet(I_Nino_mean_sig,De_mean_shift));

RooRealVar I_Nino_sigmaR_sig("I_Nino_sigmaR_sig", "I_Nino_sigmaR_sig",1.07611e-01);
RooProduct I_Nino_sigmaR_sig_Data("I_Nino_sigmaR_sig_Data", "I_Nino_sigmaR_sig_Data",RooArgSet(I_Nino_sigmaR_sig,De_ratio_sigma));

RooRealVar I_Nino_sigmaM_sig("I_Nino_sigmaM_sig", "I_Nino_sigmaM_sig",3.39246e-02);
RooProduct I_Nino_sigmaM_sig_Data("I_Nino_sigmaM_sig_Data", "I_Nino_sigmaM_sig_Data",RooArgSet(I_Nino_sigmaM_sig,De_ratio_sigma));

RooRealVar I_Nino_a_sig("I_Nino_a_sig", "I_Nino_aa_sig",6.33323e-01);

RooRealVar I_Nino_n_sig("I_Nino_n_sig", "I_Nino_nn_sig",6.02086);

RooCBShape I_Nino_CB_sig("I_Nino_ball_sig", "I_Nino_signal_sig",deltae,I_Nino_mean_sig_Data,I_Nino_sigmaM_sig_Data,I_Nino_a_sig,I_Nino_n_sig);

RooGaussian I_Nino_G2_sig("I_Nino_G2_sig", "I_Nino_gaus_sig", deltae,I_Nino_mean_sig_Data,I_Nino_sigmaR_sig_Data);

RooRealVar I_Nino_f1_sig("I_Nino_f1_sig","I_Nino_frac1_sig",9.71076e-01);

RooAddPdf I_Nino_sig("I_Nino_m_sig","I_Nino_mm_sig",RooArgList(I_Nino_CB_sig,I_Nino_G2_sig),RooArgList(I_Nino_f1_sig));

RooProdPdf UMU_Nino_sig("UMU_Nino_sig","UMUUMU_Nino_sig", RooArgList(F_Nino_Sig,I_Nino_sig));

//----------------BB pdf----------------//
//Mbc
RooRealVar F_Nino_mean_BB("F_Nino_mean_BB", "F_Nino_mean_BB",5.28181);
RooFormulaVar F_Nino_mean_BB_Data("F_Nino_mean_BB_Data","@0+@1",RooArgSet(F_Nino_mean_BB,mbc_mean_shift));

RooRealVar F_Nino_sigma_BB("F_Nino_sigma_BB", "F_Nino_sigma_BB",4.34252e-03);
RooProduct F_Nino_sigma_BB_Data("F_Nino_sigma_BB_Data", "F_Nino_sigma_BB_Data",RooArgSet(F_Nino_sigma_BB,mbc_ratio_sigma));

RooRealVar F_Nino_a_BB("F_Nino_a_BB", "F_Nino_aa_BB",2.30180e-01);

RooRealVar F_Nino_n_BB("F_Nino_n_BB", "F_Nino_nn_BB",1.00000e+02);

RooCBShape F_Nino_CB_BB("F_Nino_CB_BB", "F_Nino_CB_BB",mbc,F_Nino_mean_BB,F_Nino_sigma_BB,F_Nino_a_BB,F_Nino_n_BB);

//deltaE
RooKeysPdf I_Nino_background_BB("I_Nino_background_BB","I_Nino_background_BB",deltae,Nino_BBB,RooKeysPdf::MirrorBoth);

//I_Nino_background_BB.fitTo(Nino_BBB,Minos(true));

RooNDKeysPdf UMU_Nino_BB_2D("UMU_Nino_BB_2D","UMUUMU_Nino_BB_2D",RooArgSet(mbc,deltae),Nino_BBB,"am");
UMU_Nino_BB_2D.fitTo(Nino_BBB,Minos(true));

RooProdPdf UMU_Nino_BB("UMU_Nino_BB","UMUUMU_Nino_BB", RooArgList(UMU_Nino_BB_2D));
//----------------Ichika pdf----------------//
//Mbc
RooRealVar F_Nino_mean_Ichika("F_Nino_mean_Ichika","F_Nino_mean_Ichika",5.27895);
RooFormulaVar F_Nino_mean_Ichika_Data("F_Nino_mean_Ichika_Data","@0+@1",RooArgSet(F_Nino_mean_Ichika,mbc_mean_shift));

RooRealVar F_Nino_sigma_Ichika("F_Nino_sigma_Ichika","F_Nino_sigma_Ichika",3.14813e-03);
RooProduct F_Nino_sigma_Ichika_Data("F_Nino_sigma_Ichika_Data", "F_Nino_sigma_Ichika_Data",RooArgSet(F_Nino_sigma_Ichika,mbc_ratio_sigma));

RooRealVar F_Nino_a_Ichika("F_Nino_a_Ichika", "F_Nino_a_Ichika",2.52246);

RooRealVar F_Nino_n_Ichika("F_Nino_n_Ichika", "F_Nino_n_Ichika",1.51504);

RooRealVar F_Nino_ssigma_Ichika("F_Nino_ssigma_Ichika","F_Nino_ssigma_Ichika",0.00307848);

RooCBShape F_Nino_G_Ichika("F_Nino_G_Ichika","F_Nino_G_Ichika",mbc,F_Nino_mean_Ichika_Data,F_Nino_sigma_Ichika_Data,F_Nino_a_Ichika,F_Nino_n_Ichika);

//deltaE
RooRealVar I_Nino_mean_Ichika("I_Nino_mean_Ichika", "I_Nino_mean_Ichika",-4.94551e-02);
RooFormulaVar I_Nino_mean_Ichika_Data("I_Nino_mean_Ichika_Data","@0+@1",RooArgSet(I_Nino_mean_Ichika,De_mean_shift));

RooRealVar I_Nino_sigmaR_Ichika("I_Nino_sigmaR_Ichika", "I_Nino_sigmaR_Ichika",1.19020e-01);
RooProduct I_Nino_sigmaR_Ichika_Data("I_Nino_sigmaR_Ichika_Data", "I_Nino_sigmaR_Ichika_Data",RooArgSet(I_Nino_sigmaR_Ichika,De_ratio_sigma));

RooRealVar I_Nino_sigmaM_Ichika("I_Nino_sigmaM_Ichika", "I_Nino_sigmaM_Ichika",3.32358e-02);
RooProduct I_Nino_sigmaM_Ichika_Data("I_Nino_sigmaM_Ichika_Data", "I_Nino_sigmaM_Ichika_Data",RooArgSet(I_Nino_sigmaM_Ichika,De_ratio_sigma));

RooRealVar I_Nino_a_Ichika("I_Nino_a_Ichika", "I_Nino_a_Ichika",5.99922e-01);

RooRealVar I_Nino_n_Ichika("I_Nino_n_Ichika", "I_Nino_n_Ichika",8.85511);

RooCBShape I_Nino_CB_Ichika("I_Nino_CB_Ichika", "I_Nino_CB_Ichika",deltae,I_Nino_mean_Ichika_Data,I_Nino_sigmaM_Ichika_Data,I_Nino_a_Ichika,I_Nino_n_Ichika);

RooGaussian I_Nino_G2_Ichika("I_Nino_G2_Ichika", "I_Nino_G2_Ichika", deltae,I_Nino_mean_Ichika_Data,I_Nino_sigmaR_Ichika_Data);

RooRealVar I_Nino_f1_Ichika("I_Nino_f1_Ichika","I_Nino_f1_Ichika",9.57453e-01);

RooAddPdf I_Nino_Ichika("I_Nino_Ichika","I_Nino_Ichika",RooArgList(I_Nino_CB_Ichika,I_Nino_G2_Ichika),RooArgList(I_Nino_f1_Ichika));

RooProdPdf UMU_Nino_Ichika("UMU_Nino_Ichika","UMUUMU_Nino_Ichika", RooArgList(F_Nino_G_Ichika,I_Nino_Ichika));
//----------------qq pdf----------------//
//Mbc
RooRealVar F_Nino_argpar_qq("F_Nino_argpar_qq","F_Nino_argpar_qq",-1.74792e+01,-30.,100.);//,-50,50
RooArgusBG F_Nino_background_qq("F_Nino_background_qq","F_Nino_background_qq",mbc,RooConst(5.2899),F_Nino_argpar_qq);
//deltae
//RooRealVar I_Nino_coef1_qq("I_Nino_coef1_qq","I_Nino_coef1_qq",-1.29724);//,-5,5

RooRealVar I_Nino_coef1_qq("I_Nino_coef1_qq","I_Nino_coef1_qq",-1.4175,-5,5);//

RooRealVar I_Nino_coef2_qq("I_Nino_coef2_qq","I_Nino_coef2_qq",1.69606,-5,5);//

RooPolynomial I_Nino_background_qq("I_Nino_bg_qq","I_Nino_bbg_qq",deltae,RooArgList(I_Nino_coef1_qq,I_Nino_coef2_qq));

RooProdPdf UMU_Nino_qq("UMU_Nino_qq","UMUUMU_Nino_qq", RooArgList(F_Nino_background_qq,I_Nino_background_qq));

cout << "test pdf " << endl;
//--------------Gawa Chibaba-------------//
TChain *Ichika_Data = new TChain("merged");
TChain *Nino_Data = new TChain("merged");

Ichika_Data->Add("/mnt/d/kekcc/rootfile/Data/Cali/*.root");

double Ichika_DELTA_E_data,Ichika_FunPlus_Phoenix_data,Ichika_Mbc_data,Ichika_Pid_data,Ichika_rank_data;

Ichika_Data->SetBranchAddress("CSMVA_WithCorr_Flavor_Vertex",&Ichika_FunPlus_Phoenix_data);
Ichika_Data->SetBranchAddress("deltaE",&Ichika_DELTA_E_data);
Ichika_Data->SetBranchAddress("Modified_Mbc",&Ichika_Mbc_data);
Ichika_Data->SetBranchAddress("K_PID_bin_kaon",&Ichika_Pid_data);
Ichika_Data->SetBranchAddress("chiProb_rank",&Ichika_rank_data);

RooDataSet Ichika_data("Ichika_data", "Ichika_data",RooArgSet(mbc,deltae));

int Ichika_no_of_events_data = (int) Ichika_Data->GetEntries();
for(int idx_ichika_data=0;idx_ichika_data<Ichika_no_of_events_data;idx_ichika_data++)
{
Ichika_Data->GetEntry(idx_ichika_data);
double ichika_mbc_data = Ichika_Mbc_data;
double ichika_de_data = Ichika_DELTA_E_data;

mbc = ichika_mbc_data;
deltae = ichika_de_data;

if(Ichika_rank_data ==1 && Ichika_FunPlus_Phoenix_data>0.92 && Ichika_Pid_data>Bird)
Ichika_data.add(RooArgSet(mbc,deltae));
}

Nino_Data->Add("/mnt/d/kekcc/Nakano_Nino/Data/Cali/*.root");

double Nino_DELTA_E_data,Nino_FunPlus_Phoenix_data,Nino_Mbc_data,Nino_Pid_data,Nino_rank_data;

Nino_Data->SetBranchAddress("CSMVA_WithCorr_Flavor_Vertex",&Nino_FunPlus_Phoenix_data);
Nino_Data->SetBranchAddress("deltaE",&Nino_DELTA_E_data);
Nino_Data->SetBranchAddress("Modified_Mbc",&Nino_Mbc_data);
Nino_Data->SetBranchAddress("pi_PID_bin_pion",&Nino_Pid_data);
Nino_Data->SetBranchAddress("chiProb_rank",&Nino_rank_data);

RooDataSet Nino_data("Nino_data", "Nino_data",RooArgSet(mbc,deltae));

int Nino_no_of_events_data = (int) Nino_Data->GetEntries();
for(int idx_nino_data=0;idx_nino_data<Nino_no_of_events_data;idx_nino_data++)
{
Nino_Data->GetEntry(idx_nino_data);
double nino_mbc_data = Nino_Mbc_data;
double nino_de_data = Nino_DELTA_E_data;

mbc = nino_mbc_data;
deltae = nino_de_data;

if(Nino_rank_data ==1 && Nino_FunPlus_Phoenix_data>0.95 && Nino_Pid_data>Bird)
Nino_data.add(RooArgSet(mbc,deltae));
}
//
double scale = 1000./34.58;

double True_Assassin = 13932./scale;

double True_Rider = 5940./scale;

double Ichika_Papapa_mix = 715./scale;
double Ichika_Papapa_charge = 447./scale;

double Ichika_Papapa_BB = Ichika_Papapa_mix+Ichika_Papapa_charge;

double Ichika_Papapa_cc = 8102./scale;
double Ichika_Papapa_uu = 14786./scale;
double Ichika_Papapa_dd = 2074./scale;
double Ichika_Papapa_ss = 2482./scale;
double Ichika_Papapa_qq = Ichika_Papapa_cc+Ichika_Papapa_uu+Ichika_Papapa_dd+Ichika_Papapa_ss;

double Nino_Papapa_mix = 843./scale;
double Nino_Papapa_charge = 1205./scale;

double Nino_Papapa_BB = Nino_Papapa_mix+Nino_Papapa_charge;

double Nino_Papapa_cc = 3722./scale;
double Nino_Papapa_uu = 12364./scale;
double Nino_Papapa_dd = 3092./scale;
double Nino_Papapa_ss = 562./scale;
double Nino_Papapa_qq = Nino_Papapa_cc+Nino_Papapa_uu+Nino_Papapa_dd+Nino_Papapa_ss;
//fitting stuff
RooRealVar Ichika_NN("Ichika_NN", "Ichika_NN",True_Assassin,-20000.,20000.);//True_Assassin,-20000.,20000.
RooRealVar Nino_NN("Nino_NN", "Nino_NN",True_Rider,-20000.,20000.);//True_Rider,-20000.,20000.
//---------------------Efff---------------------
RooRealVar Ichika_sig_eff("Ichika_sig_eff", "Ichika_sig_eff",0.259);
RooRealVar Ichika_F_eff("Ichika_F_eff", "Ichika_F_eff",0.030);
RooRealVar Nino_sig_eff("Nino_sig_eff", "Nino_sig_eff",0.222);
RooRealVar Nino_F_eff("Nino_F_eff", "Nino_F_eff",0.038414);
//---------------------PID Correction---------------------
RooRealVar Ichika_ichikaa("Ichika_ichikaa", "Ichika_ichikaa",0.972042,0.,10.);
RooGaussian Ichika_ichikaa_Gaus("Ichika_ichikaa_Gaus","Ichika_ichikaa_Gaus",Ichika_ichikaa,RooConst(0.972042),RooConst(0.0107652)); 

RooRealVar Ichika_ninoo("Ichika_ninoo", "Ichika_ninoo",1.27725,0.,10.);
RooGaussian Ichika_ninoo_Gaus("Ichika_ninoo_Gaus","Ichika_ninoo_Gaus",Ichika_ninoo,RooConst(1.27725),RooConst(0.136436)); 

RooRealVar Nino_ninoo("Nino_ninoo", "Nino_ninoo",0.96917,0.,10.);
RooGaussian Nino_ninoo_Gaus("Nino_ninoo_Gaus","Nino_ninoo_Gaus",Nino_ninoo,RooConst(0.96917),RooConst(0.0100268)); 

RooRealVar Nino_ichikaa("Nino_ichikaa", "Nino_ichikaa",1.26125,0.,10.);
RooGaussian Nino_ichikaa_Gaus("Nino_ichikaa_Gaus","Nino_ichikaa_Gaus",Nino_ichikaa,RooConst(1.26125),RooConst(0.101809)); 

RooArgSet PID (Ichika_ichikaa_Gaus,Ichika_ninoo_Gaus,Nino_ninoo_Gaus,Nino_ichikaa_Gaus);

RooProduct Ichika_eff("Ichika_eff","Ichika_eff",RooArgSet(Ichika_sig_eff,Ichika_ichikaa));//2667

RooProduct Ichika_efff("Ichika_efff","Ichika_efff",RooArgSet(Ichika_F_eff,Ichika_ninoo));//29539

RooProduct Nino_eff("Nino_eff","Nino_eff",RooArgSet(Nino_sig_eff,Nino_ninoo));//217491

RooProduct Nino_efff("Nino_efff","Nino_efff",RooArgSet(Nino_F_eff,Nino_ichikaa));//31102s

RooProduct Ichika_ichika("Ichika_ichika", "Ichika_ichika",RooArgSet(Ichika_NN,Ichika_eff));
RooProduct Ichika_nino("Ichika_nino", "Ichika_nino",RooArgSet(Nino_NN,Ichika_efff));
RooProduct Nino_nino("Nino_nino", "Nino_nino",RooArgSet(Nino_NN,Nino_eff));
RooProduct Nino_ichika("Nino_ichika", "Nino_ichika",RooArgSet(Ichika_NN,Nino_efff));

RooRealVar Ichika_f3("Ichika_f3","Ichika_f3",Ichika_Papapa_BB,-10*Ichika_Papapa_BB,10*Ichika_Papapa_BB);
RooRealVar Ichika_f4("Ichika_f4","Ichika_f4",Ichika_Papapa_qq,-10*Ichika_Papapa_qq,10*Ichika_Papapa_qq);

RooRealVar Nino_f3("Nino_f3","Nino_f3",Nino_Papapa_BB,-10*Nino_Papapa_BB,10*Nino_Papapa_BB);
RooRealVar Nino_f4("Nino_f4","Nino_f4",Nino_Papapa_qq,-10*Nino_Papapa_qq,10*Nino_Papapa_qq);

RooAddPdf Ichika_UMU("Ichika_UMU","Ichika_UMUUMU",RooArgList(UMU_Ichika_sig,UMU_Ichika_Nino,UMU_Ichika_BB,UMU_Ichika_qq),RooArgList(Ichika_ichika,Ichika_nino,Ichika_f3,Ichika_f4));
RooAddPdf Nino_UMU("Nino_UMU","Nino_UMUUMU",RooArgList(UMU_Nino_sig,UMU_Nino_Ichika,UMU_Nino_BB,UMU_Nino_qq),RooArgList(Nino_nino,Nino_ichika,Nino_f3,Nino_f4));

RooCategory Nakano("Nakano","Nakano");
Nakano.defineType("ichika");
Nakano.defineType("nino");

RooSimultaneous Yotsuba_UMU("Yotsuba_UMU","Yotsuba_UMU",Nakano);

Yotsuba_UMU.addPdf(Ichika_UMU,"ichika");
Yotsuba_UMU.addPdf(Nino_UMU,"nino");

RooDataSet Yotsuba("Yotsuba","Yotsuba",RooArgSet(mbc,deltae),Index(Nakano),Import("ichika",Ichika_data),Import("nino",Nino_data));

RooFitResult* Riri = Yotsuba_UMU.fitTo(Yotsuba,Minos(true),Save(true),ExternalConstraints(RooArgSet(Classic,PID)));

TCanvas *Ichika_Toy_Plot_mbc = new TCanvas("Ichika_Toy_Plot_mbc","Ichika_Toy_Plot_mbc",600,400);
RooPlot* frame_Ichika_mbc = mbc.frame(BiN);
frame_Ichika_mbc->SetTitle("Fitting result - signal_mbc");
Yotsuba.plotOn(frame_Ichika_mbc,CutRange("signal_box_mbc"),Cut("Nakano==Nakano::ichika"),Name("ichika_data"),XErrorSize(0));
Yotsuba_UMU.plotOn(frame_Ichika_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"ichika"),ProjWData(Nakano,Yotsuba),Name("ichika_tol"));
Yotsuba_UMU.plotOn(frame_Ichika_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"ichika"),Components("UMU_Ichika_sig"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kRed),Name("ichika_sig"));
Yotsuba_UMU.plotOn(frame_Ichika_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"ichika"),Components("UMU_Ichika_Nino"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kMagenta),Name("ichika_ssig"));
Yotsuba_UMU.plotOn(frame_Ichika_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"ichika"),Components("UMU_Ichika_BB"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlue),Name("ichika_BB"));
Yotsuba_UMU.plotOn(frame_Ichika_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"ichika"),Components("UMU_Ichika_qq"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlack),Name("ichika_qq"));
frame_Ichika_mbc -> GetYaxis() -> SetTitle("Events/(2 MeV/c^{2})");
frame_Ichika_mbc -> GetXaxis() -> SetTitle("#it{M}_{bc} [GeV/c^{2}]");
frame_Ichika_mbc -> GetXaxis() -> CenterTitle(true);
TLegend *ichika_legend_mbc = new TLegend(0.45,0.93,0.75,0.63);
ichika_legend_mbc->SetBorderSize(0);
ichika_legend_mbc->SetFillStyle(0);
ichika_legend_mbc->SetTextSize(0.045);
ichika_legend_mbc->SetTextFont(42);
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_data"), "Data", "p");
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_tol"), "Total fit", "l");
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_sig"), "#it{B}^{+} #rightarrow #it{K}^{+}#it{#pi}^{0} + c.c.", "l");
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_ssig"), "#it{B}^{+} #rightarrow #it{#pi}^{+}#it{#pi}^{0} + c.c.", "l");
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_BB"), "#it{B} decay background", "l");
ichika_legend_mbc->AddEntry(frame_Ichika_mbc->findObject("ichika_qq"), "#it{q}#it{#bar{q}} background", "l");
frame_Ichika_mbc -> Draw(); 
TLatex *ichika_l_MBC = new TLatex();
ichika_l_MBC->SetTextFont(42);
ichika_l_MBC->SetNDC();
ichika_l_MBC->SetTextColor(1);
ichika_l_MBC->SetTextSize(0.045);
//BELLE2Label(0.2,0.89,"(simulation)",(kBlack));
BELLE2Label(0.2,0.89,"(preliminary)",(kBlack));
//nino_l_MBC->DrawLatex(0.2, 0.83, "2020 (preliminary)");
ichika_l_MBC->DrawLatex(0.2, 0.8, "#int #it{L} d#it{t} = 62.8 fb^{-1}");
ichika_legend_mbc->Draw();

gPad->Update();
gPad->RedrawAxis();
TLine *ichika_Toy_Mbc_line = new TLine();
ichika_Toy_Mbc_line->SetLineWidth(3);
ichika_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymin());
ichika_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmin(),gPad->GetUymax());
ichika_Toy_Mbc_line->DrawLine(gPad->GetUxmax(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymax());
ichika_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymax(),gPad->GetUxmax(),gPad->GetUymax());

char Nakano_Ichika_Toy_Plot_mbc_Title[200];
sprintf(Nakano_Ichika_Toy_Plot_mbc_Title,"/mnt/c/Users/USER73441/Desktop/Plots/Yotsuba/Ichika_Moriond_2D_Proto_mbc.png");
Ichika_Toy_Plot_mbc->SaveAs(Nakano_Ichika_Toy_Plot_mbc_Title); 

char Nakano_Ichika_Toy_Plot_mbc_Title_PDF[200];
sprintf(Nakano_Ichika_Toy_Plot_mbc_Title_PDF,"/mnt/c/Users/USER73441/Desktop/Plots/Yotsuba/pdf/Ichika_Moriond_2D_Proto_mbc.pdf");
Ichika_Toy_Plot_mbc->SaveAs(Nakano_Ichika_Toy_Plot_mbc_Title_PDF); 

TCanvas *Ichika_Toy_Plot_de = new TCanvas("Ichika_Toy_Plot_de","Ichika_Toy_Plot_de",600,400);
RooPlot* frame_Ichika_de = deltae.frame(BiN);
frame_Ichika_de->SetTitle("Fitting result - signal_de");
Yotsuba.plotOn(frame_Ichika_de,CutRange("signal_box_de"),Cut("Nakano==Nakano::ichika"),Name("ichika_data"),XErrorSize(0));
Yotsuba_UMU.plotOn(frame_Ichika_de,ProjectionRange("signal_box_de"),Slice(Nakano,"ichika"),ProjWData(Nakano,Yotsuba),Name("ichika_tol"));
Yotsuba_UMU.plotOn(frame_Ichika_de,ProjectionRange("signal_box_de"),Slice(Nakano,"ichika"),Components("UMU_Ichika_sig"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kRed),Name("ichika_sig"));
Yotsuba_UMU.plotOn(frame_Ichika_de,ProjectionRange("signal_box_de"),Slice(Nakano,"ichika"),Components("UMU_Ichika_Nino"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kMagenta),Name("ichika_ssig"));
Yotsuba_UMU.plotOn(frame_Ichika_de,ProjectionRange("signal_box_de"),Slice(Nakano,"ichika"),Components("UMU_Ichika_BB"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlue),Name("ichika_BB"));
Yotsuba_UMU.plotOn(frame_Ichika_de,ProjectionRange("signal_box_de"),Slice(Nakano,"ichika"),Components("UMU_Ichika_qq"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlack),Name("ichika_qq"));
frame_Ichika_de -> GetYaxis() -> SetTitle("Events/(30 MeV)");
frame_Ichika_de -> GetXaxis() -> SetTitle("#Delta#it{E} [GeV]");
//frame_Ichika_de -> SetMaximum(220.);
frame_Ichika_de -> GetXaxis() -> CenterTitle(true);
TLegend *ichika_legend_de = new TLegend(0.58,0.93,0.88,0.63);
ichika_legend_de->SetBorderSize(0);
ichika_legend_de->SetFillStyle(0);
ichika_legend_de->SetTextSize(0.045);
ichika_legend_de->SetTextFont(42);
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_data"), "Data", "p");
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_tol"), "Total fit", "l");
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_sig"), "#it{B}^{+} #rightarrow #it{K}^{+}#it{#pi}^{0} + c.c.", "l");
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_ssig"), "#it{B}^{+} #rightarrow #it{#pi}^{+}#it{#pi}^{0} + c.c.", "l");
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_BB"), "#it{B} decay background", "l");
ichika_legend_de->AddEntry(frame_Ichika_de->findObject("ichika_qq"), "#it{q}#it{#bar{q}} background", "l");
frame_Ichika_de -> Draw(); 
TLatex *ichika_l_DE = new TLatex();
ichika_l_DE->SetTextFont(42);
ichika_l_DE->SetNDC();
ichika_l_DE->SetTextColor(1);
ichika_l_DE->SetTextSize(0.045);
//BELLE2Label(0.2,0.89,"(simulation)",(kBlack));
BELLE2Label(0.2,0.89,"(preliminary)",(kBlack));
//nino_l_DE->DrawLatex(0.2, 0.83, "2020 (preliminary)");
ichika_l_DE->DrawLatex(0.2, 0.8, "#int #it{L} d#it{t} = 62.8 fb^{-1}");
ichika_legend_de->Draw();

gPad->Update();
gPad->RedrawAxis();
TLine *ichika_Toy_DE_line = new TLine();
ichika_Toy_DE_line->SetLineWidth(3);
ichika_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymin());
ichika_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmin(),gPad->GetUymax());
ichika_Toy_DE_line->DrawLine(gPad->GetUxmax(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymax());
ichika_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymax(),gPad->GetUxmax(),gPad->GetUymax());

char Nakano_Ichika_Toy_Plot_de_Title[200];
sprintf(Nakano_Ichika_Toy_Plot_de_Title,"/mnt/c/Users/USER73441/Desktop/Plots/Yotsuba/Ichika_Moriond_2D_Proto_de.png");
Ichika_Toy_Plot_de->SaveAs(Nakano_Ichika_Toy_Plot_de_Title); 

char Nakano_Ichika_Toy_Plot_de_Title_PDF[200];
sprintf(Nakano_Ichika_Toy_Plot_de_Title_PDF,"/mnt/c/Users/USER73441/Desktop/Plots/Yotsuba/pdf/Ichika_Moriond_2D_Proto_de.pdf");
Ichika_Toy_Plot_de->SaveAs(Nakano_Ichika_Toy_Plot_de_Title_PDF); 

TCanvas *Nino_Toy_Plot_mbc = new TCanvas("Nino_Toy_Plot_mbc","Nino_Toy_Plot_mbc",600,400);
RooPlot* frame_Nino_mbc = mbc.frame(BiN);
frame_Nino_mbc->SetTitle("Fitting result - signal_mbc");
Yotsuba.plotOn(frame_Nino_mbc,Cut("Nakano==Nakano::nino"),CutRange("signal_box_mbc"),Name("nino_data"),XErrorSize(0));
Yotsuba_UMU.plotOn(frame_Nino_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"nino"),ProjWData(Nakano,Yotsuba),Name("nino_tol"));
Yotsuba_UMU.plotOn(frame_Nino_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"nino"),Components("UMU_Nino_sig"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kRed),Name("nino_sig"));
Yotsuba_UMU.plotOn(frame_Nino_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"nino"),Components("UMU_Nino_Ichika"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kMagenta),Name("nino_ssig"));
Yotsuba_UMU.plotOn(frame_Nino_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"nino"),Components("UMU_Nino_BB"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlue),Name("nino_BB"));
Yotsuba_UMU.plotOn(frame_Nino_mbc,ProjectionRange("signal_box_mbc"),Slice(Nakano,"nino"),Components("UMU_Nino_qq"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlack),Name("nino_qq"));
frame_Nino_mbc -> GetYaxis() -> SetTitle("Events/(2 MeV/c^{2})");
frame_Nino_mbc -> GetXaxis() -> SetTitle("#it{M}_{bc} [GeV/c^{2}]");
frame_Nino_mbc -> GetXaxis() -> CenterTitle(true);
frame_Nino_mbc -> SetMaximum(160.);
TLegend *nino_legend_mbc = new TLegend(0.45,0.93,0.75,0.63);
nino_legend_mbc->SetBorderSize(0);
nino_legend_mbc->SetFillStyle(0);
nino_legend_mbc->SetTextSize(0.045);
nino_legend_mbc->SetTextFont(42);
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_data"), "Data", "p");
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_tol"), "Total fit", "l");
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_sig"), "#it{B}^{+} #rightarrow #it{#pi}^{+}#it{#pi}^{0} + c.c.", "l");
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_ssig"), "#it{B}^{+} #rightarrow #it{K}^{+}#it{#pi}^{0} + c.c.", "l");
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_BB"), "#it{B} decay background", "l");
nino_legend_mbc->AddEntry(frame_Nino_mbc->findObject("nino_qq"), "#it{q}#it{#bar{q}} background", "l");
frame_Nino_mbc -> Draw(); 
TLatex *nino_l_MBC = new TLatex();
nino_l_MBC->SetTextFont(42);
nino_l_MBC->SetNDC();
nino_l_MBC->SetTextColor(1);
nino_l_MBC->SetTextSize(0.045);
//BELLE2Label(0.2,0.89,"(simulation)",(kBlack));
BELLE2Label(0.2,0.89,"(preliminary)",(kBlack));
//nino_l_MBC->DrawLatex(0.2, 0.83, "2020 (preliminary)");
nino_l_MBC->DrawLatex(0.2, 0.8, "#int #it{L} d#it{t} = 62.8 fb^{-1}");
nino_legend_mbc->Draw();

gPad->Update();
gPad->RedrawAxis();
TLine *nino_Toy_Mbc_line = new TLine();
nino_Toy_Mbc_line->SetLineWidth(3);
nino_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymin());
nino_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmin(),gPad->GetUymax());
nino_Toy_Mbc_line->DrawLine(gPad->GetUxmax(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymax());
nino_Toy_Mbc_line->DrawLine(gPad->GetUxmin(),gPad->GetUymax(),gPad->GetUxmax(),gPad->GetUymax());

char Nakano_Nino_Toy_Plot_mbc_Title[200];
sprintf(Nakano_Nino_Toy_Plot_mbc_Title,"/mnt/c/Users/USER73441/Desktop/Plots/Nino/Nino_Moriond_2D_Proto_mbc.png");
Nino_Toy_Plot_mbc->SaveAs(Nakano_Nino_Toy_Plot_mbc_Title); 

char Nakano_Nino_Toy_Plot_mbc_Title_PDF[200];
sprintf(Nakano_Nino_Toy_Plot_mbc_Title_PDF,"/mnt/c/Users/USER73441/Desktop/Plots/Nino/pdf/Nino_Moriond_2D_Proto_mbc.pdf");
Nino_Toy_Plot_mbc->SaveAs(Nakano_Nino_Toy_Plot_mbc_Title_PDF); 

TCanvas *Nino_Toy_Plot_de = new TCanvas("Nino_Toy_Plot_de","Nino_Toy_Plot_de",600,400);
RooPlot* frame_Nino_de = deltae.frame(BiN);
frame_Nino_de->SetTitle("Fitting result - signal_de");
Yotsuba.plotOn(frame_Nino_de,Cut("Nakano==Nakano::nino"),CutRange("signal_box_de"),Name("nino_data"),XErrorSize(0));
Yotsuba_UMU.plotOn(frame_Nino_de,ProjectionRange("signal_box_de"),Slice(Nakano,"nino"),ProjWData(Nakano,Yotsuba),Name("nino_tol"));
Yotsuba_UMU.plotOn(frame_Nino_de,ProjectionRange("signal_box_de"),Slice(Nakano,"nino"),Components("UMU_Nino_sig"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kRed),Name("nino_sig"));
Yotsuba_UMU.plotOn(frame_Nino_de,ProjectionRange("signal_box_de"),Slice(Nakano,"nino"),Components("UMU_Nino_Ichika"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kMagenta),Name("nino_ssig"));
Yotsuba_UMU.plotOn(frame_Nino_de,ProjectionRange("signal_box_de"),Slice(Nakano,"nino"),Components("UMU_Nino_BB"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlue),Name("nino_BB"));
Yotsuba_UMU.plotOn(frame_Nino_de,ProjectionRange("signal_box_de"),Slice(Nakano,"nino"),Components("UMU_Nino_qq"),ProjWData(Nakano,Yotsuba),LineStyle(kDashed),LineColor(kBlack),Name("nino_qq"));
frame_Nino_de -> GetYaxis() -> SetTitle("Events/(30 MeV)");
frame_Nino_de -> GetXaxis() -> SetTitle("#Delta#it{E} [GeV]");
frame_Nino_de -> GetXaxis() ->CenterTitle(true);
//frame_Nino_de -> SetMaximum(160.);
TLegend *nino_legend_de = new TLegend(0.58,0.93,0.88,0.63);
nino_legend_de->SetBorderSize(0);
nino_legend_de->SetFillStyle(0);
nino_legend_de->SetTextSize(0.045);
nino_legend_de->SetTextFont(42);
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_data"), "Data", "p");
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_tol"), "Total fit", "l");
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_sig"), "#it{B}^{+} #rightarrow #it{#pi}^{+}#it{#pi}^{0} + c.c.", "l");
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_ssig"), "#it{B}^{+} #rightarrow #it{K}^{+}#it{#pi}^{0} + c.c.", "l");
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_BB"), "#it{B} decay background", "l");
nino_legend_de->AddEntry(frame_Nino_de->findObject("nino_qq"), "#it{q}#it{#bar{q}} background", "l");
frame_Nino_de -> Draw(); 
TLatex *nino_l_DE = new TLatex();
nino_l_DE->SetTextFont(42);
nino_l_DE->SetNDC();
nino_l_DE->SetTextColor(1);
nino_l_DE->SetTextSize(0.045);
//BELLE2Label(0.2,0.89,"(simulation)",(kBlack));
BELLE2Label(0.2,0.89,"(preliminary)",(kBlack));
//nino_l_DE->DrawLatex(0.2, 0.83, "2020 (preliminary)");
nino_l_DE->DrawLatex(0.2, 0.8, "#int #it{L} d#it{t} = 62.8 fb^{-1}");
nino_legend_de->Draw();

gPad->Update();
gPad->RedrawAxis();
TLine *nino_Toy_DE_line = new TLine();
nino_Toy_DE_line->SetLineWidth(3);
nino_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymin());
nino_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymin(),gPad->GetUxmin(),gPad->GetUymax());
nino_Toy_DE_line->DrawLine(gPad->GetUxmax(),gPad->GetUymin(),gPad->GetUxmax(),gPad->GetUymax());
nino_Toy_DE_line->DrawLine(gPad->GetUxmin(),gPad->GetUymax(),gPad->GetUxmax(),gPad->GetUymax());

char Nakano_Nino_Toy_Plot_de_Title[200];
sprintf(Nakano_Nino_Toy_Plot_de_Title,"/mnt/c/Users/USER73441/Desktop/Plots/Nino/Nino_Moriond_2D_Proto_de.png");
Nino_Toy_Plot_de->SaveAs(Nakano_Nino_Toy_Plot_de_Title); 

char Nakano_Nino_Toy_Plot_de_Title_PDF[200];
sprintf(Nakano_Nino_Toy_Plot_de_Title_PDF,"/mnt/c/Users/USER73441/Desktop/Plots/Nino/pdf/Nino_Moriond_2D_Proto_de.pdf");
Nino_Toy_Plot_de->SaveAs(Nakano_Nino_Toy_Plot_de_Title_PDF);

double Kpi_BR = Ichika_NN.getVal()/(2*62.8*1.11*(1-0.487));
double pipi_BR = Nino_NN.getVal()/(2*62.8*1.11*(1-0.487));
double Kpi_BR_HE = Kpi_BR*(Ichika_NN.getAsymErrorHi()/Ichika_NN.getVal());
double Kpi_BR_LE = Kpi_BR*(Ichika_NN.getAsymErrorLo()/Ichika_NN.getVal());
double pipi_BR_HE = pipi_BR*(Nino_NN.getAsymErrorHi()/Nino_NN.getVal());
double pipi_BR_LE = pipi_BR*(Nino_NN.getAsymErrorLo()/Nino_NN.getVal());


double Kpi_EFF = 0.259*Ichika_ichikaa.getVal();
double pipi_EFF = 0.222*Nino_ninoo.getVal();
double Kpi_EFF_HE = Kpi_EFF*(Ichika_ichikaa.getAsymErrorHi()/Ichika_ichikaa.getVal());
double Kpi_EFF_LE = Kpi_EFF*(Ichika_ichikaa.getAsymErrorLo()/Ichika_ichikaa.getVal());
double pipi_EFF_HE = pipi_EFF*(Nino_ninoo.getAsymErrorHi()/Nino_ninoo.getVal());
double pipi_EFF_LE = pipi_EFF*(Nino_ninoo.getAsymErrorLo()/Nino_ninoo.getVal());
double Log_LH = Riri->minNll();

cout << "K pi0 BR = " << Kpi_BR << " + " << Kpi_BR_HE << " - " << Kpi_BR_LE << endl;
cout << "K pi0 Eff = " << Kpi_EFF << " + " << Kpi_EFF_HE << " - " << Kpi_EFF_LE << endl;
cout << "pi pi0 BR = " << pipi_BR << " + " << pipi_BR_HE << " - " << pipi_BR_LE << endl;
cout << "pi pi0 Eff = " << pipi_EFF << " + " << pipi_EFF_HE << " - " << pipi_EFF_HE << endl;
cout << "-Log LH = " << Log_LH << endl;
cout << "China = " << frame_Ichika_mbc->chiSquare("ichika_tol","ichika_data") << endl;
cout << "China_64 = " << frame_Nino_de->chiSquare("nino_tol","nino_data") << endl;
}