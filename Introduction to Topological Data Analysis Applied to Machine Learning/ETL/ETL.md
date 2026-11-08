Para abordar la ingeniería de características (*feature engineering*) en el dataset de IEEE-CIS y replicar las técnicas más exitosas de los ganadores de la competición de Kaggle, vamos a estructurar las transformaciones clave. Estas características explotan patrones de comportamiento que distinguen claramente el fraude de las transacciones legítimas.

A continuación, tienes las técnicas más potentes y cómo implementarlas:

---

### 1. Codificación temporal avanzada (*Temporal Decoding*)

La columna `TransactionDT` es un delta de tiempo (en segundos) desde un punto de partida arbitrario. Si se usa tal cual, el modelo no entenderá el ciclo diario o semanal.

* **Hora del día y Día de la semana:** Extraer el momento en que se realiza la transacción es crucial, ya que el fraude suele concentrarse en horas de la madrugada locales o patrones atípicos.
* **Implementación matemática rápida:**

$$\text{Hour} = \left(\frac{\text{TransactionDT}}{3600}\right) \pmod{24}$$

\subsection{Phase 1: Empirical Analysis of Temporal Feature Engineering}

To address the limitations of the raw continuous timestamp \texttt{TransactionDT}—which measures elapsed seconds from an arbitrary origin—the feature extraction process decoded cyclical and continuous temporal components. The transformation maps the continuous signal into discrete diurnal and weekly indicators:
\begin{align}
    \text{DT\_hour} &= \left\lfloor \frac{\text{TransactionDT}}{3600} \right\rfloor \pmod{24} \\
    \text{DT\_day\_of\_week} &= \left\lfloor \frac{\text{TransactionDT}}{86400} \right\rfloor \pmod{7} \\
    \text{DT\_day\_continuous} &= \left\lfloor \frac{\text{TransactionDT}}{86400} \right\rfloor
\end{align}

Following the execution of the PySpark ETL job, validation performed via BigQuery confirmed dataset integrity across the full 182-day scope ($N = 590,540$). Analysis of the engineered \texttt{DT\_hour} feature reveals a pronounced non-linear relationship between transaction volume and fraud probability.

\begin{table}[h!]
\centering
\caption{Distribution of Transactions and Fraud Rates by Hour of Day (\texttt{DT\_hour})}
\label{tab:temporal_fraud_dist}
\begin{tabular}{ccccc}
\hline
\textbf{Time Window / Hour} & \textbf{Total Volume} & \textbf{Fraud Count} & \textbf{Fraud Rate (\%)} & \textbf{Risk Level} \\ \hline
05:00 -- 07:59 & 19,412 & 1,542 & 7.94\% -- 10.61\% & \textbf{Extreme} \\
08:00 -- 09:59 & 5,070 & 464 & 9.00\% -- 9.30\% & \textbf{High} \\
00:00 -- 04:59 & 142,965 & 4,809 & 3.13\% -- 5.19\% & Moderate \\
10:00 -- 12:59 & 22,905 & 837 & 3.04\% -- 5.32\% & Moderate \\
13:00 -- 15:59 & 82,502 & 2,011 & 2.29\% -- 2.54\% & \textbf{Low (Baseline)} \\
16:00 -- 23:59 & 317,686 & 11,000 & 2.95\% -- 3.70\% & Baseline \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Off-Peak Vulnerability Window:} Between \texttt{05:00} and \texttt{09:59}, transaction volume reaches its lowest daily troughs (dipping to just 2,479 total transactions at \texttt{09:00}). However, the fraud rate peaks dramatically, reaching a maximum of \textbf{10.61\% at 07:00 AM}—more than three times the dataset baseline average ($\sim3.5\%$).
    \item \textbf{High-Volume Low-Risk Windows:} Conversely, peak legitimate activity occurs during hours \texttt{13:00} through \texttt{15:59} ($\sim30,000$ to $40,000$ transactions per hour), where the fraud rate drops to its minimum of \textbf{2.29\%}.
    \item \textbf{Predictive Utility for Tree Models:} This high variance in fraud concentration across hours provides XGBoost with explicit split boundaries. Rather than attempting to learn time series decay over raw timestamps, gradient boosting decisions can isolate off-peak hours as high-probability fraud indicators.
