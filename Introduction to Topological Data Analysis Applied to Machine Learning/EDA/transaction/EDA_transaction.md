# Schema

El análisis del esquema de la tabla transaction_raw, perteneciente al conjunto de datos fraud_detection de BigQuery, permite identificar la estructura y las características generales de las variables que componen el conjunto de datos de transacciones. En total, la tabla contiene 394 variables, que presentan una combinación de identificadores, atributos relacionados con las tarjetas, información temporal, importes económicos, características categóricas y variables numéricas anonimizadas.

En primer lugar, destaca la presencia de las variables principales que permiten identificar y contextualizar cada operación. TransactionID, almacenada como INT64, actúa como identificador de la transacción, mientras que isFraud, también de tipo INT64, representa la variable objetivo del problema de clasificación, indicando si una operación es fraudulenta o legítima. Por su parte, TransactionDT, igualmente almacenada como INT64, contiene información temporal codificada numéricamente, que permitirá estudiar la distribución de las operaciones a lo largo del tiempo. Finalmente, TransactionAmt, de tipo FLOAT64, recoge el importe económico de cada transacción y constituye una de las variables cuantitativas más relevantes para analizar el comportamiento de las operaciones.

En cuanto a la distribución de los tipos físicos de almacenamiento, se observa un predominio muy significativo de las variables FLOAT64, que representan 376 de las 394 columnas (95,43 %). Esta proporción se explica principalmente por la extensa presencia de las familias de variables C, D y V. No obstante, es importante señalar que el hecho de que una variable esté almacenada como FLOAT64 no implica necesariamente que tenga una naturaleza cuantitativa continua. Por ejemplo, atributos como card2, card3, card5, addr1 o addr2 pueden representar códigos o categorías expresados numéricamente, por lo que su interpretación debe realizarse atendiendo a su significado y no exclusivamente a su tipo de almacenamiento.

Las variables relacionadas con las tarjetas constituyen otro grupo relevante del conjunto de datos. Entre ellas encontramos card1, almacenada como INT64, junto con card2, card3 y card5, de tipo FLOAT64, así como card4 y card6, almacenadas como STRING. Estas variables recogen diferentes atributos y códigos asociados a las tarjetas utilizadas en las operaciones. Su diversidad de tipos físicos refleja que no toda la información categórica se encuentra representada mediante cadenas de texto, sino que parte de ella utiliza valores numéricos como códigos. Esta particularidad deberá tenerse en cuenta durante el preprocesamiento, especialmente al seleccionar las transformaciones adecuadas para las variables categóricas.

También se identifican variables relacionadas con la dirección y la localización, como addr1 y addr2, ambas de tipo FLOAT64, así como dist1 y dist2, que contienen información relacionada con distancias. A estas se añaden P_emaildomain y R_emaildomain, almacenadas como STRING, que representan dominios de correo electrónico asociados a la transacción. Este conjunto de atributos puede aportar información complementaria para caracterizar las operaciones y estudiar posibles patrones relacionados con la identidad o el comportamiento de los usuarios.

Por otro lado, las familias de variables C1–C14 y D1–D15, todas ellas de tipo FLOAT64, amplían considerablemente la información disponible. Las primeras están relacionadas con características de conteo o agregaciones, mientras que las segundas contienen información temporal asociada a diferencias o intervalos. Además, se encuentran las variables de la familia M, que combinan ocho atributos booleanos (M1–M3 y M5–M9) con una variable categórica de tipo STRING (M4). Estas variables permiten incorporar indicadores y características adicionales de las transacciones.

Uno de los elementos más destacados de la estructura es la presencia de 339 variables pertenecientes a la familia V (V1–V339), todas almacenadas como FLOAT64. Se trata de atributos numéricos anonimizados cuyo significado individual no puede determinarse a partir del esquema disponible. Aunque no sea posible interpretar directamente su contenido, su elevada representación dentro del conjunto de datos hace que deban conservarse y analizarse durante las siguientes fases del EDA, ya que podrían contener información relevante para la identificación de operaciones fraudulentas.

En relación con la estructura de almacenamiento, todas las columnas aparecen definidas con la propiedad is_nullable=YES. Esto significa que BigQuery permite que estas variables contengan valores nulos, pero no demuestra que existan registros con valores ausentes en la tabla. Por tanto, será necesario realizar un análisis específico de valores nulos para determinar su presencia real, cuantificar su frecuencia y evaluar su posible impacto sobre el posterior procesamiento de los datos.

En definitiva, la estructura de transaction_raw refleja un conjunto de datos de elevada dimensionalidad y con una gran variedad de atributos relacionados con las transacciones, sus características económicas, temporales y contextuales. El predominio de variables numéricas, junto con la existencia de categorías codificadas mediante números y atributos anonimizados, hace especialmente importante distinguir entre el tipo físico de almacenamiento y la naturaleza semántica de cada variable. Esta diferenciación permitirá evitar interpretaciones estadísticas incorrectas y establecer criterios adecuados para el tratamiento de cada atributo.

A partir de esta primera inspección, todavía no es posible extraer conclusiones sobre la calidad efectiva de los registros, la distribución de las variables, la existencia de duplicados, los valores ausentes o la presencia de observaciones atípicas. Estos aspectos deberán estudiarse en las siguientes etapas del análisis exploratorio. En particular, se comenzará comprobando la integridad de los registros y la unicidad de TransactionID, para posteriormente analizar los valores nulos, las estadísticas descriptivas, las distribuciones de las variables categóricas y las posibles anomalías del conjunto de datos. Todo ello permitirá obtener una visión más completa de la calidad y las características de los datos originales antes de abordar las tareas de limpieza, transformación e integración necesarias para construir el conjunto de datos definitivo destinado al modelo de detección de fraude.

# duplicados

La comprobación de integridad de la tabla transaction_raw muestra que contiene un total de 590.540 registros y que todos ellos presentan un identificador TransactionID único. No se han detectado identificadores nulos ni registros duplicados adicionales, por lo que cada operación queda identificada de forma unívoca dentro del conjunto de datos.

Este resultado permite considerar que la tabla presenta una correcta integridad respecto a su identificador principal, sin necesidad de aplicar procesos de eliminación de duplicados en esta fase del análisis. No obstante, esta comprobación únicamente garantiza la unicidad de TransactionID y no descarta posibles inconsistencias o valores ausentes en el resto de atributos.

### Análisis de valores ausentes

Una vez comprobada la integridad de los identificadores, se ha realizado un análisis de los valores ausentes de las 394 variables que componen la tabla `transaction_raw`. Para ello, se ha calculado el número de valores nulos y no nulos de cada atributo, así como el porcentaje de ausencia respecto al total de 590.540 registros.

Los resultados muestran que la presencia de valores ausentes constituye una de las principales características que deben tenerse en cuenta durante el posterior procesamiento del conjunto de datos. Sin embargo, su distribución es muy desigual entre las variables, ya que coexisten atributos prácticamente completos con otros que presentan porcentajes de ausencia superiores al 90 %.

Entre las variables más afectadas destaca `dist2`, con un 93,63 % de valores nulos, seguida de `D7`, con un 93,41 %. También presentan porcentajes muy elevados `D13`, `D14`, `D12`, `D6`, `D8` y `D9`, todas ellas pertenecientes a la familia de variables temporales `D`. Este comportamiento evidencia que determinados atributos relacionados con información temporal o de distancia únicamente están disponibles para una parte reducida de las transacciones.

Asimismo, se observa una presencia importante de valores ausentes en numerosas variables anonimizadas de la familia `V`. Algunas de ellas, como las comprendidas en determinados grupos de `V138` a `V166` y de `V322` a `V339`, presentan porcentajes de ausencia próximos al 86 %. Otros grupos registran porcentajes situados entre el 76 % y el 78 %, mientras que las primeras variables de esta familia muestran niveles de ausencia más moderados. La existencia de patrones similares de valores nulos entre distintas variables podría indicar que comparten condiciones de disponibilidad o características comunes en su generación, aunque sería necesario realizar un análisis adicional para confirmar esta relación.

También destacan algunos atributos categóricos y booleanos. Por ejemplo, `R_emaildomain` presenta un 76,75 % de valores ausentes, mientras que `P_emaildomain` registra un 15,99 %. Por su parte, variables como `M5`, `M7`, `M8` y `M9` superan el 58 % de ausencia. Estas diferencias muestran que la disponibilidad de información varía considerablemente incluso entre atributos pertenecientes a categorías similares.

En contraposición, existen variables que presentan una completitud muy elevada. Entre ellas se encuentran los atributos principales de la transacción, como `TransactionID`, `isFraud`, `TransactionDT`, `TransactionAmt` y `ProductCD`, que no contienen valores nulos. También destaca el comportamiento de las variables `C1`–`C14`, que presentan información completa en los 590.540 registros. Otros atributos relacionados con las tarjetas, como `card2`, `card3`, `card4`, `card5` y `card6`, presentan porcentajes de ausencia reducidos, inferiores al 2 %.

