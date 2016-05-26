#scp oshpddata@140.142.177.144:/Users/oshpddata/Desktop/vikhyati/PredictingFrequentUseOfEmergencyDepartment/adaboost_randomforest.R .
#scp adaboost_randomforest.R oshpddata@140.142.177.144:/Users/oshpddata/Desktop/vikhyati/PredictingFrequentUseOfEmergencyDepartment/ 
#
#!/usr/bin/env Rscript
#library(cvTools)
library(rpart)
library(caret)
library(plyr)
library(randomForest)
library(adabag)
#library(gbm)
#library(fastAdaboost)
library(AUC)
library(nnet)
#library(pROC)
#library(ROCR)

med <- c("ELIX_CHF","ELIX_PULMCIRC","ELIX_PERIVASC","ELIX_HTN","ELIX_HTNCX","ELIX_PARA","ELIX_VALVE", "ELIX_unclassified",
              "ELIX_NEURO","ELIX_CHRNLUNG","ELIX_DM","ELIX_DMCX","ELIX_HYPOTHY","ELIX_RENLFAIL","ELIX_LIVER",
              "ELIX_ULCER","ELIX_AIDS","ELIX_LYMPH","ELIX_METS","ELIX_TUMOR","ELIX_ARTH","ELIX_COAG","ELIX_OBESE",
              "ELIX_WGHTLOSS","ELIX_LYTES","ELIX_BLDLOSS","ELIX_ANEMDEF","ELIX_ALCOHOL","ELIX_DRUG","ELIX_PSYCH",
              "ELIX_DEPRESS","MSDRG_0", "MSDRG_1", "MSDRG_2")
dis = c('distance_lt_eq_5','distance_gt_20')
dem = c('gender','race_grp','age_lt_5', 'age_5_14', 'age_15_24')



multi_class_auc <-function(act_label, pred_scores) {
  #print(act_label$cat1)
  auc_cat1 = auc(roc(pred_scores[,1], act_label$cat1))
  auc_cat2 = auc(roc(pred_scores[,2], act_label$cat2))
  auc_cat3 = auc(roc(pred_scores[,3], act_label$cat3))

  return (list(auc_cat_1=auc_cat1, auc_cat2=auc_cat2,
               auc_cat3=auc_cat3))
}

multi_proc_auc <- function(pred_scores, pred_label) {
  new_pred_scores = rep(0, length(pred_label))
  cat1_rows = which(pred_label == "1")
  new_pred_scores[cat1_rows] = pred_scores[cat1_rows, 1]

  cat2_rows = which(pred_label == "2")
  new_pred_scores[cat2_rows] = pred_scores[cat2_rows, 2]

  cat3_rows = which(pred_label == "3")
  new_pred_scores[cat3_rows] = pred_scores[cat3_rows, 3]
  
  predictors = as.numeric(new_pred_scores)
  auc  = multiclass.roc(pred_label, predictors, levels=c(1, 2, 3))

  return(auc)
}

confusion_matrix_prec <- function(confusion_mat_table) {

  CAT_1_RECALL = confusion_mat_table[1,1] / (confusion_mat_table[1,1] + confusion_mat_table[2,1] +
                                               confusion_mat_table[3,1] )
  CAT_1_PRECISION = confusion_mat_table[1,1] / (confusion_mat_table[1,1] + 
                                                  confusion_mat_table[1,2] + confusion_mat_table[1,3])
  CAT_2_RECALL = confusion_mat_table[2,2] / (confusion_mat_table[1,2] + 
                                               confusion_mat_table[2,2] + confusion_mat_table[3,2] )
  CAT_2_PRECISION = confusion_mat_table[2,2] / (confusion_mat_table[2,1] + 
                                                  confusion_mat_table[2,2] + confusion_mat_table[2,3])
  CAT_3_RECALL = confusion_mat_table[3,3] / (confusion_mat_table[1,3] + 
                                               confusion_mat_table[2,3] + confusion_mat_table[3,3] )
  CAT_3_PRECISION = confusion_mat_table[3,3] / (confusion_mat_table[3,1] + 
                                                  confusion_mat_table[3,2] + confusion_mat_table[3,3])
  
  correct_dec = confusion_mat_table[1,1] + confusion_mat_table[2,2] + confusion_mat_table[3,3]
  total_pop = sum(confusion_mat_table)
  
  return(list(cat_1_rec=CAT_1_RECALL, cat_1_prc=CAT_1_PRECISION, 
              cat_2_rec=CAT_2_RECALL, cat_2_prc=CAT_2_PRECISION, 
              cat_3_rec = CAT_3_RECALL, cat_3_prc = CAT_3_PRECISION,
              accuracy= correct_dec / total_pop
              ))
}

