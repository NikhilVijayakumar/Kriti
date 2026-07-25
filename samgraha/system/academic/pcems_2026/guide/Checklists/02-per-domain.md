# Per-Domain Checklist

> *Source: PCEMS 2026 Sample Papers + Domain Documentation Standards*

## Purpose

Domain-specific requirements beyond the general pre-submission checklist. Select the checklist matching your paper's primary domain.

## Computer Science / Machine Learning

### Model and Data
- [ ] Model architecture described or diagrammed
- [ ] Dataset source identified (URL or citation)
- [ ] Dataset size stated (samples, features, classes)
- [ ] Class distribution provided (if classification)
- [ ] Train/validation/test split specified
- [ ] Preprocessing steps documented

### Training Configuration
- [ ] Learning rate specified
- [ ] Optimizer identified (Adam, SGD, etc.)
- [ ] Batch size stated
- [ ] Number of epochs or stopping criterion specified
- [ ] Hardware used for training (GPU model, memory)
- [ ] Software framework and version specified
- [ ] Random seed set and reported for reproducibility

### Evaluation
- [ ] At least 3 baseline methods compared
- [ ] Multiple metrics reported (not just accuracy)
- [ ] Standard deviations or confidence intervals included
- [ ] Statistical significance tested (if claiming improvement)
- [ ] Ablation study included (if composite method)
- [ ] Confusion matrix or per-class results provided

### Presentation
- [ ] Model architecture diagram included
- [ ] Training curves shown (loss, accuracy over epochs)
- [ ] Results in both table and figure formats
- [ ] Code availability stated (if applicable)

## Electronics / VLSI

### Device or Circuit
- [ ] Device structure or circuit schematic included
- [ ] All design parameters listed with symbols and units
- [ ] Material properties specified (if applicable)
- [ ] Technology node or feature size stated

### Simulation or Measurement
- [ ] Simulation tool identified (Silvaco, Cadence, etc.)
- [ ] Physical models specified (transport, mobility, etc.)
- [ ] Mesh or grid configuration described
- [ ] Measurement equipment identified (if experimental)

### Performance Metrics
- [ ] Key metrics reported (power, delay, area, I_ON/I_OFF)
- [ ] Comparison with analytical models or published data
- [ ] Scaling behavior shown across parameter range
- [ ] Temperature or process variation effects discussed

### Presentation
- [ ] Device cross-section or circuit diagram included
- [ ] I-V characteristics or timing diagrams shown
- [ ] Performance comparison table included
- [ ] Key parameters in a reference table

## IoT / Embedded Systems

### System Architecture
- [ ] Block diagram of complete system included
- [ ] All hardware components identified with model numbers
- [ ] Communication protocols specified
- [ ] Power requirements stated

### Hardware
- [ ] Sensor specifications listed (range, accuracy, interface)
- [ ] Microcontroller or processor identified
- [ ] PCB layout or prototype photograph included
- [ ] Bill of materials provided (if applicable)

### Software
- [ ] Development environment specified
- [ ] Libraries and frameworks identified with versions
- [ ] Firmware or code structure described
- [ ] Cloud or backend platform identified (if applicable)

### Testing
- [ ] Test conditions documented (temperature, humidity)
- [ ] Calibration procedure described
- [ ] Real-world deployment or prototype demonstrated
- [ ] Power consumption measured and reported
- [ ] Latency or response time measured

### Presentation
- [ ] System architecture diagram included
- [ ] Prototype photograph included
- [ ] Data flow diagram included
- [ ] Live demo or video link provided (if applicable)

## Signal Processing

### Signal Description
- [ ] Signal type identified (synthetic, real-world, both)
- [ ] Signal parameters specified (frequency, SNR, duration)
- [ ] Sampling frequency stated
- [ ] Number of samples stated

### Method
- [ ] Mathematical formulation provided
- [ ] Algorithm steps numbered and clear
- [ ] Computational complexity analyzed
- [ ] Parameters justified (window size, overlap, etc.)

### Evaluation
- [ ] Multiple performance measures used (SSE, NRE, etc.)
- [ ] Reference or ground truth established
- [ ] Noise robustness tested
- [ ] Comparison with established methods included

### Presentation
- [ ] Time-domain signal shown
- [ ] Time-frequency representation shown
- [ ] Comparison figures with multiple methods
- [ ] Quantitative results in tables
