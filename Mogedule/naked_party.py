import basf2 as b2
import os
import modularAnalysis as ma
import stdPi0s
from variables import variables as vm
import variables.utils as vu
import variables.collections as vc
import re

Prompt_Exp = [20,22,24,26]

def Smol_Ame(particle='',name='',cut='',path=''):
	Name=particle+":"+name
	if (particle != 'pi0'):
		GoodTrack = 'thetaInCDCAcceptance and nCDCHits>20 and dr < 0.5 and abs(dz) < 2'
		ma.fillParticleList(Name,GoodTrack,True,path)
		ma.applyCuts(Name,cut,path)
		if (name.find('_cor') != -1):
			ma.fillParticleList('gamma:brems','[[clusterReg == 1 and clusterE > 0.075] or [clusterReg == 2 and clusterE > 0.05] or [clusterReg == 3 and clusterE > 0.1]]',True,path)
			ma.correctBremsBelle(Name[:-4],Name,'gamma:brems',multiplePhotons=True,path=path)
	else:
		stdPi0s.stdPi0s(listtype=cut,path=path)
		ma.copyLists(Name,'pi0:'+cut[:-3],path=path)
	ma.matchMCTruth(Name,path)

def makePretty(varlist):
    """
    Makes the names of some variables pretty for the ntuples.
    """

    output = []
    for var in varlist:
        newvar = re.sub('[\*\+:(,\-]', '_', var)
        nnewvar = re.sub('[)]','',newvar)
        if (nnewvar != var):
            vm.addAlias(nnewvar, var)
        output += [nnewvar]
    return output


def Recon_type(teyp = ''):
	allowedtype = ['taumu','taue']
#	if teyp not in allowedtype:
#	b2.B2FATAL("The allowed input file types are 'taumu' or 'taue'.")
	if teyp == 'taumu':
		Lep_name = 'mu-:sick'
	elif teyp == 'taue':
		Lep_name = 'e-:sick'
	return(Lep_name)

#Bset Acnditade
def addRanking(particleList='', ppath=''):
	ma.rankByHighest(particleList, 'chiProb', numBest=0,outputVariable='chiProb_rank', path=ppath)
	vm.addAlias('chiProb_rank', 'extraInfo(chiProb_rank)')
	ma.rankByHighest(particleList, 'daughter(1,useCMSFrame(p))', numBest=0,outputVariable='l_pcms_rank', path=ppath)
	vm.addAlias('l_pcms_rank', 'extraInfo(l_pcms_rank)')
	ma.rankByHighest(particleList, 'daughter(1,muonID_noSVD)', numBest=0,outputVariable='l_muid_rank', path=ppath)
	vm.addAlias('l_muid_rank', 'extraInfo(l_muid_rank)')
	ma.rankByHighest(particleList, 'daughter(1,electronID_noSVD)', numBest=0,outputVariable='l_eid_rank', path=ppath)
	vm.addAlias('l_eid_rank', 'extraInfo(l_eid_rank)')
	ma.rankByHighest(particleList, 'daughter(1,useCMSFrame(p))', numBest=0,outputVariable='l_pcms_muid_rank',cut="l_muid_rank == 1", path=ppath)
	vm.addAlias('l_pcms_muid_rank', 'extraInfo(l_pcms_muid_rank)')
	ma.rankByHighest(particleList, 'daughter(1,useCMSFrame(p))', numBest=0,outputVariable='l_pcms_eid_rank',cut="l_eid_rank == 1", path=ppath)
	vm.addAlias('l_pcms_eid_rank', 'extraInfo(l_pcms_eid_rank)')

	rank_vars = ['chiProb_rank','l_pcms_rank','l_muid_rank','l_eid_rank','l_pcms_muid_rank','l_pcms_eid_rank']
	return(rank_vars)

#PDG	
vm.addAlias("MotherPDG", "genMotherPDG(0)")
vm.addAlias("GMotherPDG", "genMotherPDG(1)")
vm.addAlias("D_0_PDG", "daughter(0,mcPDG)")
vm.addAlias("D_1_PDG", "daughter(1,mcPDG)")
vm.addAlias("D_2_PDG", "daughter(2,mcPDG)")
Your_mom = ['MotherPDG','GMotherPDG','D_0_PDG','D_1_PDG','D_2_PDG']

cms_kinematics = vu.create_aliases(vc.kinematics + ['cosTheta'], "useCMSFrame({variable})", "CMS")
cms_mc_kinematics = vu.create_aliases(vc.mc_kinematics, "useCMSFrame({variable})", "CMS")

LepID=['muonID_noSVD','muonID','electronID_noSVD','electronID_noTOP','electronID','pionID']

vm.addAlias('BKID','binaryPID(321,211)')
KID = ['BKID']

Kine_vars = cms_kinematics + vc.kinematics + vc.mc_kinematics + cms_mc_kinematics + vc.inv_mass
Lep_vars = LepID + Kine_vars + vc.track + vc.mc_truth + vc.vertex + ['isInRestOfEvent']
tau_vars = []

tau_pi0_vars = []

