library(dplyr)
library(ggplot2)
library(xgboost)
library(caret)

# Step 1: Pull in data from baseball savant
data <- read.csv("total_savant_data2.csv")

# Adjust xwOBA for swinging strikes
data <- data %>%
  mutate(estimated_woba_using_speedangle = ifelse(description %in% c('swinging_strike', 'swinging_strike_blocked'),
                                                  0, estimated_woba_using_speedangle))

# Step 2: Feature engineering
data2 <- data %>%
  mutate(xwOBA = estimated_woba_using_speedangle,
         plate_x = plate_x * -1) %>% #Flip this to be from pitcher's angle
  select(player_name, pitch_type, plate_x, plate_z, xwOBA) %>%
  filter(!is.na(xwOBA))

# Cut up by pitch type
Fastballs <- data2 %>%
  filter(pitch_type %in% c('FF', 'SI'))

Breaking_Balls <- data2 %>% 
  filter(pitch_type %in% c('CU','SL','FC','ST','KC','SV'))

Off_Speeds <- data2 %>%
  filter(pitch_type %in% c('CH','FS','FO'))

create_location_plus_model <- function(pitch_data, pitch_type_name) {
  set.seed(42)
  
  # Split data
  train_index <- createDataPartition(pitch_data$xwOBA, p = 0.8, list = FALSE)
  train_data <- pitch_data[train_index, ]
  test_data <- pitch_data[-train_index, ]
  
  # Ensure only numeric columns are used for modeling
  numeric_train_data <- train_data %>% select_if(is.numeric)
  numeric_test_data <- test_data %>% select_if(is.numeric)
  
  # Define parameters for tuning
  tune_grid <- expand.grid(
    nrounds = c(150),
    max_depth = c(4, 6, 8),
    eta = c(0.01, 0.1, 0.3),
    gamma = c(0, 0.1, 0.2),
    colsample_bytree = c(0.5, 0.7, 1),
    min_child_weight = c(1, 5, 10),
    subsample = c(0.5, 0.7, 1)
  )
  
  # Train the model with hyperparameter tuning
  xgb_train_control <- trainControl(method = "cv", number = 5, verboseIter = TRUE)
  
  xgb_model <- train(
    x = as.matrix(numeric_train_data %>% select(-xwOBA)),
    y = train_data$xwOBA,
    method = "xgbTree",
    trControl = xgb_train_control,
    tuneGrid = tune_grid
  )
  
  # Get the best model
  best_xgb_model <- xgb_model$finalModel
  
  # Save the best model to an RDS file
  model_filename <- paste0(pitch_type_name, "_locationPlus.rds")
  saveRDS(best_xgb_model, file = model_filename)
  
  # Add predictions to the original data
  pitch_data <- pitch_data %>% 
    mutate(predicted_xwOBA = predict(best_xgb_model, newdata = as.matrix(pitch_data %>% select_if(is.numeric) %>% select(-xwOBA)), iteration_range = 1:nrow(best_xgb_model$evaluation_log)))
  
  # Calculate the mean and standard deviation of predicted xwOBA
  avg_predicted_xwOBA <- mean(pitch_data$predicted_xwOBA)
  std_predicted_xwOBA <- sd(pitch_data$predicted_xwOBA)
  
  # Calculate location scores using the new formula
  pitch_data <- pitch_data %>%
    mutate(location_score = -1 * ((predicted_xwOBA - avg_predicted_xwOBA) / std_predicted_xwOBA) * 10 + 100)
  
  # Create heatmap data by averaging location scores for each location
  heatmap_data <- pitch_data %>%
    group_by(plate_x, plate_z) %>%
    summarize(mean_location_score = mean(location_score), .groups = "drop")
  
  # Define the strike zone boundaries
  top <- 3.7
  bottom <- 1.5
  left <- -17/24
  right <- 17/24
  
  # Generate grid of points for prediction
  x_grid <- seq(-2, 2, by = 0.005)
  y_grid <- seq(0, 6, by = 0.005)
  grid <- expand.grid(plate_x = x_grid, plate_z = y_grid)
  
  # Predict xwOBA for each point in the grid
  grid_predictions <- grid %>%
    mutate(predicted_xwOBA = predict(best_xgb_model, newdata = as.matrix(grid), iteration_range = 1:nrow(best_xgb_model$evaluation_log))) %>%
    mutate(location_score = -1 * ((predicted_xwOBA - avg_predicted_xwOBA) / std_predicted_xwOBA) * 10 + 100)
  
  # Create heatmap data for the grid
  heatmap_grid_data <- grid_predictions %>%
    group_by(plate_x, plate_z) %>%
    summarize(mean_location_score = mean(location_score), .groups = "drop")
  
  # Create the heatmap with the strike zone for the grid
  heatmap_with_strike_zone_grid <- ggplot() +
    geom_tile(data = heatmap_grid_data, aes(x = plate_x, y = plate_z, fill = mean_location_score)) +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 100, name = "Location Score (%)") +
    labs(title = paste(pitch_type_name, "Grid Location Score Heatmap with Strike Zone"), x = "Plate X", y = "Plate Z") +
    geom_rect(aes(xmin = left, xmax = right, ymin = bottom, ymax = top), 
              color = "black", fill = NA, linetype = "solid", size = 1) +  # Draw the strike zone
    coord_fixed() +  # Ensure the aspect ratio is 1:1
    theme_minimal()
  
  # Display the grid heatmap plot
  print(heatmap_with_strike_zone_grid)
  
  # Return the pitch data with predictions and location scores
  return(pitch_data)
}

# Apply the model to different pitch types
Fastballs <- create_location_plus_model(Fastballs, "Fastballs")
Breaking_Balls <- create_location_plus_model(Breaking_Balls, "Breaking Balls")
Off_Speeds <- create_location_plus_model(Off_Speeds, "Off Speeds")

# Calculate and print the mean predicted xwOBA for each group
Fastball_mean_predicted_xwOBA <- mean(Fastballs$predicted_xwOBA)
Fastball_std_predicted_xwOBA <- sd(Fastballs$predicted_xwOBA)
print(paste("Fastballs Mean Predicted xwOBA:", Fastball_mean_predicted_xwOBA, "Std:", Fastball_std_predicted_xwOBA))

Breaking_Balls_mean_predicted_xwOBA <- mean(Breaking_Balls$predicted_xwOBA)
Breaking_Balls_std_predicted_xwOBA <- sd(Breaking_Balls$predicted_xwOBA)
print(paste("Breaking Balls Mean Predicted xwOBA:", Breaking_Balls_mean_predicted_xwOBA, "Std:", Breaking_Balls_std_predicted_xwOBA))

Off_Speeds_mean_predicted_xwOBA <- mean(Off_Speeds$predicted_xwOBA)
Off_Speeds_std_predicted_xwOBA <- sd(Off_Speeds$predicted_xwOBA)
print(paste("Off Speeds Mean Predicted xwOBA:", Off_Speeds_mean_predicted_xwOBA, "Std:", Off_Speeds_std_predicted_xwOBA))
