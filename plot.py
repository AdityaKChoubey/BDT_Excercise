import ROOT
from array import array

ROOT.TMVA.Tools.Instance()

reader = ROOT.TMVA.Reader()

x1 = array('f',[0])
x2 = array('f',[0])
x3 = array('f',[0])
x4 = array('f',[0])

reader.AddVariable("x1",x1)
reader.AddVariable("x2",x2)
reader.AddVariable("x3",x3)
reader.AddVariable("x4",x4)

reader.BookMVA(
    "BDTG",
    "dataset/weights/TMVAClassification_BDTG.weights.xml"
)

# -------------------------------
# Load dataset
# -------------------------------

sig_file = ROOT.TFile.Open("signal.root")
bkg_file = ROOT.TFile.Open("background.root")

sig_tree = sig_file.Get("tree")
bkg_tree = bkg_file.Get("tree")

# -------------------------------
# Scatter plots
# -------------------------------

sig = ROOT.TGraph()
bkg = ROOT.TGraph()

for i,e in enumerate(sig_tree):
    sig.SetPoint(i,e.x1,e.x2)

for i,e in enumerate(bkg_tree):
    bkg.SetPoint(i,e.x1,e.x2)

sig.SetMarkerColor(ROOT.kRed)
bkg.SetMarkerColor(ROOT.kBlue)

sig.SetMarkerSize(0.6)
bkg.SetMarkerSize(0.6)

# -------------------------------
# Compute BDT boundary
# -------------------------------

N=200

xmin=-3
xmax=3
ymin=-3
ymax=3

h = ROOT.TH2F("h","BDT Boundary",N,xmin,xmax,N,ymin,ymax)

for i in range(N):
    for j in range(N):

        x = xmin + (xmax-xmin)*i/N
        y = ymin + (ymax-ymin)*j/N

        x1[0]=x
        x2[0]=y
        x3[0]=0
        x4[0]=x*y

        score = reader.EvaluateMVA("BDTG")

        h.SetBinContent(i+1,j+1,score)

# -------------------------------
# Plot
# -------------------------------
c = ROOT.TCanvas("c","Boundary",1000,800)

# Wider axis range
frame = ROOT.TH2F(
    "frame","BDT Decision Boundary; x_{1}; x_{2}",
    10,-4,4,
    10,-4,4
)

frame.SetStats(0)
frame.Draw()

# Bigger scatter points
sig.SetMarkerStyle(20)
sig.SetMarkerColor(ROOT.kRed+1)
sig.SetMarkerSize(0.4)

bkg.SetMarkerStyle(20)
bkg.SetMarkerColor(ROOT.kBlue+1)
bkg.SetMarkerSize(0.4)

sig.Draw("P SAME")
bkg.Draw("P SAME")

# Bold decision boundary
h.SetContour(1)
h.SetContourLevel(0,0)

h.SetLineColor(ROOT.kBlack)
h.SetLineWidth(4)

h.Draw("CONT3 SAME")
leg = ROOT.TLegend(0.65,0.75,0.9,0.9)
leg.AddEntry(sig,"Signal","p")
leg.AddEntry(bkg,"Background","p")
leg.AddEntry(h,"BDT Boundary","l")

leg.Draw()

c.SaveAs("bdt_boundary_scatter.png")
