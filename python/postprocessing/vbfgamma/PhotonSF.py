import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def GetFileAddress(File):
    if "CMSSW_BASE" in os.environ:
        return "{0}/src/PhysicsTools/NanoAODTools/{1}".format( os.environ['CMSSW_BASE'] , File )
    else:
        return "{0}/{1}".format( os.environ['NANOAODTOOLS_BASE'] , File )
    

class PhotonSF:
    def __init__(self , File , nBranch):
        self.fName = GetFileAddress( File )
        self.BranchName = nBranch
        pass
    
    def beginJob(self):
        self.File = ROOT.TFile.Open( self.fName )
        self.Histo = self.File.Get("EGamma_SF2D")
        pass
    def endJob(self):
        self.File.Close()
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("VBFGamma_{0}".format(self.BranchName) ,  "F" )
        self.out.branch("VBFGamma_{0}_Uncert".format(self.BranchName) ,  "F" )
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        if hasattr( event , "VBFGamma_gamma_index" ):
            ph_index = event.VBFGamma_gamma_index
            all_photons = Collection(event, "Photon")
            ph_pt = all_photons[ ph_index ].pt
            ph_eta = all_photons[ ph_index ].eta

            ph_bin = self.Histo.FindBin( ph_eta , ph_pt )
            sf = self.Histo.GetBinContent( ph_bin )
            sf_err = self.Histo.GetBinError( ph_bin )
            self.out.fillBranch("VBFGamma_{0}".format(self.BranchName) ,  sf )
            self.out.fillBranch("VBFGamma_{0}_Uncert".format(self.BranchName) ,  sf_err )
            
        return True
        

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
photonSFFall17V2_2016_Tight = lambda : PhotonSF( "python/postprocessing/data/photonSF/Fall17V2_2016_Tight_photons.root" , "Fall17V2_2016_Tight_SF" )
photonSFFall17V2_2017_Tight = lambda : PhotonSF( "python/postprocessing/data/photonSF/Fall17V2_2017_Tight_photons.root" , "Fall17V2_2017_Tight_SF" )
photonSFFall17V2_2018_Tight = lambda : PhotonSF( "python/postprocessing/data/photonSF/Fall17V2_2018_Tight_photons.root" , "Fall17V2_2018_Tight_SF" )
