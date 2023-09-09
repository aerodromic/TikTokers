# TikTokers
TikTok Hackathon 2023 - Team Submission - (1) Optimize Advertisement Moderation

## Biographies of Team Members

<b> Chia Lu Ting </b>
Lu Ting is a Year 3 Business & Computing student at NTU.  Lu Ting is a driven undergraduate exploring the tech world, with previous internship experiences in data science and machine learning. He is currently on track to get a specialisation in Artificial Intelligence for his Computing major.

<b> Estella Peh Cher Hwee </b>
Estella is a Year 3 Data Science & Analytics student at NUS, with a second major in Quantitative Finance. Estella’s skills in data analytics are well-developed, with involvement in various data science projects and internships as an undergraduate.

<b> Joel Lo Liang Ze </b>
Joel is a Year 3 Industrial & Systems Engineering student at NUS, with a double major in Data Analytics and a minor in Computer Science. Joel has a diverse work experience including a stint with Viettonkin Consulting in Hanoi, Vietnam, that has exposed him to data wrangling, data visualisation, machine learning and project management skills among other skills. 

<b> Kevin Pek Yue Ting </b>
Kevin is a Year 3 Data Science & Analytics student at NUS. Kevin has much software development experience under various companies through his undergraduate journey.

<b> Teo De Xuan Justin </b>
Justin is a Year 3 Business & Computing student at NTU. Justin is currently a Program Manager Intern with TikTok Trust & Safety.

## Inspiration
Chosen Problem: (1) Optimise Advertisement Moderation 

In carrying out our problem-solving, we split our solution into two broad halves and accompanying models to address (A) dynamic scoring and prioritisation of advertisements for review and (B) matching reviewed content to the best-fitting moderator.

In addition, we used simulation to observe and understand changes in the outputs with our models (i.e. risk scores, utilization) to choose the models that are most optimal for our solution.


## What it does

### Scripts:
main.py – main code section 
ad_scorer.py – function to compute ad risk scores
preprocessing.py – data preprocessing, feature engineering
simulator.py – monte carlo simulation in model 

### (A) Scoring of Advertisements
- Fit a Bayesian GMM (Gaussian Mixture Model) to the advertisement data, compute risk scores for each advertisement, select best GMM based on custom loss function
- GMM computes advertisement risk scores before moderation jobs are assigned to moderators

### (B) Matching Ads to Moderators
- Classify ads (jobs) into low,medium,high risk segments by risk score
- Classify moderators into lower,medium,higher capabilities by accuracy
- Match ad moderation jobs to moderators (risk score matched to moderator capabilities) based on critical factors (e.g. moderators’ markets, efficiency metrics, number of jobs a moderator has, present utilisation)

### (A/B) Discrete Time Simulation Modelling of the assigning of Advertisements to Moderators
- Model uses a multiple queue system that takes into account the capacity of each moderator
- Dispatcher (B) assigns moderators based on risk score from( A), country of delivery and the availability of the moderator

Overall outcome: assign workflows optimally to each moderator based on the two key objective functions which are minimising mean mismatch error and maximising the utilisation of moderators.


## How we built it
- Python libraries: Pandas, Numpy, Simpy, Statistics, Sklearn
- We have a 3 stage model: risk scoring model that feeds into our simulation model and a dispatcher model in the simulation model that allocates the advertisement for moderation.


## Challenges we ran into
- Understanding the moderation metrics, and how to incorporate them into our solution or use as benchmark, e.g. productivity %, utilization etc. 
- Refactoring and optimising our code, integrating separate parts of our code together
- Collaboration under heavy time pressure

## Accomplishments that we're proud of
- Overcoming the many above challenges to complete a working solution
- Putting together concepts that we have learnt in linear optimisation, operation research and simulation

## What we learned
- Understanding the considerations and challenges in advertisement moderation for TikTok
- Using different Python libraries e.g. SimPy, constraint matching etc. in crafting out our solution
- Having frequent discussions, syncs to keep pace with workflows, planning ahead and managing time well

## What's next for TikTokers
- Inspire creativity and enrich life
- Use simulation and mathematical modelling skills for future projects