\end{itemize}

### 2. Creación de "Usuarios Virtuales" (*Virtual User ID*)

El dataset de IEEE-CIS no incluye un identificador único de usuario (`UserID`). Para solucionar esto y rastrear el comportamiento histórico de una misma tarjeta o dispositivo, los ganadores construyeron un identificador sintético combinando campos estáticos de la tarjeta y la dirección:

* **Combinación:** Concatenar columnas como `card1`, `card2`, `card3`, `card5` y `addr1`.
* **Por qué funciona:** Si una misma tarjeta realiza 10 transacciones en 5 minutos en diferentes partes del mundo, el modelo lo detectará fácilmente gracias a este ID virtual.

\subsection{Phase 2: Empirical Analysis of Synthetic Virtual User Identifiers}

Due to the absence of a explicit customer account key within the dataset, a synthetic Virtual User Identifier (\texttt{UID\_card\_addr}) was constructed by concatenating static card parameters (\texttt{card1}--\texttt{card6}) and location metadata (\texttt{addr1}). Frequency encoding (\texttt{UID\_card\_addr\_fq}) was subsequently computed to quantify historical transaction density per synthesized entity.

\begin{equation}
    \text{UID\_card\_addr} = \text{card1} \mathbin{\Vert} \text{card2} \mathbin{\Vert} \text{card3} \mathbin{\Vert} \text{card4} \mathbin{\Vert} \text{card5} \mathbin{\Vert} \text{card6} \mathbin{\Vert} \text{addr1}
\end{equation}

Validation across the step output confirms the synthesis of $43,018$ unique entity profiles from raw individual fields ($13,553$ unique \texttt{card1} instances and $332$ unique \texttt{addr1} regions).

\begin{table}[h!]
\centering
\caption{Distribution of Transactions and Fraud Concentration by Virtual User Activity Bucket}
\label{tab:uid_activity_dist}
\begin{tabular}{lcccc}
\hline
\textbf{User Activity Bucket} & \textbf{Total Volume} & \textbf{Fraud Count} & \textbf{Fraud Rate (\%)} & \textbf{\% of Total Fraud} \\ \hline
1 Transaction (Single-use) & 17,358 & 572 & 3.30\% & 2.77\% \\
2 -- 5 Transactions & 40,121 & 1,216 & 3.03\% & 5.88\% \\
6 -- 20 Transactions & 80,177 & 2,246 & 2.80\% & 10.87\% \\
$>$ 20 Transactions (High Volume) & 452,884 & 16,629 & 3.67\% & \textbf{80.48\%} \\ \hline
\textbf{Total / Summary} & \textbf{590,540} & \textbf{20,663} & \textbf{3.50\%} & \textbf{100.00\%} \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Entity Consolidation:} The composite identifier effectively resolves entity disambiguation, reducing $590,540$ raw logs into $43,018$ distinct behavioral profiles with an average density of $757.33$ transactions per profile key.
    \item \textbf{Fraud Concentration in High-Velocity Profiles:} Entities exhibiting $> 20$ transactions account for $80.48\%$ ($16,629$ out of $20,663$) of all fraudulent instances. This behavioral concentration provides tree-based models like XGBoost with an explicit mechanism to flag automated high-frequency card testing.
\end{itemize}

### 4. Frecuencia y Agregaciones por Ventanas Temporales (*Aggregation & Frequency Encoding*)

El fraude suele manifestarse mediante ráfagas repentinas de actividad.

* **Frecuencia de tarjetas/IPs:** Contar cuántas veces aparece una dirección IP (`P_emaildomain` o `id_01` a `id_11`) o una tarjeta en el dataset. Las IPs o tarjetas que aparecen una sola vez o miles de veces inusualmente suelen tener patrones de riesgo.
* **Agregaciones por Usuario Virtual:** Calcular métricas acumuladas utilizando ventanas temporales sobre el ID virtual (por ejemplo: importe medio gastado por ese usuario, número de transacciones en las últimas 24 horas). Un incremento repentino respecto al comportamiento histórico del usuario es un indicador masivo de fraude (*account takeover*).

