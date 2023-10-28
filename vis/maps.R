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
##Top 5 Populated Countries ##
#############################
top_countries <- data %>%
  group_by(iso3, region) %>%
  summarise(total_density = mean(pop_density)) %>%
  arrange(desc(total_density)) %>%
  head(10)

data$iso3 = factor(
  data$iso3,
  levels = c('GNB', 'SEN', 'NGA', 'TGO', 'KEN', 'MUS', 'MLI', 'NAM', 'BDI', 'BEN'),
  labels = c('Guinea Bissau', 'Senegal', 'Nigeria', 'Togo', 'Kenya', 
             'Mauritius', 'Mali', 'Namibia', 'Burundi', 'Benin'))


countries_10 <- ggplot(data = top_countries, aes(x = reorder(iso3, -total_density), y = total_density, fill = region)) +
  geom_bar(stat = 'identity', position = position_dodge(0.9)) + coord_flip() + 
  geom_text(aes(label = formatC(signif(after_stat(y), 3), 
                                digits = 3, format = "fg", flag = "#")),
            size = 1.8, position = position_dodge(0.9),
            vjust = 0.5, hjust = -0.3) + scale_fill_brewer(palette = "Set2") +
  labs(colour = NULL,
       title = 'Top 10 SSA Densely Populated Countries',
       x = NULL,
       fill = NULL) + ylab(expression('Number of People (km'^2*')')) +
  theme(legend.position = 'bottom',
        axis.text.x = element_text(size = 5),
        panel.spacing = unit(0.6, "lines"),
        plot.title = element_text(size = 11),
        plot.subtitle = element_text(size = 10),
        axis.text.y = element_text(size = 7),
        legend.title = element_text(size = 8),
        legend.text = element_text(size = 7),
        axis.title.x = element_text(size = 8),
        axis.title.y = element_markdown(size = 7)) +
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 5, title = 'SSA Regions')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0),
  labels = function(y) format(y, scientific = FALSE),limits = c(0, 5000)) 


#################################
##Bottom 5 Populated Countries ##
#################################
data <- read.csv(file.path(folder, '..', 'results', 'SSA', 'SSA_optimized_ev_center.csv'))
data <- data %>%
  mutate(value = c(1))

bottom_countries <- data %>%
  group_by(iso3, region) %>%
  summarise(total_density = mean(pop_density)) %>%
  arrange(desc(total_density)) %>%
  tail(10)

data$iso3 = factor(
  data$iso3,
  levels = c('GAB', 'MRT', 'COG', 'CAF', 'SOM', 'GIN', 'MOZ', 'ZMB', 'SSD', 'BFA'),
  labels = c('Gabon', 'Mauritania', 'Republic of Congo', 'Central African Republic', 
             'Somalia', 'Guinea', 'Mozambique', 'Zimbabwe', 'South Sudan', 'Burkina Fasso'))


countries_bottom_10 <- ggplot(data = bottom_countries, aes(x = reorder(iso3, -total_density), y = total_density, fill = region)) +
  geom_bar(stat = 'identity', position = position_dodge(0.9)) + coord_flip() + 
  geom_text(aes(label = formatC(signif(after_stat(y), 3), 
                                digits = 3, format = "fg", flag = "#")),
            size = 1.8, position = position_dodge(0.9),
            vjust = 0.5, hjust = -0.3) + scale_fill_brewer(palette = "Set2") +
  labs(colour = NULL,
       title = 'Bottom 10 SSA Populated Countries',
       x = NULL,
       fill = NULL) + ylab(expression('Number of People (km'^2*')')) +
  theme(legend.position = 'bottom',
        axis.text.x = element_text(size = 5),
        panel.spacing = unit(0.6, "lines"),
        plot.title = element_text(size = 11),
        plot.subtitle = element_text(size = 10),
        axis.text.y = element_text(size = 7),
        legend.title = element_text(size = 8),
        legend.text = element_text(size = 7),
        axis.title.x = element_text(size = 8),
        axis.title.y = element_markdown(size = 7)) +
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 5, title = 'SSA Regions')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0),
                     labels = function(y) format(y, scientific = FALSE),limits = c(0, 70)) 

#############################
##Top and Bottom Countries ##
#############################
countries_10 <-
  ggarrange(
    countries_10,
    countries_bottom_10,
    ncol = 2,
    common.legend = FALSE,
    labels = c('A', 'B'),
    legend = 'bottom'
  )


