library(ggpubr)
library(ggplot2)
library(tidyverse)
library(ggtext)
library(readr)
library(png)
library(sf)

suppressMessages(library(tidyverse))
folder <- dirname(rstudioapi::getSourceEditorContext()$path)
data <- read.csv(file.path(folder, '..', 'results', 'SSA', 'SSA_optimized_ev_center.csv'))
data <- data %>%
  mutate(value = c(1))

#############################
##Built EV Service Centers ##
#############################
df = data %>%
  group_by(region, build) %>%
  summarize(total = sum(value))

df$build = factor(
  df$build,
  levels = c('Yes', 'No'),
  labels = c('Build EV Service Center', 'Do not Build EV Service Center')
)

built_sites <-
  ggplot(df,  aes(x = region, y = total, fill = build)) +
  geom_bar(width = 1, stat = "identity", position = position_dodge(0.9)) +
  geom_text(
    aes(label = total, digits = 3, format = "fg", flag = "#"),
    size = 3,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) +
  labs(
    colour = NULL,
    title = 'Proposed Number of Electric Vehicle (EV) Service Centers to be Built.',
    subtitle = 'Reported by African Union Regional Classification.',
    x = 'Sub-Saharan African Regions',
    y = "Number of EV Service Centers",
  ) +  ylab('Number of EV Service Centers') + 
  scale_fill_brewer(palette = "Set2") +
  theme(
    legend.position = 'bottom',
    axis.text.x = element_text(size = 8),
    panel.spacing = unit(0.6, "lines"),
    plot.title = element_text(size = 11),
    plot.subtitle = element_text(size = 10),
    axis.text.y = element_text(size = 8),
    axis.title.y = element_text(size = 8),
    legend.title = element_text(size = 6),
    legend.text = element_text(size = 8),
    axis.title.x = element_text(size = 9)
  ) +
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 6, title = 'Decision')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(
    expand = c(0, 0),
    labels = function(y)
      format(y, scientific = FALSE),
    limits = c(0, 212)
  ) 

##########################################
##Minimized Average Costs of EV Centers ##
##########################################
df = data %>%
  group_by(region) %>%
  summarize(ssa_mean = mean(minimized_cost))

minimized_average_cost <-
  ggplot(df,  aes(x = region, y = ssa_mean/1e6)) +
  geom_bar(width = 0.98, stat = "identity", position = position_dodge(0.9),
           fill = c("#66CC99", "#33CCCC", "#FF9966", "#FFFFCC")) +
  geom_text(
    aes(label = round(ssa_mean/1e6, 2), digits = 3, format = "fg", flag = "#"),
    size = 2.5,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) + 
  labs(
    colour = NULL,
    title = 'Minimized Average Costs',
    subtitle = NULL,
    x = 'Sub-Saharan African Regions',
    y = "Number of EV Service Centers",
  ) +  ylab('Minimized Average Costs (million dollars)') + 
  scale_fill_brewer(palette = "Paired") +
  theme(
    legend.position = 'bottom',
    axis.text.x = element_text(size = 8),
    panel.spacing = unit(0.6, "lines"),
    plot.title = element_text(size = 11),
    plot.subtitle = element_text(size = 10),
    axis.text.y = element_text(size = 8),
    axis.title.y = element_text(size = 8),
    legend.title = element_text(size = 6),
    legend.text = element_text(size = 8),
    axis.title.x = element_text(size = 9)
  ) +
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 6, title = 'Minimized Cost Type')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(
    expand = c(0, 0),
    labels = function(y)
      format(y, scientific = FALSE),
    limits = c(0, 8)
  )

##########################################
##Minimized Total Costs of EV Centers ##
##########################################
df = data %>%
  group_by(region) %>%
  summarize(ssa_total = sum(minimized_cost))

