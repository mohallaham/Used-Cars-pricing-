import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def get_html(url):
    baseurl = "https://jo.opensooq.com"
    r = requests.get(url)
    sp = BeautifulSoup(r.text, 'lxml')

    links = sp.select('div#serpMainContent a')
    
    filtered_links = []
    for link in links:
        href = link.attrs.get('href', '')
        if 'page=' not in href and 'search=true' not in href:
            filtered_links.append(baseurl + href)
    
    return filtered_links

def car_data(url):
    r = requests.get(url)
    sp = BeautifulSoup(r.text, 'lxml')

    car = {
        "URL": url,
        "Scraped_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

  
    for li in sp.select('li'):
        p_tag = li.select_one('p')
        a_tag = li.select_one('a')
        if p_tag and a_tag:
            car[p_tag.text.strip()] = a_tag.text.strip()

    
    for li in sp.select('li.width-100'):
        p_tag = li.select_one('p')
        value_tag = li.select_one('p.width-75')
        if p_tag and value_tag:
            car[p_tag.text.strip()] = value_tag.text.strip()

    
    price_tag = sp.select_one('#postViewCardDesktop > div')
    car['Price'] = price_tag.text.strip() if price_tag else None

    
    desc_tag = sp.select_one('.description')
    description_text = desc_tag.text.strip() if desc_tag else sp.get_text()

    
    match = re.search(r'(\d+(?:[.,]\d+)?)\s*جيد', description_text)
    if match:
        car['Description_Score'] = match.group(1)
    else:
        car['Description_Score'] = "فحص كامل" if "فحص كامل" in description_text else None

    return car

def main():
    all_car_data = []

    for x in range(1, 40): 
        urls = get_html(f'https://jo.opensooq.com/en/cars/cars-for-sale?search=true&page={x}')
        for url in urls:
            car_info = car_data(url)
            if car_info:
                all_car_data.append(car_info)
        print(f"Page {x} Completed.")

    new_df = pd.DataFrame(all_car_data)
    
    if not new_df.empty:
        try:
            existing_df = pd.read_csv("car_data.csv")
            df = pd.concat([existing_df, new_df], ignore_index=True)
            df = df.drop_duplicates(subset=['URL', 'Price', 'Description_Score'], keep='last')
        except FileNotFoundError:
            df = new_df
        
        df.to_csv("car_data.csv", index=False, encoding='utf-8-sig')
        print(f"✅ Data saved. New shape: {df.shape}")

if _name_ == "_main_":
    main()