adaboost_model <- function(train_data, test_data) {
  #print(train_data)
  ad <- boosting(formula=category ~ ., data=train_data, 
                 boos=T, mfinal=1)
  print("finished modeling")
  pred_label = predict(ad, test_data, type="response")
  # pred_label has three attributes, prob, class, confusion
  print("finished prediction")
  return(pred_label)
}

gbm_boost <- function(train_data, test_data) {
  #print(train_data)
  ad <- gbm(formula=category ~ ., data=train_data, 
                 n.trees=50, train.fraction = 0.9)
  print("finished modeling")
  pred_label = predict(ad, test_data, type="response")
  print(pred_label)
  #pred_probs = predict(ad, test_data)
  #print (pred_label[1:10])
  #print (pred_probs[1:10])
  # pred_label has three attributes, prob, class, confusion
  print("finished prediction")
  return(pred_label)
}

logistic <- function(train_data, test_data, cut_off=0.5) {
  logit <- multinom(category ~ ., data = train_data)
  class = predict(logit, test_data, type="class")
  prob = predict(logit, test_data, type="probs")
  cm = confusionMatrix(class, test_data$category)
  return(list(class=class, prob=prob, confusion=cm$table))
}

fast_adaboost_model <- function(train_data, test_data) {
  print(train_data$category)
  ad <- adaboost(formula=category ~ ., data=train_data, nIter=50)
  print("finished modeling")
  pred_label = predict(ad, test_data, type="response")
  # pred_label has three attributes, prob, class, confusion
  print("finished prediction")
  return(pred_label)
}

random_forest_model <- function(train_data, test_data) {
  
  rf <- randomForest(formula=category ~ ., data=train_data, mtry=ncol(train_data)-1, 
                     ntree=25)
  pred_prob = predict(rf, test_data, type="prob")
  
  pred_label = predict(rf, test_data, type="response")
  
  ground_truth = test_data$category
  cm = confusionMatrix(pred_label, ground_truth)

  return(list(confusion_matrix=cm$table, pred_label=pred_label, pred_prob=pred_prob))
}

get_balanced_sample <- function(train_data) {
  cat_1_rows = train_data[which(train_data$category == "1"), ]
  cat_2_rows = train_data[which(train_data$category == "2"), ]
  cat_3_rows = train_data[which(train_data$category == "3"), ]
  min_rows_to_sample = 15000
  sampled_data = rbind(cat_1_rows[sample(min_rows_to_sample), ], 
                       cat_2_rows[sample(min_rows_to_sample), ],
                       cat_3_rows[sample(min_rows_to_sample), ])
  
  sampled_data <- sampled_data[sample(nrow(sampled_data)), ] # Randomize the data
  return(sampled_data)
}


