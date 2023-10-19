#				#                  #
#			   # #                # #
#             #   #              #   #
#            #     #            #     #
#           #       #          #       #
#          #         #        #         #
#         #           #######            #
#        #                                #
#       #                                  #
#                #               #         
#      #        # #             # #         #
#              #   #           #   #        
#     #                                      #
#
#     #                                      #
#                      ###
#      #              #   #                 # 
#                      ###
#        #                                #  
#           #                          #   
#                #                #
#                      

import basf2 as b2
import sys 
import os
import modularAnalysis as ma
import variables.collections as vc
import variables.utils as vu
from variables import variables as vm
from stdPhotons import stdPhotons
from stdPi0s import stdPi0s
from basf2 import conditions
import reconstruction
from softwaretrigger.path_utils import add_skim_software_trigger
from softwaretrigger.path_utils import add_filter_software_trigger

if sys.argv[1] != 'grid':
	'''
	a = sys.argv[2]
	b = sys.argv[3]
	num = int(b)-1
	sys.path.append(os.environ['Mogedule'])
	import strip_club as strip
	input_file = strip.location.get(a)+strip.files[a][num]
	output_file = f'./Ntuple/{strip.category.get(a)}/{os.path.basename(os.getcwd())}_{a}_{b}.root'
	'''
	input_file = ''
	output_file = 'test.root'
	#b2.conditions.prepend_globaltag('hlt_filters_exp24')
else : 
	#b2.conditions.prepend_globaltag('hlt_filters_exp24')
	input_file = 'test.root'
	output_file = 'Qdst.root'

his_path=b2.Path()
ma.inputMdst('default',input_file,path=his_path)

#trigger_skim_module = his_path.add_module("TriggerSkim",triggerLines=["software_trigger_cut&skim&accept_hadronb2"])
#trigger_skim_module.if_value("==0",b2.Path(),b2.AfterConditionPath.END)
#,loadPhotonBeamBackgroundMVA=True
ma.fillParticleList('gamma:not_all','E>0.02',path=his_path)

stdPhotons('cdc', path=his_path)
ma.applyCuts('gamma:cdc','E>0.05',path=his_path)

#ma.cutAndCopyList('gamma:we_want','gamma:cdc'," ",path=his_path)
CellList = []
for i in [1000,4000,6000,8000] : CellList += [*range(i,i+30)]
CellList += [*range(6769,7030)]

CellID_cut = f"clusterCellID=={' or clusterCellID=='.join(str(x) for x in CellList)}"
#CellID_cut = '[clusterCellID==1000 or clusterCellID==1001 or clusterCellID==2000 or clusterCellID==2001 or clusterCellID==3000 or clusterCellID==3001 or clusterCellID==4000 or clusterCellID==4001 or clusterCellID==8000 or clusterCellID==8001]'

ma.reconstructDecay('pi0:tight -> gamma:cdc gamma:cdc', '0.11<InvM<0.15', 1, True, path=his_path)
vm.addAlias('tight','isDescendantOfList(pi0:tight,1)')

ma.reconstructDecay('pi0:tight_tight -> gamma:cdc gamma:cdc', '0.12<InvM<0.145', 1, True, path=his_path)
vm.addAlias('tight_tight','isDescendantOfList(pi0:tight_tight,1)')

ma.reconstructDecay('pi0:eff30 -> gamma:cdc gamma:cdc', '0.12<InvM<0.145 and -1.5<daughterDiffOfPhi(0,1)<1.5 and daughterAngle(0,1)<1.4', 1, True, path=his_path)
vm.addAlias('eff30','isDescendantOfList(pi0:eff30,1)')

ma.reconstructDecay('pi0:tight_tight_tight -> gamma:cdc gamma:cdc', '0.121<InvM<0.142', 1, True, path=his_path)
vm.addAlias('tight_tight_tight','isDescendantOfList(pi0:tight_tight_tight,1)')

ma.reconstructDecay('pi0:eff20 -> gamma:cdc gamma:cdc', '0.121<InvM<0.142 and -1.0<daughterDiffOfPhi(0,1)<1.0 and daughterAngle(0,1)<0.9', 1, True, path=his_path)
vm.addAlias('eff20','isDescendantOfList(pi0:eff20,1)')