En conjunto, estos resultados muestran que los valores ausentes no se distribuyen de manera uniforme, sino que se concentran especialmente en determinadas familias de variables. Por tanto, no sería adecuado aplicar una única estrategia de tratamiento para todos los atributos. La eliminación indiscriminada de registros podría provocar una pérdida considerable de información, mientras que la eliminación automática de variables con un elevado porcentaje de valores nulos podría descartar características potencialmente relevantes para la detección de fraude.

Por este motivo, será necesario evaluar posteriormente cada variable teniendo en cuenta su naturaleza, su porcentaje de ausencia y su posible capacidad predictiva. También deberá analizarse si la ausencia de información presenta alguna relación con la variable objetivo `isFraud`, ya que el hecho de que un atributo esté ausente podría aportar información sobre el contexto de una transacción.

Finalmente, cabe señalar que no se han identificado variables completamente vacías, por lo que todas conservan algún grado de información aprovechable. En consecuencia, los resultados de este análisis servirán como base para definir las estrategias de limpieza e imputación durante las siguientes fases del procesamiento, evitando tomar decisiones prematuras sobre la eliminación de atributos o registros.

### Análisis descriptivo de las variables numéricas

El análisis descriptivo de las variables numéricas de la tabla `transaction_raw` permite obtener una primera aproximación a la estructura y las características estadísticas del conjunto de datos. Para ello, se han estudiado medidas de tendencia central y dispersión, percentiles, valores mínimos y máximos, así como la disponibilidad de información de cada variable. Los resultados muestran una considerable heterogeneidad en las distribuciones y en la calidad de los datos, aspectos que deberán tenerse en cuenta durante las posteriores etapas de preparación y modelización.

En primer lugar, las variables del grupo C (`C1-C14`) presentan una disponibilidad completa, sin valores nulos en ninguno de sus registros. Sin embargo, sus distribuciones muestran diferencias importantes entre las medias y las medianas. En varias de estas características, la mediana se sitúa en valores muy reducidos, mientras que la media es considerablemente superior. Por ejemplo, `C1` presenta una mediana de 1 frente a una media de 14,09, mientras que `C13` alcanza una media de 32,54 y una mediana de 3. Este comportamiento evidencia una distribución asimétrica hacia la derecha, en la que la mayoría de las observaciones presentan valores relativamente bajos, pero existen determinados registros con valores mucho más elevados. Esta característica también se refleja en los valores máximos, que alcanzan varios miles en algunas variables. Por tanto, aunque estas características no presentan problemas de disponibilidad, será necesario estudiar la influencia de sus valores extremos y evaluar si requieren algún tipo de transformación antes de incorporarlas a los modelos.

Por otro lado, las variables del grupo D (`D1-D15`) presentan un comportamiento especialmente heterogéneo en cuanto a la disponibilidad de información. Mientras que `D1` apenas presenta un 0,21 % de valores nulos, otras características superan ampliamente el 80 % de ausencia de datos. Destacan especialmente `D7`, con un 93,41 % de valores ausentes, y `D13` y `D14`, con porcentajes próximos al 90 %. Esta distribución desigual indica que la información disponible no es homogénea entre las distintas características. En consecuencia, no sería adecuado aplicar una única estrategia de tratamiento de valores ausentes a todo el conjunto de variables. Será necesario evaluar individualmente su porcentaje de ausencia y su posible utilidad predictiva antes de decidir si conviene conservarlas, imputarlas o descartarlas. Asimismo, se han identificado valores negativos en algunas de estas variables. Aunque podrían parecer atípicos a primera vista, no deben considerarse automáticamente errores, ya que sería necesario conocer con mayor precisión su significado y comportamiento para determinar si son registros válidos.

En relación con las variables principales de la transacción, `TransactionAmt` presenta una distribución claramente asimétrica hacia la derecha. Su media es de 135,03, mientras que su mediana se sitúa en 68,90, con un tercer cuartil de 125. Además, el valor máximo alcanza 31.937,39, muy por encima de los valores correspondientes a la mayor parte de las observaciones. Esta diferencia entre las medidas de tendencia central pone de manifiesto que existen transacciones con importes considerablemente superiores a los habituales. Desde el punto de vista estadístico, estos valores pueden influir notablemente en la media y en la desviación típica, por lo que resulta conveniente complementar su estudio mediante percentiles y representaciones gráficas. También será interesante evaluar posteriormente si una transformación de la variable permite reducir su asimetría y facilitar el aprendizaje de determinados algoritmos.

Por su parte, `TransactionDT` no presenta valores nulos y contiene información temporal codificada numéricamente. Su rango de valores permite identificar una dimensión temporal dentro del conjunto de datos, aunque su interpretación requiere tener en cuenta que no se trata directamente de una fecha convencional. Esta característica puede resultar especialmente relevante en un problema de detección de fraude, ya que permite estudiar la distribución de las transacciones a lo largo del periodo recogido y explorar posibles patrones temporales. En fases posteriores podrá transformarse para obtener representaciones temporales más interpretables y facilitar el análisis de la evolución de las operaciones.

Una parte especialmente relevante del conjunto de datos está formada por las variables anonimizadas del grupo V (`V1-V339`). El análisis de estas características revela una elevada heterogeneidad tanto en la disponibilidad de información como en sus propiedades estadísticas. Se identifican diferentes grupos de variables con porcentajes de valores nulos muy elevados, algunos superiores al 75 %, al 85 % e incluso al 90 %. Al mismo tiempo, existen otras características que presentan una disponibilidad prácticamente completa. Esta circunstancia resulta especialmente importante porque la ausencia de información puede reducir considerablemente el número de observaciones disponibles para determinados análisis si se opta por eliminar registros incompletos. Por ello, será necesario estudiar las variables y sus patrones de ausencia de forma individual, evitando aplicar criterios generales que puedan provocar una pérdida innecesaria de información.

En cuanto a sus distribuciones, numerosas variables del grupo V presentan una concentración muy elevada de valores en torno a cero y uno. En algunos casos, incluso los tres cuartiles se sitúan en cero o en uno, lo que indica que una parte importante de las observaciones comparte valores idénticos. Aunque estas características están almacenadas como variables numéricas de tipo `FLOAT64`, sus distribuciones sugieren que algunas pueden tener un comportamiento predominantemente discreto. Esta particularidad deberá considerarse al estudiar su variabilidad y su posible utilidad para los modelos, puesto que una variable con una distribución muy concentrada puede aportar información limitada en determinados contextos, aunque no necesariamente carezca de capacidad predictiva.

También se observan diferencias considerables en las escalas y rangos de estas variables. Mientras que algunas presentan valores máximos reducidos, otras alcanzan magnitudes superiores a 100.000. En determinados casos, la media y la desviación típica son considerablemente superiores a los valores que representan los percentiles centrales, lo que apunta a distribuciones fuertemente asimétricas y a la presencia de observaciones extremas. Esta heterogeneidad puede tener implicaciones en los algoritmos de aprendizaje automático que utilizan distancias o son sensibles a la escala de las características. Por este motivo, en las siguientes fases será conveniente evaluar la necesidad de aplicar técnicas de escalado o transformación, teniendo en cuenta las características y los requisitos de cada modelo.

Por último, se han identificado características con una variabilidad muy reducida, cuyos valores permanecen prácticamente constantes en la mayoría de las observaciones. Este comportamiento puede limitar la cantidad de información que aportan al proceso de aprendizaje, especialmente si apenas permiten distinguir entre diferentes transacciones. No obstante, su eliminación no debe realizarse únicamente a partir de las estadísticas descriptivas, sino que conviene evaluar posteriormente su relación con la variable objetivo y su posible contribución al rendimiento predictivo.

En conjunto, el análisis descriptivo pone de manifiesto que la tabla `transaction_raw` contiene información de naturaleza estadística muy diversa. La presencia de valores ausentes en determinadas variables, las distribuciones asimétricas, la existencia de valores extremos, las diferencias de escala y la concentración de observaciones en determinados valores constituyen los principales aspectos que deberán abordarse durante el preprocesamiento. Por tanto, estos resultados proporcionan una base para definir las siguientes operaciones de limpieza, transformación y selección de características, que deberán realizarse de forma fundamentada y teniendo en cuenta tanto las propiedades individuales de las variables como su utilidad para la detección de transacciones fraudulentas.### Análisis descriptivo de las variables numéricas

El análisis descriptivo de las variables numéricas de la tabla `transaction_raw` permite obtener una primera aproximación a la estructura y las características estadísticas del conjunto de datos. Para ello, se han estudiado medidas de tendencia central y dispersión, percentiles, valores mínimos y máximos, así como la disponibilidad de información de cada variable. Los resultados muestran una considerable heterogeneidad en las distribuciones y en la calidad de los datos, aspectos que deberán tenerse en cuenta durante las posteriores etapas de preparación y modelización.

