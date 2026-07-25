# Methodology Examples

> *Source: PCEMS 2026 Sample Papers*

## Purpose

The methodology section must provide enough detail for replication. This document shows effective methodology writing from accepted sample papers with annotations.

## Example 1: Machine Learning Pipeline (Credit Card Fraud Detection)

### Dataset Description

> "The dataset taken is from Kaggle, which has two days of transactions of European Credit card holders. The dataset was saved as a CSV file. The dataset consists of 2,84,807 transactions with only 492 fraud transactions... Due to the confidentiality problem, the attributes are PCA transformed, and the input-viable dataset is converted into numerical values."

**What works**:
- Source identified (Kaggle)
- Size stated (284,807 transactions)
- Class distribution provided (492 fraud out of 284,807)
- Preprocessing explained (PCA transformation)
- Justification for transformation given (confidentiality)

### Algorithm Description

> "1. Logistic Regression: This is the foremost in-style ML algorithm for binary classification of the data points... 2. Random Forest: The random forest comes under ensemble learning. It is the combination of multiple classifiers."

**What works**:
- Each algorithm is briefly described
- Justification for selection is implied by the description
- Algorithms are numbered consistently

### Experimental Setup

> "80% is used for training, and the remaining 20% is used for testing."

**What works**:
- Train/test split clearly stated
- Consistent across all comparisons

## Example 2: Hardware System (IoT Smart Warehouse)

### Hardware Components

> "1) MQ2: The smoke detector is MQ2. It calculates the amount of fire gases in the immediate area... 2) PIR sensor: A detector which sense infrared is a section of electrical device that senses infrared light from items inside its field of vision... 3) Node MCU: It has open supply prototyping board designs and is a free software."

**What works**:
- Each component listed and described
- Function explained
- Specifications given where relevant

### Software Stack

> "1) Arduino IDE: It is simple to encode and deliver it to a panel using the Arduino IDE, a free development tool... 2) Blynk: To use the Internet of Things service Blynk, which is accessible for iOS or Android smartphones, users may remotely manage gadgets."

**What works**:
- Software tools identified
- Purpose stated
- Platform compatibility mentioned

### Working Principle

> "The PIR Sensor, MQ135 Sensor, and DHT 11 Sensor are the important sensors utilised in this research. MQ135 monitors CO2 levels and smoke, whereas DHT 11 detects temperature and humidity. Rodent motion is recognised by PIR sensors."

**What works**:
- Each sensor's role mapped to a monitoring function
- Clear data flow description
- Integration explained

## Example 3: Simulation Study (Nanotube JLFET)

### Simulation Tool

> "The simulations are run using Silvaco TCAD software. The Boltzman model is used to carrier statistics. For lower carrier concentration in strongly doped areas, the Fermi-Dirac model is applied."

**What works**:
- Software identified (Silvaco TCAD)
- Physical models specified
- Justification for model selection provided

### Device Parameters

Presented as a table (Table 1 in original):

| Parameter | Value |
|-----------|-------|
| Nanotube Thickness (d_nt) | 10 nm |
| Core gate diameter (d_core) | 5 nm |
| Gate oxide thickness (t_ox) | 1 nm |
| Gate Length (L_g) | 5-20 nm |
| Spacer Length (L_s) | 5 nm |
| Doping Concentration (N_D) | 1x10^19 cm^-3 |
| Gate electrode work function (Φ_m) | 4.7 eV |

**What works**:
- All design parameters listed with symbols and units
- Consistent notation with the text
- Table format for quick reference

## Methodology Writing Checklist

- [ ] Dataset source, size, and preprocessing described
- [ ] Algorithm or method described with enough detail for replication
- [ ] Hardware or software tools identified with versions
- [ ] All parameters specified with symbols and units
- [ ] Experimental configuration explained (train/test split, cross-validation)
- [ ] Justification provided for key design decisions
- [ ] Metrics for evaluation defined
- [ ] Tables used for parameter listings
- [ ] Figures used for architecture or workflow diagrams

## Anti-Patterns

| Weak | Strong |
|------|--------|
| "A dataset was used" | "The dataset consists of 284,807 transactions with 492 fraud cases from Kaggle" |
| "The model was trained" | "The model was trained for 100 epochs with batch size 32 using Adam optimizer (lr=0.001)" |
| "Experiments were conducted" | "Experiments were performed on a system with Intel i7-12700H, 16GB RAM, NVIDIA RTX 3060" |
| "Several parameters were tested" | "Core gate diameter was varied from 3nm to 7nm in 1nm increments" |
