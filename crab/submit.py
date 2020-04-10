import getpass
import sys
import os
import glob
import datetime
inputfile = sys.argv[1]
action = sys.argv[2]
f = open(inputfile)
for sample in f.readlines():
    job_ = sample.split('/')
    if job_[1] in ['SinglePhoton' , 'EGamma']:
        job = job_[1] + "_" + job_[2]
    else:
        job = job_[1]
        if 'ext' in job_[2]:
            ext_index = job_[2].find( 'ext' )
            job += '_' + job_[2][ ext_index:ext_index+4 ]
        if 'backup' in job_[2]:
            job += '_backup'
    if True: #any( [ s in job for s in ['SinglePhoton_Run2017F'] ] ): #['ext' , 'backup' , 'amcatnlo' , 'INT'] ] ):
        if action=='print':
            print( 'sample {0} and job name is {1}'.format( sample[0:-1] , job ) )
        if action=='submit':
            print('crab submit --proxy=/tmp/x509up_u12330 --config=crab_cfg.py General.requestName={1} Data.inputDataset={0} General.workArea=SMP19005April9_2017;'.format( sample[0:-1] , job ) )
        elif action=='dasquery':
            print("dasgoclient -query='site dataset={0}';".format(sample[0:-1]) )
        elif action=='status':
            directory = sys.argv[3]
            print('crab status --proxy=/tmp/x509up_u12330 {0}/crab_{1};'.format( directory , job ) )
        elif action=='hadd':
            logdir = sys.argv[3]
            eosdir = sys.argv[4]
            outdir = sys.argv[5]

            directory_name = eosdir.split('/')[-1]
            if directory_name == '' : directory_name = eosdir.split('/')[-2]
            outdir += '/' + directory_name + '/'
            if not os.path.exists( outdir ):
                os.mkdir( outdir )
            outfilename = outdir + job + '.root'

            jobtime = ''
            if not os.path.exists( '{0}/crab_{1}/.requestcache'.format( logdir , job ) ):
                print( 'echo "Job {0}/crab_{1} doesnt exist, it is skipped";'.format( logdir , job ) )
                continue
            with  open('{0}/crab_{1}/.requestcache'.format( logdir , job ) ) as f:
                for line in f:
                    if '{0}_crab'.format(getpass.getuser()) in line:
                        jobtime = line[1:14]
            D, T = jobtime.split('_')
            date = datetime.datetime( int(D[:2])+2000 , int(D[2:4]) , int(D[4:]) , int(T[:2]) , int(T[2:4]) , int(T[4:]) )

            all_rootfiles = glob.glob( "{0}/{1}/crab_{2}/{3}/*/*.root".format( eosdir , job_[1] , job , jobtime ) )
            print( 'hadd {0} {1};'.format( outfilename , ' '.join( all_rootfiles ) ) )
            print( 'touch -c -t {0:%y%m%d%H%M.%S} {1};'.format( date , outfilename ) )
            