En primer lugar, las variables del grupo C (`C1-C14`) presentan una disponibilidad completa, sin valores nulos en ninguno de sus registros. Sin embargo, sus distribuciones muestran diferencias importantes entre las medias y las medianas. En varias de estas características, la mediana se sitúa en valores muy reducidos, mientras que la media es considerablemente superior. Por ejemplo, `C1` presenta una mediana de 1 frente a una media de 14,09, mientras que `C13` alcanza una media de 32,54 y una mediana de 3. Este comportamiento evidencia una distribución asimétrica hacia la derecha, en la que la mayoría de las observaciones presentan valores relativamente bajos, pero existen determinados registros con valores mucho más elevados. Esta característica también se refleja en los valores máximos, que alcanzan varios miles en algunas variables. Por tanto, aunque estas características no presentan problemas de disponibilidad, será necesario estudiar la influencia de sus valores extremos y evaluar si requieren algún tipo de transformación antes de incorporarlas a los modelos.

Por otro lado, las variables del grupo D (`D1-D15`) presentan un comportamiento especialmente heterogéneo en cuanto a la disponibilidad de información. Mientras que `D1` apenas presenta un 0,21 % de valores nulos, otras características superan ampliamente el 80 % de ausencia de datos. Destacan especialmente `D7`, con un 93,41 % de valores ausentes, y `D13` y `D14`, con porcentajes próximos al 90 %. Esta distribución desigual indica que la información disponible no es homogénea entre las distintas características. En consecuencia, no sería adecuado aplicar una única estrategia de tratamiento de valores ausentes a todo el conjunto de variables. Será necesario evaluar individualmente su porcentaje de ausencia y su posible utilidad predictiva antes de decidir si conviene conservarlas, imputarlas o descartarlas. Asimismo, se han identificado valores negativos en algunas de estas variables. Aunque podrían parecer atípicos a primera vista, no deben considerarse automáticamente errores, ya que sería necesario conocer con mayor precisión su significado y comportamiento para determinar si son registros válidos.

En relación con las variables principales de la transacción, `TransactionAmt` presenta una distribución claramente asimétrica hacia la derecha. Su media es de 135,03, mientras que su mediana se sitúa en 68,90, con un tercer cuartil de 125. Además, el valor máximo alcanza 31.937,39, muy por encima de los valores correspondientes a la mayor parte de las observaciones. Esta diferencia entre las medidas de tendencia central pone de manifiesto que existen transacciones con importes considerablemente superiores a los habituales. Desde el punto de vista estadístico, estos valores pueden influir notablemente en la media y en la desviación típica, por lo que resulta conveniente complementar su estudio mediante percentiles y representaciones gráficas. También será interesante evaluar posteriormente si una transformación de la variable permite reducir su asimetría y facilitar el aprendizaje de determinados algoritmos.

Por su parte, `TransactionDT` no presenta valores nulos y contiene información temporal codificada numéricamente. Su rango de valores permite identificar una dimensión temporal dentro del conjunto de datos, aunque su interpretación requiere tener en cuenta que no se trata directamente de una fecha convencional. Esta característica puede resultar especialmente relevante en un problema de detección de fraude, ya que permite estudiar la distribución de las transacciones a lo largo del periodo recogido y explorar posibles patrones temporales. En fases posteriores podrá transformarse para obtener representaciones temporales más interpretables y facilitar el análisis de la evolución de las operaciones.

Una parte especialmente relevante del conjunto de datos está formada por las variables anonimizadas del grupo V (`V1-V339`). El análisis de estas características revela una elevada heterogeneidad tanto en la disponibilidad de información como en sus propiedades estadísticas. Se identifican diferentes grupos de variables con porcentajes de valores nulos muy elevados, algunos superiores al 75 %, al 85 % e incluso al 90 %. Al mismo tiempo, existen otras características que presentan una disponibilidad prácticamente completa. Esta circunstancia resulta especialmente importante porque la ausencia de información puede reducir considerablemente el número de observaciones disponibles para determinados análisis si se opta por eliminar registros incompletos. Por ello, será necesario estudiar las variables y sus patrones de ausencia de forma individual, evitando aplicar criterios generales que puedan provocar una pérdida innecesaria de información.

En cuanto a sus distribuciones, numerosas variables del grupo V presentan una concentración muy elevada de valores en torno a cero y uno. En algunos casos, incluso los tres cuartiles se sitúan en cero o en uno, lo que indica que una parte importante de las observaciones comparte valores idénticos. Aunque estas características están almacenadas como variables numéricas de tipo `FLOAT64`, sus distribuciones sugieren que algunas pueden tener un comportamiento predominantemente discreto. Esta particularidad deberá considerarse al estudiar su variabilidad y su posible utilidad para los modelos, puesto que una variable con una distribución muy concentrada puede aportar información limitada en determinados contextos, aunque no necesariamente carezca de capacidad predictiva.

También se observan diferencias considerables en las escalas y rangos de estas variables. Mientras que algunas presentan valores máximos reducidos, otras alcanzan magnitudes superiores a 100.000. En determinados casos, la media y la desviación típica son considerablemente superiores a los valores que representan los percentiles centrales, lo que apunta a distribuciones fuertemente asimétricas y a la presencia de observaciones extremas. Esta heterogeneidad puede tener implicaciones en los algoritmos de aprendizaje automático que utilizan distancias o son sensibles a la escala de las características. Por este motivo, en las siguientes fases será conveniente evaluar la necesidad de aplicar técnicas de escalado o transformación, teniendo en cuenta las características y los requisitos de cada modelo.

Por último, se han identificado características con una variabilidad muy reducida, cuyos valores permanecen prácticamente constantes en la mayoría de las observaciones. Este comportamiento puede limitar la cantidad de información que aportan al proceso de aprendizaje, especialmente si apenas permiten distinguir entre diferentes transacciones. No obstante, su eliminación no debe realizarse únicamente a partir de las estadísticas descriptivas, sino que conviene evaluar posteriormente su relación con la variable objetivo y su posible contribución al rendimiento predictivo.

En conjunto, el análisis descriptivo pone de manifiesto que la tabla `transaction_raw` contiene información de naturaleza estadística muy diversa. La presencia de valores ausentes en determinadas variables, las distribuciones asimétricas, la existencia de valores extremos, las diferencias de escala y la concentración de observaciones en determinados valores constituyen los principales aspectos que deberán abordarse durante el preprocesamiento. Por tanto, estos resultados proporcionan una base para definir las siguientes operaciones de limpieza, transformación y selección de características, que deberán realizarse de forma fundamentada y teniendo en cuenta tanto las propiedades individuales de las variables como su utilidad para la detección de transacciones fraudulentas.

### Análisis de las variables categóricas

El análisis de frecuencias de las variables categóricas permite estudiar la distribución de las distintas categorías presentes en las transacciones, así como identificar valores predominantes y comprobar la proporción de información ausente.

En primer lugar, `ProductCD` presenta una distribución concentrada principalmente en la categoría W, que representa el 74,45 % de las observaciones. A continuación, se encuentran las categorías C (11,60 %), R (6,38 %), H (5,59 %) y S (1,97 %). Por tanto, existe un claro predominio de una de las categorías, mientras que el resto presenta una representación considerablemente menor dentro del conjunto de datos.

En cuanto a las variables relacionadas con las tarjetas, `card4` muestra un predominio de Visa, con un 65,16 % de los registros, seguida de Mastercard, que representa el 32,04 %. Las categorías American Express y Discover tienen una presencia mucho más reducida, con un 1,41 % y un 1,13 %, respectivamente. Los valores ausentes apenas alcanzan el 0,27 %. Por su parte, `card6` presenta una distribución en la que predominan las tarjetas de débito (74,50 %), frente a las de crédito (25,23 %). Las categorías restantes tienen una representación prácticamente residual y los valores nulos también se sitúan en torno al 0,27 %.

Las variables `P_emaildomain` y `R_emaildomain` presentan una mayor diversidad de categorías, correspondientes a los dominios de correo electrónico asociados a las transacciones. En `P_emaildomain`, Gmail es el dominio más frecuente, con un 38,67 % de los registros, seguido de Yahoo (17,09 %) y Hotmail (7,66 %). También aparecen otros dominios con frecuencias inferiores, lo que genera una distribución con unas pocas categorías predominantes y una larga lista de dominios minoritarios. Esta variable presenta un 15,99 % de valores ausentes. En cambio, `R_emaildomain` muestra una proporción de valores nulos considerablemente superior, que alcanza el 76,75 %. Entre los valores disponibles destacan Gmail (9,68 %), Hotmail (4,66 %), anonymous.com (3,48 %) y Yahoo (2,01 %). La elevada ausencia de información en esta última variable limita notablemente la cantidad de registros en los que se dispone de un dominio asociado.

Respecto a las variables M (`M1-M9`), se observa una presencia importante de valores ausentes, aunque su distribución varía entre características. En `M1`, `M2` y `M3`, los valores nulos representan el 45,91 % de las observaciones. En `M4`, esta proporción asciende al 47,66 %, mientras que en `M5`, `M7`, `M8` y `M9` se sitúa aproximadamente entre el 58 % y el 59 %. Por su parte, `M6` presenta una proporción menor, con un 28,68 % de valores ausentes. En las variables booleanas, los valores disponibles se distribuyen entre las categorías verdadero y falso, con diferentes proporciones según la característica. Destaca especialmente `M1`, donde prácticamente todos los registros no nulos corresponden al valor verdadero, mientras que en otras variables existe una distribución más equilibrada entre ambas categorías. `M4`, por su parte, presenta tres categorías: M0, M1 y M2, siendo M0 la más frecuente entre los valores disponibles.

