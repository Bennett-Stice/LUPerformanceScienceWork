library(dplyr)
library(baseballr)
library(xgboost)
library(caret)

# Step 1: Pull in data set from baseball savant
data <- read.csv("total_savant_data2.csv")

# Adjust xwOBA for swinging strikes
data <- data %>%
  mutate(estimated_woba_using_speedangle = ifelse(description %in% c('swinging_strike', 'swinging_strike_blocked'),
                                                  0, estimated_woba_using_speedangle))

# Step 2: Feature engineering
data2 <- data %>%
  mutate(horizontal_movement = pfx_x * -1, #Flip this to get movement from pitcher view
         vertical_movement = pfx_z,
         xwOBA = estimated_woba_using_speedangle,
         release_pos_x = release_pos_x * -1) %>%
  select(player_name, pitch_type, release_speed, release_pos_x, release_pos_z, release_spin_rate,
         horizontal_movement, vertical_movement, xwOBA) %>%
  filter(!is.na(xwOBA))

# Cut up pitches into buckets
Fastballs <- data2 %>%
  filter(pitch_type %in% c('FF', 'SI'))

Breaking_Balls <- data2 %>% 
  filter(pitch_type %in% c('CU','SL','FC','ST','KC','SV'))

Off_Speed <- data2 %>%
  filter(pitch_type %in% c('CH','FS','FO'))

create_stuff_plus_model <- function(pitch_data, pitch_type_name) {
  set.seed(42)
  
  # Split data
  train_index <- createDataPartition(pitch_data$xwOBA, p = 0.8, list = FALSE)
  train_data <- pitch_data[train_index, ]
  test_data <- pitch_data[-train_index, ]
  
  # Ensure only numeric columns are used for modeling
  numeric_train_data <- train_data %>% select_if(is.numeric)
  numeric_test_data <- test_data %>% select_if(is.numeric)
  
  # Define the grid of hyperparameters
  tune_grid <- expand.grid(
    nrounds = c(50, 100, 150),
    eta = c(0.01, 0.1, 0.3),
    max_depth = c(3, 6, 9),
    gamma = c(0, 0.1, 0.2),
    colsample_bytree = c(0.5, 0.7, 1),
    min_child_weight = c(1, 5, 10),
    subsample = c(0.5, 0.7, 1)
  )
  
  # Set up training control with cross-validation
  train_control <- trainControl(
    method = "cv", 
    number = 5,  # 5-fold cross-validation
    verboseIter = TRUE
  )
  
  # Train the model with hyperparameter tuning
  xgb_model <- train(
    x = as.matrix(numeric_train_data %>% select(-xwOBA)),
    y = train_data$xwOBA,
    method = "xgbTree",
    trControl = train_control,
    tuneGrid = tune_grid
  )
  
  # Get the number of boosting rounds used by the best model
  best_nrounds <- xgb_model$bestTune$nrounds
  
  # Evaluate the model with iteration range
  predictions <- predict(xgb_model, newdata = as.matrix(numeric_test_data %>% select(-xwOBA)), iteration_range = c(1, best_nrounds))
  
  
  
  # Calculate RMSE
  rmse <- sqrt(mean((predictions - test_data$xwOBA)^2))
  print(paste(pitch_type_name, "RMSE:", rmse))
  
  # Calculate R-squared
  ss_total <- sum((test_data$xwOBA - mean(test_data$xwOBA))^2)
  ss_residual <- sum((test_data$xwOBA - predictions)^2)
  r_squared <- 1 - (ss_residual / ss_total)
  print(paste(pitch_type_name, "R-squared:", r_squared))
  
  # Add predictions to the original data
  pitch_data <- pitch_data %>% 
    mutate(predicted_xwOBA = predict(xgb_model, newdata = as.matrix(pitch_data %>% select_if(is.numeric) %>% select(-xwOBA))))
  
  # Feature importance and save the model
  importance_matrix <- xgb.importance(model = xgb_model$finalModel)
  xgb.plot.importance(importance_matrix)
  model_filename <- paste0(pitch_type_name, "_StuffPlusV3.rds")
  saveRDS(xgb_model, file = model_filename)
  
  return(pitch_data)
}


# Run the function for each pitch type and add the predicted xwOBA column
Fastballs <- create_stuff_plus_model(Fastballs, "Fastball")
Breaking_Balls <- create_stuff_plus_model(Breaking_Balls, "Breaking_Ball")
Off_Speed <- create_stuff_plus_model(Off_Speed, "Off_Speed")

Fastball_mean_predicted_xwOBA <- mean(Fastballs$predicted_xwOBA)
Breaking_Ball_mean_predicted_xwOBA <- mean(Breaking_Balls$predicted_xwOBA)
Off_Speed_mean_predicted_xwOBA <- mean(Off_Speed$predicted_xwOBA)

Fastballs_std_predicted_xwOBA <- sd(Fastballs$predicted_xwOBA)
Breaking_Balls_std_predicted_xwOBA <- sd(Breaking_Balls$predicted_xwOBA)
Off_Speeds_std_predicted_xwOBA <- sd(Off_Speed$predicted_xwOBA)

print(paste("Fastball Mean:", Fastball_mean_predicted_xwOBA, "Std:", Fastballs_std_predicted_xwOBA))
print(paste("Breaking Ball Mean:", Breaking_Ball_mean_predicted_xwOBA, "Std:", Breaking_Balls_std_predicted_xwOBA))
print(paste("Off Speed Mean:", Off_Speed_mean_predicted_xwOBA, "Std:", Off_Speeds_std_predicted_xwOBA))
