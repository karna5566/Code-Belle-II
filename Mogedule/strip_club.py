import os
sample = ["chovy","charged","mixed","uu","cc","dd","ss","tt","mumu","ee1","ee2","eeee","eemumu","gg","J_psi","Kpipi0","pipipi0"]

category = {"chovy":"Signal","charged":"Generic","mixed":"Generic","uu":"Generic","cc":"Generic","dd":"Generic","ss":"Generic","tt":"Generic","mumu":"Generic","ee1":"Bhabha","ee2":"Bhabha","eeee":"Low_Multi","eemumu":"Low_Multi","gg":"Bhabha","J_psi":"Signal","Kpipi0":"Signal","pipipi0":"Signal"}

location = {"chovy":"/home/belle2/lch/MC15/zignal/Chovy/","charged":"/mnt/qnap_01/MC15/MC15ri_b_generic/charged/sub00/","mixed":"/mnt/qnap_01/MC15/MC15ri_b_generic/mixed/sub00/","uu":"/mnt/qnap_01/MC15/MC15ri_b_generic/uubar/sub00/","cc":"/mnt/qnap_01/MC15/MC15ri_b_generic/ccbar/sub00/","dd":"/mnt/qnap_01/MC15/MC15ri_b_generic/ddbar/sub00/","ss":"/mnt/qnap_01/MC15/MC15ri_b_generic/ssbar/sub00/","tt":"/mnt/qnap_01/MC15/MC15ri_b_generic/taupair/sub00/","mumu":"/mnt/qnap_01/MC15/MC15ri_b_generic/mumu/sub00/","ee1":"/mnt/qnap_01/MC15/MC15ri_a_default/ee/sub00/","ee2":"/mnt/qnap_01/MC15/MC15ri_a_default/ee/sub01/","eeee":"/mnt/qnap_01/MC15/MC15ri_a_default/eeee/sub00/","eemumu":"/mnt/qnap_01/MC15/MC15ri_a_default/eemumu/sub00/","gg":"/mnt/qnap_01/MC15/MC15ri_a_default/gg/sub00/","J_psi":"/mnt/qnap_01/MC14/MC14ri_a_signal/1111520200/sub00/","Kpipi0":"/mnt/qnap_01/MC15/MC15ri_b_signal/1110022003/sub00/","pipipi0":"/mnt/qnap_01/MC15/MC15ri_b_unofficial/1110022005/sub00/"}

files = {"chovy":[],"charged":[],"mixed":[],"uu":[],"cc":[],"dd":[],"ss":[],"tt":[],"mumu":[],"ee1":[],"ee2":[],"eeee":[],"eemumu":[],"gg":[],"J_psi":[],"Kpipi0":[],"pipipi0":[]}

for u in sample:
	dir_path = r''+location.get(u)
	for paths in os.listdir(dir_path):
		if os.path.isfile(os.path.join(dir_path, paths)):files[u].append(paths)
