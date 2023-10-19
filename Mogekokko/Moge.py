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
from basf2 import conditions
b2.conditions.prepend_globaltag("analysis_tools_release-04-02")

if sys.argv[1] != 'grid':
	a = sys.argv[2]
	b = sys.argv[3]
	num = int(b)-1
	sys.path.append(os.environ['Mogedule'])
	import strip_club as strip
	input_file = strip.location.get(a)+strip.files[a][num]
	output_file = f'./Ntuple/{strip.category.get(a)}/{os.path.basename(os.getcwd())}_{a}_{b}.root'
else : 
	input_file = 'test.root'
	output_file = 'Qdst.root'
his_path=b2.Path()
ma.inputMdst('default',input_file,path=his_path)

trigger_skim_module = his_path.add_module("TriggerSkim",triggerLines=["software_trigger_cut&skim&accept_hadron"])
trigger_skim_module.if_value("==0",b2.Path(),b2.AfterConditionPath.END)

ma.fillParticleList(decayString='e+:basic',cut='dr < 2 and abs(dz) < 4',path=his_path)

CellID_cut = '[clusterCellID==1000 or clusterCellID==1001 or clusterCellID==2000 or clusterCellID==2001 or clusterCellID==3000 or clusterCellID==3001 or clusterCellID==4000 or clusterCellID==4001 or clusterCellID==6000 or clusterCellID==6001 or clusterCellID==8000 or clusterCellID==8001]'
ma.ApplyCuts('e+:basic',cut=CellID_cut,path=his_path)


ma.matchMCTruth('e+:basic',path=his_path)

cms_kinematics = vu.create_aliases(vc.kinematics + ['cosTheta'], "useCMSFrame({variable})", "CMS")
cms_mc_kinematics = vu.create_aliases(vc.mc_kinematics, "useCMSFrame({variable})", "CMS")
Kine_vars = cms_kinematics + vc.kinematics + vc.mc_kinematics + cms_mc_kinematics + vc.inv_mass


vm.addAlias("GMotherPDG", "genMotherPDG(1)")
vm.addAlias("MotherPDG", "genMotherPDG(0)")
Cluster_vars = Kine_vars + vc.pid + ['electronID_noSVD'] + vc.mc_truth + vc.cluster + vc.event_level_cluster + ['clusterE','clusterTheta','clusterCellID','clusterMCMatchWeight','GMotherPDG','MotherPDG','thetaInCDCAcceptance','nCDCHits']

ma.variablesToNtuple('e+:basic',Cluster_vars,filename=output_file, treename='merged',path=his_path)
#b2.process(his_path,max_event=100)
b2.process(his_path)
print(b2.statistics)