path = file.path(folder, 'figures', 'top_countries.png')
dir.create(file.path(folder, 'figures'), showWarnings = FALSE)
png(
  path,
  units = "in",
  width = 6,
  height = 6.5,
  res = 480
)
print(countries_10)
dev.off()

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
    size = 2,
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
    limits = c(0, 215)
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
    size = 2.,
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
    size = 2.,
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
  width = 6,
  height = 6.5,
  res = 480
)
print(ssa_results)
dev.off()


##########################
##Case Study Countries  ##
##########################
data <- read.csv(file.path(folder, '..', 'results', 'SSA', 'four_countries.csv'))
data <- data %>%
  mutate(value = c(1))

################################
## 4 Built EV Service Centers ##
################################
df = data %>%
  group_by(iso3, build) %>%
  summarize(total = sum(value))

df$build = factor(
  df$build,
  levels = c('Yes', 'No'),
  labels = c('Build EV Service Center', 'Do not Build EV Service Center')
)

df$iso3 = factor(
  df$iso3,
  levels = c('CMR', 'GHA', 'KEN', 'MOZ'),
  labels = c('Cameroon', 'Ghana', 'Kenya', 'Mozambique')
)

built_sites_4 <-
  ggplot(df,  aes(x = iso3, y = total, fill = build)) +
  geom_bar(width = 1, stat = "identity", position = position_dodge(0.9)) +
  geom_text(
    aes(label = total, digits = 3, format = "fg", flag = "#"),
    size = 2,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) +
  labs(
    colour = NULL,
    title = 'Proposed Number of Electric Vehicle (EV) Service Centers to be Built.',
    subtitle = 'Reported by African Union Regional Classification.',
    x = NULL,
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
    legend.title = element_text(size = 8),
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
    limits = c(0, 55)
  ) 


##########################################
## 4 Minimized Average Costs of EV Centers ##
##########################################
df = data %>%
  group_by(iso3) %>%
  summarize(ssa_mean = mean(minimized_cost))

df$iso3 = factor(
  df$iso3,
  levels = c('CMR', 'GHA', 'KEN', 'MOZ'),
  labels = c('Cameroon', 'Ghana', 'Kenya', 'Mozambique')
)

minimized_average_cost_4 <-
  ggplot(df,  aes(x = iso3, y = ssa_mean/1e6)) +
  geom_bar(width = 0.98, stat = "identity", position = position_dodge(0.9),
           fill = c("#66CC99", "#33CCCC", "#FF9966", "#FFFFCC")) +
  geom_text(
    aes(label = round(ssa_mean/1e6, 2), digits = 3, format = "fg", flag = "#"),
    size = 2.,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) + 
  labs(
    colour = NULL,
    title = 'Minimized Average Costs',
    subtitle = NULL,
    x = NULL,
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
    limits = c(0, 4.5)
  )


##########################################
##4 Minimized Total Costs of EV Centers ##
##########################################
df = data %>%
  group_by(iso3) %>%
  summarize(ssa_total = sum(minimized_cost))

df$iso3 = factor(
  df$iso3,
  levels = c('CMR', 'GHA', 'KEN', 'MOZ'),
  labels = c('Cameroon', 'Ghana', 'Kenya', 'Mozambique')
)

minimized_total_cost_4 <-
  ggplot(df,  aes(x = iso3, y = ssa_total/1e6)) +
  geom_bar(width = 0.98, stat = "identity", position = position_dodge(0.9),
           fill = c("#66CC99", "#33CCCC", "#FF9966", "#FFFFCC")) +
  geom_text(
    aes(label = round(ssa_total/1e6, 2), digits = 3, format = "fg", flag = "#"),
    size = 2.,
    position = position_dodge(0.9),
    vjust = 0.5,
    hjust = -0.1,
    angle = 90
  ) + 
  labs(
    colour = NULL,
    title = 'Minimized Total Costs',
    subtitle = NULL,
    x = NULL,
    y = "Number of EV Service Centers",
  ) +  ylab('Minimized Total Costs (million dollars)') + 
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
    limits = c(0, 450)
  )


##########################
##4 Africa cost Results ##
##########################
four_costs <-
  ggarrange(
    minimized_average_cost_4,
    minimized_total_cost_4,
    ncol = 2,
    common.legend = TRUE,
    labels = c('B', 'C'),
    legend = 'bottom'
  )

############################
##4 African Panel Results ##
############################
four_results <-
  ggarrange(
    built_sites_4,
    four_costs,
    nrow = 2,
    labels = c('A', 'B')
  )

path = file.path(folder, 'figures', 'four_ev_sites.png')
dir.create(file.path(folder, 'figures'), showWarnings = FALSE)
png(
  path,
  units = "in",
  width = 6,
  height = 6.5,
  res = 480
)
print(four_results)
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





