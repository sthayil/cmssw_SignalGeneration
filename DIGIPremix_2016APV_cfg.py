# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016_HIPM --filein file:SIM_2016APV.root --fileout file:DIGIPremix_2016APV.root --python_filename DIGIPremix_2016APV_cfg.py -n 1
import FWCore.ParameterSet.Config as cms
import random, os
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ("python")
options.register("inputFile", "file:SIM.root", VarParsing.multiplicity.singleton, VarParsing.varType.string, "")
options.register("numEvents", -1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "")
options.setDefault("outputFile", "file:DIGIPremix.root")
options.parseArguments()
from Configuration.Eras.Era_Run2_2016_HIPM_cff import Run2_2016_HIPM
from Configuration.ProcessModifiers.premix_stage2_cff import premix_stage2

process = cms.Process('DIGI2RAW',Run2_2016_HIPM,premix_stage2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.DigiDM_cff')
process.load('Configuration.StandardSequences.DataMixerPreMix_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorDM_cff')
process.load('Configuration.StandardSequences.DigiToRawDM_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.numEvents)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(options.inputFile),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.PREMIXRAWoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = process.PREMIXRAWEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
f=open("RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1.list", "r")
PU_files = f.readlines()
f.close()
PU_file = random.choice(PU_files)

# Other statements
process.mixData.input.fileNames = cms.untracked.vstring(['file:root://cmsxrootd.fnal.gov/'+PU_file])
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_preVFP_v8', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi)
process.datamixing_step = cms.Path(process.pdatamix)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.PREMIXRAWoutput_step = cms.EndPath(process.PREMIXRAWoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.datamixing_step,process.L1simulation_step,process.digi2raw_step,process.endjob_step,process.PREMIXRAWoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# #Setup FWK for multithreaded
# process.options.numberOfThreads=cms.untracked.uint32(8)
# process.options.numberOfStreams=cms.untracked.uint32(0)
# process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
