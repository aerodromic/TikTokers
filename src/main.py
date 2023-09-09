import pandas as pd
from ad_scorer import compute_risk_scores
from preprocessing import clean_ads
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from simulator import simulate

path = "./data/data.xlsx"
ads_table = pd.read_excel(path, sheet_name = 0, header = 1)
mod_table = pd.read_excel(path, sheet_name = 1)

ads_table = clean_ads(ads_table)

print(ads_table.describe())
print(ads_table.head())

scaler_ads = StandardScaler()
X_ads = scaler_ads.fit_transform(
    ads_table.drop(columns=['delivery_country', 'queue_market', 'ad_id']).values)

best_loss = -float('inf')  # or -float('inf') if you're maximizing
best_gmm = None
tolerance = 1e-5
max_iterations = 10000
previous_loss = best_loss
n_components = 3 # use if using GaussianMixture instead of BayesianGaussianMixture

for _ in range(max_iterations):
    gmm = GaussianMixture(n_components=n_components)
    gmm.fit(X_ads)

    current_risk_scores = compute_risk_scores(X_ads, gmm)
    X_ads['risk_score'] = current_risk_scores
    current_loss = simulate(X_ads)

    if abs(current_loss - previous_loss) < tolerance:
        break

    if current_loss > best_loss:  # Use > if you're maximizing the loss
        best_loss = current_loss
        best_gmm = gmm

    previous_loss = current_loss

# best_gmm now contains the model with the lowest observed loss
final_risk_scores = compute_risk_scores(X_ads, best_gmm)
X_ads['risk_score'] = final_risk_scores