\subsection{Phase 4: Empirical Analysis of Virtual User Aggregations and Relative Amount Velocity}

To detect account takeover anomalies and unusual purchasing spikes, statistical aggregations were computed across each Virtual User Identifier (\texttt{UID\_card\_addr}). Features measuring relative deviation and proportional ratios against individual historical spending were engineered:
\begin{align}
    \text{uid\_amt\_diff\_mean} &= \text{TransactionAmt} - \mu_{\text{UID}} \\
    \text{uid\_amt\_ratio\_mean} &= \frac{\text{TransactionAmt}}{\mu_{\text{UID}} + \epsilon}
\end{align}
where $\mu_{\text{UID}} = \mathbb{E}[\text{TransactionAmt} \mid \text{UID\_card\_addr}]$ and $\epsilon = 10^{-5}$ prevents division by zero for single-transaction profiles.

Validation confirms dataset volume retention ($N = 590,540$) with an overall mean spending baseline of $\$135.03$ ($\sigma = \$239.16$).

\begin{table}[h!]
\centering
\caption{Transaction Volume and Fraud Concentration by Relative Amount Deviation Bucket}
\label{tab:user_agg_dist}
\begin{tabular}{lcccc}
\hline
\textbf{Amount Deviation Bucket} & \textbf{Total Volume} & \textbf{Fraud Count} & \textbf{Fraud Rate (\%)} & \textbf{\% of Total Fraud} \\ \hline
1.5x -- 3x User Average (Moderate Spike) & 67,373 & 3,471 & \textbf{5.15\%} & 16.80\% \\
$>$ 3x User Average (Extreme Spike) & 23,383 & 1,076 & \textbf{4.60\%} & 5.21\% \\
Normal Range ($\sim$1x User Average) & 176,027 & 6,720 & 3.82\% & 32.52\% \\
$<$ 0.8x User Average (Below Usual) & 323,757 & 9,396 & 2.90\% & 45.47\% \\ \hline
\textbf{Total / Summary} & \textbf{590,540} & \textbf{20,663} & \textbf{3.50\%} & \textbf{100.00\%} \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Velocity Risk Signal:} Transactions departing from a user's historical mean by $1.5\times$ to $3.0\times$ exhibit a peak fraud incidence of \textbf{5.15\%}, representing a $1.47\times$ lift over the population baseline ($3.50\%$).
    \item \textbf{High-Value Anomaly Detection:} Normalization against $\mu_{\text{UID}}$ allows gradient boosted decision trees to distinguish between high-value transactions made by high-spending users versus sudden unauthorized spend spikes on lower-tier cards.
\end{itemize}

---

### 3. Limpieza de dominios de correo (*Email Domain Grouping*)

Columnas como `P_emaildomain` y `R_emaildomain` tienen docenas de variaciones (ej. `gmail.com`, `gmail.es`, `hotmail.com`, `outlook.com`).

* Agrupar dominios similares bajo su proveedor matriz (ej. unificar todo lo relacionado con Microsoft en `microsoft`, y Google en `google`) reduce la cardinalidad inútil y agrupa mejor la información para que los árboles de decisión de XGBoost encuentren divisiones óptimas.

\subsection{Phase 3: Empirical Analysis of Email Domain Standardisation and Feature Extraction}

Email metadata fields \texttt{P\_emaildomain} (purchaser) and \texttt{R\_emaildomain} (recipient) initially contained high sparsity and regional fragmentation (59 and 60 unique domain suffixes, respectively). Furthermore, missing values represented $16.00\%$ of purchaser emails ($94,456$ logs) and $76.75\%$ of recipient emails ($453,249$ logs). 

