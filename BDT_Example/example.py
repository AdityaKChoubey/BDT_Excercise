import ROOT
import numpy as np

ROOT.TMVA.Tools.Instance()

# ------------------------------------------------
# Create signal file
# ------------------------------------------------
sig_file = ROOT.TFile("signal.root","RECREATE")
sig_tree = ROOT.TTree("tree","signal")

x1 = np.zeros(1,dtype=float)
x2 = np.zeros(1,dtype=float)
x3 = np.zeros(1,dtype=float)
x4 = np.zeros(1,dtype=float)

sig_tree.Branch("x1",x1,"x1/D")
sig_tree.Branch("x2",x2,"x2/D")
sig_tree.Branch("x3",x3,"x3/D")
sig_tree.Branch("x4",x4,"x4/D")

N = 10000

# ---------------------------
# SIGNAL
# ---------------------------

for i in range(N):

    r = np.random.uniform(0,1.5)
    theta = np.random.uniform(0,2*np.pi)

    noise = np.random.normal(0,0.25)

    x1[0] = (r+noise)*np.cos(theta)
    x2[0] = (r+noise)*np.sin(theta)

    x3[0] = np.random.normal(0,1)
    x4[0] = x1[0]*x2[0] + np.random.normal(0,0.5)

    sig_tree.Fill()



sig_tree.Write()
sig_file.Close()


# ------------------------------------------------
# Create background file
# ------------------------------------------------
bkg_file = ROOT.TFile("background.root","RECREATE")
bkg_tree = ROOT.TTree("tree","background")

bkg_tree.Branch("x1",x1,"x1/D")
bkg_tree.Branch("x2",x2,"x2/D")
bkg_tree.Branch("x3",x3,"x3/D")
bkg_tree.Branch("x4",x4,"x4/D")

# ---------------------------
# BACKGROUND
# ---------------------------

for i in range(N):

    r = np.random.uniform(1.5,2.5)
    theta = np.random.uniform(0,2*np.pi)

    noise = np.random.normal(0,0.25)

    x1[0] = (r+noise)*np.cos(theta)
    x2[0] = (r+noise)*np.sin(theta)

    x3[0] = np.random.normal(0,1)
    x4[0] = x1[0]*x2[0] + np.random.normal(0,0.5)

    bkg_tree.Fill()
bkg_tree.Write()
bkg_file.Close()

print("Toy dataset created.")


# ------------------------------------------------
# Reopen files (important for PyROOT)
# ------------------------------------------------
sig_file = ROOT.TFile.Open("signal.root")
bkg_file = ROOT.TFile.Open("background.root")

sig_tree = sig_file.Get("tree")
bkg_tree = bkg_file.Get("tree")

print("Signal entries:", sig_tree.GetEntries())
print("Background entries:", bkg_tree.GetEntries())


# ------------------------------------------------
# TMVA setup
# ------------------------------------------------
output = ROOT.TFile("tmva.root","RECREATE")

factory = ROOT.TMVA.Factory(
    "TMVAClassification",
    output,
    "!V:Color:DrawProgressBar:AnalysisType=Classification"
)

loader = ROOT.TMVA.DataLoader("dataset")

loader.AddVariable("x1","F")
loader.AddVariable("x2","F")
loader.AddVariable("x3","F")
loader.AddVariable("x4","F")

loader.AddSignalTree(sig_tree,1.0)
loader.AddBackgroundTree(bkg_tree,1.0)

loader.PrepareTrainingAndTestTree(
    ROOT.TCut(""),
    "SplitMode=Random:NormMode=NumEvents:!V"
)


# ------------------------------------------------
# Fisher
# ------------------------------------------------
factory.BookMethod(
    loader,
    ROOT.TMVA.Types.kFisher,
    "Fisher",
    "!H:!V"
)


# ------------------------------------------------
# Gradient Boosted Decision Tree
# ------------------------------------------------
factory.BookMethod(
    loader,
    ROOT.TMVA.Types.kBDT,
    "BDTG",
    "!H:!V:"
    "NTrees=1000:"
    "MaxDepth=5:"
    "BoostType=Grad:"
    "Shrinkage=0.05:"
    "UseBaggedBoost:"
    "BaggedSampleFraction=0.5:"
    "SeparationType=GiniIndex:"
    "nCuts=20"
)


factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()

print("TMVA training finished.")
