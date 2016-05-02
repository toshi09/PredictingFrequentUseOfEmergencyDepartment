library(cvTools)
library(rpart) #  Decision Tree

set.seed(2123)

response_variable_name = 'category_gt_eq_4'

file <- "/Users/oshpddata/Desktop/vikhyati/MLHC_ED_2009.csv"
data = read.csv(file, header=T)
data_without_rln = subset(data, select=-c(rln))
# Print the names of the columns
names(data_without_rln)


logit <- glm(category_gt_eq_4 ~ ., data = data_without_rln, family = "binomial")

folds <- cvFolds(nrow(data_without_rln), K = 10, R = 10)
prediction_error = repCV(logit, cost = rtmspe, folds = folds, trim = 0.1)
print("10 fold repeated Cross validation result ")
print(prediction_error)

#tree <- rpart(category_gt_eq_4 ~ ., data=g)

#cvFit(rpart, formula = category_gt_eq_4 ~ . , data=data_without_rln, 
#      cost=function(y, yHat) (y != yHat) + 0, folds = folds, trim = 0.1)