for vars in Lep_vars + Your_mom:
	vm.addAlias(f"Tau_l_{vars}", f"daughter(0,daughter(0,{vars}))")
	tau_vars.append(f"Tau_l_{vars}")
for vars in Kine_vars :
	vm.addAlias(f"Tau_pi0_{vars}", f"daughter(0,daughter(1,{vars}))")
	tau_pi0_vars.append(f"Tau_pi0_{vars}")

vm.addAlias("dMID", "daughter(0,extraInfo(decayModeID))")
tau_vars.append("dMID")

roe_kinematics = ["roeE()", "roeM()", "roeP()","roePx()","roePy()","roePz()","roeMbc()", "roeDeltae()"]
roe_mckinematics = ["roeMC_E","roeMC_P","roeMC_Px","roeMC_Py","roeMC_Pz"]
cms_roe_kinematics = []
for var in roe_kinematics:
	cms_roe_kinematics.append(f"useCMSFrame({var})")
roe_multiplicities = ["nROE_Charged()","nROE_Photons()","nROE_NeutralHadrons()",]
def ROE_vars(Mask=str()):
	roe_vars=roe_mckinematics
	for roe_variable in roe_kinematics + roe_multiplicities:
		roe_variable_with_mask = roe_variable.replace("()", f"({Mask})")
		roe_variable_name_with_mask = roe_variable.replace("()", f"_{Mask}")
		vm.addAlias(roe_variable_name_with_mask,roe_variable_with_mask)
		roe_vars.append(roe_variable_name_with_mask)
	return(roe_vars)
#: Continuum suppression variables
cont_suppr_base = [
    'R2',
    'thrustBm',
    'thrustOm',
    'cosTBTO',
    'cosTBz'
]

#: Transverse energy and missing momentum squared (calculated within the KSFW moments)
et_mm2 = makePretty([
    'KSFWVariables(et)',
    'KSFWVariables(mm2)'
])

#: KSFW Moments calculated using primary particles
ksfw_moments = makePretty([
    'KSFWVariables(hso00)',
    'KSFWVariables(hso02)',
    'KSFWVariables(hso04)',
    'KSFWVariables(hso10)',
    'KSFWVariables(hso12)',
    'KSFWVariables(hso14)',
    'KSFWVariables(hso20)',
    'KSFWVariables(hso22)',
    'KSFWVariables(hso24)',
    'KSFWVariables(hoo0)',
    'KSFWVariables(hoo1)',
    'KSFWVariables(hoo2)',
    'KSFWVariables(hoo3)',
    'KSFWVariables(hoo4)',
])

#: KSFW Moments calculated only from final-state particles
ksfw_moments_fs1 = makePretty([
    'KSFWVariables(hso00,FS1)',
    'KSFWVariables(hso02,FS1)',
    'KSFWVariables(hso04,FS1)',
    'KSFWVariables(hso10,FS1)',
    'KSFWVariables(hso12,FS1)',
    'KSFWVariables(hso14,FS1)',
    'KSFWVariables(hso20,FS1)',
    'KSFWVariables(hso22,FS1)',
    'KSFWVariables(hso24,FS1)',
    'KSFWVariables(hoo0,FS1)',
    'KSFWVariables(hoo1,FS1)',
    'KSFWVariables(hoo2,FS1)',
    'KSFWVariables(hoo3,FS1)',
    'KSFWVariables(hoo4,FS1)',
])

#: Cleo cones
cleo_cones = makePretty([
    'CleoConeCS(1)',
    'CleoConeCS(2)',
    'CleoConeCS(3)',
    'CleoConeCS(4)',
    'CleoConeCS(5)',
    'CleoConeCS(6)',
    'CleoConeCS(7)',
    'CleoConeCS(8)',
    'CleoConeCS(9)',
])

#: Cleo cones calculated using only the ROE
roe_cleo_cones = makePretty([
    'CleoConeCS(1,ROE)',
    'CleoConeCS(2,ROE)',
    'CleoConeCS(3,ROE)',
    'CleoConeCS(4,ROE)',
    'CleoConeCS(5,ROE)',
    'CleoConeCS(6,ROE)',
    'CleoConeCS(7,ROE)',
    'CleoConeCS(8,ROE)',
    'CleoConeCS(9,ROE)'
])

#: All available continuum suppression variables
cont_suppr_all = cont_suppr_base + et_mm2 + cleo_cones + roe_cleo_cones + ksfw_moments + ksfw_moments_fs1


B_vars = vc.deltae_mbc + Kine_vars + vc.mc_truth + vc.vertex + vc.mc_vertex + vc.tag_vertex + vc.mc_tag_vertex + Your_mom + tau_vars + vc.event_shape + cont_suppr_all + ['cosHelicityAngleMomentum']

#Cluster
Cluster_vars = Kine_vars + vc.mc_truth + vc.cluster + vc.event_level_cluster + ['MotherPDG','GMotherPDG','clusterCellID']
gamma_vars = []
for vars in Cluster_vars:
	vm.addAlias(f"gamma_1_{vars}", f"daughter(0,{vars})")
	vm.addAlias(f"gamma_2_{vars}", f"daughter(1,{vars})")
	gamma_vars.append(f"gamma_1_{vars}")
	gamma_vars.append(f"gamma_2_{vars}")
	
