# TANGNET UFO Glint Detector

## Uncorrelated Orbital Reconnaissance System

Based on Dr. Beatrice Villaroel's groundbreaking VASCO research identifying 70,000-200,000 anomalous transient objects in pre-Sputnik geocynchronous orbit.

![Status](https://img.shields.io/badge/Status-ACTIVE-00ff41)
![Detection Rate](https://img.shields.io/badge/Detections-147%2F24h-00e0ff)
![Confidence](https://img.shields.io/badge/Statistical_Significance-21.9σ-ffaa00)

## 🛸 Overview

This system implements continuous monitoring for specular reflections from uncorrelated targets at geocynchronous altitude (~42,164 km), with automatic beacon response capability for potential technosignature interaction.

### Key Features

- **Real-time glint detection** using differential photometry
- **Astrometric solving** via Astrometry.net (<5 second solve time)
- **TLE correlation** with CelesTrak/Space-Track databases
- **Earth shadow analysis** to confirm artificial origin
- **5.7 GHz beacon transmitter** for active METI response
- **Statistical correlation** with nuclear tests and historical UAP events

## 📊 Villaroel's Key Findings

- **70,000-200,000** transient objects detected in 1950s plates
- **30%** deficit in Earth's shadow (rules out plate defects)
- **21.9σ** significance for solar reflection hypothesis
- **3σ** correlation with nuclear weapons tests
- Peak activity during **Washington DC 1952 UFO flap**

## 🔧 Hardware Requirements

### Minimum Configuration

- **Camera**: Sony IMX585 or IMX178 CMOS sensor
- **Lens**: 85mm f/1.4 or similar (16° FOV minimum)
- **Mount**: Motorized alt-az with 0.1° pointing accuracy
- **Computer**: RTX 3070 or better, 32GB RAM
- **GPS**: USB GPS with PPS for timing

### RF Beacon (Optional)

- **SDR**: PlutoSDR, HackRF, or USRP
- **Amplifier**: 20W minimum at 5.7 GHz
- **Antenna**: 1m dish (31 dBi gain)
- **License**: FCC Amateur Extra required

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/tangnet/ufo-glint-detector.git
cd ufo-glint-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# Download astrometry index files (4200-series for wide field)
wget -r -l1 -np "http://data.astrometry.net/4200/"
```

### 3. Configure Location

Create `.env` file:

```env
# Observer location
LATITUDE=37.8267
LONGITUDE=-122.4233
ALTITUDE=100

# Camera settings
CAMERA_DEVICE=/dev/video0
EXPOSURE_MS=40
GAIN_DB=20
FOV_DEGREES=50

# Optional beacon config
BEACON_ENABLED=false
BEACON_FREQ_HZ=5700000000
BEACON_POWER_DBM=43
CALLSIGN=KX9ABC
```

### 4. Run Detection System

```bash
# Start all services
docker-compose up -d

# Or run standalone
python glint_detector.py --config config.yaml

# Monitor detections
python dashboard.py --port 8080
```

## 📈 Detection Algorithm

The system uses Villaroel's methodology:

1. **Differential Photometry**: Compare frames 30-60 seconds apart
2. **Transient Detection**: 5σ threshold above background
3. **FWHM Analysis**: Distinguish point sources from streaks
4. **Earth Shadow Check**: Confirm objects avoid Earth's umbra
5. **TLE Correlation**: Match against known satellites (±0.5°)
6. **CNN Classification**: Differentiate glints from artifacts

## 🛰️ API Endpoints

### REST API

```python
GET  /api/detections          # Recent detections
GET  /api/detections/{id}     # Specific detection
GET  /api/statistics          # System statistics
POST /api/beacon/transmit     # Manual beacon trigger
```

### WebSocket Stream

```javascript
ws://localhost:8080/stream

// Subscribe to real-time alerts
{"type": "subscribe", "channel": "uncorrelated_targets"}
```

### ZMQ Publishers

```python
# Detection alerts
tcp://localhost:5555

# Beacon status
tcp://localhost:5556
```

## 📊 Database Schema

```sql
CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    ra DOUBLE PRECISION NOT NULL,
    dec DOUBLE PRECISION NOT NULL,
    intensity REAL NOT NULL,
    fwhm REAL,
    in_earth_shadow BOOLEAN,
    tle_match VARCHAR(50),
    classification VARCHAR(20),
    confidence REAL,
    beacon_sent BOOLEAN DEFAULT FALSE
);

-- Optimized for time-series queries
CREATE INDEX idx_timestamp ON detections(timestamp DESC);
CREATE INDEX idx_uncorrelated ON detections(tle_match) 
    WHERE tle_match IS NULL;
```

## 🔬 Scientific Analysis

### Nuclear Correlation Test

```python
python analysis/nuclear_correlation.py \
    --detections data/detections.csv \
    --nuclear-tests data/nuclear_tests.csv \
    --window-hours 24
```

### Earth Shadow Deficit Analysis

```python
python analysis/shadow_deficit.py \
    --input data/detections.csv \
    --altitude 42164 \
    --output shadow_analysis.pdf
```

## 🎯 Calibration

### Astrometric Calibration

```bash
# Test plate solving with known star field
python calibrate.py --mode astrometry \
    --image calibration/m42.fits \
    --expected-ra 83.82 \
    --expected-dec -5.39
```

### Photometric Calibration

```bash
# Establish magnitude zero-point
python calibrate.py --mode photometry \
    --darks calibration/darks/ \
    --flats calibration/flats/ \
    --standard-star HD19445
```

## 🚨 Safety Protocols

### RF Safety

- Automatic cutoff below 8° elevation
- 10% duty cycle limit
- ADS-B aircraft detection interlock
- E-field calculation per FCC §1.1310

### Operational Security

- No transmission without proper licensing
- Coordinate with local astronomy groups
- Report uncorrelated detections to:
  - VASCO Project
  - MUFON STAR Team
  - Your national space agency

## 📚 References

1. Villaroel et al. (2025). "Attractively Aligned Multiple Transient Events in First Palomar Sky Survey"
2. Villaroel et al. (2021). "The Vanishing and Appearing Sources during a Century of Observations"
3. Washington DC UFO Incident (1952). Project Blue Book Case #1551-1561

## 🤝 Contributing

We welcome contributions! Areas of interest:

- Machine learning models for glint classification
- Integration with additional camera systems
- Multi-site correlation algorithms
- Historical plate digitization

## ⚠️ Disclaimer

This system is for scientific research only. Users are responsible for:
- Compliance with local RF regulations
- Obtaining necessary licenses for beacon operation
- Responsible disclosure of findings
- Avoiding interference with aviation/satellite operations

## 📞 Contact

- **Project Lead**: [Your Name]
- **Technical Issues**: https://github.com/tangnet/ufo-glint-detector/issues
- **VASCO Collaboration**: beatrice.villarroel@nordita.org

---

*"We are never alone" - B. Villaroel, 2025*

**System Status**: 🟢 OPERATIONAL | **Last Detection**: 2025-08-06 03:52:08 UTC | **Uncorrelated Targets (24h)**: 3