# Query incial para ver estructura de la table: variables y tipos de datos:

### Análisis de la estructura y los tipos de variables

El conjunto de datos `identity_raw` está compuesto por un total de 41 variables, que contienen información complementaria sobre la identidad y los dispositivos asociados a las transacciones financieras.

En cuanto a los tipos de datos, se observa un claro predominio de las variables numéricas de tipo `FLOAT64`, que representan aproximadamente el 68,29 % del total. Por su parte, las variables de tipo `STRING` constituyen el 19,51 %, mientras que las variables booleanas (`BOOL`) representan el 9,76 %. Finalmente, únicamente se identifica una variable de tipo `INT64`, equivalente al 2,44 %.

Esta distribución refleja una estructura de datos predominantemente numérica, aunque también incorpora información categórica y atributos binarios que permiten caracterizar diferentes aspectos de la identidad y los dispositivos utilizados.

Cabe destacar que `TransactionID`, almacenada como variable entera, desempeña una función identificativa y permite relacionar este conjunto de datos con la información transaccional. Por tanto, no se considera una variable explicativa para los análisis estadísticos posteriores.

En conjunto, la diversidad de tipos de datos hace necesario adaptar el análisis exploratorio a la naturaleza de cada variable, diferenciando entre el tratamiento estadístico de las variables numéricas, el análisis de frecuencias de las categóricas y el estudio de las variables booleanas.

# Query comprobar registros y duplicados

### Análisis de duplicados

El conjunto de datos `identity_raw` contiene un total de 144.233 registros, todos ellos asociados a un identificador de transacción único. La variable `TransactionID` no presenta valores nulos y tampoco se han detectado identificadores repetidos.

Por tanto, no se han identificado registros duplicados atendiendo a esta clave. Este resultado permite considerar que la integridad de los identificadores es adecuada y facilita la posterior integración de este conjunto de datos con la información transaccional mediante `TransactionID`.

### Análisis de valores nulos

El análisis de valores nulos muestra que la ausencia de información constituye una de las principales características del conjunto de datos `identity_raw`. Aunque algunas variables presentan una disponibilidad completa o prácticamente completa, otras contienen porcentajes de valores ausentes considerablemente elevados.

Destaca especialmente un grupo de nueve variables (`id_07`, `id_08`, `id_21`, `id_22`, `id_23`, `id_24`, `id_25`, `id_26` e `id_27`), cuyos porcentajes de valores nulos se sitúan aproximadamente entre el 96,42 % y el 96,71 %. Por tanto, estas variables únicamente contienen información en una pequeña proporción de los registros.

También se observan porcentajes elevados de ausencia en `id_18`, con un 68,72 % de valores nulos, y en `id_03` e `id_04`, ambas con un 54,02 %. Otras variables, como `id_33`, `id_09` e `id_10`, presentan porcentajes próximos al 48-49 %.

Por otro lado, existe un conjunto de variables con una disponibilidad considerablemente mayor. Entre ellas destacan `id_01`, `id_12` y `TransactionID`, que no presentan valores ausentes. Asimismo, variables como `id_35`, `id_36`, `id_37`, `id_38` e `id_15` presentan porcentajes de ausencia cercanos al 2,25 %.

En conjunto, estos resultados evidencian una distribución desigual de los valores ausentes entre las variables. Esta circunstancia deberá tenerse especialmente en cuenta durante la preparación de los datos, ya que la eliminación indiscriminada de registros o variables podría provocar una pérdida importante de información. Será necesario evaluar individualmente la utilidad de cada característica y seleccionar una estrategia de tratamiento de nulos adecuada.

# Analisis Estadistrico descriptivo

## Análisis descriptivo de las variables numéricas de `identity_raw`

Los resultados permiten identificar varios patrones importantes. No obstante, hay que tener presente que estas variables son de tipo `FLOAT64`, pero eso no significa necesariamente que todas sean variables continuas. Algunas presentan valores muy concentrados en determinados números, lo que podría indicar que representan categorías codificadas o atributos discretos.

### 1. Distribución y dispersión

En primer lugar, se observa una gran diferencia en las escalas de las variables:

- `id_02` presenta una media de 174.716,58 y una desviación estándar de 159.651,82. Además, sus valores oscilan entre 1 y 999.595, lo que refleja una dispersión considerable.
- `id_19` e `id_20` también presentan una variabilidad destacable, con desviaciones estándar de 141,10 y 152,16, respectivamente.
- En cambio, variables como `id_18`, `id_11`, `id_03` e `id_04` muestran una dispersión mucho menor.

Esto indica que las variables numéricas tienen escalas y comportamientos muy diferentes. Por tanto, si posteriormente se emplean modelos sensibles a la escala de las características, será necesario evaluar la aplicación de técnicas de normalización o estandarización.

### 2. Concentración de valores

Uno de los aspectos más relevantes es que varias variables presentan una fuerte concentración de observaciones en determinados valores.

Por ejemplo:

- `id_11` tiene una mediana y unos cuartiles Q1 y Q3 iguales a 100.
- `id_09`, `id_10`, `id_03` e `id_04` presentan una mediana igual a cero.
- `id_18` concentra sus valores centrales entre 13 y 15.
- `id_13` presenta una mediana de 52 y un tercer cuartil también igual a 52.

Esto sugiere que algunas variables podrían tener distribuciones discretas o estar dominadas por unos pocos valores frecuentes. En consecuencia, no sería suficiente analizar únicamente su media y desviación estándar: también convendría estudiar sus frecuencias y valores más habituales.

### 3. Posibles valores extremos

También se observan diferencias importantes entre los valores mínimos y los cuartiles:

- `id_01` alcanza un mínimo de -100, mientras que su primer cuartil es -10.
- `id_06` presenta un mínimo de -100, frente a una mediana de 0.
- `id_10` también alcanza -100, aunque sus tres cuartiles son iguales a 0.
- `id_14` presenta un máximo de 720, mientras que su mediana y tercer cuartil son -300.
- `id_05` oscila entre -72 y 52, aunque su mediana es 0.

Estas diferencias apuntan a la existencia de valores extremos o poco frecuentes. Sin embargo, no deben considerarse automáticamente errores o valores atípicos que deban eliminarse: podrían contener información relevante sobre el comportamiento de las transacciones o los dispositivos.

### 4. Variables con pocos registros disponibles

Los resultados también permiten comprobar el efecto de los valores nulos identificado anteriormente. Algunas variables cuentan con muy pocas observaciones:

- `id_24`: 4.747 valores disponibles.
- `id_25`: 5.132.
- `id_26`: 5.163.
- `id_21`: 5.159.
- `id_22`: 5.169.
- `id_07` e `id_08`: 5.155 cada una.

En comparación, otras variables presentan una disponibilidad mucho mayor, como `id_01`, que contiene información para los 144.233 registros, o `id_02`, con 140.872 observaciones.

Esta diferencia será importante al seleccionar las variables para el entrenamiento de los modelos, ya que algunas características podrían aportar información útil, pero también introducir una proporción elevada de valores ausentes.

### 5. Conclusión general

En conjunto, el análisis descriptivo pone de manifiesto que las variables numéricas de `identity_raw` presentan comportamientos heterogéneos. Se observan diferencias importantes en sus escalas, niveles de dispersión y concentración de valores. Algunas características muestran una variabilidad elevada, mientras que otras presentan distribuciones muy concentradas en determinados valores.

Asimismo, se identifican posibles valores extremos y una disponibilidad desigual de observaciones entre variables, aspectos que deberán tenerse en cuenta durante la preparación de los datos. En particular, será necesario evaluar tanto el tratamiento de los valores ausentes como la posible necesidad de escalar determinadas características.

Por último, dado que algunas variables presentan cuartiles coincidentes o una elevada concentración de valores, conviene estudiar sus distribuciones de frecuencia antes de aplicar técnicas estadísticas o modelos predictivos. Esto permitirá determinar si resulta más adecuado tratarlas como variables continuas o como atributos discretos.

# Analisis de frecuencias

### Análisis de frecuencias de las variables numéricas