Finalmente, el análisis de `isFraud`, que constituye la variable objetivo del problema, evidencia un importante desequilibrio entre las dos clases. De las 590.540 transacciones analizadas, 569.877 corresponden a operaciones legítimas, lo que representa el 96,50 % del conjunto, mientras que únicamente 20.663 están identificadas como fraudulentas, equivalentes al 3,50 %. Esta distribución confirma que las operaciones fraudulentas constituyen una clase minoritaria. Por tanto, el desequilibrio deberá tenerse especialmente en cuenta durante el entrenamiento y la evaluación de los modelos, ya que una clasificación basada únicamente en la clase mayoritaria podría alcanzar una elevada exactitud sin identificar adecuadamente las operaciones fraudulentas.

En conjunto, las variables categóricas presentan distribuciones muy diferentes: algunas están dominadas por una o dos categorías, otras contienen una gran diversidad de valores y varias muestran porcentajes elevados de información ausente. Estas características deberán considerarse en las siguientes fases de preparación de los datos, especialmente al definir la codificación de las variables categóricas y el tratamiento de los valores nulos. Asimismo, el desequilibrio observado en la variable objetivo constituye una característica fundamental del problema de clasificación que condicionará la selección de métricas y estrategias de entrenamiento.


### Análisis de variables numéricas con comportamiento categórico

Además de las variables categóricas identificadas por su tipo de dato, el conjunto de datos contiene determinadas características almacenadas como valores numéricos que representan códigos o identificadores. Por este motivo, su análisis se ha centrado en estudiar la cardinalidad y la frecuencia de sus valores, en lugar de utilizar medidas estadísticas propias de variables cuantitativas continuas.

En primer lugar, las variables relacionadas con las tarjetas presentan diferentes niveles de cardinalidad. `card1` destaca por contener 13.553 valores distintos y no presentar registros nulos. Sus categorías más frecuentes representan porcentajes relativamente reducidos del conjunto, siendo la más habitual la correspondiente al código 7919, con un 2,53 %. Esto refleja una distribución repartida entre un elevado número de identificadores. Por su parte, `card2` contiene 500 valores distintos y un 1,51 % de registros ausentes. Sus categorías más frecuentes son los códigos 321, 111 y 555, que representan el 8,29 %, el 7,65 % y el 7,11 % del total, respectivamente.

En cambio, `card3` presenta una distribución mucho más concentrada: aunque contiene 114 valores distintos, el código 150 representa el 88,27 % de todas las transacciones, seguido del código 185, con un 9,54 %. Los valores ausentes suponen únicamente el 0,27 %. Una concentración similar, aunque menos acusada, se observa en `card5`, que cuenta con 119 valores distintos y un 0,72 % de valores nulos. Su categoría más frecuente es el código 226, presente en el 50,22 % de las observaciones, seguida del código 224, con un 13,80 %.

Por otro lado, las variables `addr1` y `addr2` presentan porcentajes de valores ausentes idénticos, del 11,13 %. `addr1` contiene 332 valores distintos y muestra una distribución relativamente repartida entre sus categorías más frecuentes, cuyos porcentajes se sitúan entre el 2,58 % y el 7,85 %. En cambio, `addr2` presenta 74 valores distintos, pero su distribución está fuertemente concentrada en el código 87, que representa el 88,14 % de todas las observaciones. El resto de categorías tiene una presencia considerablemente menor.

En conjunto, estas variables presentan comportamientos diferentes en cuanto a cardinalidad, concentración de categorías y disponibilidad de información. Mientras que algunas contienen un número elevado de identificadores distribuidos entre muchas categorías, otras están dominadas por unos pocos valores. Estas características deberán tenerse en cuenta durante la codificación y preparación de las variables para los modelos de aprendizaje automático, especialmente en aquellas con cardinalidad elevada o distribuciones muy concentradas.

### Análisis de valores atípicos rango intercuartílico (IQR)

Para identificar posibles valores atípicos en las variables numéricas se ha aplicado el método del rango intercuartílico (IQR), utilizando como límites los valores situados por debajo de Q1 - 1,5 × IQR o por encima de Q3 + 1,5 × IQR.

Los resultados muestran que numerosas variables presentan una proporción significativa de observaciones fuera de estos límites. Entre ellas destacan C8 (24,19 %), C4 (23,48 %), C10 (23,22 %), D14 (23,39 %) y D12 (21,24 %). También se observan porcentajes elevados en otras variables como D6, D7, C12 y dist1.

En las variables del grupo C se observa una particularidad: algunas presentan tanto el primer como el tercer cuartil iguales a cero, por lo que su rango intercuartílico también es cero. En estos casos, cualquier valor positivo queda clasificado automáticamente como atípico. Este comportamiento está relacionado con la elevada concentración de observaciones en cero y debe interpretarse con cautela, ya que no implica que todos esos valores positivos sean anomalías.

Por su parte, TransactionAmt presenta 66.480 observaciones identificadas como atípicas, equivalentes al 11,26 % de los registros válidos. Su valor máximo alcanza 31.937,391, muy por encima del tercer cuartil (125), lo que evidencia una distribución con una marcada asimetría positiva y una cola derecha pronunciada.

Las variables dist1 y dist2 también presentan valores extremos considerablemente alejados de sus respectivos cuartiles superiores. Asimismo, algunas variables del grupo D muestran observaciones fuera de los límites establecidos, aunque su interpretación debe considerar la elevada presencia de valores ausentes que caracteriza a este conjunto de atributos.

En conjunto, los resultados evidencian que el dataset contiene distribuciones muy asimétricas, concentraciones importantes de valores en cero y observaciones alejadas de los rangos centrales. No obstante, la identificación estadística de un valor atípico no implica necesariamente que se trate de un dato erróneo. En un problema de detección de fraude, estas observaciones podrían contener información relevante para identificar comportamientos inusuales. Por este motivo, no se plantea su eliminación automática, sino su conservación inicial y evaluación posterior durante el análisis de su relación con la variable objetivo y la preparación de los datos para el modelado.

# 1. Perfilado estadístico de V1-V339
Vamos a obtener para cada variable:
- Número de registros válidos y nulos.
- Porcentaje de valores ausentes.
- Número y porcentaje de ceros.
- Mínimo y máximo.
- Primer cuartil, mediana y tercer cuartil.
- Media y desviación típica.
- Cardinalidad aproximada.


### Conclusiones generales del análisis descriptivo de las variables V1-V339

El análisis descriptivo de las 339 variables anonimizadas del conjunto de datos permite identificar una importante heterogeneidad en cuanto a la disponibilidad, distribución y variabilidad de la información. A pesar de las diferencias entre grupos, se observan varios patrones comunes que resultan relevantes para las siguientes fases del proyecto.

En primer lugar, destaca la presencia de valores ausentes, cuya distribución no es homogénea. Mientras que algunos grupos de variables presentan porcentajes reducidos de valores nulos, otros alcanzan proporciones superiores al 75 % e incluso al 86 %. Estas ausencias aparecen agrupadas en determinados intervalos de variables, lo que sugiere que podrían compartir patrones de disponibilidad. Por tanto, no sería adecuado aplicar una única estrategia de tratamiento a todos los atributos. Será necesario estudiar el origen y la distribución de los valores ausentes, así como valorar si su propia presencia puede aportar información útil para la detección del fraude.

En segundo lugar, se observa una elevada concentración de valores iguales a cero o uno en numerosas variables. En algunos casos, estos valores representan prácticamente la totalidad de las observaciones válidas, lo que se traduce en una variabilidad muy reducida. Sin embargo, también existen variables en las que una pequeña proporción de registros presenta valores considerablemente superiores, generando distribuciones asimétricas y desviaciones típicas elevadas. Este comportamiento pone de manifiesto que las medias y las desviaciones estándar no siempre describen adecuadamente la distribución de los datos, por lo que resulta conveniente complementarlas con medidas de posición, cardinalidad y análisis de valores extremos.

Por otro lado, se identifican variables con cardinalidades muy diferentes: desde atributos que apenas presentan dos valores distintos hasta otros que contienen miles de valores. Esta diversidad indica que el conjunto combina características de naturaleza estadística muy distinta y que, por tanto, el tratamiento deberá adaptarse a cada grupo. En particular, será importante evaluar la posible influencia de los valores extremos, la conveniencia de aplicar transformaciones y la capacidad discriminativa de las variables con escasa variabilidad.

En conjunto, los resultados muestran que la disponibilidad de información, la concentración de valores y la dispersión constituyen aspectos fundamentales para la preparación del conjunto de datos. No obstante, estas características descriptivas no permiten determinar por sí solas la utilidad predictiva de cada atributo. Por este motivo, no se descartan variables únicamente por presentar un elevado porcentaje de valores nulos, una concentración importante de ceros o una variabilidad reducida. En las siguientes fases se estudiará su relación con la variable objetivo *isFraud*, con el propósito de identificar qué atributos aportan información relevante para distinguir las transacciones fraudulentas de las legítimas y definir, a partir de esa evidencia, las estrategias de preprocesamiento y selección de características más adecuadas.

