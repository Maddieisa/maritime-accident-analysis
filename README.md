# 🚢 Maritime Accident Analysis(HS-MACs）

This repository presents the results and visualizations of a **HFACS-based causal analysis** of maritime accidents from 2015 to 2024——HS-MACs. It integrates structured data, large language model (LLM)-assisted classification, and statistical causal inference methods to explore the relationships between human and environmental factors and accident outcomes.

---

## 📌 Project Overview

This study applies the **Human Factors Analysis and Classification System (HFACS)** to a collection of over 300 maritime accident reports. By combining HFACS classifications with selected environmental attributes, we construct and evaluate **causal chains** leading to various accident types.

---

## 🧠 Analysis Workflow

The full analysis pipeline includes:

1. **Data Collection**:  
   - Maritime accident reports (2015–2024) saved as PDFs  
   - Extraction of the “*Probable Cause*” paragraph from each report

2. **LLM-based Classification**:  
   - Use of [DeepSeek](https://www.deepseek.com/) API with three prompt variations to classify probable causes based on the HFACS framework  
   - Three rounds of classification with varying perspectives

3. **Decision Algorithm**:  
   - A majority-voting-based decision logic was applied to unify the three classification results into a single HFACS label per case

4. **Human Validation**:  
   - Manual verification of selected samples for final classification consistency. In order to ensure the stability of the classification results of the large model and algorithm, we found three scholars in related fields to supplement and optimize the results, manually judge and classify the data that the large model failed to classify, and judge the results of abnormal outputs of the decision algorithm based on the complete content of the corresponding accident report. All results have been manually reviewed many times.

5. **Causal Analysis**:  
   - Construction of structured datasets:  
     `HFACS factor + up to 3 environmental factors (e.g., date, location, vessel type, wind)`  
     → `Accident Type`  
   - Evaluation using **Average Treatment Effect (ATE)** and **p-value (Stouffer combination)**
   - Filtered and selected high-performing causal relationships for final dataset

---
## 📈 Key Components

### 📁 Causal Analysis Dataset

- **Structure**:  
  `HFACS Category + Environmental Factors(≤3 combination) → Accident Type`
- **Includes**:
  - Average Treatment Effect (ATE)
  - 95% Confidence Intervals
  - Combined significance using Stouffer’s method

### 🌐 Interactive Sankey Diagrams

- Clickable, dynamic diagrams in HTML format
- Visualize causal chains for different accident types
- Files located in `/visualizations/`

## 🎯 Project Purpose

This repository is designed to serve as a resource for:

- **Safety Analysts** — to trace risk factors and root causes in accident progression  
- **Policy Makers** — to understand environmental and human patterns in maritime incidents  
- **Research Community** — to experiment with LLM-based classification and HFACS frameworks  
- **Developers** — to reuse modular scripts for classification, decision-making, and visualization

---

## 📬 Contact

If you have questions, suggestions, or would like to collaborate:

📧 Email: `qianqianz540@gmail.com`  
📘 GitHub Issues: [Create an issue](https://github.com/Maddieisa/maritime-accident-analysis/issues)

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
