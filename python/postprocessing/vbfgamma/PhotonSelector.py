class PhotonSelector:
    def __init__(self):
        self.Leptons = []
        pass

    def __call__(self, photons , electrons , muons):
        del self.Leptons[:]
        self.SelectElectrons(electrons)
        self.SelectMuons(muons)
        
        self.indices = []
        for i in range(len(photons)):
            ph = photons[i]
            if self.SelectPhoton( ph , 75 , 2.4 ):
                self.indices.append( i )

        return self.indices
        
    def SelectPhoton(self , photon , min_pt , max_eta ):
        ele_veto = photon.electronVeto
        tight_cutbased17v1 = photon.cutBased17Bitmap==7
        has_pixelseed = photon.pixelSeed
        pt_cut = photon.pt > min_pt
        eta_cut = abs( photon.eta ) < max_eta

        min_dr = float('inf')
        for lep in self.Leptons:
            dr = lep.DeltaR( photon )
            if min_dr > dr:
                min_dr = dr

        return ele_veto and tight_cutbased17v1 and has_pixelseed and pt_cut and eta_cut and min_dr > 0.4
        

    def SelectElectrons(self, electrons):
        for ele in electrons:
            if ele.pt > 20 and abs(ele.eta) < 2.5 and ele.mvaFall17V2Iso_WP80 :
                self.Leptons.append( ele )

    def SelectMuons(self, muons):
        for mu in muons:
            if mu.pt > 20 and abs(mu.eta) < 2.5 and mu.mediumId :
                self.Leptons.append( mu )

    def FillBranches(self):
        self.out.fillBranch( "VBFGamma_gamma_index" , self.indices[0] )
                
    def MakeBranches(self, out):
        self.out = out
        self.out.branch("VBFGamma_gamma_index", "I")
