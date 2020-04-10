import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhotonSelector import *
from JetSelector import *
from AJJEvent import *

class Skimmer(Module):
    def __init__(self , isSignal , isData , era):
        self.isSignal = isSignal
        self.isData = isData
        self.era = era
        
        self.PhotonSelector = PhotonSelector(era)
        self.JetSelector = JetSelector(era)
        self.AJJ = AJJEvent()
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ROOT.gROOT.ProcessLine(".L {0}/EventShapeVariables.cc++".format(current_dir))
        
        pass
    
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        self.hTotalEvents = ROOT.TH1F( "hTotalNEvents" , "" , 10 , 0 , 10 );
        
        self.out = wrappedOutputTree
        self.out.branch("VBFGamma_evcats",  "I" , 2)
        self.out.branch("VBFGamma_wgt", "F" )
        self.PhotonSelector.MakeBranches( self.out )
        self.JetSelector.MakeBranches( self.out )
        self.AJJ.MakeBranches( self.out )
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        self.hTotalEvents.Write()
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        wgt = 1
        if hasattr(event,'Generator_weight') and event.Generator_weight < 0:
            wgt = -1
        self.hTotalEvents.Fill(0.5 , wgt)
        evcats = []
        if self.era==2016:
            evcats.append( event.HLT_Photon175 )
            evcats.append( event.HLT_Photon75_R9Id90_HE10_Iso40_EBOnly_VBF )
        elif self.era==2017:
            if hasattr( event , 'HLT_Photon200' ):
                evcats.append( event.HLT_Photon200 )
            else:
                evcats.append( -1 )

            if hasattr( event , 'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3' ):
                evcats.append( event.HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3 )
            else:
                evcats.append( -1 )
        elif self.era==2018:
            if hasattr( event , 'HLT_Photon200' ):
                evcats.append( event.HLT_Photon200 )
            else:
                evcats.append( -1 )

            if hasattr( event , 'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3' ):
                evcats.append( event.HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3 )
            else:
                evcats.append( -1 )

        self.out.fillBranch( "VBFGamma_evcats" , evcats )

        if not evcats[0] and not evcats[1]:
            return False
        self.hTotalEvents.Fill(1.5 , wgt)
        
        all_electrons = Collection(event, "Electron")
        all_muons = Collection(event, "Muon")
        all_photons = Collection(event, "Photon")
        photons = self.PhotonSelector( all_photons , all_electrons , all_muons )
        if len(photons)==0 :
            return False
        self.hTotalEvents.Fill(2.5 , wgt)
        self.PhotonSelector.FillBranches()


        selObjs = self.PhotonSelector.Leptons
        selObjs.append( all_photons[ photons[0] ] )
        all_jets = Collection(event, "Jet")
        if len(all_jets) < 2:
            return False
        self.hTotalEvents.Fill(3.5 , wgt)
        jets = self.JetSelector( all_jets , selObjs )
        if not self.JetSelector.Pass :
            return False
        self.hTotalEvents.Fill(4.5 , wgt)
        self.out.fillBranch( "VBFGamma_wgt" , wgt )
        self.JetSelector.FillBranches()
        self.AJJ.FillBranches( all_photons[ photons[0] ].p4() , self.JetSelector.LeadingJet.p4() , self.JetSelector.SubLeadingJet.p4() )
        return True
        


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
Skimmer2016 = lambda : Skimmer(False, True , 2016) 
Skimmer2017 = lambda : Skimmer(False, True , 2017) 
Skimmer2018 = lambda : Skimmer(False, True , 2018) 
