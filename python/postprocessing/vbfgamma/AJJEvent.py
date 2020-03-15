import ROOT

class AJJEvent:
    def __init__(self):
        pass

    def MakeBranches(self, out):
        self.out = out
        self.out.branch("VBFGamma_a_ystar", "F" )
        self.out.branch("VBFGamma_lead_dr2a", "F" )
        self.out.branch("VBFGamma_sublead_dr2a", "F" )
        self.out.branch("VBFGamma_jj_dr2a", "F" )
        self.out.branch("VBFGamma_ajj_pt", "F" )
        self.out.branch("VBFGamma_ajj_eta", "F" )
        self.out.branch("VBFGamma_ajj_phi", "F" )
        self.out.branch("VBFGamma_ajj_m", "F" )
        self.out.branch("VBFGamma_scalarht", "F" )
        self.out.branch("VBFGamma_mht", "F" )
        self.out.branch("VBFGamma_es_isotropy", "F" )
        self.out.branch("VBFGamma_es_circularity", "F" )
        self.out.branch("VBFGamma_es_sphericity", "F" )
        self.out.branch("VBFGamma_es_aplanarity", "F" )
        self.out.branch("VBFGamma_es_C", "F" )
        self.out.branch("VBFGamma_es_D", "F" )


    def FillBranches(self, A , J1 , J2 ):
        self.out.fillBranch("VBFGamma_a_ystar", A.Eta()-0.5*( J1.Eta()+J2.Eta()) )
        self.out.fillBranch("VBFGamma_lead_dr2a", A.DeltaR( J1 ) )
        self.out.fillBranch("VBFGamma_sublead_dr2a", A.DeltaR(J2) )
        self.out.fillBranch("VBFGamma_jj_dr2a", A.DeltaR( J1+J2 ) )

        AJJ = A + J1 + J2
        self.out.fillBranch("VBFGamma_ajj_pt", AJJ.Pt() )
        self.out.fillBranch("VBFGamma_ajj_eta", AJJ.Eta() )
        self.out.fillBranch("VBFGamma_ajj_phi", AJJ.Phi() )
        self.out.fillBranch("VBFGamma_ajj_m", AJJ.M() )
        self.out.fillBranch("VBFGamma_scalarht", A.Pt()+J1.Pt()+J2.Pt() )
        self.out.fillBranch("VBFGamma_mht", 0 )

        eventShape = ROOT.EventShapeVariables()
        eventShape.addObject( A )
        eventShape.addObject( J1 )
        eventShape.addObject( J2 )
        self.out.fillBranch("VBFGamma_es_isotropy", eventShape.isotropy() )
        self.out.fillBranch("VBFGamma_es_circularity", eventShape.circularity() )
        self.out.fillBranch("VBFGamma_es_sphericity", eventShape.sphericity() )
        self.out.fillBranch("VBFGamma_es_aplanarity", eventShape.aplanarity() )
        self.out.fillBranch("VBFGamma_es_C", eventShape.C() )
        self.out.fillBranch("VBFGamma_es_D", eventShape.D() )
        del eventShape
        