El análisis de frecuencias permite profundizar en el comportamiento de algunas variables numéricas que, durante el estudio descriptivo, mostraban una elevada concentración de valores.

En primer lugar, destacan las variables `id_03`, `id_04`, `id_09` e `id_10`, donde el valor cero representa entre el 93,93 % y el 99,12 % de las observaciones disponibles. Este resultado evidencia una distribución muy concentrada, especialmente en el caso de `id_04`, donde prácticamente la totalidad de los registros presentan el mismo valor.

La variable `id_11` también presenta una concentración significativa, ya que el 94,46 % de sus observaciones corresponden al valor 100. El resto de los registros se distribuye entre diferentes valores, principalmente próximos a dicho valor.

Por otro lado, `id_13` presenta una distribución más diversa, aunque también muestra cierta concentración en determinados valores. Destacan especialmente los valores 52 y 49, que representan conjuntamente aproximadamente el 66,34 % de las observaciones.

En conjunto, estos resultados ponen de manifiesto que algunas variables almacenadas como numéricas presentan un comportamiento predominantemente discreto y una distribución muy concentrada en determinados valores. Por este motivo, resulta conveniente considerar su naturaleza y distribución antes de seleccionar las técnicas de transformación y tratamiento que se aplicarán durante la preparación de los datos.

### Análisis de cardinalidad

El análisis de cardinalidad permite identificar diferencias significativas en la diversidad de valores de las variables que componen el conjunto `identity_raw`.

En primer lugar, destacan algunas variables con una elevada cardinalidad, como `id_02`, que presenta 115.655 valores distintos, así como `DeviceInfo`, con 1.786 valores diferentes. Otras características, como `id_19`, `id_20` e `id_11`, también presentan una diversidad considerable de valores.

Por otro lado, se identifican variables numéricas con una cardinalidad reducida, como `id_03`, `id_04`, `id_14` e `id_18`. Este comportamiento coincide con los resultados obtenidos en el análisis de frecuencias, donde se observaba una elevada concentración de registros en determinados valores.

En cuanto a las variables categóricas, algunas presentan únicamente dos o tres valores distintos, mientras que otras, como `id_30` e `id_33`, contienen un número considerablemente mayor de categorías. Las variables booleanas, por su propia naturaleza, presentan dos valores posibles.

En conjunto, estos resultados muestran que el conjunto de identidad combina características con diferentes niveles de cardinalidad y naturaleza estadística. Esta circunstancia deberá tenerse en cuenta durante la preparación de los datos, especialmente a la hora de seleccionar las técnicas de codificación de variables categóricas y las transformaciones aplicables a las variables numéricas.

# Frecuencias para variables categoricas

### Análisis de frecuencias de las variables categóricas

El análisis de frecuencias de las variables categóricas permite identificar la distribución de las distintas categorías presentes en el conjunto `identity_raw`.

En primer lugar, se observan diferencias importantes entre las variables relacionadas con la identidad. Mientras que `id_12` presenta un claro predominio de la categoría `NotFound`, con un 85,30 %, otras variables como `id_15` e `id_16` muestran distribuciones más equilibradas entre sus respectivas categorías.

Por su parte, `id_23` presenta un predominio de la categoría `IP_PROXY:TRANSPARENT`, que representa el 67,50 % de sus observaciones. También destaca `id_27`, donde el 99,73 % de los registros corresponden a la categoría `Found`, evidenciando una distribución muy concentrada.

En cuanto a las variables booleanas, se observan comportamientos heterogéneos. `id_35` e `id_38` presentan distribuciones relativamente equilibradas entre sus dos posibles valores, mientras que `id_36` está claramente dominada por el valor `false`, que representa el 95,09 % de los registros. En `id_37`, por el contrario, predomina el valor `true`, con un 78,34 %.

Finalmente, la variable `DeviceType` muestra un mayor predominio de dispositivos de escritorio (`desktop`), que representan el 60,48 % de las observaciones, frente al 39,52 % correspondiente a dispositivos móviles (`mobile`).

