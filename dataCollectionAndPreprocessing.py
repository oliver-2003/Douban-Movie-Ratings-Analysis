from bs4 import BeautifulSoup
import math
import pandas as pd
import pymysql
import randHeaderProxy
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_url():
    href_list = []

    driver = webdriver.Edge()
    driver.get('https://movie.douban.com/explore')
    time.sleep(2)

    # Select 2020s as the era of the movies
    era_selector = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[3]/div')
    era_selector.click()
    target_era = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div/div/ul/li[2]')
    target_era.click()
    time.sleep(3)

    # Keeping reloading more content until reaching the bottom
    for reload_time in range(100):
        try:
            reload_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div')
            reload_button.click()
            time.sleep(3)
        # Scrape all URLs of the movies after reloading
        except Exception:
            url_list = driver.find_elements(By.XPATH, "/html/body/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li//a")
            for url in url_list:
                href = url.get_attribute("href")
                href_list.append(href)
            break

    # Select other eras
    for era in range(7, 14):
        era_selector = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[3]/div')
        era_selector.click()
        era_button = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div[1]/div/div[1]/div[3]/div/div[2]/div/div/ul/li[{era}]')
        era_button.click()
        time.sleep(3)

        for reload_time in range(100):
            try:
                reload_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div')
                reload_button.click()
                time.sleep(3)
            except Exception:
                url_list = driver.find_elements(By.XPATH, "/html/body/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li//a")
                for url in url_list:
                    href = url.get_attribute("href")
                    href_list.append(href)
                break

    return href_list


def get_data():
    href_list = get_url()

    for href in href_list:
        url = href

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        proxy = randHeaderProxy.get_random_proxy()

        try:
            time.sleep(random.randint(1, 4))
            res = requests.get(url, headers=headers, proxies=proxy, timeout=(3, 7))
            soup = BeautifulSoup(res.text, "html.parser")

            name = soup.find("h1").text.replace("\n", "")
            rating = soup.find("strong", class_="ll rating_num").text
            region = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', res.text, re.S)[0]
            date = re.findall('"datePublished": "(.*?)",', res.text, re.S)[0]
            tag_list = re.findall('<span property="v:genre">(.*?)</span>', res.text)
            # Keep only first five tags of each movie
            if len(tag_list) > 5:
                tag_list = tag_list[0:5]
            genre_tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]

            rating_list = re.findall('<span class="rating_per">(.*?)</span>', res.text)
            final_rating_list = ['DEFAULT']
            for i in rating_list:
                final_rating_list.append(i)

            to_movie_ratings = f"(DEFAULT, '{name}', '{rating}', '{region}', '{date}')"
            data_to_sql("movie_ratings", to_movie_ratings)

            # Convert the list to a tuple to follow the SQL syntax
            to_tags = tuple(tag_list)
            # If the tuple has only one element, remove the comma of the tuple
            if len(to_tags) == 1:
                final_to_tags = str(to_tags).replace(",", "")
                # Fill in columns based on the number of tags
                data_to_sql("movie_tags", final_to_tags, str(tuple(genre_tags[0:len(to_tags)])).replace("'", "").replace(",", ""))
            else:
                final_to_tags = to_tags
                data_to_sql("movie_tags", final_to_tags, str(tuple(genre_tags[0:len(to_tags)])).replace("'", ""))

            # Remove the quotation marks of 'DEFAULT'
            to_distributions = str(tuple(final_rating_list)).replace("%", "").replace("'", "", 2)
            data_to_sql("rating_distributions", to_distributions)
            print([to_movie_ratings, final_to_tags, to_distributions])

        except Exception:
            continue


def get_database_connection(host, port, user, passwd, db="movie_rating"):
    # Establish the connection with the database
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    return db


def data_to_sql(table, data, columns=""):
    db = get_database_connection("localhost", 3306, "root", "123456")
    sql = f"INSERT INTO {table} {columns} VALUES{data}"
    db.query(sql)
    db.commit()


def data_preprocessing():
    db = get_database_connection("localhost", 3306, "root", "123456")
    sql = """
    SELECT * 
    FROM movie_ratings
    JOIN movie_tags, 
    rating_distributions 
    WHERE tag_id=movie_id AND tag_id=distribution_id
    """
    # The SQL code above joins three different tables

    df = pd.read_sql(sql, db)
    # Melt columns of different tags into a single column
    df_tag_melt = pd.melt(df, id_vars=['name', 'rating', 'region', 'date', 'one', 'two', 'three', 'four', 'five'],
                          value_vars=['tag1', 'tag2', 'tag3', 'tag4', 'tag5'], var_name="tag", value_name="tag_name")

    # Split the region separated by "/" into different columns
    df_region_split = pd.DataFrame((x.split('/') for x in df_tag_melt['region']),
                                   columns=['region1', 'region2', 'region3', 'region4', 'region5', 6, 7, 8, 9, 10])

    df = pd.concat([df_tag_melt, df_region_split], axis=1)
    # Melt the columns of different regions into a single column
    df = pd.melt(df, id_vars=['name', 'rating', 'date', 'one', 'two', 'three', 'four', 'five', 'tag', 'tag_name'],
                 value_vars=['region1', 'region2', 'region3', 'region4', 'region5'], var_name='region',
                 value_name='region_name')
    df = df.dropna()
    df = df.reset_index(drop=True)

    # Use the era dict to assign "eras" for corresponding dates
    era_dict = {r"202\d": "2020s", r"201\d": "2010s", r"200\d": "2000s", r"199\d": "1990s", r"198\d": "1980s",
                r"197\d": "1970s", r"196\d": "1960s"}
    for row in df.itertuples():
        for era in era_dict:
            df.loc[row[0], 'era'] = 'Earlier'
            if len(re.findall(era, str(row))) > 0:
                df.loc[row[0], 'era'] = era_dict[era]
                break
        # If the region contains "中国"，the movie is made in China. Set the is_made_in_china variable to be 1.
        if len(re.findall("中国", str(row))) > 0:
            df.loc[row[0], 'is_made_in_china'] = 1
        else:
            df.loc[row[0], 'is_made_in_china'] = 0

        # Take the log10 of the five-stars proportion to better fit the linear model
        try:
            df.loc[row[0], 'log10_proportion'] = math.log10(df.loc[row[0], "one"])
        except ValueError:
            # Drop rows with a log10_proportion that is not a number
            df = df.drop(index=row[0])
            continue

    df.to_csv("movie_ratings_data.csv")

    return df


def data_collection_and_preprocessing():
    get_data()
    data_preprocessing()


data_collection_and_preprocessing()