class JetSelector:
    def __init__(self):
        pass

    def __call__(self , jets , selected_objects ):
        self.SelectedObjs = selected_objects
        indices = []
        
        for i,jet in enumerate(jets):
            if self.SelectJet( jet , 20 , 4.7 ):
                indices.append( i )

        self.Pass = False
        if len(indices) > 1:
            jetindices_by_pt = sorted(  indices , key= lambda j : jets[j].pt , reverse=True)
            #print( [ jets[i].pt for i in indices] )
            self.LeadingJetIndex = jetindices_by_pt[0]
            self.SubLeadingJetIndex = jetindices_by_pt[1]
            
            self.LeadingJet = jets[ jetindices_by_pt[0] ]
            self.SubLeadingJet = jets[ jetindices_by_pt[1] ]
            self.JJ = self.LeadingJet.p4() + self.SubLeadingJet.p4()

            self.Pass = self.LeadingJet.pt > 50 and self.SubLeadingJet.pt > 40 and self.JJ.M() > 200 

            eta1 = self.LeadingJet.p4().Eta()
            eta2 = self.SubLeadingJet.p4().Eta()
            self.jj_deta=abs( eta1 - eta2 )
            self.jj_seta= eta1 + eta2
            self.jj_dphi= self.LeadingJet.p4().DeltaPhi( self.SubLeadingJet.p4() )
            if eta1*eta2 > 0:
                central_eta_max = min( abs(eta1) , abs(eta2) ) - 0.2
                central_eta_min = -1*central_eta_max
            else:
                central_eta_min = min( eta1 , eta2 ) + 0.2
                central_eta_max = max( eta1 , eta2 ) - 0.2
                
            self.nCentJets = 0
            self.CentralJetIndex = -1
            self.centj_ystar = -100
            for j in jetindices_by_pt[2:] :
                j_p4 = jets[j].p4()
                if central_eta_min < j_p4.Eta() < central_eta_max :
                    self.nCentJets+=1
                    if self.nCentJets == 1:
                        self.CentralJetIndex = j
                        #self.centj_pt   = j_p4.Pt();
                        self.centj_eta  = j_p4.Eta();
                        #self.centj_phi  = j_p4.Phi();
                        self.centj_ystar= self.centj_eta-0.5*(eta1+eta2);
                        
        return indices

    def SelectJet(self , jet , min_pt , max_eta):
        pt_cut = jet.pt > min_pt
        eta_cut = abs(jet.eta) < max_eta
        min_dr = float('inf')
        for obj in self.SelectedObjs:
            dr = obj.DeltaR( jet )
            if min_dr > dr:
                min_dr = dr
        loose_puid = bool( jet.puId & 4 ) or jet.pt > 50
        return pt_cut and eta_cut and min_dr > 0.4 and loose_puid


    def FillBranches(self):
        self.out.fillBranch("VBFGamma_LeadinJet_index", self.LeadingJetIndex )
        self.out.fillBranch("VBFGamma_SubLeadinJet_index", self.SubLeadingJetIndex )
        self.out.fillBranch("VBFGamma_JJ_M", self.JJ.M() )
        self.out.fillBranch("VBFGamma_JJ_Pt", self.JJ.Pt() )
        self.out.fillBranch("VBFGamma_JJ_ScalarSum", self.SubLeadingJet.p4().Pt()+self.LeadingJet.p4().Pt() )
        self.out.fillBranch("VBFGamma_JJ_Phi", self.JJ.Phi() )
        self.out.fillBranch("VBFGamma_JJ_Eta", self.JJ.Eta() )
        self.out.fillBranch("VBFGamma_JJ_DPhi", self.jj_dphi )
        self.out.fillBranch("VBFGamma_JJ_SEta", self.jj_seta )
        self.out.fillBranch("VBFGamma_JJ_DEta", self.jj_deta )
        self.out.fillBranch("VBFGamma_nCentJets", self.nCentJets )
        self.out.fillBranch("VBFGamma_CentJet_Index", self.CentralJetIndex )
        self.out.fillBranch("VBFGamma_CentJet_YStar", self.centj_ystar )
        
    def MakeBranches(self, out):
        self.out = out
        self.out.branch("VBFGamma_LeadinJet_index", "I" )
        self.out.branch("VBFGamma_SubLeadinJet_index", "I" )
        self.out.branch("VBFGamma_JJ_M", "F" )
        self.out.branch("VBFGamma_JJ_Pt", "F" )
        self.out.branch("VBFGamma_JJ_ScalarSum", "F" )
        self.out.branch("VBFGamma_JJ_Phi", "F" )
        self.out.branch("VBFGamma_JJ_Eta", "F" )
        self.out.branch("VBFGamma_JJ_DPhi", "F" )
        self.out.branch("VBFGamma_JJ_SEta", "F" )
        self.out.branch("VBFGamma_JJ_DEta", "F" )
        self.out.branch("VBFGamma_nCentJets", "I" )
        self.out.branch("VBFGamma_CentJet_Index", "I" )
        self.out.branch("VBFGamma_CentJet_YStar", "F" )
        
        