# Análisis temporal de TransactionDT

El análisis de `TransactionDT` permite identificar variaciones temporales tanto en el volumen de transacciones como en la proporción de operaciones fraudulentas. La agregación diaria muestra fluctuaciones a lo largo de los 182 días identificados, con porcentajes de fraude que oscilan entre el 1,097 % y el 6,994 %. No se aprecia una tendencia temporal uniforme, aunque sí determinados intervalos en los que la incidencia del fraude es superior.

Por otro lado, el análisis por hora relativa revela diferencias más pronunciadas. Destaca especialmente el intervalo correspondiente a la hora relativa 7, donde el porcentaje de fraude alcanza el 10,61 %, frente a valores próximos al 2-3 % en buena parte de las horas posteriores. Estos resultados apuntan a que la dimensión temporal puede aportar información útil para la detección de operaciones fraudulentas.

No obstante, dado que `TransactionDT` representa un desplazamiento temporal y no una fecha y hora de calendario directamente interpretable, los intervalos obtenidos deben considerarse relativos y no asociarse a franjas horarias reales.

### Análisis de ProductCD y fraude

La variable `ProductCD`, que identifica las distintas categorías de producto, presenta diferencias significativas en la distribución del fraude. La categoría W concentra aproximadamente el 74,4 % de las transacciones, pero registra una tasa de fraude de tan solo el 2,04 %. En cambio, la categoría C presenta la mayor incidencia, con un 11,687 % de operaciones fraudulentas, a pesar de representar únicamente el 11,6 % del total de registros.

También se observan tasas de fraude superiores a la de W en las categorías S (5,9 %), H (4,766 %) y R (3,783 %). Destaca especialmente que la categoría C concentra cerca del 38,8 % de todas las operaciones fraudulentas del conjunto de datos.

Estos resultados muestran que `ProductCD` presenta una asociación relevante con la variable objetivo `isFraud`, por lo que resulta conveniente conservarla y evaluar su contribución durante la construcción de los modelos predictivos.

# card1-6

### Análisis de las variables de tarjeta

Las variables `card1` a `card6` presentan diferentes niveles de cardinalidad y ausencia de información. Destaca `card1`, que no contiene valores nulos y registra 13.553 valores distintos, mientras que `card2` presenta 500 categorías diferentes. Por su parte, `card3` y `card5` muestran cardinalidades intermedias, con 114 y 119 valores distintos, respectivamente. Finalmente, `card4` y `card6` presentan únicamente cuatro categorías cada una.

En cuanto a los valores ausentes, todas las variables presentan porcentajes reducidos, inferiores al 1,6 %. Por tanto, no se considera justificado descartar ninguna de ellas en esta fase del análisis. Será necesario estudiar su relación con la variable objetivo `isFraud` para determinar su posible utilidad predictiva.


### Análisis de las variables de tarjeta con fraude

Las variables `card1` a `card6` presentan diferentes niveles de cardinalidad y ausencia de información. Destaca `card1`, que no contiene valores nulos y registra 13.553 valores distintos, mientras que `card2` presenta 500 categorías diferentes. Por su parte, `card3` y `card5` muestran cardinalidades intermedias, con 114 y 119 valores distintos, respectivamente. Finalmente, `card4` y `card6` presentan únicamente cuatro categorías cada una.

En cuanto a los valores ausentes, todas las variables presentan porcentajes reducidos, inferiores al 1,6 %. Por tanto, no se considera justificado descartar ninguna de ellas en esta fase del análisis. Será necesario estudiar su relación con la variable objetivo `isFraud` para determinar su posible utilidad predictiva.


### relacion card con fraude card3-6
Ahora vamos a calcular la tasa de fraude para cada valor de las variables. Como card1 tiene más de 13.000 categorías, no conviene mostrar todos sus valores directamente. Empezaremos por las variables con menor cardinalidad: card3, card4, card5 y card6.


El análisis de las variables de tarjeta revela diferencias relevantes en la incidencia del fraude según sus distintas categorías.

En `card3`, destaca especialmente la categoría 185, que presenta una tasa de fraude del 13,066 %, frente al 2,457 % de la categoría 150, que concentra la mayor parte de las transacciones. En cuanto a `card4`, las categorías Visa y Mastercard muestran porcentajes similares, mientras que Discover registra una incidencia superior, del 7,728 %.

Por su parte, `card5` presenta diferencias destacables entre determinadas categorías. La categoría 137 alcanza una tasa de fraude del 14,718 %, seguida de las categorías 138 y 102, con un 8,522 % y un 6,294 %, respectivamente. Finalmente, en `card6` se observa una diferencia significativa entre las operaciones realizadas con tarjetas de crédito y débito: las primeras presentan una tasa de fraude del 6,678 %, frente al 2,426 % de las segundas.

En conjunto, estos resultados sugieren que las características asociadas a las tarjetas pueden aportar información relevante para la detección del fraude. No obstante, las categorías con un número reducido de observaciones deben interpretarse con cautela, ya que sus porcentajes pueden presentar una elevada variabilidad.

### card1 fraud


Siguiente paso: analizar su relación con el fraude
Con 13.553 categorías, no tiene demasiado sentido mostrar todas. Podemos empezar por las categorías con al menos 100 transacciones y ordenar por tasa de fraude.

La variable `card1` presenta una elevada cardinalidad, con 13.553 valores distintos en un total de 590.540 transacciones. Además, no contiene valores nulos, por lo que dispone de información para todos los registros del conjunto de datos. Aunque se representa mediante valores numéricos, no debe interpretarse como una variable cuantitativa continua, sino como una variable categórica que identifica diferentes tipos o categorías de tarjeta.

Con el objetivo de estudiar su posible relación con el fraude, se ha calculado la tasa de transacciones fraudulentas para cada valor de `card1`, considerando únicamente aquellas categorías que aparecen en al menos 100 registros. Este criterio permite reducir la influencia de categorías con muy poca representación, cuyos porcentajes podrían resultar poco representativos debido a un número reducido de observaciones.

Los resultados muestran una elevada variabilidad en las tasas de fraude entre las distintas categorías. Algunas presentan porcentajes especialmente altos, como el valor 3643, con un 52,07 % de transacciones fraudulentas sobre 121 operaciones, o el valor 17999, con un 48,52 % sobre 101 operaciones. También destacan categorías con un volumen de observaciones considerablemente mayor, como el valor 9917, que registra 919 transacciones y una tasa de fraude del 33,30 %, o el valor 9026, con 2.076 transacciones y un 19,12 % de fraude. Estos resultados son especialmente relevantes porque muestran que las diferencias no se limitan exclusivamente a categorías con pocos registros.

En el extremo contrario, también se identifican categorías con tasas de fraude muy reducidas o incluso nulas. Por ejemplo, el valor 14858 acumula 1.383 transacciones sin ningún caso de fraude, mientras que el valor 10856 presenta 921 operaciones, también sin registros fraudulentos. Esta variabilidad contrasta con la tasa global de fraude del conjunto de datos, situada aproximadamente en el 3,50 %.

Estas diferencias podrían indicar que determinadas categorías de `card1` están asociadas a patrones de comportamiento con una mayor o menor exposición al fraude. Una posible explicación es que esta variable recoge información relacionada con distintos emisores o perfiles de tarjeta, cuyas características y patrones de utilización pueden diferir. No obstante, los resultados únicamente muestran una asociación estadística y no permiten establecer una relación causal.

En consecuencia, `card1` se considera una variable potencialmente relevante para la detección de operaciones fraudulentas. Sin embargo, debido a su elevada cardinalidad, será necesario prestar especial atención a su tratamiento durante la fase de preparación de los datos. En particular, no sería adecuado interpretarla directamente como una variable numérica continua, por lo que deberán evaluarse estrategias de codificación categórica que permitan aprovechar la información que contiene sin introducir sesgos ni fugas de información durante el entrenamiento de los modelos.

### Análisis de la variable card2

La variable `card2` presenta 500 valores distintos y 8.933 registros nulos, lo que representa aproximadamente el 1,51 % del total de transacciones. Por tanto, aunque la variable contiene algunos valores ausentes, su nivel de completitud es elevado y permite realizar un análisis de su relación con la variable objetivo `isFraud`.

Al igual que sucede con `card1`, sus valores numéricos deben interpretarse como categorías y no como magnitudes cuantitativas. Para estudiar su comportamiento frente al fraude, se ha calculado la tasa de operaciones fraudulentas para cada categoría, considerando aquellas con al menos 100 transacciones. Este umbral permite reducir la influencia de grupos con una representación demasiado limitada.

Los resultados muestran una variabilidad considerable en las tasas de fraude asociadas a los distintos valores de `card2`. Entre las categorías con mayores porcentajes destacan los valores 289 y 405, con tasas del 40,68 % y 40,35 %, respectivamente. También resulta relevante el valor 176, que presenta una tasa del 36,06 % sobre un total de 513 transacciones. Estas cifras se encuentran muy por encima de la tasa global de fraude del conjunto de datos, situada en torno al 3,50 %.

