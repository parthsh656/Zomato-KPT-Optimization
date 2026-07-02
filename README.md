# Zomato KPT Optimization Architecture 🚀

A Python-based Data Engineering and ETL pipeline designed to de-noise Kitchen Prep Time (KPT) signals, eliminate human bias, and drastically improve ETA accuracy for food delivery networks.

## 📌 The Problem: "Garbage In, Garbage Out"
Legacy food delivery Machine Learning models rely heavily on manual "Food Ready" inputs from restaurant merchants. However, this data is often contaminated:
* Merchants press the button early to avoid algorithmic penalties.
* The system is blind to offline physical kitchen load (e.g., crowded dine-in rushes).
* **Result:** Extreme variance in P90 ETA predictions, wasted delivery fleet capacity, and high customer cancellation rates.

## 🛠️ The Architecture (The Solution)
Instead of altering the core predictive ML models, this architecture introduces a robust **upstream ETL pipeline** to sanitize and enrich the data before ingestion.

### 1. The Trust Score (Signal De-noising)
A mathematical penalty function that compares a merchant's manual "Food Ready" click against passive ground-truth telemetry (Rider GPS departure). Highly inaccurate merchants are automatically down-weighted to prevent data contamination.

### 2. The Chaos Index (Zero-CapEx Edge-AI)
An environmental load multiplier that captures the "offline blind spot" dynamically:
* **Tier 1 & 2 (POS Integration):** Simulates API webhooks extracting live external ticket counts.
* **Tier 3 (Acoustic Edge-AI):** Simulates repurposed merchant tablets acting as local acoustic sensors (TensorFlow Lite), translating ambient kitchen decibels into a load multiplier without requiring physical hardware deployment.

## 📊 The Simulation & Business Impact
The repository includes a simulation engine (`zomato_kpt_simulation.py`) that generates a 3,000-order synthetic dataset, runs it through the ETL pipeline, and calculates the resulting business metrics.

**Key Results:**
* **ETA Accuracy:** Slashed worst-case (P90) ETA prediction error by **53%** (dropping from 8.00 minutes to 3.70 minutes).
* **Fleet Efficiency:** Reclaimed **36.18 hours** of cumulative fleet idle time by enabling Just-In-Time (JIT) rider dispatch.
* **Customer Retention:** Neutralized the primary trigger for order cancellations by dynamically inflating pre-checkout ETAs during high-friction kitchen events.

## 💻 Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy
* **Methodologies:** ETL Pipeline Design, Feature Engineering, Synthetic Data Generation

