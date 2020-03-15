#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.vbfgamma.Skimmer import Skimmer2016
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016
from PhysicsTools.NanoAODTools.postprocessing.vbfgamma.PhotonSF import photonSFFall17V2_2016_Tight,photonSFFall17V2_2017_Tight
p = PostProcessor( "." , inputFiles() , maxEntries = None, branchsel=None, cut=None, compression='LZMA:9', outputbranchsel='python/postprocessing/vbfgamma/keep_and_drop.txt', postfix=None, modules=[Skimmer2016, puAutoWeight_2016, photonSFFall17V2_2017_Tight,photonSFFall17V2_2016_Tight ], noOut=False, prefetch=False, justcount=False, firstEntry=0, jsonInput=None, longTermCache=False, friend=False )
p.run()

print "DONE"