minimized_total_cost <-
  ggplot(df,  aes(x = region, y = ssa_total/1e9)) +
  geom_bar(width = 0.98, stat = "identity", position = position_dodge(0.9),
           fill = c("#66CC99", "#33CCCC", "#FF9966", "#FFFFCC")) +
  geom_text(
    aes(label = round(ssa_total/1e9, 2), digits = 3, format = "fg", flag = "#"),
    size = 2.5,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) + 
  labs(
    colour = NULL,
    title = 'Minimized Total Costs',
    subtitle = NULL,
    x = 'Sub-Saharan African Regions',
    y = "Number of EV Service Centers",
  ) +  ylab('Minimized Total Costs (billion dollars)') + 
  scale_fill_brewer(palette = "Paired") +
  theme(
    legend.position = 'bottom',
    axis.text.x = element_text(size = 8),
    panel.spacing = unit(0.6, "lines"),
    plot.title = element_text(size = 11),
    plot.subtitle = element_text(size = 10),
    axis.text.y = element_text(size = 8),
    axis.title.y = element_text(size = 8),
    legend.title = element_text(size = 6),
    legend.text = element_text(size = 8),
    axis.title.x = element_text(size = 9)
  ) +
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 6, title = 'Minimized Cost Type')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(
    expand = c(0, 0),
    labels = function(y)
      format(y, scientific = FALSE),
    limits = c(0, 3)
  )


####################################
##Sub-saharan Africa cost Results ##
####################################
ssa_costs <-
  ggarrange(
    minimized_average_cost,
    minimized_total_cost,
    ncol = 2,
    common.legend = TRUE,
    labels = c('B', 'C'),
    legend = 'bottom'
  )

#####################################
##Sub-saharan Africa Panel Results ##
#####################################
ssa_results <-
  ggarrange(
    built_sites,
    ssa_costs,
    nrow = 2,
    labels = c('A', 'B')
  )

path = file.path(folder, 'figures', 'ssa_ev_sites.png')
dir.create(file.path(folder, 'figures'), showWarnings = FALSE)
png(
  path,
  units = "in",
  width = 9.5,
  height = 7,
  res = 480
)
print(ssa_results)
dev.off()


########################
##Optimized Loactions ##
########################
ken <-
  readPNG(file.path(folder, 'figures', 'optimized', 'KEN_optimized_sites.png'))

moz <-
  readPNG(file.path(folder, 'figures', 'optimized', 'MOZ_optimized_sites.png'))

cmr <-
  readPNG(file.path(folder, 'figures', 'optimized', 'CMR_optimized_sites.png'))

gha <-
  readPNG(file.path(folder, 'figures', 'optimized', 'GHA_optimized_sites.png'))

### Kenya ###
kenya <- ggplot() + background_image(ken) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### MOZAMBIQUE ###
mozambique <- ggplot() + background_image(moz) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### CAMEROON ###
cameroon <- ggplot() + background_image(cmr) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### GHANA ###
ghana <- ggplot() + background_image(gha) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) + 
  ggspatial::annotation_north_arrow(location = "br")

### Combine the Four maps ###
comb_map <- ggarrange(kenya, mozambique, cameroon, ghana, ncol = 2, nrow = 2,
  common.legend = T, legend = "bottom", labels = c('A', 'B', 'C', 'D'))

###Save the combined image ###
path = file.path(folder, "figures", "Combined_optimized_maps.png")
dir.create(file.path(folder), showWarnings = FALSE)
png(path, units = "in", width = 12, height = 12., res = 300)
print(comb_map)
dev.off()


####################
##Demand Requests ##
####################
ken <-
  readPNG(file.path(folder, 'figures', 'KEN_annual_requests.png'))

moz <-
  readPNG(file.path(folder, 'figures', 'MOZ_annual_requests.png'))

cmr <-
  readPNG(file.path(folder, 'figures', 'CMR_annual_requests.png'))

gha <-
  readPNG(file.path(folder, 'figures', 'GHA_annual_requests.png'))

### Kenya ###
kenya <- ggplot() + background_image(ken) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### MOZAMBIQUE ###
mozambique <- ggplot() + background_image(moz) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### CAMEROON ###
cameroon <- ggplot() + background_image(cmr) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### GHANA ###
ghana <- ggplot() + background_image(gha) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) + 
  ggspatial::annotation_north_arrow(location = "br")

### Combine the Four maps ###
comb_map <- ggarrange(kenya, mozambique, cameroon, ghana, ncol = 2, nrow = 2,
                      common.legend = T, legend = "bottom", labels = c('A', 'B', 'C', 'D'))

