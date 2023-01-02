library(data.table)
library(ggplot2)

data <- read.csv("movie_ratings_data.csv", fileEncoding = "utf-8")

# Build the linear regression model between the ratings of the movies and the five-stars proportion
model <- lm(log10_proportion~rating, data = data)
summary(model)

# Add in the prediction interval
pred.int <- predict(model, interval = "prediction")
mydata <- cbind(data, pred.int)

# Graph the scatter plot and fit the regression line
p <- ggplot(mydata, aes(rating, log10_proportion)) +
  geom_point(colour="#4D4D4D") +labs(x="Rating", y="Five-Stars Proportion", title='Relationship between Rating and Five-Stars Proportion')+
  stat_smooth(method = lm, colour="black")

# Graph the prediction interval
p + geom_line(aes(y = lwr), color = "red", linetype = "dashed")+
  geom_line(aes(y = upr), color = "red", linetype = "dashed")

#  Establish the multiple linear regression with the response variable being the rating of the movies and the explanatory variables being the five-stars proportion and whether the movie is made in China. 
fitregion <- lm(rating~log10_proportion+is_made_in_china, data=data_region)
summary(fitregion)

# Graph the multiple linear regression with the response variable being the rating of the movies and the explanatory variables being the five-stars proportion and whether the movie is made in China. 
ggplot(data, aes(log10_proportion, rating, color=factor(is_made_in_china)))+geom_point()+
  labs(x="Five-stars Proportion", y="Rating", title="Relationship Between Rating and Five-stars Proportion")+
  theme_bw()+scale_y_log10()+geom_smooth(method="lm")+guides(color=guide_legend(title="Whether made in China \n (0:No, 1:Yes)"))

# Graph the relationships separately based on different eras. 
ggplot(data, aes(log10_proportion, rating, color=factor(is_made_in_china)))+geom_point()+
  labs(x="Five-stars Proportion", y="Rating", title="Relationship Between Rating and Five-stars Proportion")+
  theme_bw()+scale_y_log10()+geom_smooth(method="lm")+guides(color=guide_legend(title="Whether made in China \n (0:No, 1:Yes)"))+facet_wrap("era")