pi0_vars = Kine_vars + vc.mc_truth + gamma_vars

def getInputOptions_service():
	import argparse
	parser = argparse.ArgumentParser(description='You can find the argparse at /home/belle2/lch/Mogege/Mogedule/naked_party.py \n So.py : Make pdf, Fo.py : Fitting, Jo.py : Draw MC-only plots (Show different components & purity), Do.py : Draw MC-Data 2D plots, Qo.py : Draw MC-Data 1D plots')
	parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data')
	parser.add_argument('-id','--ID', nargs='+',help='Cell ID', type=int)
	parser.add_argument('-e','--E',nargs='+',help='Min E and Max E',type=int)
	parser.add_argument('-type','--Type',nargs='?',help='gamma,lepton,hadron,l_h,nan or all (Used in So.py)')
	parser.add_argument('-v','--Var',nargs='?',help='clusterTiming,clusterHighestE,clusterZernikeMVA,minC2TDist,clusterE9E21 (Used in Qo.py)',default='clusterTiming')
	parser.add_argument('-v2','--Var2',nargs='?',help='clusterTiming,clusterHighestE,clusterZernikeMVA,minC2TDist,clusterE9E21 (Used in Do.py)',default='clusterZernikeMVA')
	args = parser.parse_args()
	return args

class LegendDrawer:
	def __init__(self, x1, y1, x2, y2):
		self.legend = ROOT.TLegend(x1, y1, x2, y2)
		self.legend.SetBorderSize(0)
		self.legend.SetFillStyle(0)
		self.legend.SetTextSize(0.045)
		self.legend.SetTextFont(42)

	def add_entry(self, obj, label, option):
		self.legend.AddEntry(obj, label, option)

	def draw(self):
		self.legend.Draw()

def setup_tree_branches(tree):
    from array import array
    width = array('d', [0.])
    tree.Branch("width", width, "width/D")
    width_err = array('d', [0.])
    tree.Branch("width_err", width_err, "width_err/D")
    Mean = array('d', [0.])
    tree.Branch("Mean", Mean, "Mean/D")
    Mean_err = array('d', [0.])
    tree.Branch("Mean_err", Mean_err, "Mean_err/D")
    ClusterE = array('d', [0.])
    tree.Branch("ClusterE", ClusterE, "ClusterE/D")
    ClusterE_err = array('d', [0.])
    tree.Branch("ClusterE_err", ClusterE_err, "ClusterE_err/D")
    CellID_lo = array('i', [0])
    tree.Branch("CellID_lo", CellID_lo, "CellID_lo/I")
    CellID_up = array('i', [0])
    tree.Branch("CellID_up", CellID_up, "CellID_up/I")
    Purity = array('d', [0.])
    tree.Branch("Purity", Purity, "Purity/D")
    Log_LH_mc = array('d', [0.])
    tree.Branch("Log_LH_mc", Log_LH_mc, "Log_LH_mc/D")
    Log_LH_data = array('d', [0.])
    tree.Branch("Log_LH_data", Log_LH_data, "Log_LH_data/D")
    nevents = array('i', [0])
    tree.Branch("nevents", nevents, "nevents/I")
    FWHM_MC = array('d', [0.])
    tree.Branch("FWHM_MC", FWHM_MC, "FWHM_MC/D")
    FWHM_Data = array('d', [0.])
    tree.Branch("FWHM_Data", FWHM_Data, "FWHM_Data/D")
    Mean_MC = array('d', [0.])
    tree.Branch("Mean_MC", Mean_MC, "Mean_MC/D")
    Mean_MC_err = array('d', [0.])
    tree.Branch("Mean_MC_err", Mean_MC_err, "Mean_MC_err/D")
    n_gamma = array('d', [0.])
    tree.Branch("n_gamma", n_gamma, "n_gamma/D")
    n_gamma_err = array('d', [0.])
    tree.Branch("n_gamma_err", n_gamma_err, "n_gamma_err/D")
    n_gamma_pull = array('d', [0.])
    tree.Branch("n_gamma_pull", n_gamma_pull, "n_gamma_pull/D")

#Believe in the spin
'''
def Mozzarella_Pizza(B_or_ROE=str(),Mask=str()):
	if B_or_ROE == 'B':
		P_Lab = ['mcE','mcPX','mcPY','mcPZ']
		vm.addAlias("dMID", "formula()")
	elif B_or_ROE == 'ROE'
		P_Lab = ['roeMC_E','roeMC_Px','roeMC_Py','roeMC_Pz']
	L_Matrix = [[],[],[],[]]
	for roe_variable in roe_kinematics + roe_multiplicities:
		roe_variable_with_mask = roe_variable.replace("()", "(BcleanMask)")
		roe_vars.append(roe_variable_with_mask)
	P_ROE = ['roeP']
	V_B = []
'''


