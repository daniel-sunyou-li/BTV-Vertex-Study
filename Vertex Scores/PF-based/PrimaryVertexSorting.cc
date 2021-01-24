#include "fastjet/PseudoJet.hh"
#include "FWCore/Utilities/interface/isFinite.h"

using namespace fastjet;
using namespace std;


float PrimaryVertexSorting::score(const reco::Vertex & pv,const  std::vector<const reco::Candidate *> & cands, bool useMet, float arr[] ) const {
  typedef math::XYZTLorentzVector LorentzVector;
  float sumPt2=0;
  float sumPt2_jet=0;
  float sumPt2_lep=0;
  float sumPt2_met=0;
  float sumEt=0;
  LorentzVector met;
  std::vector<fastjet::PseudoJet> fjInputs_;
  fjInputs_.clear();
  size_t countScale0 = 0;
  for (size_t i = 0 ; i < cands.size(); i++) {
    const reco::Candidate * c= cands[i];
    float scale=1.;
    if(c->bestTrack() != nullptr)
      {
        if(c->pt()!=0) {
                 scale=(c->pt()-c->bestTrack()->ptError())/c->pt();
        }
        if(edm::isNotFinite(scale)) {
                edm::LogWarning("PrimaryVertexSorting") << "Scaling is NAN ignoring this candidate/track" << std::endl;
                scale=0;
        }
        if(scale<0){
          scale=0;
          countScale0++;
        }
      }

    int absId=abs(c->pdgId());
    if(absId==13 or absId == 11) {
      float pt =c->pt()*scale;
      sumPt2_lep+=pt*pt;
      sumPt2+=pt*pt;
      met+=c->p4()*scale;
      sumEt+=c->pt()*scale;
    } else {
      if (scale != 0){ // otherwise, what is the point to cluster zeroes
        fjInputs_.push_back(fastjet::PseudoJet(c->px()*scale,c->py()*scale,c->pz()*scale,c->p4().E()*scale));
        //      fjInputs_.back().set_user_index(i);
      }
    }
  }
  fastjet::ClusterSequence sequence( fjInputs_, JetDefinition(antikt_algorithm, 0.4));
  auto jets = fastjet::sorted_by_pt(sequence.inclusive_jets(0));
  for (const auto & pj : jets) {
    auto p4 = LorentzVector( pj.px(), pj.py(), pj.pz(), pj.e() ) ;
    sumPt2+=(p4.pt()*p4.pt())*0.8*0.8;
    sumPt2_jet+=(p4.pt()*p4.pt())*0.8*0.8;
    met+=p4;
    sumEt+=p4.pt();
  }
  float metAbove = met.pt() - 2*sqrt(sumEt);
  if(metAbove > 0 and useMet) {
    sumPt2_met+=metAbove*metAbove;
    sumPt2+=metAbove*metAbove;
  }
  if (countScale0 == cands.size()) sumPt2 = countScale0*0.01; //leave some epsilon value to sort vertices with unknown pt
  //cout << "Total: " << sumPt2 << ", Jet: " << sumPt2_jet << ", MET: " << sumPt2_met << ", Lepton: " << sumPt2_lep << endl;
  arr[0] = sumPt2;
  arr[1] = sumPt2_jet;
  arr[2] = sumPt2_met;
  arr[3] = sumPt2_lep;
  return sumPt2;
}
