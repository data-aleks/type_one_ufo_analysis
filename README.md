# 🛸 Unveiling UFO Sightings: A Data-Driven Analysis of Space Activity Correlations

## Overview
This project investigates the interplay between **Tier 1 UFO sightings** (highly anomalous, structured craft reports) and external astronomical and human space activity. By analyzing publicly available data on **space launches** and **near-Earth asteroid detections**, we explore potential correlations that could explain fluctuations in sighting reports over time.

## Project Structure
- type_one_ufo_analysis
  - ufo_sightings_project.ipynb
  - data
    - nuforc_type1_sighting_data.csv
    - scraper
      - nuforc_org_scraper.py
      
## Technologies Used
This project employs:
- `pandas` – Data manipulation and preprocessing
- `matplotlib` – Data visualization
- `scipy` – Statistical analysis
- `sklearn` – Regression modeling
- `statsmodels` – Advanced statistical diagnostics

## Data Sources
This study utilizes reputable datasets:
- **[National UFO Reporting Center (NUFORC)](https://nuforc.org)** – A database of reported UFO sightings, filtered for Tier 1 incidents in the US.
- **[Our World in Data](https://ourworldindata.org)** – Space activity data, including the number of US space launches and detected near-Earth asteroids.

## Methodology
The analysis is structured around several key processes:
- **Data Acquisition** – Extracting real-world datasets via a Python scraper.
- **Data Cleaning & Preprocessing** – Addressing missing values, standardizing formats, and transforming raw data for analysis.
- **Correlation Studies** – Investigating statistical relationships between UFO sightings, space activity, and astronomical observations.
- **Visualizations** – Leveraging plots and trendlines to uncover patterns and anomalies across **time** and **geography**.

## Key Findings
After analyzing **65 years** of data, the results reveal **significant positive correlations**:
- 🚀 **Space Launches** – Each additional space launch corresponds to an estimated **68.7% increase** in Tier 1 UFO sightings.
- ☄️ **Near-Earth Asteroid Detections** – A **29.7% rise** in sightings is linked to an increase in asteroid detection efforts.
- 🔍 **Model Performance** – Statistical modeling explained **27.13%** of the variance in UFO sighting frequency.

Based on model's findings, I can conclude that the **increase in human space activity**, particularly the sharp rise in launches and **near-Earth asteroid detections** observed post-2010 (a period characterized by increased privatization of space exploration and advancements in detection technologies), **positively contributes** to the number of reported sightings. I propose that the **heightened public coverage** and awareness surrounding **human space activity** and **astronomical events** increases the likelihood of individuals observing, interpreting, and consequently reporting unusual aerial phenomena as "Tier 1" UFOs.



