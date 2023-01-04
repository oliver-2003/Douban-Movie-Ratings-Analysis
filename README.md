# Douban-Movie-Ratings-Analysis
This project analyzes the relationship between the rating and the proportion of five-star ratings of movies on Douban, a Chinese online rating platform. By fitting the data to the linear model, this project reveals the prediction confidence interval of five-star proportions, showing that some movies display exceptional distribution of ratings.
## Data Collection
### Establishing Database
This project uses MySQL to store data. Execute MovieRating.sql to prepare the data tables required.
### Data Collection
This project takes two steps to collect data from Douban. 
Firstly, this project uses Selenium to carry out the stratified sampling of movies in different eras. Selenium scrapes around 3800 movie URLs in total, with each URL directing to the individual page of the movie with the rating, distribution of ratings, published region and date, and movie tags. Secondly, this project uses requests and regular expression to scrape data from the individual movie pages. 
### Data Preprocessing
#### Melting columns of different tags
Movies have different numbers of tags recorded in columns from tag1 to tag5. Melting all tags into one column generates a tag variable for further analysis.
```Python
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
```
#### Splitting and Melting Regions 
In the raw data, movies have their produced regions joined by "/". To consider the effect of the produced region, the region column must be firstly split into different columns by "/", and then melted into a single column.
```Python
df_region_split = pd.DataFrame((x.split('/') for x in df_tag_melt['region']), columns=['region1', 'region2', 'region3', 'region4', 'region5', 6, 7, 8, 9, 10])
df = pd.concat([df_tag_melt, df_region_split], axis=1)
# Melt the columns of different regions into a single column
df = pd.melt(df, id_vars=['name', 'rating', 'date', 'one', 'two', 'three', 'four', 'five', 'tag', 'tag_name'],
value_vars=['region1', 'region2', 'region3', 'region4', 'region5'], var_name='region',
value_name='region_name')
```
#### Dropping Missing Values
The operations of splitting and melting generate many rows with missing values. Dropping the missing values keeps the valid data. 
```Python
df = df.dropna()
df = df.reset_index(drop=True)
```
#### Generating the "Era" Variable
To take the date released into consideration, assign the era of the movies as a variable according to the date released.
```Python
# Use the era dict to assign "eras" for corresponding dates
era_dict = {r"202\d": "2020s", r"201\d": "2010s", r"200\d": "2000s", r"199\d": "1990s", r"198\d": "1980s", r"197\d": "1970s", r"196\d": "1960s"}
for row in df.itertuples():
    for era in era_dict:
        df.loc[row[0], 'era'] = 'Earlier'
        if len(re.findall(era, str(row))) > 0:
            df.loc[row[0], 'era'] = era_dict[era]
            break
```
#### Generating "is_made_in_china" variable
To consider the relationship between the rating and whether the movie is produced in China, assign 1 for movies that are made in China, and 0 for those that are not.
#### Taking the Logarithm of the Five-Star Proportion
To better fit the linear model, take log10 of the response variable "five-star proportion."

### Data Analysis
#### Building the Linear Regression Model 
```R
model <- lm(log10_proportion~rating, data = data)
summary(model)
```
#### Adding the Prediction Interval
```R
pred.int <- predict(model, interval = "prediction")
mydata <- cbind(data, pred.int)
```
#### Graphing the Scatter Plot and Fitting the Regression Line
```R
p <- ggplot(mydata, aes(rating, log10_proportion)) +
geom_point(colour="#4D4D4D") +labs(x="Rating", y="Five-Stars Proportion", title='Relationship between Rating and Five-Stars Proportion')+
stat_smooth(method = lm, colour="black")
```

#### Graphing the prediction interval
```R
p + geom_line(aes(y = lwr), color = "red", linetype = "dashed")+
geom_line(aes(y = upr), color = "red", linetype = "dashed")
```
![image](https://github.com/oliver-2003/Douban-Movie-Ratings-Analysis/blob/main/Regression%20Models/Linear%20Model.png)

#### Graphing the Multiple Linear Regression Model
``` R
ggplot(data, aes(log10_proportion, rating, color=factor(is_made_in_china)))+geom_point()+
labs(x="Five-stars Proportion", y="Rating", title="Relationship Between Rating and Five-stars Proportion")+
theme_bw()+scale_y_log10()+geom_smooth(method="lm")+guides(color=guide_legend(title="Whether made in China \n (0:No, 1:Yes)"))
```
![image](https://github.com/oliver-2003/Douban-Movie-Ratings-Analysis/blob/main/Regression%20Models/Multiple%20Regression%20Model.png)

#### Graphing the Relationships Separately Based on Eras
```R
ggplot(data, aes(log10_proportion, rating, color=factor(is_made_in_china)))+geom_point()+
labs(x="Five-stars Proportion", y="Rating", title="Relationship Between Rating and Five-stars Proportion")+
theme_bw()+scale_y_log10()+geom_smooth(method="lm")+guides(color=guide_legend(title="Whether made in China \n (0:No, 1:Yes)"))+facet_wrap("era")
```
![image](https://github.com/oliver-2003/Douban-Movie-Ratings-Analysis/blob/main/Regression%20Models/Multiple%20Regression%20By%20Era.png)

