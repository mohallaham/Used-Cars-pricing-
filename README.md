# Used Car Pricing System - Data Collection & Preprocessing

This repository contains the initial stages of a project aimed at developing an AI-powered pricing system for used cars. Currently, two key components have been completed:

1. **Web Scraping**: Extracting used car listings from OpenSooq.
2. **Data Preprocessing**: Cleaning and preparing the data for further analysis and modeling.

## Features

- **Web Scraping**:
  - Scrapes used car listings from [OpenSooq](https://jo.opensooq.com).
  - Extracts car attributes such as price, description score, and other details.
  - Saves the scraped data to a CSV file.
  
- **Data Preprocessing**:
  - Cleans missing values and standardizes data formats.
  - Handles outliers and irrelevant features.
  - Separates data into electric and non-electric cars.
  - Prepares the dataset for machine learning.

## Project Structure

```
📂 Used_Car_Pricing_Project
│── 📂 Data
│   ├── cars_data_cleaned.csv
│   ├── Electric_cars_cleaned.csv
│   ├── Non_Electric_cars_cleaned.csv
|   ├── cars_data.csv
│── 📂 Data Preprocessing & EDA
│   ├── Data Preprocessing.ipynb
│── 📂 Web Scraping
│   ├── web_scraping_opensooq.py
│── requirements.txt
│── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the web scraping script:
   ```bash
   python scripts/web_scraping_opensooq.py
   ```

4. Process the data:
   ```bash
   jupyter notebook
   ```
   Open `notebooks/Data Preprocessing.ipynb` and run the cells.

## Future Work

- **Feature Engineering**
- **Model Development**
- **Deployment of the Pricing System**

---

 *Stay tuned for updates!*