No obstante, también se observan diferencias importantes entre categorías con un volumen elevado de operaciones. Por ejemplo, el valor 545 registra 16.355 transacciones y una tasa de fraude del 8,68 %, mientras que el valor 583, con 21.803 operaciones, presenta una tasa del 4,12 %. En el extremo contrario, existen categorías con tasas muy reducidas, como el valor 194, con 16.938 transacciones y un 0,77 % de fraude, o el valor 476, con 5.822 operaciones y un 0,74 %. Incluso se identifican categorías con más de 100 transacciones en las que no se ha registrado ningún caso de fraude.

En cuanto a los registros nulos, se contabilizan 8.933 transacciones, de las cuales 423 son fraudulentas, lo que representa una tasa del 4,74 %. Este porcentaje es ligeramente superior a la tasa global del conjunto de datos, aunque la diferencia no permite concluir por sí sola que la ausencia de este atributo esté directamente relacionada con una mayor probabilidad de fraude.

En conjunto, los resultados evidencian que `card2` contiene información potencialmente relevante para la detección de operaciones fraudulentas. La diferencia entre las tasas observadas en sus distintas categorías sugiere que determinados valores pueden estar asociados a patrones de riesgo diferentes. Sin embargo, estas asociaciones deben interpretarse con cautela, especialmente en las categorías con menor número de observaciones. Por ello, al igual que con `card1`, será necesario tratar esta variable como categórica y evaluar su contribución durante el entrenamiento y la validación de los modelos predictivos.

### Análisis de las variables addr1 y addr2

Las variables `addr1` y `addr2` contienen información relacionada con la dirección de las transacciones y presentan 65.706 valores nulos cada una, lo que representa el 11,126 % del total de registros. En cuanto a su cardinalidad, `addr1` cuenta con 332 valores distintos, mientras que `addr2` presenta 74. Dado que sus valores representan códigos categóricos y no magnitudes numéricas, ambas variables deben tratarse como variables cualitativas durante las siguientes fases del análisis.

El estudio de las tasas de fraude por categoría revela diferencias significativas en el comportamiento de ambas variables. En el caso de `addr1`, algunas categorías presentan tasas de fraude considerablemente superiores a la media global del conjunto de datos (3,499 %). Destacan los valores 296, 161 y 536, con tasas del 21,253 %, 19,477 % y 16,181 %, respectivamente. Estas diferencias también se observan en categorías con un volumen considerable de transacciones. Por el contrario, existen categorías como 444 y 494 cuyas tasas se sitúan por debajo del 1 %.

En cuanto a `addr2`, se observa una distribución especialmente concentrada en la categoría 87, que agrupa 520.481 transacciones y presenta una tasa de fraude del 2,397 %, inferior a la media global. Sin embargo, las categorías 96 y 60 registran tasas notablemente superiores, del 13,950 % y 9,047 %, respectivamente, aunque cuentan con un volumen de observaciones mucho menor.

En conjunto, los resultados muestran que ambas variables presentan diferencias en la incidencia del fraude según sus categorías, lo que sugiere que pueden aportar información relevante para la identificación de operaciones fraudulentas. Por este motivo, se conservarán para las siguientes fases del proyecto, donde se evaluará su capacidad predictiva y se determinará el tratamiento más adecuado para los valores ausentes y las distintas categorías.


# P_emaildomain y R_emaildomain: dominios de correo, valores ausentes, categorías más frecuentes y relación con el fraude. 

Las variables `P_emaildomain` y `R_emaildomain` recogen información sobre el dominio del correo electrónico asociado al comprador y al destinatario, respectivamente. Ambas presentan una distribución categórica con numerosos dominios distintos y una presencia relevante de valores ausentes, aunque existen diferencias importantes entre ellas.

En el caso de `P_emaildomain`, se identifican 94.456 valores nulos, equivalentes al 15,99 % del total de transacciones. Entre los dominios registrados, destacan `gmail.com`, con 228.355 operaciones, y `yahoo.com`, con 100.934, seguidos de `hotmail.com`, con 45.250. Estos tres dominios concentran una parte importante de los registros de la variable. En cuanto a su relación con el fraude, se observan diferencias entre categorías. Por ejemplo, `gmail.com` presenta una tasa del 4,354 %, mientras que `yahoo.com` registra un 2,276 %. Destaca especialmente `hotmail.com`, cuya tasa alcanza el 5,295 %, así como `outlook.com`, con un 9,458 %. También aparecen tasas elevadas en dominios con menor representación, como `mail.com` (18,962 %) y `outlook.es` (13,014 %). Por su parte, los registros sin dominio asociado presentan una tasa de fraude del 2,954 %, inferior a la media global del conjunto de datos (3,499 %).

La variable `R_emaildomain` presenta una proporción de valores ausentes considerablemente superior: 453.249 registros, lo que representa aproximadamente el 76,75 % del total. Entre los valores disponibles, `gmail.com` es el dominio más frecuente, con 57.147 transacciones, seguido de `hotmail.com`, con 27.509, y `anonymous.com`, con 20.529. En relación con el fraude, `gmail.com` registra una tasa del 11,918 %, mientras que `hotmail.com` alcanza el 7,779 %. También destacan `outlook.com`, con un 16,514 %, e `icloud.com`, con un 12,876 %. En el caso de los valores ausentes, la tasa de fraude es del 2,082 %, inferior a la media global.

En ambas variables se observan diferencias en las tasas de fraude según el dominio registrado. No obstante, es importante considerar el volumen de observaciones de cada categoría, ya que algunos porcentajes elevados corresponden a dominios con muy pocos registros y, por tanto, deben interpretarse con cautela. Por ejemplo, `protonmail.com` presenta una tasa del 95,122 % en `R_emaildomain`, pero únicamente cuenta con 41 transacciones, por lo que este resultado no permite establecer una conclusión general sobre dicho dominio.

En conjunto, `P_emaildomain` presenta una proporción de valores disponibles significativamente mayor que `R_emaildomain`, lo que podría hacerla especialmente útil durante la fase de modelado. A pesar de su elevado porcentaje de valores ausentes, `R_emaildomain` también podría aportar información relevante, dado que determinados dominios muestran tasas de fraude diferenciadas. Por este motivo, se considera conveniente conservar ambas variables inicialmente y evaluar su contribución predictiva, prestando especial atención al tratamiento de los valores ausentes y a la agrupación de categorías poco frecuentes.

# matriz correlaciones

1. Matriz de correlación de variables numéricas
Seleccionaremos las variables que realmente tienen naturaleza numérica, por ejemplo:
- TransactionAmt
- TransactionDT
- dist1
- dist2
- Variables C1–C14
- Variables D1–D15
- Variables V (si procede, seleccionando las más relevantes o agrupándolas)
Incluiríamos isFraud para observar su asociación lineal con las variables numéricas.

### Análisis de correlación con la variable objetivo

Con el objetivo de estudiar la relación entre las variables numéricas y la variable objetivo `isFraud`, se ha calculado el coeficiente de correlación de Pearson. Este indicador permite evaluar la intensidad y la dirección de la relación lineal entre dos variables, tomando valores comprendidos entre -1 y 1.

Los resultados obtenidos muestran que ninguna de las variables analizadas presenta una correlación lineal especialmente elevada con la variable objetivo. Los coeficientes se sitúan en un intervalo reducido, entre -0,0317 y 0,0372. La mayor correlación positiva corresponde a `C2` (0,0372), seguida de `C12` (0,0319), `C1` (0,0306) y `C4` (0,0304). Por otro lado, las correlaciones negativas más destacadas corresponden a `C9` (-0,0317) y `C5` (-0,0308).

Las variables `TransactionAmt` (0,0113) y `TransactionDT` (0,0131) también presentan correlaciones lineales muy débiles con `isFraud`. Este resultado indica que, consideradas individualmente mediante una relación lineal, no muestran una asociación destacable con la clasificación de fraude.

En conjunto, los resultados reflejan que la correlación lineal de Pearson tiene una capacidad limitada para identificar relaciones entre estas variables y la variable objetivo. Sin embargo, estos valores no implican que las variables carezcan de utilidad predictiva, ya que podrían existir relaciones no lineales, interacciones entre variables o patrones que otros métodos de análisis y modelado permitan identificar. Por tanto, no se descarta ninguna variable únicamente a partir de estos coeficientes.

### Análisis de correlación de las variables D1-D15

El análisis de correlación de Pearson de las variables comprendidas entre `D1` y `D15` muestra que todas presentan una relación lineal negativa con la variable objetivo `isFraud`, aunque su intensidad varía entre ellas. Los coeficientes obtenidos se sitúan entre -0,0087 y -0,1426, por lo que, en términos generales, las correlaciones son débiles.

La variable `D8` presenta la correlación negativa de mayor magnitud (-0,1426), seguida de `D7` (-0,1272). También destacan `D2` (-0,0836), `D15` (-0,0775) y `D10` (-0,0720). En el extremo contrario, `D14` presenta una correlación prácticamente nula (-0,0087), mientras que `D12` (-0,0289), `D9` (-0,0443) y `D11` (-0,0451) muestran relaciones lineales especialmente débiles.