En conjunto, estos resultados muestran que las variables categóricas presentan diferentes grados de concentración y diversidad. Algunas tienen distribuciones relativamente equilibradas, mientras que otras están dominadas por una categoría mayoritaria. Estas características deberán tenerse en cuenta durante la preparación de los datos, especialmente al seleccionar las técnicas de codificación y valorar la información aportada por cada variable.

### frecuencias para id_30, id_31 y id_33

El análisis de las variables categóricas de mayor cardinalidad muestra una diversidad considerable en la información relacionada con los dispositivos utilizados durante las transacciones.

La variable DeviceInfo presenta la mayor cardinalidad, con 1.786 categorías distintas, aunque existe una concentración importante en valores como Windows, iOS Device y MacOS. Por su parte, id_30 recoge información sobre los sistemas operativos y sus versiones, destacando Windows 10 y Windows 7. La variable id_31 identifica los navegadores utilizados, con una presencia destacada de Chrome y Safari en distintas versiones.

Por último, id_33 recoge las resoluciones de pantalla, donde destacan especialmente 1920x1080 y 1366x768. Esta variable presenta la particularidad de que sus categorías pueden descomponerse en dimensiones numéricas de anchura y altura.

En conjunto, los resultados ponen de manifiesto la necesidad de estudiar distintas estrategias de transformación de estas variables antes de incorporarlas a los modelos predictivos. Entre las alternativas se encuentran la agrupación de categorías poco frecuentes, la consolidación de versiones y la extracción de características numéricas, con el objetivo de reducir la dimensionalidad sin perder información potencialmente relevante.

### id_34

La variable id_34 presenta cuatro categorías distintas relacionadas con el estado de coincidencia (match_status). La categoría match_status:2 concentra el 77,13 % de los registros no nulos, seguida de match_status:1, con un 22,33 %. Las categorías match_status:0 y match_status:-1 tienen una representación muy reducida, especialmente esta última, que aparece únicamente en tres registros.

Estos resultados muestran una distribución muy desequilibrada entre categorías. Por tanto, aunque su cardinalidad no supone un problema para la codificación, será necesario considerar la escasa representación de algunas categorías durante el posterior preprocesamiento y entrenamiento de los modelos.

---

### matriz correlaciones

El análisis de correlaciones de Pearson entre las variables numéricas de identity_raw muestra que, en términos generales, no existen relaciones lineales excesivamente elevadas entre la mayoría de las características.

La relación más destacada corresponde a id_03 e id_09, con una correlación positiva de 0,7108. También sobresalen las relaciones entre id_17 e id_22 (0,5920), id_21 e id_32 (-0,4310) e id_02 e id_17 (0,4130).

No obstante, es necesario considerar el número de observaciones utilizado en cada cálculo, ya que algunas correlaciones se obtienen a partir de un subconjunto relativamente reducido de registros debido a la presencia de valores ausentes.

En consecuencia, estos resultados permiten identificar posibles relaciones y redundancias entre características, aunque no justifican por sí solos la eliminación de variables. Será necesario complementar este análisis durante el preprocesamiento y la evaluación de los modelos predictivos.

### correlacion adicional entre id_03 e id_09

Las variables id_03 e id_09 presentan una correlación positiva elevada (0,7108). No obstante, se observa que el 94,80 % de las observaciones disponibles para ambas variables contienen simultáneamente el valor cero. Para comprobar si la relación estaba condicionada por esta concentración, se calculó nuevamente la correlación excluyendo los registros en los que alguna de las dos variables tomaba dicho valor. El resultado fue de 0,9193, lo que evidencia una asociación lineal positiva muy elevada también entre sus valores no nulos. Sin embargo, este último resultado se basa en 2.292 observaciones, por lo que debe interpretarse con cautela.

# Conclusiones

Yo daría por finalizado el EDA inicial de `identity_raw`. Hemos cubierto los aspectos más importantes y no veo necesario seguir profundizando antes de pasar a la otra tabla.

Hemos realizado un análisis bastante completo:

## 1. Conclusiones del EDA de `identity_raw`

Te propongo estas conclusiones para incorporar al TFM:

### Conclusiones del análisis exploratorio de `identity_raw`

