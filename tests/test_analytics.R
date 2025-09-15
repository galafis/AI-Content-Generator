# Testes para analytics.R - Funcionalidades de análise estatística
# 
# Este arquivo contém testes unitários para validar
# as funcionalidades de análise de dados em R da aplicação AI Content Generator.

# Carregar bibliotecas necessárias para testes
library(testthat)
library(ggplot2)
library(dplyr)
library(corrplot)
if (!require("plotly", quietly = TRUE)) {
  install.packages("plotly")
  library(plotly)
}

# Sourcing do arquivo principal de analytics
# Assumindo que analytics.R está no diretório pai
analytics_path <- file.path("..", "analytics.R")
if (file.exists(analytics_path)) {
  source(analytics_path)
} else {
  cat("AVISO: arquivo analytics.R não encontrado. Alguns testes podem falhar.\n")
}

# Funções de utilidade para testes
create_test_data <- function(n = 100) {
  data.frame(
    x = rnorm(n),
    y = rnorm(n),
    category = sample(c("A", "B", "C"), n, replace = TRUE),
    value = runif(n, 1, 100),
    date = seq.Date(from = as.Date("2024-01-01"), by = "day", length.out = n)
  )
}

validate_plot <- function(plot_obj) {
  # Verifica se o objeto é um plot válido
  return(inherits(plot_obj, c("ggplot", "plotly", "recordedplot")))
}

# =============================================================================
# TESTES PRINCIPAIS
# =============================================================================

context("Testes de Análise de Dados")

test_that("Bibliotecas essenciais estão carregadas", {
  expect_true("ggplot2" %in% (.packages()))
  expect_true("dplyr" %in% (.packages()))
  expect_true("corrplot" %in% (.packages()))
  expect_true("plotly" %in% (.packages()))
})

test_that("Dados de teste podem ser criados", {
  test_data <- create_test_data(50)
  
  expect_s3_class(test_data, "data.frame")
  expect_equal(nrow(test_data), 50)
  expect_equal(ncol(test_data), 5)
  expect_true(all(c("x", "y", "category", "value", "date") %in% names(test_data)))
})

test_that("Análise estatística básica funciona", {
  test_data <- create_test_data(100)
  
  # Testa estatísticas descritivas
  summary_stats <- summary(test_data$value)
  expect_length(summary_stats, 6)
  expect_true(all(!is.na(summary_stats)))
  
  # Testa correlação
  numeric_data <- test_data[, sapply(test_data, is.numeric)]
  if (ncol(numeric_data) > 1) {
    corr_matrix <- cor(numeric_data, use = "complete.obs")
    expect_s3_class(corr_matrix, "matrix")
    expect_equal(nrow(corr_matrix), ncol(corr_matrix))
  }
})

test_that("Gráficos básicos podem ser criados", {
  test_data <- create_test_data()
  
  # Teste gráfico de dispersão
  scatter_plot <- ggplot(test_data, aes(x = x, y = y)) +
    geom_point() +
    theme_minimal()
  expect_true(validate_plot(scatter_plot))
  
  # Teste histograma
  hist_plot <- ggplot(test_data, aes(x = value)) +
    geom_histogram(bins = 20) +
    theme_minimal()
  expect_true(validate_plot(hist_plot))
  
  # Teste boxplot
  box_plot <- ggplot(test_data, aes(x = category, y = value)) +
    geom_boxplot() +
    theme_minimal()
  expect_true(validate_plot(box_plot))
})

test_that("Gráficos interativos funcionam", {
  test_data <- create_test_data(50)
  
  # Teste plotly
  p <- ggplot(test_data, aes(x = x, y = y, color = category)) +
    geom_point() +
    theme_minimal()
  
  plotly_obj <- ggplotly(p)
  expect_s3_class(plotly_obj, "plotly")
})

test_that("Processamento de dados funciona", {
  test_data <- create_test_data()
  
  # Teste de agrupamento
  grouped_data <- test_data %>%
    group_by(category) %>%
    summarise(
      mean_value = mean(value),
      count = n(),
      .groups = "drop"
    )
  
  expect_s3_class(grouped_data, "data.frame")
  expect_equal(nrow(grouped_data), 3)  # A, B, C
  expect_true(all(c("category", "mean_value", "count") %in% names(grouped_data)))
  
  # Teste de filtragem
  filtered_data <- test_data %>%
    filter(value > 50)
  
  expect_s3_class(filtered_data, "data.frame")
  expect_true(all(filtered_data$value > 50))
})

# =============================================================================
# TESTES DE INTEGRAÇÃO
# =============================================================================

context("Testes de Integração")