En comparación con las variables `C1-C14`, cuyos coeficientes se encontraban aproximadamente entre -0,0317 y 0,0372, las variables del grupo `D` presentan correlaciones negativas de mayor magnitud, especialmente `D7` y `D8`. Esto indica que algunas de estas variables muestran una asociación lineal algo más destacada con la variable objetivo.

No obstante, los coeficientes siguen siendo relativamente bajos, por lo que no puede concluirse que exista una relación lineal fuerte entre estas variables y la presencia de fraude. Tampoco debe descartarse su utilidad predictiva, ya que podrían contener información relevante mediante relaciones no lineales o combinaciones con otras características. Por tanto, se considera conveniente conservar inicialmente estas variables y evaluar su contribución durante la fase de modelado.

### Análisis de correlación de las variables dist1 y dist2

El análisis de correlación de Pearson de las variables `dist1` y `dist2` muestra una relación lineal muy débil con la variable objetivo `isFraud`. En concreto, `dist1` presenta una correlación positiva de 0,0215, mientras que `dist2` registra una correlación negativa de -0,0191.

Ambos coeficientes se encuentran próximos a cero, lo que indica que, consideradas individualmente, estas variables no presentan una asociación lineal destacable con la presencia de fraude. Además, sus valores son inferiores en magnitud a los obtenidos para algunas variables de los grupos `C` y `D`.

No obstante, estos resultados no implican que `dist1` y `dist2` carezcan de capacidad predictiva. Podrían existir relaciones no lineales o interacciones con otras características que no quedan reflejadas mediante el coeficiente de Pearson. Por este motivo, se considera conveniente mantener ambas variables inicialmente y evaluar su utilidad durante la fase de modelado.

# M1 – M9 correlation
### Tratamiento de las variables M1-M9 para el análisis de correlación

Las variables `M1` a `M9` presentan características binarias, aunque su representación en el conjunto de datos no es homogénea. Ocho de ellas (`M1`, `M2`, `M3` y `M5-M9`) son de tipo booleano (`BOOL`), mientras que `M4` está almacenada como una cadena de texto (`STRING`).

Para poder calcular el coeficiente de correlación de Pearson con la variable objetivo `isFraud`, ha sido necesario transformar estas variables a un formato numérico. En las variables booleanas, los valores `TRUE` y `FALSE` se han convertido en 1 y 0, respectivamente. En el caso de `M4`, se ha aplicado una conversión equivalente, asignando 1 al valor `T` y 0 al valor `F`. Los valores nulos se han mantenido como tales para evitar asignarles una categoría incorrecta.

Una vez realizada esta transformación, se ha calculado la correlación de Pearson entre cada una de las variables y `isFraud`, con el objetivo de analizar la intensidad y dirección de su asociación lineal con la presencia de operaciones fraudulentas.

```SQL
SELECT
  CORR(IF(M1 IS TRUE, 1.0, IF(M1 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M1,
  CORR(IF(M2 IS TRUE, 1.0, IF(M2 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M2,
  CORR(IF(M3 IS TRUE, 1.0, IF(M3 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M3,
  CORR(IF(M4 = 'T', 1.0, IF(M4 = 'F', 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M4,
  CORR(IF(M5 IS TRUE, 1.0, IF(M5 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M5,
  CORR(IF(M6 IS TRUE, 1.0, IF(M6 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M6,
  CORR(IF(M7 IS TRUE, 1.0, IF(M7 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M7,
  CORR(IF(M8 IS TRUE, 1.0, IF(M8 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M8,
  CORR(IF(M9 IS TRUE, 1.0, IF(M9 IS FALSE, 0.0, NULL)), CAST(isFraud AS FLOAT64)) AS corr_M9
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;
```
Resultado: m1-9_correlation.json

```SQL
SELECT
  CORR(IF(M4 = 'M0', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M0,
  CORR(IF(M4 = 'M1', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M1,
  CORR(IF(M4 = 'M2', 1.0, 0.0), CAST(isFraud AS FLOAT64)) AS corr_M4_M2
FROM `fraud-detection-eda.fraud_detection.transaction_raw`;
```

### Análisis de correlación de las variables M1-M9

Los resultados del análisis de correlación de Pearson muestran que las variables `M1` a `M9` presentan, en general, asociaciones lineales débiles con la variable objetivo `isFraud`.

Entre las variables binarias, `M3` presenta la correlación negativa de mayor magnitud (-0,0387), seguida de `M2` (-0,0371) y `M9` (-0,0321). Por su parte, `M5` registra la correlación positiva más elevada (0,0318), mientras que `M6` presenta un coeficiente de -0,0233. El resto de las variables muestran valores próximos a cero, como `M1` (0,0013), `M7` (0,0068) y `M8` (-0,0191).

En el caso de `M4`, al tratarse de una variable categórica con tres valores distintos (`M0`, `M1` y `M2`), se ha aplicado una transformación mediante variables indicadoras para analizar la asociación de cada categoría con la variable objetivo. Los resultados muestran diferencias entre ellas: la categoría `M0` presenta una correlación de 0,0064, mientras que `M1` registra una correlación negativa de -0,0135. Destaca especialmente la categoría `M2`, cuya correlación positiva alcanza 0,1439, siendo la asociación de mayor magnitud entre las variables de este grupo.

Este último resultado es coherente con el análisis de las tasas de fraude por categoría, en el que `M2` presenta un porcentaje de operaciones fraudulentas del 11,374 %, frente al 3,665 % de `M0` y el 2,705 % de `M1`. Por tanto, la categoría `M2` muestra una asociación más destacada con la presencia de fraude.

Por otro lado, cabe señalar que `M4` presenta 281.444 valores nulos, aproximadamente el 47,66 % del conjunto de transacciones. Esta proporción deberá tenerse en cuenta durante el tratamiento de los datos y la posterior fase de modelado.

En conjunto, los resultados indican que la mayoría de las variables `M1-M9` presentan correlaciones lineales débiles con `isFraud`. Sin embargo, la categoría `M2` de la variable `M4` destaca por su mayor asociación positiva con el fraude. Estos resultados sugieren que determinadas características de este grupo podrían aportar información útil para la clasificación, por lo que se considera conveniente conservarlas inicialmente y evaluar su contribución durante la fase de modelado.


# v1 - v339 fraud correlation

Los resultados de las 339 variables V muestran un patrón bastante diferente al que habíamos observado en los grupos anteriores (C, D y M). En este caso, aparecen varias variables con una correlación lineal moderada respecto a isFraud, lo que indica que el grupo V contiene información potencialmente relevante para distinguir las transacciones fraudulentas.

Las correlaciones positivas más elevadas corresponden a V257 (0,3831), V246 (0,3669), V244 (0,3641), V242 (0,3606) y V201 (0,3280). También destacan V200 (0,3188), V189 (0,3082), V188 (0,3036) y V258 (0,2972). Estas variables presentan una asociación positiva con la condición de fraude: sus valores tienden a aumentar en las observaciones clasificadas como fraudulentas. No obstante, esta relación no implica causalidad ni garantiza por sí sola una elevada capacidad predictiva.

En sentido contrario, las correlaciones negativas más destacadas son considerablemente más débiles. Entre ellas se encuentran V48 (-0,1158), V49 (-0,1109), V90 (-0,1102), V29 (-0,1079) y V91 (-0,1055). Por tanto, aunque algunas variables muestran una asociación inversa con el fraude, su intensidad es inferior a la observada en las principales correlaciones positivas.

También se observa una distribución desigual de la información: mientras que un conjunto de variables presenta correlaciones moderadas, una parte importante de las 339 variables tiene valores próximos a cero. Por ejemplo, V136 (-0,00004), V137 (-0,00011), V135 (-0,00028) y V299 (-0,00031) apenas muestran asociación lineal con la variable objetivo. Esto no significa necesariamente que carezcan de utilidad, ya que podrían aportar información mediante relaciones no lineales o interacciones con otras características.

Un aspecto importante es que estas correlaciones deben interpretarse como un análisis exploratorio, no como un criterio definitivo para eliminar variables. En particular, una correlación baja con isFraud no implica que una variable sea irrelevante para un modelo de clasificación. Además, dado que el conjunto presenta un claro desequilibrio entre transacciones legítimas y fraudulentas, conviene complementar este análisis con técnicas de selección de características y evaluación del rendimiento predictivo.

# LIMITE DE DEMASIADAS COMPARACIONES

Para calcular una matriz de correlación de Pearson entre 339 variables, tenemos:
- 339 × 339 = 114.921 posiciones en la matriz.
- 339 correlaciones diagonales (cada variable consigo misma, siempre 1).
- 57.291 correlaciones únicas entre parejas diferentes.
La matriz es simétrica: la correlación entre V1 y V2 es idéntica a la de V2 y V1.

La fórmula para calcular las parejas únicas es:
\[
\frac{n(n-1)}{2}=\frac{339\cdot338}{2}
=\boxed{57.291}
\]

Por tanto, tendríamos que calcular 57.291 correlaciones de Pearson distintas para construir la matriz completa, sin contar la diagonal.

# conclusiones

### Conclusiones generales del análisis exploratorio de `transaction_raw`

