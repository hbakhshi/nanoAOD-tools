#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis,outFileName
import os

from PhysicsTools.NanoAODTools.postprocessing.vbfgamma.Skimmer import Skimmer2016, Skimmer2017, Skimmer2018
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018
from PhysicsTools.NanoAODTools.postprocessing.vbfgamma.PhotonSF import photonSFFall17V2_2016_Tight,photonSFFall17V2_2017_Tight, photonSFFall17V2_2018_Tight

#II = inputFiles()
II = ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/270000/1FB6AF93-29B0-F34E-92EC-E9C859AED428.root']
#II= ['/eos/cms/store/data/Run2017F/SinglePhoton/NANOAOD/Nano25Oct2019-v1/20000/F9D973FF-123F-C841-A2C0-14DFC3D38975.root']
#['/afs/cern.ch/user/h/hbakhshi/eos/Personal/Projects/VBFGamma/NanoAODTools/GJets_8AD6BAB6-0FFD-7449-A58D-96DAAA1402E5.root', './a.root']
if len(II)>0 and 'SinglePhoton' in II[0] : #running on data
    if 'Run2016' in II[0]:
        modules_=[Skimmer2016()]
    elif 'Run2017' in II[0]:
        print('HERE')
        modules_=[Skimmer2017()]
    elif 'Run2018' in II[0]:
        modules_=[Skimmer2018()]
elif len(II)>0:
    if 'Summer16' in II[0]:
        modules_=[Skimmer2016(), puAutoWeight_2016(), photonSFFall17V2_2017_Tight(),photonSFFall17V2_2016_Tight() ]
    elif 'Fall17' in II[0]:
        print('here')
        modules_=[Skimmer2017(), puAutoWeight_2017(), photonSFFall17V2_2017_Tight(),photonSFFall17V2_2016_Tight() ]
    elif 'Autumn18' in II[0]:
        print('Autumn18')
        modules_=[Skimmer2018(), puAutoWeight_2018(), photonSFFall17V2_2017_Tight(),photonSFFall17V2_2016_Tight(), photonSFFall17V2_2018_Tight ]
p = PostProcessor( "." , II , maxEntries = None, branchsel=None, cut=None, compression='LZMA:9',
                   outputbranchsel='{0}/python/PhysicsTools/NanoAODTools/postprocessing/vbfgamma/keep_and_drop.txt'.format(os.environ['CMSSW_BASE']),
                   postfix=None, modules=modules_ , noOut=False, prefetch=False, justcount=False,
                   firstEntry=0, longTermCache=False, friend=False,
                   provenance=True,fwkJobReport=True,jsonInput=runsAndLumis() )
p.run()

print "DONE"

