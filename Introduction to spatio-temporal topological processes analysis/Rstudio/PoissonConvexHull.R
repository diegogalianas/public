install.packages("sf")
install.packages("ggplot2")
install.packages("dplyr")
install.packages("png")

library(png)
library(sf)
library(ggplot2)
library(dplyr)

# Cargar el shapefile de Valencia
valencia_map <- st_read("C:/Users/Diego/Desktop/Valencia_shape/Road Network/valencia_road.shp")

# Cargar los datos CSV
data <- read.csv("C:/Users/Diego/Desktop/datasets/Valencia.csv")

# Convertir el DataFrame a un objeto sf
data_sf <- st_as_sf(data, coords = c("crime_lon", "crime_lat"), crs = st_crs(valencia_map))

# Cargar el shapefile del polígono delimitador
hull_map <- st_read("C:/Users/Diego/Desktop/Valencia_crime_hull.shp")

# Crear el plot

  ggplot() +
    geom_sf(data = valencia_map, fill = "white", color = "black") +  # Silueta de Valencia con fondo blanco y borde negro
    geom_sf(data = data_sf, aes(color = crime_type), size = 1) +  # Puntos de los crímenes con color según 'crime_type'
    geom_sf(data = hull_map, fill = NA, color = "blue", size = 1) +  # Polígono delimitador en azul
    theme_minimal(base_size = 15) +
    theme(panel.background = element_rect(fill = "white", color = NA),  # Fondo blanco
          plot.background = element_rect(fill = "white", color = NA),   # Fondo del gráfico blanco
          legend.position = "none")+   labs(color = NULL)  # Añadir título y leyenda de colores

dev.off()

# Guardar el plot
ggsave("ValenciaXD.png", width = 10, height = 8, bg = "white")