To consolidate these features, regex-based parsing mapped raw strings into 8 corporate parent providers (\texttt{google}, \texttt{microsoft}, \texttt{yahoo}, \texttt{apple}, \texttt{aol}, \texttt{anonymous}, \texttt{missing}, and \texttt{other}). Additionally, a binary indicator \texttt{email\_domain\_match} was extracted:
\begin{equation}
    \text{email\_domain\_match} = \begin{cases} 
    1 & \text{if } \text{P\_emaildomain} = \text{R\_emaildomain} \neq \varnothing \\ 
    0 & \text{otherwise} 
    \end{cases}
\end{equation}

\begin{table}[h!]
\centering
\caption{Transaction Distribution and Fraud Rates by Mapped Purchaser Email Provider}
\label{tab:email_provider_dist}
\begin{tabular}{lcccc}
\hline
\textbf{Mapped Provider (\texttt{P\_emaildomain\_bin})} & \textbf{Total Volume} & \textbf{Fraud Count} & \textbf{Fraud Rate (\%)} & \textbf{\% of Total Fraud} \\ \hline
Microsoft & 59,477 & 3,170 & \textbf{5.33\%} & 15.34\% \\
Google & 228,851 & 9,954 & \textbf{4.35\%} & \textbf{48.17\%} \\
Missing & 94,456 & 2,790 & 2.95\% & 13.50\% \\
Apple & 8,225 & 238 & 2.89\% & 1.15\% \\
Anonymous & 36,998 & 859 & 2.32\% & 4.16\% \\
AOL & 28,604 & 657 & 2.30\% & 3.18\% \\
Yahoo & 105,305 & 2,370 & 2.25\% & 11.47\% \\
Other & 28,624 & 625 & 2.18\% & 3.03\% \\ \hline
\textbf{Total / Summary} & \textbf{590,540} & \textbf{20,663} & \textbf{3.50\%} & \textbf{100.00\%} \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Dimensionality Reduction:} Mapping reduced category cardinality by $>86\%$, preventing feature space explosion prior to model ingestion.
    \item \textbf{Provider Risk Asymmetry:} Transactions originating from \texttt{Microsoft} domains present a fraud rate ($5.33\%$) that is $2.44\times$ higher than legacy providers such as \texttt{Other} ($2.18\%$) or \texttt{Yahoo} ($2.25\%$).
    \item \textbf{Concentration of Fraud Volume:} \texttt{Google} and \texttt{Microsoft} collectively account for \textbf{63.51\%} of total fraud events ($13,124$ out of $20,663$), establishing purchaser email provider as a primary splitting candidate for gradient boosted decision trees.
\end{itemize}

---

Script de la Fase 5 Ajustado: etl_05_encoding_selection.py
En vista de tu gráfica, mantenemos todas las variables con nulos altos y aplicamos una lógica limpia:

Eliminamos explícitamente las variables de texto plano originales y de ID (TransactionID, P_emaildomain, R_emaildomain, UID_card_addr).

Convertimos todas las variables categóricas (como los _bin de correo que creamos) usando StringIndexer con handleInvalid="keep".

Eliminamos únicamente columnas de varianza cero (constantes), si existiera alguna.

Guarda este código en tu bucket como gs://fraud-detection-imf/etl/etl_05_encoding_selection.py:

\subsection{Phase 5: Categorical Encoding and Feature Matrix Standardization}

To prepare the high-dimensional feature set for ingestion into gradient-boosted decision tree architectures, all residual textual attributes were converted into numeric representations. Rather than utilizing one-hot encoding—which would exponentially expand the feature matrix given high-cardinality attributes—a null-preserving \texttt{StringIndexer} transformation (label encoding) was implemented.

Identifier variables lacking predictive variance or serving strictly as raw keys (\texttt{TransactionID}, original unparsed \texttt{P\_emaildomain}, \texttt{R\_emaildomain}, and raw string \texttt{UID\_card\_addr}) were purged from the feature space, reducing total matrix dimensionality from $448$ to $444$ columns.

