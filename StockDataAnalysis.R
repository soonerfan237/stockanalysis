library(Amelia) #needed for missmap
library(ggplot2)  #for graphics
library(gridExtra) #for arranging graphs

setwd("/Users/soonerfan237/PycharmProjects/stockanalysis")
print(getwd())

stockdata_dict <- read.csv("pricechangedaylist.csv", stringsAsFactors=FALSE)  #reading in exoplanet data
summary(stockdata_dict)

histogram <- ggplot(stockdata_dict,aes(x = stockdata_dict$Day)) + geom_density() + xlab("feature1") + scale_color_gradient(low="blue", high="red") + theme(legend.position="bottom") 
histogram