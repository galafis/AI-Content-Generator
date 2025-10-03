# Advanced Analytics in R
# Author: Gabriel Demetrios Lafis
# Statistical analysis and data visualization

library(ggplot2)
library(dplyr)
library(corrplot)
library(plotly)

# Data Analysis Class
DataAnalyzer <- setRefClass("DataAnalyzer",
  fields = list(
    data = "data.frame",
    results = "list"
  ),
  methods = list(
    load_data = function(file_path) {
      data <<- read.csv(file_path)
      cat("Data loaded:", nrow(data), "rows\n")
    },
    
    analyze = function() {
      # Statistical summary
      summary_stats <- summary(data)
      
      # Correlation analysis
      numeric_cols <- sapply(data, is.numeric)
      cor_matrix <- NULL
      if(sum(numeric_cols) > 1) {
        cor_matrix <- cor(data[, numeric_cols], use = "complete.obs")
        # Removed direct call to corrplot
      }
      
      # Visualization (return ggplot object instead of printing)
      plot_obj <- NULL
      if(ncol(data) >= 2) {
        plot_obj <- ggplot(data, aes_string(x = names(data)[1], y = names(data)[2])) +
          geom_point(alpha = 0.6) +
          geom_smooth(method = "lm") +
          theme_minimal() +
          labs(title = "Data Analysis Visualization")
        # Removed direct call to print(p)
      }
      
      results <<- list(
        summary = summary_stats,
        correlation = cor_matrix,
        plot = plot_obj
      )
    },
    
    generate_report = function() {
      cat("=== Analytics Report ===\n")
      cat("Dataset shape:", dim(data), "\n")
      cat("Analysis completed successfully!\n")
    }
  )
)

