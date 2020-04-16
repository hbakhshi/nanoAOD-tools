import getpass
import sys
import os
import glob
import datetime
import json
inputfile = sys.argv[1]
action = sys.argv[2]
year = inputfile.split('.')[0][-4:]
f = open(inputfile)

def GetJobStatus( logdir , job ):
    Failed = []
    Finished = []
    Others = []
    nTotal = 0
    if not os.path.exists( '{0}/crab_{1}/status.json'.format( logdir , job )  ):
        return -10,-1,Failed,Finished,Others
    with open('{0}/crab_{1}/status.json'.format( logdir , job ) ) as f:
        try:
            js = json.load( f )
        except ValueError as ve:
            return -20,-1,Failed,Finished,Others
        for job in js:
            nTotal += 1
            if js[job]['State'] == 'failed':
                Failed.append( job )
            elif js[job]['State'] == 'finished':
                Finished.append( int(job) )
            else:
                Others.append( job )
    Failed.sort()
    Finished.sort()
    Others.sort()

    if len(Others)==0 and len(Failed) == 0:
        return 1,0,Failed,Finished,Others
    elif len(Others)==0:
        return 0,(1.0*len(Failed))/nTotal,Failed,Finished,Others
    else:
        return 2,(1.0*len(Failed))/nTotal,Failed,Finished,Others

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
        if action=='resubmit':
            directory = sys.argv[3]
            stat,ratio,failds,finishds,others = GetJobStatus( directory , job )
            if stat==1:
                continue
            if stat > -1 and len(failds)>0:
                print( 'crab resubmit --proxy=/tmp/x509up_u12330 --dir={0}/crab_{1} --jobids={2};'.format( directory , job , ','.join(failds) ) )
            else:
                print( 'crab resubmit --proxy=/tmp/x509up_u12330 --dir={0}/crab_{1};'.format( directory , job  ) )
        if action=='submit':
            dirname = sys.argv[3]
            print('mkdir -p {0}_{1};'.format(dirname , year) )
            print('crab submit --proxy=/tmp/x509up_u12330 --config=crab_cfg.py General.requestName={1} Data.inputDataset={0} General.workArea={3}_{2};'.format( sample[0:-1] , job , year , dirname) )
        elif action=='dasquery':
            #print("dasgoclient -query='site dataset={0}';".format(sample[0:-1]) )
            newsamplename = sample[0:-1].replace( 'Nano25Oct2019_102X_mcRun2' , '*02Apr2020*')
            print("dasgoclient -query='dataset={0}';".format(newsamplename) )
        elif action=='simplestatus':
            directory = sys.argv[3]
            print('crab status --proxy=/tmp/x509up_u12330 {0}/crab_{1};'.format( directory , job ) )        
        elif action=='kill':
            directory = sys.argv[3]
            print('crab kill --proxy=/tmp/x509up_u12330 --dir={0}/crab_{1};'.format( directory , job ) )        
            print('crab purge --proxy=/tmp/x509up_u12330 --dir={0}/crab_{1};'.format( directory , job ) )        
        elif action=='status':
            directory = sys.argv[3]
            print('crab status --json --proxy=/tmp/x509up_u12330 {0}/crab_{1}  | grep \'"1":\' > {0}/crab_{1}/status.json ;'.format( directory , job ) )        
        elif action=='printstatus':
            directory = sys.argv[3]
            print( "{0}/crab_{1}/status.json".format( directory, job ) )
            stat,ratio,failds,finishds,others = GetJobStatus( directory , job )
            if stat==1:
                continue
            print( 'job {0} status is {1},{2:.1f}%'.format( job , stat , ratio*100 ) )
            if stat != 1 :
                print ('\tList of failed jobs: {0}'.format( str( failds ) ) )
                print ('\tList of other jobs: {0}'.format( str( others ) ) )

        elif action=='hadd':
            logdir = sys.argv[3]
            eosdir = sys.argv[4]
            outdir = sys.argv[5]

            directory_name = eosdir.split('/')[-1]
            if directory_name == '' : directory_name = eosdir.split('/')[-2]
            outdir += '/' + directory_name + '/'
            if not os.path.exists( outdir ):
                os.mkdir( outdir )
            outdir += '/' + str(year) + '/'
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

            stat,ratio,failds,finishds,others = GetJobStatus( logdir , job )

            all_rootfiles = glob.glob( "{0}/{1}/crab_{2}/{3}/*/*.root".format( eosdir , job_[1] , job , jobtime ) )
            mvdir = '{0}/{1}/crab_{2}/{3}/moved/'.format( eosdir , job_[1] , job , jobtime )
            all_movedfiles = glob.glob( "{0}/*.root".format( mvdir ) )
            file_ids = sorted( [ int(i.split('.')[0].split('_')[-1]) for i in all_rootfiles ] )
            for movedfile in all_movedfiles:
                id = int(movedfile.split('.')[0].split('_')[-1])
                if id in file_ids:
                    print( 'mv {0} {0}_wrong;'.format( movedfile ) )
                else:
                    all_rootfiles.append( movedfile )
                    file_ids.append( id )
            import ROOT
            all_fine_rootfiles = []
            for fname in all_rootfiles:
                try:
                    f = ROOT.TFile.Open( fname )
                    if f:
                        all_fine_rootfiles.append( fname ) 
                except :
                    print( "echo {0} is currpted;".format( fname ) )
            if not file_ids == finishds:
                print( 'echo There are some mismatch in finished jobs for {0}/crab_{1}:;'.format( logdir , job ) )
                print( 'echo {0};'.format( str( file_ids ) ) )
                print( 'echo {0};'.format( str( finishds ) ) )

            print( 'rm -f {0};'.format( outfilename ) )
            print( 'haddnano.py {0} {1};'.format( outfilename , ' '.join( all_fine_rootfiles ) ) )
            print( 'touch -c -t {0:%y%m%d%H%M.%S} {1};'.format( date , outfilename ) )
            print( 'mkdir -p {0};'.format( mvdir ) )
            print( 'mv {0} {1};'.format( ' '.join( all_fine_rootfiles) , mvdir  ) )