\begin{table}[h!]
\centering
\caption{Feature Matrix Pipeline Schema Evolution Across ETL Phases}
\label{tab:etl_schema_evolution}
\begin{tabular}{lccc}
\hline
\textbf{ETL Phase / Storage Artifact} & \textbf{Total Records ($N$)} & \textbf{Column Count} & \textbf{String Attributes} \\ \hline
Phase 0 (Raw Joined Parquet) & 590,540 & 434 & 31 \\
Phase 1 (\texttt{step\_01\_temporal.parquet}) & 590,540 & 437 & 31 \\
Phase 2 (\texttt{step\_02\_uid.parquet}) & 590,540 & 439 & 32 \\
Phase 3 (\texttt{step\_03\_email.parquet}) & 590,540 & 442 & 34 \\
Phase 4 (\texttt{step\_04\_agg.parquet}) & 590,540 & 448 & 34 \\
Phase 5 (\texttt{step\_05\_encoding\_selection.parquet}) & \textbf{590,540} & \textbf{444} & \textbf{0} \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Missing Value Preservation for GBDT:} Null values across high-missingness feature blocks (e.g., $V$-series and $D$-series variables) were explicitly preserved rather than imputed, allowing XGBoost to learn optimal default split directions for missing indicators natively.
    \item \textbf{Type Uniformity:} All boolean flags and indexed strings were cast to discrete integer representations, producing a pure numerical matrix ($\mathbf{X} \in \mathbb{R}^{590540 \times 443}$, excluding the binary target vector $y = \text{isFraud}$).
\end{itemize}

\subsection{Phase 6: Temporal Partitioning and Imbalance Ratio Calibration}

To simulate operational deployment and prevent temporal data leakage—wherein future transaction artifacts inadvertently inform past predictions—a strict out-of-time (OOT) temporal split was enforced on \texttt{DT\_day\_continuous}. Random $k$-fold cross-validation was explicitly avoided due to its tendency to produce overly optimistic performance estimates in time-series fraud detection.

Transactions occurring during the first 145 days were allocated to the baseline training set, while the remaining window (days 146 through 182) was reserved exclusively for out-of-time evaluation.

\begin{table}[h!]
\centering
\caption{Temporal Partitioning Metrics and Label Stability Across Split Windows}
\label{tab:temporal_split_dist}
\begin{tabular}{lccccc}
\hline
\textbf{Partition Name} & \textbf{Day Range} & \textbf{Total Volume ($N$)} & \textbf{Fraud Count} & \textbf{Fraud Rate (\%)} & \textbf{Volume (\%)} \\ \hline
Baseline Train & Days 1 -- 145 & 484,847 & 17,052 & 3.52\% & 82.10\% \\
Baseline Test (OOT) & Days 146 -- 182 & 105,693 & 3,611 & 3.42\% & 17.90\% \\ \hline
\textbf{Total / Population} & \textbf{Days 1 -- 182} & \textbf{590,540} & \textbf{20,663} & \textbf{3.50\%} & \textbf{100.00\%} \\ \hline
\end{tabular}
\end{table}

\subsubsection{Key Structural Insights}
\begin{itemize}
    \item \textbf{Absence of Label Concept Drift:} The target class prevalence remains remarkably stable across time windows ($3.52\%$ in training vs. $3.42\%$ in out-of-time validation), confirming that class distribution does not shift dramatically across temporal boundaries.
    \item \textbf{Loss Function Calibration:} To address severe class imbalance ($1:27.44$ positive-to-negative ratio) without synthesizing artificial observations via SMOTE, the gradient boosted loss function parameter \texttt{scale\_pos\_weight} is calibrated directly on the training partition:
    \begin{equation}
        \text{scale\_pos\_weight} = \frac{N_{\text{train, negative}}}{N_{\text{train, positive}}} = \frac{467,795}{17,052} \approx 27.43
    \end{equation}
    This weight forces XGBoost to scale gradients corresponding to positive fraud instances, optimizing the Precision-Recall Area Under the Curve (PR-AUC) during gradient optimization.
\end{itemize}