balanced_model <- function(train_data, test_data , prediction_f_name, year) {
  train_data <- train_data[sample(nrow(train_data)), ]
  result <- c()

  cat1_label = rep("0", nrow(test_data))
  cat2_label = rep("0", nrow(test_data))
  cat3_label = rep("0", nrow(test_data))


  cat1_label[which(test_data$category == "1")] = "1"
  cat2_label[which(test_data$category == "2")] = "1"
  cat3_label[which(test_data$category == "3")] = "1"
  cat1_label = as.factor(cat1_label)
  cat2_label = as.factor(cat2_label)
  cat3_label = as.factor(cat3_label)
  print('Finished Processing labels')  
  
  predictions_log = c()
  for (idx in seq(1)) {
    sampled_train <- get_balanced_sample(train_data)
    #print(sampled_train$category)
    #pred <- logistic(sampled_train, test_data)
    pred <- adaboost_model(sampled_train, test_data)
    if (nrow(pred$confusion) > 2) {
      prec_and_rec = confusion_matrix_prec(pred$confusion)
      print("BOOST")
      print(pred$confusion)
      experiment_id <- paste("ada_multi", year, idx , nrow(sampled_train), sep="_")
      
      #m_auc = multi_proc_auc(pred$prob, test_data$category)
      #print(cat1_label)
      labels = list(cat1=cat1_label, cat2=cat2_label, cat3=cat3_label)
      mult_auc = multi_class_auc(labels, pred$prob)
      print (mult_auc)
      predict_dump = data.frame(exp_id=experiment_id, 
                                rln=test_data$rln, 
                                original_cat=test_data$category, 
                                converted_cat=as.character(test_data$category),
                                predicted_cat=as.character(pred$class), 
                                class_prob=pred$prob, auc=mult_auc)
      
      
      predictions_log <- rbind(predictions_log, predict_dump)
      
      #result <- rbind(result, c(experiment_id, prec_and_rec, m_auc$auc))
      result <- rbind(result, c(experiment_id, prec_and_rec, mult_auc))
    }
  }
  print(result)
  write.csv(result, prediction_f_name, row.names=F)
  write.csv(predictions_log, prediction_f_name, row.names=F)
  
}


one_vs_all <- function(train_data, test_data, pred_file, auc_file, exp_tag, year, sample=T) {
  train_data <- train_data[sample(nrow(train_data)), ]
  result <- c()
  predictions_log <- c()
  print('Finished Processing labels')  

  for (idx in seq(1)) {
    if(sample) 
      sampled_train <- get_balanced_sample(train_data)
    else
      sampled_train <- train_data
    
    for (lev in list(c("2"), c("3"), c("2","3"), c("1"))) {
      sample_train_clone <- sampled_train[,]
      test_data_clone <- test_data[,]
      
      sample_train_clone[which(sample_train_clone$category %in% lev), "new_category"] = "1"  
      sample_train_clone[-which(sample_train_clone$category  %in%  lev), "new_category"] = "0"  
      sample_train_clone = subset(sample_train_clone, select=-c(category))
      sample_train_clone = rename(sample_train_clone, c("new_category" = "category"))
      sample_train_clone$category <- as.factor(sample_train_clone$category)
      
      
      test_data_clone[which(test_data_clone$category  %in% lev), "new_category"] = "1"
      test_data_clone[-which(test_data_clone$category %in% lev), "new_category"] = "0"  
      test_data_clone = subset(test_data_clone, select=-c(category))
      test_data_clone = rename(test_data_clone, c("new_category" = "category"))
      test_data_clone$category <- as.factor(test_data_clone$category)
  
      print("start of model")

      pred <- fast_adaboost_model(sample_train_clone, test_data_clone)
      #pred <- logistic(sampled_train, test_data)
      lev_str = paste(lev, sep="_" ,collapse="_")
      
      experiment_id <- paste("log", "col_removed", exp_tag ,"level",lev_str, 'yr', year, 
                             "train_sz",nrow(sample_train_clone), sep="_")

      predict_dump = data.frame(exp_id=experiment_id, rln=test_data_clone$rln, original_cat=test_data$category, 
                                converted_cat=as.character(test_data_clone$category),
                                predicted_cat=as.character(pred$class), 
                                class_prob=pred$prob)
      
      
      predictions_log <- rbind(predictions_log, predict_dump)
      
      print("BOOST")
      print(experiment_id)
      confusion <- table(pred$class,test_data_clone$category)
      print(confusion)
        
      recall = confusion[2,2] / (confusion[1,2] +confusion[2,2])
      precision =  confusion[2,2] / (confusion[2,1] +confusion[2,2])

      auc = auc(roc(pred$prob[,2], test_data_clone$category))
      print(auc)
      result <- rbind(result, list(experiment_id = experiment_id, 
                                    positive_class = lev_str,
                                    precision=precision, 
                                    recall = recall,
                                    auc=auc))
      
    }
  }
  
  print(result)
  write.csv(result, auc_file, row.names=F)
  write.csv(predictions_log, pred_file, row.names=F)
  
}