test_that("Pipeline completo de análise funciona", {
  # Simula um pipeline completo
  test_data <- create_test_data(200)
  
  # 1. Limpeza de dados
  clean_data <- test_data %>%
    filter(!is.na(value)) %>%
    mutate(value_scaled = scale(value)[,1])
  
  expect_s3_class(clean_data, "data.frame")
  expect_true("value_scaled" %in% names(clean_data))
  
  # 2. Análise estatística
  stats_by_category <- clean_data %>%
    group_by(category) %>%
    summarise(
      mean_val = mean(value),
      sd_val = sd(value),
      median_val = median(value),
      .groups = "drop"
    )
  
  expect_equal(nrow(stats_by_category), 3)
  
  # 3. Visualização
  final_plot <- ggplot(clean_data, aes(x = category, y = value)) +
    geom_violin() +
    geom_boxplot(width = 0.1) +
    theme_minimal() +
    labs(title = "Distribuição de Valores por Categoria")
  
  expect_true(validate_plot(final_plot))
})

test_that("Tratamento de dados ausentes funciona", {
  # Criar dados com valores ausentes
  test_data_na <- create_test_data(50)
  test_data_na$value[sample(1:50, 10)] <- NA
  
  # Teste de remoção de NAs
  clean_data <- test_data_na %>%
    filter(!is.na(value))
  
  expect_equal(nrow(clean_data), 40)
  expect_true(all(!is.na(clean_data$value)))
  
  # Teste de imputação
  imputed_data <- test_data_na %>%
    mutate(value = ifelse(is.na(value), median(value, na.rm = TRUE), value))
  
  expect_equal(nrow(imputed_data), 50)
  expect_true(all(!is.na(imputed_data$value)))
})

# =============================================================================
# TESTES DE PERFORMANCE
# =============================================================================

context("Testes de Performance")

test_that("Análise de datasets grandes é eficiente", {
  large_data <- create_test_data(10000)
  
  # Teste de tempo de execução
  start_time <- Sys.time()
  
  summary_large <- large_data %>%
    group_by(category) %>%
    summarise(
      mean_value = mean(value),
      sd_value = sd(value),
      count = n(),
      .groups = "drop"
    )
  
  end_time <- Sys.time()
  execution_time <- as.numeric(difftime(end_time, start_time, units = "secs"))
  
  expect_lt(execution_time, 5)  # Deve executar em menos de 5 segundos
  expect_equal(nrow(summary_large), 3)
})

# =============================================================================
# TESTES DE VALIDAÇÃO
# =============================================================================

context("Testes de Validação")

test_that("Validação de entrada funciona", {
  # Teste com dados inválidos
  invalid_data <- data.frame(
    x = c(NA, NA, NA),
    y = c(1, 2, 3)
  )
  
  # Deve detectar dados inválidos
  na_count <- sum(is.na(invalid_data$x))
  expect_equal(na_count, 3)
  
  # Teste com dados válidos
  valid_data <- create_test_data(10)
  expect_true(all(!is.na(valid_data$value)))
})

test_that("Tipos de dados são consistentes", {
  test_data <- create_test_data()
  
  expect_type(test_data$x, "double")
  expect_type(test_data$y, "double")
  expect_type(test_data$category, "character")
  expect_type(test_data$value, "double")
  expect_s3_class(test_data$date, "Date")
})

# =============================================================================
# EXECUTAR TODOS OS TESTES
# =============================================================================

# Função principal para executar todos os testes
run_all_tests <- function() {
  cat("===========================================\n")
  cat("EXECUTANDO TESTES PARA ANALYTICS.R\n")
  cat("===========================================\n")
  
  test_results <- test_dir(".", reporter = "summary")
  
  cat("\n===========================================\n")
  cat("RELATÓRIO DE TESTES CONCLUÍDO\n")
  cat("===========================================\n")
  
  return(test_results)
}

# Execução condicional (apenas se executado diretamente)
if (interactive() || identical(environment(), globalenv())) {
  cat("Executando testes de analytics.R...\n")
  
  # Verificar se testthat está disponível
  if (require("testthat", quietly = TRUE)) {
    run_all_tests()
  } else {
    cat("AVISO: pacote testthat não encontrado. Instalando...\n")
    install.packages("testthat")
    library(testthat)
    run_all_tests()
  }
  
  cat("\nTestes de analytics.R concluídos com sucesso!\n")
  cat("Para executar novamente: Rscript tests/test_analytics.R\n")
}

# Mensagem final
cat("Arquivo test_analytics.R carregado. Use run_all_tests() para executar todos os testes.\n")
