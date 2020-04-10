import ROOT
import os
import sys

for root, dirs, files in os.walk( sys.argv[1] ):
    printed = False
    for f in files:        
        if '.root' in f:
            f_o = ROOT.TFile.Open( root + '/' + f )

            hist = f_o.Get('hTotalNEvents')
            nSelectedHist = hist.GetBinContent( 5 )

            events = f_o.Get('Events')
            nSelectedTree = events.GetEntries()

            if nSelectedTree != nSelectedHist :
                if not printed:
                    print( '{0}:'.format( root.split('/')[-3] ) )
                    printed = True
                print( "\t{0}: {1} in histo and {2} in tree".format(  f , nSelectedHist , nSelectedTree ) )

            f_o.Close()
