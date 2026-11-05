install.packages("sf")
install.packages("ggplot2")
install.packages("dplyr")



library(sf)
library(ggplot2)
library(dplyr)

# Cargar el shapefile de Valencia
valencia_map <- st_read("C:/Users/Diego/Desktop/Valencia_shape/Road Network/valencia_road.shp")

# Cargar los datos CSV
data <- read.csv("C:/Users/Diego/Desktop/datasets/Valencia_2018_AlarmasMujer_sampled.csv")

# Convertir el DataFrame a un objeto sf
data_sf <- st_as_sf(data, coords = c("crime_lon", "crime_lat"), crs = st_crs(valencia_map))

# Crear el plot
ggplot() +
  geom_sf(data = valencia_map, fill = "white", color = "black") +  # Silueta de Valencia con fondo blanco y borde negro
  geom_sf(data = data_sf, aes(color = "violet"), size = 1) +  # Puntos de los crímenes con color violeta
  theme_minimal(base_size = 15) +
  theme(panel.background = element_rect(fill = "white", color = NA),  # Fondo blanco
        plot.background = element_rect(fill = "white", color = NA),   # Fondo del gráfico blanco
        legend.position = "none",  # Sin leyenda
        plot.title = element_blank()) +  # Sin título
  labs(color = NULL)

# Guardar el plot
ggsave("ValenciaRandom1.png", width = 10, height = 8, bg = "white")


