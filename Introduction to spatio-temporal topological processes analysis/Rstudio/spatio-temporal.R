install.packages("stpp")
update.packages(ask = FALSE)
sessionInfo()


library(stpp)
library(sf)
library(ggplot2)
library(dplyr)
library(spatstat.geom)  # Necesario para usar la función owin


# Cargar el archivo CSV
data <- read.csv("C:/Users/Diego/Desktop/datasets/Valencia_2018_AlarmasMujer_DAY_sorted.csv")

# Verificar que las columnas 'utm_x' y 'utm_y' sean numéricas
data$utm_x <- as.numeric(data$utm_x)
data$utm_y <- as.numeric(data$utm_y)

# Verificar si hay NA's en las columnas 'utm_x' y 'utm_y'
if (any(is.na(data$utm_x)) || any(is.na(data$utm_y))) {
  stop("Existen valores NA en las coordenadas. Por favor, revisa los datos.")
}

# Extraer las coordenadas de los puntos y el día
coords <- data %>% select(utm_x, utm_y) %>% as.matrix()
days <- as.numeric(data$day)

# Crear el objeto 3D para `stpp`
spatiotemporal_points <- as.3dpoints(coords[,1], coords[,2], days)

# Definir la región espacial usando owin
spatial_window <- owin(xrange = range(coords[,1]), yrange = range(coords[,2]))
spatial_window

# Extraer los valores de xrange y yrange del objeto spatial_window
xrange <- spatial_window$xrange
yrange <- spatial_window$yrange

# Crear la matriz de 4x2 con las coordenadas de los vértices del rectángulo
spatial_matrix <- matrix(c(xrange[1], yrange[1],  # (xmin, ymin) -> Esquina inferior izquierda
                           xrange[1], yrange[2],  # (xmin, ymax) -> Esquina superior izquierda
                           xrange[2], yrange[2],  # (xmax, ymax) -> Esquina superior derecha
                           xrange[2], yrange[1]), # (xmax, ymin) -> Esquina inferior derecha
                         ncol = 2, byrow = TRUE)
spatial_matrix
# Asignar nombres a las columnas
colnames(spatial_matrix) <- c("x", "y")


# Definir la región temporal como un vector con el rango de days
temporal_region <- range(days)
temporal_region
# Definir dist y times como secuencias numéricas
dist <- seq(0, min(diff(range(coords[,1])), diff(range(coords[,2])))/4, length.out = 50)
times <- seq(0, (max(days) - min(days))/4, length.out = 50)


# Intentar la llamada sin corrección
pcf_result <- PCFhat(xyt = spatiotemporal_points, 
                     s.region = spatial_matrix,
                     t.region = temporal_region,
                     dist = dist, 
                     times = times)
plotPCF(pcf_result)
# Plotear sin título ni anotación de corrección de borde
# Plotear sin título ni anotación de corrección de borde
plotPCF(pcf_result, type = "persp", theta = -180, phi = 10, main = "", sub = "")


