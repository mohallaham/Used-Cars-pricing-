# Used Car Pricing System

This project aims to develop an AI-powered pricing system for used cars, helping end-users set optimal prices when selling on online platforms. Currently, two key components have been completed: web scraping and data preprocessing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Next Steps](#next-steps)

## Overview

The project focuses on extracting and processing car listing data from OpenSooq, a popular online marketplace. The collected data will be used to build an AI-powered pricing model.

## Features

### Web Scraping

- Extracts car listings from OpenSooq.
- Captures details such as price, description, and specifications.
- Saves the scraped data in a CSV file for further processing.

### Data Preprocessing

- Cleans and standardizes extracted data.
- Handles missing values and inconsistencies.
- Prepares the dataset for further analysis and modeling.

## Installation

To run the project, ensure you have Python installed along with the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Running the Web Scraper

```sh
python web_scraping_opensooq.py
```

### Running Data Preprocessing

```sh
jupyter notebook
```

Then open `Data Preprocessing.ipynb` and run the notebook cells.

## Project Structure

```
📂 Used-Car-Pricing-System
├── 📄 web_scraping_opensooq.py  # Web scraping script
├── 📄 Data Preprocessing.ipynb  # Data preprocessing steps
├── 📄 car_data.csv              # Scraped car data
├── 📄 requirements.txt          # Dependencies
└── 📄 README.md                 # Project documentation
```

## Next Steps

- Feature engineering and data analysis.
- Model development for price prediction.
- Deployment and integration with a user-friendly interface.

Stay tuned for further updates! 