load_data <- function(train_file_name) {
  train_data = read.csv(train_file_name, header=T)

  train_data = rename(train_data, c("ED_ADMIT_NEXT_VISIT_CNT_BUCKET_2010" = "category",
                                    
                                    "NUM_EDADMIT_2009" = "NUM_EDADMIT", "NUM_ADMIT_2009"="NUM_ADMIT"))
  
  train_data = subset(train_data, select=-c(rln, distance_6_20,
                                            category_gt_eq_4, 
                                            ED_ADMIT_NEXT_VISIT_CNT_2010))
  train_data$category[train_data$category == 0 ] = 1

  train_data$category <- as.factor(train_data$category)
  return(train_data)  
}

main <- function(train_file_name, test_file_name, pred_file) {
  train_data = read.csv(train_file_name, header=T)
  test_data = read.csv(test_file_name, header=T)

  train_data = rename(train_data, c("ED_ADMIT_NEXT_VISIT_CNT_BUCKET_2010" = "category",
                                    
                                    "NUM_EDADMIT_2009" = "NUM_EDADMIT", "NUM_ADMIT_2009"="NUM_ADMIT"))

  train_data = subset(train_data, select=-c(rln, distance_6_20,
                                            category_gt_eq_4, 
                                            ED_ADMIT_NEXT_VISIT_CNT_2010))
  
  test_data = rename(test_data, c("ED_ADMIT_NEXT_VISIT_CNT_BUCKET_2013" = "category",
                                  "NUM_EDADMIT_2012" = "NUM_EDADMIT", 
                                  "NUM_ADMIT_2012"="NUM_ADMIT"))
  
  
  #test_data= subset(test_data, select=-c(rln, category_gt_eq_4,
  #                                        distance_6_20,
  #                                        ED_ADMIT_NEXT_VISIT_CNT_2011))
  

  train_data$category[train_data$category == 0 ] = 1
  test_data$category[test_data$category == 0 ] = 1

  train_data$category <- as.factor(train_data$category)
  test_data$category <- as.factor(test_data$category)
  
  #balanced_model(train_data, test_data, "pred_ada_multiclass_2011.csv" , 2011)
  print("Running on Sampled data with columns")
  
  #one_vs_all(train_data, test_data, "predictions_all_cols_2012.csv", "one_vs_all_cols_2012.csv", 
  #           "sample_all_cols", 2012)

  train_data <- train_data[ , !(names(train_data) %in% med)]
  test_data <- test_data[ , !(names(test_data) %in% med)]
   
  print("Running on Sampled data after removing Med cols")
  balanced_model(train_data, test_data, "pred_ada_multiclass_2011.csv" , 2012)
  #one_vs_all(train_data, test_data, "predictions_med_rm_2012.csv",
  #           "one_vs_all_2012_med_rm.csv", 
  #           "med_rm", 2012)
  
  train_data <- train_data[ , !(names(train_data) %in% dis)]
  test_data <- test_data[ , !(names(test_data) %in% dis)]
  balanced_model(train_data, test_data, "pred_ada_multiclass_2011.csv" , 2012)
  print("Running on Sampled data after removing Med & Dist cols")
  #one_vs_all(train_data, test_data , "predictions_dist_rm_2012.csv","one_vs_all_2012_dist_rm.csv", 
  #           "dist_rm", 2012)
  #
  
  train_data <- train_data[ , !(names(train_data) %in% dem)]
  test_data <- test_data[ , !(names(test_data) %in% dem)]

  print("Running on Sampled data after removing Med & Dist & Dem cols")
  balanced_model(train_data, test_data, "pred_ada_multiclass_2011.csv" , 2012)
  #one_vs_all(train_data, test_data, "predictions_dem_rm_2012.csv",
  #           "one_vs_all_2012_dem_rm.csv", 
  #           "dem_rm", 2012)
  
}


args = commandArgs(trailingOnly=TRUE)
print(args)
if (length(args) == 2) {
    main(args[1], args[2])
}