El conjunto de datos `identity_raw` contiene **144.233 registros y 41 columnas**, incluyendo el identificador `TransactionID`, variables numéricas, categóricas y booleanas relacionadas con la información de identidad y del dispositivo utilizado durante las transacciones.

En primer lugar, se ha comprobado la integridad del identificador `TransactionID`, verificando que todos los registros contienen un valor no nulo y que no existen identificadores duplicados. Esto permite considerar esta columna como una clave adecuada para la posterior integración con el conjunto de transacciones.

Uno de los principales aspectos detectados es la **elevada presencia de valores ausentes**. Su distribución es muy desigual: mientras que algunas variables no presentan valores nulos, otras superan el 96 % de ausencia. Esta circunstancia deberá tenerse en cuenta durante la preparación de los datos, evitando eliminar indiscriminadamente variables que podrían aportar información relevante.

El análisis de las variables numéricas ha permitido identificar diferencias importantes en sus escalas, distribuciones y niveles de dispersión. Algunas presentan una elevada concentración de valores concretos, especialmente ceros y valores próximos a 100, mientras que otras muestran una mayor diversidad. También se han observado valores extremos que deberán evaluarse antes de aplicar posibles técnicas de transformación o tratamiento de datos.

Respecto a las variables categóricas, se han identificado tanto atributos de cardinalidad reducida, como los indicadores booleanos y el tipo de dispositivo, como otros de cardinalidad elevada, especialmente `DeviceInfo`, `id_30`, `id_31` e `id_33`. Estas últimas contienen información relacionada con sistemas operativos, navegadores, dispositivos y resoluciones de pantalla, por lo que podrían requerir procesos específicos de normalización o agrupación.

Por último, el análisis de correlaciones ha permitido detectar algunas relaciones lineales relevantes entre variables numéricas. Destaca especialmente la correlación entre `id_03` e `id_09` (0,7108), que aumenta hasta 0,9193 al considerar únicamente sus observaciones no nulas. También se han identificado otras asociaciones, como la existente entre `id_02` e `id_17` (0,4130). No obstante, estas relaciones no justifican por sí solas la eliminación de atributos, por lo que su posible redundancia deberá evaluarse en fases posteriores.

En conjunto, el análisis muestra que `identity_raw` contiene información potencialmente útil para la detección de fraude, aunque presenta importantes desafíos relacionados con los valores ausentes, la heterogeneidad de las variables y la cardinalidad de algunos atributos. Estos aspectos deberán abordarse durante las siguientes etapas del proceso ETL y de preparación del conjunto de datos.

## 2. ¿Falta algo antes de pasar a `transactions_raw`?

No considero imprescindible hacer más consultas ahora. Dejaría pendientes para una fase posterior:

- Tratamiento de valores nulos.
- Detección y tratamiento de valores atípicos.
- Codificación de variables categóricas.
- Evaluación de redundancia y selección de características.
- Análisis de la relación con `isFraud`.

Estas tareas tienen más sentido cuando tengamos una visión conjunta de los datos y de la variable objetivo.

## 3. Siguiente paso: EDA de `transactions_raw`

Repetiremos una estructura similar, pero tendremos que prestar especial atención a algunos aspectos adicionales:

1. Estructura: número de registros, columnas y tipos de datos.
2. Integridad: valores nulos, duplicados y unicidad de `TransactionID`.
3. Variable objetivo: distribución de `isFraud`, proporción de fraude y desbalanceo.
4. Variables numéricas: estadísticas descriptivas, distribuciones y valores extremos.
5. Variables categóricas: cardinalidad y frecuencias.
6. Correlaciones: relaciones entre variables numéricas y posibles redundancias.
7. Análisis específico del fraude: diferencias entre transacciones fraudulentas y legítimas.

Una diferencia importante: en `transactions_raw` quiero que demos bastante más protagonismo a `isFraud`. No basta con describir las variables: necesitamos empezar a entender qué características distinguen las transacciones fraudulentas.

Podemos empezar por la estructura y los tipos de datos de `transactions_raw`, igual que hicimos con `identity_raw`.