ma.reconstructDecay('pi0:too_tight -> gamma:cdc gamma:cdc', '0.127<InvM<0.139', 1, True, path=his_path)
vm.addAlias('too_tight','isDescendantOfList(pi0:too_tight,1)')

ma.reconstructDecay('pi0:eff10 -> gamma:cdc gamma:cdc', '0.127<InvM<0.139 and -0.9<daughterDiffOfPhi(0,1)<0.9 and daughterAngle(0,1)<0.8', 1, True, path=his_path)
vm.addAlias('eff10','isDescendantOfList(pi0:eff10,1)')

stdPi0s('eff60_May2020',path=his_path)
vm.addAlias('eff60_May2020','isDescendantOfList(pi0:eff60_May2020,1)')
stdPi0s('eff50_May2020',path=his_path)
vm.addAlias('eff50_May2020','isDescendantOfList(pi0:eff50_May2020,1)')
stdPi0s('eff40_May2020',path=his_path)
vm.addAlias('eff40_May2020','isDescendantOfList(pi0:eff40_May2020,1)')
stdPi0s('eff30_May2020',path=his_path)
vm.addAlias('eff30_May2020','isDescendantOfList(pi0:eff30_May2020,1)')
stdPi0s('eff20_May2020',path=his_path)
vm.addAlias('eff20_May2020','isDescendantOfList(pi0:eff20_May2020,1)')
stdPi0s('eff10_May2020',path=his_path)
vm.addAlias('eff10_May2020','isDescendantOfList(pi0:eff10_May2020,1)')

ma.applyCuts('gamma:not_all',CellID_cut,path=his_path)
ma.matchMCTruth('gamma:not_all',path=his_path)
#ma.applyCuts('gamma:cdc',CellID_cut,path=his_path)
#ma.matchMCTruth('gamma:cdc',path=his_path)

cms_kinematics = vu.create_aliases(vc.kinematics + ['cosTheta'], "useCMSFrame({variable})", "CMS")
cms_mc_kinematics = vu.create_aliases(vc.mc_kinematics, "useCMSFrame({variable})", "CMS")
Kine_vars = cms_kinematics + vc.kinematics + vc.mc_kinematics + cms_mc_kinematics + vc.inv_mass
pi0_mass_list = ['tight','tight_tight','eff30','tight_tight_tight','eff20','too_tight','eff10','eff60_May2020','eff50_May2020','eff40_May2020','eff30_May2020','eff20_May2020','eff10_May2020']
#pi0_mass_list = ['tight','tight_tight','eff30','tight_tight_tight','eff20','too_tight','eff10']
add_filter_software_trigger(his_path)
add_filter_software_trigger(his_path)
add_skim_software_trigger(his_path)

vm.addAlias('hlt_hadron','SoftwareTriggerResult(software_trigger_cut&skim&accept_hadron)')
vm.addAlias('hlt_hadronb','SoftwareTriggerResult(software_trigger_cut&skim&accept_hadronb)')
vm.addAlias('hlt_hadronb1','SoftwareTriggerResult(software_trigger_cut&skim&accept_hadronb1)')
vm.addAlias('hlt_hadronb2','SoftwareTriggerResult(software_trigger_cut&skim&accept_hadronb2)')

vm.addAlias("GMotherPDG", "genMotherPDG(1)")
vm.addAlias("MotherPDG", "genMotherPDG(0)")

Cluster_vars = pi0_mass_list + Kine_vars + vc.mc_truth + vc.cluster + vc.event_level_cluster + ['hlt_hadron','hlt_hadronb','hlt_hadronb1','hlt_hadronb2','minC2TDist','beamBackgroundProbabilityMVA','clusterE','clusterTheta','clusterCellID','clusterMCMatchWeight','GMotherPDG','MotherPDG']

ma.variablesToNtuple('gamma:not_all',Cluster_vars,filename=output_file, treename='merged',path=his_path)
#b2.process(his_path,max_event=100)
b2.process(his_path)
print(b2.statistics)
