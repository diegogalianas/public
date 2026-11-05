# Instalar y cargar las bibliotecas necesarias
install.packages(c("sf", "spatstat", "ggplot2", "dplyr"))

library(sf)
library(spatstat)
library(ggplot2)
library(dplyr)

# Cargar el archivo CSV
data <- read.csv("C:/Users/Diego/Desktop/datasets/Valencia_2019_AlarmasMujer_DAY_sorted.csv")

# Redondear las coordenadas UTM a 2 decimales (por ejemplo) para evitar duplicados debido a la precisión
data$utm_x <- round(data$utm_x, 2)
data$utm_y <- round(data$utm_y, 2)

# Eliminar duplicados basados únicamente en la ubicación
data_unique <- data %>%
  distinct(utm_x, utm_y, .keep_all = TRUE)

# Convertir el DataFrame a un objeto sf
data_sf <- st_as_sf(data_unique, coords = c("utm_x", "utm_y"), crs = 32630) # Ajusta el CRS si es necesario

# Extraer las coordenadas de los puntos
coords <- st_coordinates(data_sf)

# Crear un objeto ppp (puntos espaciales) para spatstat
# Definir el marco de referencia para los puntos
window <- owin(range(coords[,1]), range(coords[,2]))

# Crear el objeto ppp
data_ppp <- ppp(coords[,1], coords[,2], window = window)

# Calcular la función de correlación de pares
pair_corr <- pcf(data_ppp)

# Calcular la función K
k_function <- Kest(data_ppp)

# Guardar la función de correlación de pares
png("Valencia_2019_AlarmasMujer_DAY_pcf.png", width = 800, height = 600)
plot(pair_corr, main = "AlarmasMujer2019 Pair Correlation Function (PCF)")
dev.off()

# Guardar la función K
png("Valencia_2019_AlarmasMujer_DAY_k.png", width = 800, height = 600)
plot(k_function, main = "AlarmasMujer2019 K Function")
dev.off()

window
