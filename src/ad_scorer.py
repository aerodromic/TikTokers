import numpy as np

def compute_risk_scores(X, gmm):
    responsibilities = gmm.predict_proba(X)
    risk_scores = np.max(responsibilities, axis=1)
    return risk_scores