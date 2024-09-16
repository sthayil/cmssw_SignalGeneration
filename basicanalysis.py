from ROOT import *
from DataFormats.FWLite import Events, Handle
import glob, sys

#inputfiles=glob.glob("/eos/uscms/store/user/huiwang/ElectroWeakino/miniAOD_test/mini_mn1_300_mx1_310_*.root")
#inputfiles=glob.glob("/eos/uscms/store/user/lpcrutgers/sthayil/pseudoaxions/ttPhiPS_M-1000/mini*_0.root")

inputfiles=[]
for i in range(int(sys.argv[1])*10,int(sys.argv[1])*10 +10):
    inputfile = "/eos/uscms/store/user/lpcrutgers/sthayil/pseudoaxions/ttPhiPS_M-"+sys.argv[2]+"/miniAOD_"+str(i)+".root"
    inputfiles.append(inputfile)
print inputfiles
# create handle outside of loop
handle1  = Handle ('vector<reco::GenJet>')
label1 = ("slimmedGenJets")
handle2  = Handle ('vector<pat::Jet>')
label2 = ("slimmedJetsPuppi")
handle3  = Handle ('edm::TriggerResults')
#label3 = ("TriggerResults")
label3 = ("TriggerResults", "", "HLT")

handle  = Handle ('vector<reco::GenParticle>')
label = ("prunedGenParticles")
#label = ("genParticles")

outputfile = "mini_hist_"+sys.argv[2]+"_"+sys.argv[1]+".root"
out_file = TFile(outputfile, 'recreate')

leptons = [11, 13]

hist_mothermass = TH1D('h_mothermass','h_mothermass',100,0,5)
hist_numleptons  = TH1F('hist_numleptons','numleptons',20,0,20)
hist_numjets     = TH1F('hist_numjets','numjets',30,0,30)
hist_leptonpt       = TH1F('hist_leptonpt','leptonpt',30,0,300)
hist_jetpt          = TH1F('hist_jetpt','jetpt',100,0,1000)
hist_eventht        = TH1F('hist_eventht','eventht',300,0,3000)

# hist_numjets_PF     = TH1F('hist_numjets_PF','numjets_PF',30,0,30)
# hist_jetpt_PF          = TH1F('hist_jetpt_PF','jetpt_PF',100,0,1000)
# hist_eventht_PF        = TH1F('hist_eventht_PF','eventht_PF',300,0,3000)
# hist_eventhtonlyjets        = TH1F('hist_eventhtonlyjets','eventhtonlyjets',300,0,3000)
# hist_eventhtonlyjets_PF        = TH1F('hist_eventhtonlyjets_PF','eventhtonlyjets_PF',300,0,3000)
# hist_leptoniso   = TH1F('hist_leptoniso','leptoniso_deltar',150,0,15)
# hist_HLT_Ele15_IsoVVVL_PFHT450   = TH1F('hist_HLT_Ele15_IsoVVVL_PFHT450','hist_HLT_Ele15_IsoVVVL_PFHT450',2,0,2)
# hist_HLT_Mu15_IsoVVVL_PFHT450   = TH1F('hist_HLT_Mu15_IsoVVVL_PFHT450','hist_HLT_Mu15_IsoVVVL_PFHT450',2,0,2)
# hist_HLT_PFHT1050   = TH1F('hist_HLT_PFHT1050','hist_HLT_PFHT1050',2,0,2)

count=0

for inputfile in inputfiles:
    events = Events (inputfile)
    print inputfile

    # loop over events
    cnt=0
    for event in events:

        numlep=0
        numjets=0
        visE=0
        visEonlyjets=0
        numjets_PF=0
        visE_PF=0
        visEonlyjets_PF=0
 
        # event.getByLabel(label3, handle3)
        # triggerResults = handle3.product()
        # #for trigger in triggerResults.getTriggerNames():
        # #    print trigger
        # names = event.object().triggerNames(triggerResults)
        # for i in xrange(triggerResults.size()):
        # #if cnt == 0: print names.triggerName(i)
        #     if "HLT_PFHT1050_v" in names.triggerName(i): hist_HLT_PFHT1050.Fill(triggerResults.accept(i))
        #     if "HLT_Mu15_IsoVVVL_PFHT450_v" in names.triggerName(i): hist_HLT_Mu15_IsoVVVL_PFHT450.Fill(triggerResults.accept(i))
        #     if "HLT_Ele15_IsoVVVL_PFHT450_v" in names.triggerName(i): hist_HLT_Ele15_IsoVVVL_PFHT450.Fill(triggerResults.accept(i))

        event.getByLabel(label, handle)
        genparticles = handle.product()
    
        for particle in genparticles:
            #if ( particle.statusFlags().fromHardProcess()==1 ):
            if abs(particle.pdgId()) in [54] and particle.status()==23: 
                hist_mothermass.Fill( particle.mass() )

            if particle.status() == 1: #if stable

                    if abs(particle.pdgId()) in leptons:
                        if particle.pt()>3:
                            numlep+=1
                            hist_leptonpt.Fill(particle.pt())

                            # conept=0
                            # isolation=0
                            # pvec = TLorentzVector()
                            # pvec.SetPtEtaPhiM(particle.pt(), particle.eta(), particle.phi(), particle.mass())
                            # for oparticle in genparticles:
                            #     if oparticle.status() == 1:
                            #         opvec = TLorentzVector()
                            #         opvec.SetPtEtaPhiM(oparticle.pt(), oparticle.eta(), oparticle.phi(), oparticle.mass())
                            #         deltar = pvec.DeltaR(opvec)
                            #         if deltar < 0.3 and deltar > 0:
                            #             conept+=oparticle.pt()
                            # isolation = conept / particle.pt()
                            # hist_leptoniso.Fill(isolation)

                            visE+=(particle.pt())

        event.getByLabel(label1, handle1)
        genjets = handle1.product()
    
        for jet in genjets:
            if jet.pt()>30 and abs(jet.eta())<2.5:
                numjets+=1
                visE+=jet.pt()
                visEonlyjets+=jet.pt()
                hist_jetpt.Fill(jet.pt())

        # event.getByLabel(label2, handle2)
        # PFjets = handle2.product()
    
        # for jet in PFjets:
        #     if jet.pt()>30 and abs(jet.eta())<2.5:
        #         numjets_PF+=1
        #         visE_PF+=jet.pt()
        #         visEonlyjets_PF+=jet.pt()
        #         hist_jetpt_PF.Fill(jet.pt())

        hist_numleptons.Fill(numlep)
        hist_numjets.Fill(numjets)
        hist_eventht.Fill(visE)
        # hist_eventhtonlyjets.Fill(visEonlyjets)
        # hist_numjets_PF.Fill(numjets_PF)
        # hist_eventht_PF.Fill(visE_PF)
        # hist_eventhtonlyjets_PF.Fill(visEonlyjets_PF)

        cnt+=1

out_file.cd()
out_file.Write()
out_file.Close()
