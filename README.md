# Zomato KPT Optimization Architecture 🚀

**Developed by:** Parth Sharma

An advanced Python-based Data Engineering and ETL pipeline designed to de-noise Kitchen Prep Time (KPT) signals, eliminate human behavioral bias, and establish mathematical ground truth for food delivery networks[cite: 1].

## 📖 Project Overview
At Zomato, the KPT model dictates delivery logistics by predicting when food will be ready. However, the model historically trained on contaminated labels—specifically, the manual "Food Order Ready" (FOR) signals marked by merchants on the Zomato Merchant Experience (Mx) app[cite: 1]. Instead of tuning machine learning hyperparameters, this project introduces a robust, upstream ETL pipeline to sanitize input signals and dynamically capture offline kitchen friction before the data ever reaches the predictive engine[cite: 1]. 

## 🚨 The Core Business Problem
The underlying issue was "Garbage In, Garbage Out" driven by offline blind spots and human bias[cite: 1]. The legacy manual KPT signal was flawed due to:
* **Rider-Influenced Marking:** Merchants often press "Food Ready" only when the rider arrives to avoid algorithm penalties, causing the system to learn inaccurate prep patterns[cite: 1].
* **Hidden Offline Workload:** The model only saw active Zomato queues, remaining completely blind to offline friction like dine-in rushes, walk-ins, and competitor app orders[cite: 1].
* **Human Behavior Bias:** Inconsistent merchant discipline resulted in bulk-marking, forgetting to mark, or instant-marking orders during rush hours[cite: 1].
* **The Fallout:** Extreme variance in P90 ETA predictions, leading to surging platform costs, elevated rider idle times, and high customer cancellation rates[cite: 1].

## 🏗️ The Architectural Solution
This project establishes a bifurcated, tier-specific ingestion pipeline to secure operational scalability without relying on expensive hardware deployments[cite: 1].

### Phase 1: Signal De-noising (The Trust Score)
To programmatically eliminate human bias, the system anchors to passive GPS telemetry[cite: 1]. 
* **The Logic:** The pipeline compares the merchant's manual FOR timestamp against the rider's physical GPS departure timestamp to quantify the exact gap[cite: 1].
* **The Impact:** A continuous decay function penalizes fraudulent merchants. If the Trust Score drops, the dispatch engine mutes their manual inputs and defaults to mathematical ground truth[cite: 1].

### Phase 2: Signal Enrichment (The Chaos Index)
A real-time environmental load multiplier designed to quantify the "Offline Blind Spot"[cite: 1].
* **Tier 1 & 2 (Organized Chains):** Deep POS API webhooks extract live ticket counts (including dine-in and competitors) to scale the ETA dynamically[cite: 1].
* **Tier 3 (Unorganized Vendors):** A software-based Edge-AI acoustic sensor that repurposes existing merchant tablets to measure ambient kitchen decibels (dB), detecting physical kitchen chaos without CapEx hardware deployment[cite: 1].
* **Macro-Validation:** Integrates Geospatial Footfall proxies to measure localized traffic density and app-open surges in a 50-meter geofence[cite: 1].

## 📊 Quantitative Simulation & Business Impact
To validate the architecture, a Python simulation was engineered using Pandas and NumPy to process a 3,000-order synthetic dataset, modeling real-world physical constraints and merchant fraud[cite: 1].

**Conclusive Business Outcomes:**
* **ETA P90 Accuracy:** Slashed the worst-case (90th percentile) ETA prediction error by **53%**, dropping the variance from 8.00 minutes down to 3.70 minutes[cite: 1].
* **Reclaimed Fleet Capacity:** Eliminated **36.18 hours** of cumulative fleet idle time by replacing premature dispatching with mathematical Just-In-Time (JIT) Rider Dispatch[cite: 1].
* **Proactive Cancellation Mitigation:** Dynamically inflated pre-checkout ETAs during high-friction kitchen events, successfully intercepting and neutralizing >20-minute surprise delays that drive customer churn[cite: 1].

## 💻 Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy
* **Methodologies:** Data Engineering, ETL Pipeline Architecture, Feature Engineering, Synthetic Data Modeling