El análisis exploratorio de la tabla `transaction_raw` ha permitido identificar las principales características de las transacciones, estudiar su relación con la variable objetivo y detectar varios aspectos que deberán tenerse en cuenta durante las posteriores fases de preprocesamiento y modelado.

En primer lugar, el conjunto de datos está compuesto por **590.540 transacciones**, de las cuales 20.663 corresponden a operaciones fraudulentas, lo que representa aproximadamente un **3,50 % del total**. Esta distribución evidencia un importante desequilibrio entre las clases, ya que la gran mayoría de las operaciones son legítimas. Se trata de una de las principales dificultades del problema de clasificación, puesto que un modelo podría obtener una elevada exactitud simplemente clasificando la mayoría de las operaciones como legítimas, sin identificar adecuadamente los casos fraudulentos. Por este motivo, durante el modelado será necesario prestar especial atención a métricas como la precisión, el recall, el F1-score y el área bajo la curva ROC, así como a las técnicas de tratamiento del desequilibrio de clases.

En relación con las variables transaccionales, destaca especialmente `TransactionAmt`, cuya distribución presenta una marcada asimetría positiva. La diferencia entre su media (135,03) y su mediana (68,90), junto con la existencia de importes considerablemente elevados, evidencia la presencia de valores extremos. Aproximadamente el 11,26 % de las observaciones fueron identificadas como valores atípicos según el criterio aplicado. Estos registros no deben eliminarse automáticamente, ya que podrían representar operaciones legítimas de importe elevado o contener información relevante para detectar comportamientos fraudulentos. Por tanto, será conveniente estudiar su influencia y valorar posibles transformaciones o técnicas de tratamiento.

El análisis de `ProductCD` también ha revelado diferencias importantes entre las categorías. Mientras que la categoría W concentra la mayor parte de las transacciones, con una tasa de fraude del 2,04 %, la categoría C presenta una tasa considerablemente superior, del **11,69 %**. Este resultado indica que determinadas categorías de producto pueden aportar información relevante para la identificación de operaciones fraudulentas. Asimismo, el análisis de las variables relacionadas con las tarjetas (`card1`–`card6`) muestra diferencias en las tasas de fraude entre determinadas categorías. Entre los resultados más destacables se encuentra la diferencia entre los métodos de pago de débito y crédito: las operaciones asociadas a tarjetas de crédito presentan una tasa de fraude del 6,68 %, frente al 2,43 % de las tarjetas de débito. No obstante, estas diferencias deben interpretarse teniendo en cuenta el volumen de observaciones de cada categoría, especialmente en aquellas con una frecuencia reducida.

Por otra parte, las variables geográficas `addr1` y `addr2` presentan un porcentaje de valores ausentes del **11,13 %**, mientras que las variables relacionadas con los dominios de correo electrónico muestran un comportamiento especialmente desigual. En particular, `R_emaildomain` presenta aproximadamente un **76,75 % de valores nulos**, frente al 15,99 % de `P_emaildomain`. Este elevado nivel de ausencia constituye uno de los principales problemas identificados durante el análisis, por lo que será necesario estudiar si la ausencia de información tiene relación con el comportamiento fraudulento antes de decidir cómo tratarla. La imputación, la conservación de una categoría específica para los valores ausentes o la eliminación de determinadas variables deberán valorarse en función de su utilidad predictiva.

Respecto a la variable temporal `TransactionDT`, se ha observado que contiene un valor relativo de tiempo y no una fecha y hora reales. Su distribución abarca aproximadamente 182 días y presenta variaciones en las tasas de fraude a lo largo del periodo analizado, aunque no se identifica una tendencia lineal clara. También se han observado diferencias entre los distintos intervalos horarios relativos. Por tanto, esta variable puede aportar información sobre patrones temporales, pero su interpretación debe realizarse teniendo presente que no representa directamente el calendario real.

El estudio de las variables agregadas C, D y M mediante correlaciones de Pearson con `isFraud` ha mostrado, en términos generales, asociaciones lineales débiles. En el grupo C, las correlaciones se mantienen próximas a cero; en el grupo D, las asociaciones son algo más pronunciadas, aunque siguen siendo débiles, destacando D8 (-0,143) y D7 (-0,127). En el grupo M, la mayoría de las variables también presentan correlaciones reducidas, con la excepción de la categoría M2 de la variable M4, cuya correlación alcanza aproximadamente 0,144. Este resultado pone de manifiesto que la información contenida en estos grupos no siempre puede explicarse mediante relaciones lineales simples con la variable objetivo.

En cambio, el grupo de variables V presenta asociaciones más destacadas con la variable objetivo. Entre las variables con mayor correlación positiva se encuentran V257 (0,383), V246 (0,367), V244 (0,364), V242 (0,361) y V201 (0,328). Estas variables constituyen algunos de los indicadores con mayor asociación lineal con la condición de fraude dentro de los grupos numéricos analizados. Sin embargo, también se ha observado que numerosas variables V presentan correlaciones próximas a cero. Esto no implica necesariamente que carezcan de utilidad, ya que podrían aportar información mediante relaciones no lineales o interacciones con otras características.

Finalmente, el análisis de correlaciones debe entenderse como una primera aproximación a la relación entre las variables y el fraude, y no como un criterio definitivo de selección de características. Una correlación reducida no implica necesariamente ausencia de capacidad predictiva, del mismo modo que una correlación elevada no garantiza que una variable mejore el rendimiento de un modelo. Será necesario complementar estos resultados con técnicas de selección de variables y evaluaciones experimentales durante la fase de modelado.

En conjunto, el análisis exploratorio ha permitido identificar varios aspectos que condicionarán el desarrollo posterior del proyecto: el desequilibrio entre las clases, la presencia de valores extremos, los elevados porcentajes de datos ausentes en determinadas variables y las diferencias en las tasas de fraude entre categorías. Asimismo, se ha identificado un conjunto de variables numéricas, especialmente dentro del grupo V, que presenta asociaciones relevantes con la variable objetivo. Estos hallazgos proporcionan una base para diseñar las siguientes etapas de integración, transformación y preparación de los datos, procurando conservar la información potencialmente útil para la construcción de los modelos de detección de fraude.

### Análisis de valores nulos y su relación con el fraude

El análisis de los valores ausentes en las variables V1–V339 revela que la distribución de los datos faltantes presenta patrones compartidos entre distintos grupos de variables. En lugar de distribuirse de manera independiente, los valores nulos tienden a concentrarse en determinados conjuntos, con porcentajes de ausencia que alcanzan aproximadamente el 86 % en algunos grupos, el 78 % en otros y el 76 % en otro conjunto relevante. También se identifican grupos con porcentajes de ausencia inferiores, como V1–V11, con aproximadamente un 47,3 %, y otros conjuntos con proporciones situadas entre el 13 % y el 29 %.

Para evaluar si la ausencia de información podría estar relacionada con la variable objetivo, se ha comparado la tasa de fraude entre los registros que presentan valores nulos y aquellos que disponen de información para cada patrón identificado.

Los resultados muestran diferencias relevantes en determinados grupos. Por ejemplo, en uno de los patrones con 460.110 registros nulos, la tasa de fraude es del 2,28 %, frente al 7,81 % de los registros disponibles. Se observan diferencias similares en otros grupos con aproximadamente 450.000 registros nulos, donde la tasa de fraude de los registros disponibles se sitúa alrededor del 7,9 %, mientras que la correspondiente a los registros con valores ausentes ronda el 2,1 %.

En cambio, otros patrones presentan una relación en sentido contrario. Es el caso de las variables con aproximadamente un 47,3 % de valores nulos, donde la tasa de fraude alcanza el 5,21 % entre los registros ausentes, frente al 1,96 % entre aquellos que contienen información. También destacan algunos grupos con porcentajes de ausencia más reducidos: para un patrón con 89.164 registros nulos, la tasa de fraude es del 4,80 %, frente al 3,27 % de los registros disponibles; mientras que otro con 77.096 registros nulos presenta tasas del 5,85 % y el 3,15 %, respectivamente.

Por otro lado, no todos los patrones muestran diferencias relevantes. Algunos grupos presentan tasas de fraude bastante similares entre registros con valores nulos y disponibles, lo que sugiere una asociación marginal más limitada. Asimismo, se han identificado casos con cantidades muy reducidas de valores ausentes, como un patrón de únicamente 12 registros, cuya tasa de fraude no resulta representativa debido al reducido tamaño de la muestra.

En conjunto, estos resultados indican que la ausencia de información puede contener información relevante para la detección del fraude. Por tanto, los valores nulos no deberían eliminarse ni imputarse automáticamente sin evaluar previamente su comportamiento. Durante la fase de preprocesamiento se considerará la incorporación de indicadores binarios que identifiquen la ausencia de información, así como la comparación de los resultados de los modelos con y sin estos indicadores.

Finalmente, es importante señalar que las diferencias observadas representan asociaciones individuales entre la ausencia de datos y la variable objetivo, por lo que no permiten establecer relaciones causales ni determinar por sí solas la capacidad predictiva de cada patrón. Su utilidad deberá comprobarse posteriormente mediante la evaluación de los modelos de clasificación.
