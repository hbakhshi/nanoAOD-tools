from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = ''
config.General.workArea = 'SMP19005April9_2018'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/hbakhshi/SMP19005/April9/'
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
#config.Site.whitelist = ['T2_DE_DESY', 'T2_US_Caltech' , 'T2_US_MIT' , 'T2_US_Nebraska']
#config.Site.storageSite = "T2_DE_DESY"
#config.section_("User")
#config.User.voGroup = 'dcms'

