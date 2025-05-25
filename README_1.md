
# Used Car Pricing System

An AI-powered system for predicting used car prices using data scraped from OpenSooq.

## 🚗 Overview

This project encompasses the entire pipeline from data collection to deployment:

- **Web Scraping**: Collects car listings from OpenSooq.
- **Data Preprocessing & EDA**: Cleans and analyzes the data.
- **Modeling**: Builds machine learning models to predict car prices.
- **Deployment**: Provides a Streamlit web app for user interaction.

## 🧰 Features

### Web Scraping

- Scrapes used car listings from [OpenSooq](https://jo.opensooq.com).
- Extracts attributes such as price, description score, and other details.
- Saves the scraped data to a CSV file.

### Data Preprocessing & EDA

- Cleans missing values and standardizes data formats.
- Handles outliers and irrelevant features.
- Separates data into electric and non-electric cars.
- Prepares the dataset for machine learning.

### Modeling

- Implements machine learning models for price prediction.
- Evaluates model performance and fine-tunes parameters.

### Deployment

- Develops a Streamlit web application for user-friendly interaction.
- Allows users to input car details and receive price predictions.

## 📁 Project Structure

```
Used_Car_Pricing_Project/
├── Data/
│   ├── cars_data.csv
│   ├── cars_data_cleaned.csv
│   ├── Electric_cars_cleaned.csv
│   └── Non_Electric_cars_cleaned.csv
├── Data Preprocessing & EDA/
│   └── Data Preprocessing.ipynb
├── Modeling/
│   └── modeling_pipeline.ipynb
├── Web Scraping/
│   └── web_scraping_opensooq.py
├── streamlit app/
│   └── app.py
├── requirements.txt
└── README.md
```

## 💻 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mohallaham/Used-Cars-pricing-.git
   cd Used-Cars-pricing-
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Run the web scraping script:**

   ```bash
   python Web\ Scraping/web_scraping_opensooq.py
   ```

2. **Process the data:**

   ```bash
   jupyter notebook
   ```

   - Open `Data Preprocessing & EDA/Data Preprocessing.ipynb` and run the cells.

3. **Train the model:**

   - Open `Modeling/modeling_pipeline.ipynb` and execute the notebook to train and evaluate the model.

4. **Launch the Streamlit app:**

   ```bash
   streamlit run streamlit\ app/app.py
   ```

   - Access the web application in your browser to input car details and receive price predictions.

## 🔮 Future Work

- **Enhanced Feature Engineering**: Incorporate additional features to improve model accuracy.
- **Model Optimization**: Experiment with advanced algorithms and hyperparameter tuning.
- **Deployment**: Deploy the Streamlit app to a cloud platform for broader accessibility.

---

*Stay tuned for updates!*

---

For more information, visit the [Used-Cars-pricing- GitHub repository](https://github.com/mohallaham/Used-Cars-pricing-).
