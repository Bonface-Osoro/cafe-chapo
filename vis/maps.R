library(ggplot2)
library(sf)

suppressMessages(library(tidyverse))
folder <- dirname(rstudioapi::getSourceEditorContext()$path)
data <- read.csv(file.path(folder, '..', 'results', 'final', 'KEN', 'population', 'KEN_population_results.csv'))

data_sf <- st_as_sf(data, coords = c('longitude', 'latitude'))