###Save the combined image ###
path = file.path(folder, "figures", "Combined_demand_maps.png")
dir.create(file.path(folder), showWarnings = FALSE)
png(path, units = "in", width = 12, height = 12., res = 300)
print(comb_map)
dev.off()


####################
##Potential Sites ##
####################
ken <-
  readPNG(file.path(folder, 'figures', 'KEN_potential_sites.png'))

moz <-
  readPNG(file.path(folder, 'figures', 'MOZ_potential_sites.png'))

cmr <-
  readPNG(file.path(folder, 'figures', 'CMR_potential_sites.png'))

gha <-
  readPNG(file.path(folder, 'figures', 'GHA_potential_sites.png'))

### Kenya ###
kenya <- ggplot() + background_image(ken) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### MOZAMBIQUE ###
mozambique <- ggplot() + background_image(moz) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### CAMEROON ###
cameroon <- ggplot() + background_image(cmr) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### GHANA ###
ghana <- ggplot() + background_image(gha) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) + 
  ggspatial::annotation_north_arrow(location = "br")

### Combine the Four maps ###
comb_map <- ggarrange(kenya, mozambique, cameroon, ghana, ncol = 2, nrow = 2,
                      common.legend = T, legend = "bottom", labels = c('A', 'B', 'C', 'D'))

###Save the combined image ###
path = file.path(folder, "figures", "Combined_potential_sites_maps.png")
dir.create(file.path(folder), showWarnings = FALSE)
png(path, units = "in", width = 12, height = 12., res = 300)
print(comb_map)
dev.off()


####################
##Discarded Sites ##
####################
ken <-
  readPNG(file.path(folder, 'figures', 'KEN_discarded_sites.png'))

moz <-
  readPNG(file.path(folder, 'figures', 'MOZ_discarded_sites.png'))

cmr <-
  readPNG(file.path(folder, 'figures', 'CMR_discarded_sites.png'))

gha <-
  readPNG(file.path(folder, 'figures', 'GHA_discarded_sites.png'))

### Kenya ###
kenya <- ggplot() + background_image(ken) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### MOZAMBIQUE ###
mozambique <- ggplot() + background_image(moz) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### CAMEROON ###
cameroon <- ggplot() + background_image(cmr) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### GHANA ###
ghana <- ggplot() + background_image(gha) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) + 
  ggspatial::annotation_north_arrow(location = "br")

### Combine the Four maps ###
comb_map <- ggarrange(kenya, mozambique, cameroon, ghana, ncol = 2, nrow = 2,
                      common.legend = T, legend = "bottom", labels = c('A', 'B', 'C', 'D'))

###Save the combined image ###
path = file.path(folder, "figures", "Combined_discarded_sites_maps.png")
dir.create(file.path(folder), showWarnings = FALSE)
png(path, units = "in", width = 12, height = 12., res = 300)
print(comb_map)
dev.off()

########################
##SSA Potential Sites ##
########################
ssa_pop <-
  readPNG(file.path(folder, 'figures', 'SSA_population.png'))

ssa_sites <-
  readPNG(file.path(folder, 'figures', 'SSA_potential_sites.png'))

ssa_demand <-
  readPNG(file.path(folder, 'figures', 'SSA_avg_demand.png'))

### Sites ###
pop <- ggplot() + background_image(ssa_pop) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

sites <- ggplot() + background_image(ssa_sites) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) 

### Demand ###
demand <- ggplot() + background_image(ssa_demand) +
  theme(plot.margin = margin(t = 0, l = 0, r = 0, b = 0, unit = "cm")) + 
  ggspatial::annotation_north_arrow(location = "br")

### Combine the Two maps ###
two_maps <- ggarrange(sites, demand, ncol = 2,
                      common.legend = T, legend = "bottom", labels = c('B', 'C'))

three_maps <- ggarrange(pop, two_maps, nrow = 2,
                     common.legend = T, legend = "bottom", labels = c('A'))

###Save the combined image ###
path = file.path(folder, "figures", "Combined_SSA_sites_maps.png")
dir.create(file.path(folder), showWarnings = FALSE)
png(path, units = "in", width = 10, height = 11., res = 300)
print(three_maps)
dev.off()





