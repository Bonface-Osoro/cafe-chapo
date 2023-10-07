library(ggplot2)
library(sf)

suppressMessages(library(tidyverse))
folder <- dirname(rstudioapi::getSourceEditorContext()$path)
data <- read.csv(file.path(folder, '..', 'results', 'final', 'KEN', 'population', 'KEN_population_results.csv'))

data_sf <- st_as_sf(data, coords = c('longitude', 'latitude'), crs = 4326)
base_map <- ggplot() + geom_blank(data = data_sf) + coord_quickmap()

map <- base_map +
  geom_sf(data = data_sf, aes(), color = "blue", size = 3) +
  labs(title = "GeoDataFrame Plot")