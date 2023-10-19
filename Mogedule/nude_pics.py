Westbrick = {'mu_pBrest':[0.2,2.7,'$\mathrm{p}^{B\:rest}_{\mathrm{\mu}}$ $[GeV/c]$','p_Brest'],'Mbc':[3.8,5.3,'$\mathrm{m}_{\mathrm{bc}}$ $[GeV/c^{2}]$','mbc'],'deltaE':[-5,0,'$\Delta E$ $[GeV]$','de'],'roeMbc_BcleanMask':[4.0,5.3,'$\mathrm{m}^{ROE}_{\mathrm{bc}}$ $[GeV/c^{2}]$','roe_mbc'],'roeDeltae_BcleanMask':[-5,5,'$\Delta E^{ROE}$ $[GeV]$','roe_de'],'roeP_BcleanMask':[0,6,'$p^{ROE}$ $[GeV/c]$','roe_p'],'Open_Angle':[-1,1,r'$cos \theta$','cos_polar'],'CMS_Open_Angle':[-1,1,r'$cos \theta\:in\:CMS\:frame$','cms_cos_polar'],'BRest_Open_Angle':[-1,1,r'$cos \theta\:in\:ROE\:frame$','brest_cos_polar']}

Jerusalem = {'clusterTiming':[-200,200,'ClusterTiming [ns]','ClusterTiming',0.2,0.7,1],'clusterHighestE':[0,5,'ClusterE [GeV]','ClusterE',0.4,0.7,0],'clusterMCMatchWeight/clusterE':[0,1.2,'clusterMCMatchWeight/clusterE','clusterMCWeight',0.2,0.7,0],'clusterZernikeMVA':[0.25,1.,'clusterZernikeMVA','ZernikeMVA',0.2,0.5,0],'clusterE9E21':[0.5,1.,'clusterE9E21','E9E21',0.2,0.5,1],'minC2TDist':[25,250,'minC2TDist [cm]','minC2TDist',0.2,0.5,0],'clusterLAT':[0.,1.,'clusterLAT','LAT',0.2,0.5,0]}

Constantinople = {'clusterTiming':[-200,200,'ClusterTiming [ns]','ClusterTiming'],'clusterHighestE':[0,0.3,'ClusterE [GeV]','ClusterE'],'clusterZernikeMVA':[0.25,1.,'clusterZernikeMVA','ZernikeMVA'],'clusterE9E21':[0.,1.,'clusterE9E21','E9E21'],'minC2TDist':[25,250,'minC2TDist [cm]','minC2TDist']}

Venezia = {'Bucket26':['#int #it{L} d#it{t} = 37.8 fb^{-1}','#int #it{L} d#it{t} = 151.2 fb^{-1}','==20',0,994,'Bucket26'],'Bucket28':['#int #it{L} d#it{t} = 11.8 fb^{-1}','#int #it{L} d#it{t} = 47.2 fb^{-1}','==22',21,370,'Bucket28'],'Bucket29':['#int #it{L} d#it{t} = 20.1 fb^{-1}','#int #it{L} d#it{t} = 80.4 fb^{-1}','==22',371,723,'Bucket29'],'Bucket30':['#int #it{L} d#it{t} = 20.5 fb^{-1}','#int #it{L} d#it{t} = 82.0 fb^{-1}','==24',790,998,'Bucket30'],'Bucket31':['#int #it{L} d#it{t} = 17.4 fb^{-1}','#int #it{L} d#it{t} = 69.6 fb^{-1}','==24',1077,1460,'Bucket31'],'Bucket32':['#int #it{L} d#it{t} = 22.8 fb^{-1}','#int #it{L} d#it{t} = 47.2 fb^{-1}','==24',1547,1916,'Bucket32'],'Bucket33':['#int #it{L} d#it{t} = 24.4 fb^{-1}','#int #it{L} d#it{t} = 97.6 fb^{-1}','==24',1917,2311,'Bucket33'],'Bucket35':['#int #it{L} d#it{t} = 35.4 fb^{-1}','#int #it{L} d#it{t} = 141.6 fb^{-1}','==26',33,1409,'Bucket35'],'Bucket36':['#int #it{L} d#it{t} = 18.7 fb^{-1}','#int #it{L} d#it{t} = 74.8 fb^{-1}','==26',1410,1968,'Bucket36'],'Prompt_data':['#int #it{L} d#it{t} = 174.8 fb^{-1}','#int #it{L} d#it{t} = 699.2 fb^{-1}','>=20',0,9999,'prompt']}
Merv = {repr([50,100]):[0.75,75],repr([100,200]):[0.5,50],repr([200,400]):[0.5,50],repr([400,1000]):[0.25,25]}

import ROOT

class Legend:
	def __init__(self, x1, y1, x2, y2):
		self.legend = ROOT.TLegend(x1, y1, x2, y2)
		self.legend.SetBorderSize(0)
		self.legend.SetFillStyle(0)
		self.legend.SetTextSize(0.045)
		self.legend.SetTextFont(42)

	def add_entry(self, obj, label, option):
		self.legend.AddEntry(obj, label, option)
	def clear(self):
		self.legend.Clear()
	def draw(self):
		self.legend.Draw()

class Lumi:
	def __init__(self, x, sample,id_text):
		self.lumi = ROOT.TLatex()
		self.lumi.SetTextFont(42)
		self.lumi.SetNDC()
		self.lumi.SetTextColor(1)
		self.lumi.SetTextSize(0.045)
		self.lumi.DrawLatex(x1+0.1, 0.89,"(simulation)" )
		self.lumi.DrawLatex(x, 0.8, Venezia[sample][1])
		self.lumi.DrawLatex(x, 0.7, f"MC15_rd ({Venezia[sample][5]} data)")
		self.lumi.DrawLatex(x, 0.65, id_text)

	def draw(self):
		self.lumi.Draw()





