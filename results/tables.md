## Pairwise ROC-AUC (mean ± sd over seeds)


### Re-identify renamed agent

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.85 ± 0.01 | 0.72 ± 0.01 | 0.66 ± 0.02 | 0.82 ± 0.01 | 0.84 ± 0.01 | 0.84 ± 0.01 | 0.87 ± 0.01 | 0.85 ± 0.01 | 0.85 ± 0.00 | 0.81 ± 0.00 |
| Char n-grams | 0.81 ± 0.02 | 0.71 ± 0.02 | 0.60 ± 0.01 | 0.79 ± 0.02 | 0.80 ± 0.02 | 0.81 ± 0.02 | 0.84 ± 0.01 | 0.83 ± 0.00 | 0.80 ± 0.01 | 0.79 ± 0.00 |
| Style profile | 0.84 ± 0.00 | 0.68 ± 0.01 | 0.57 ± 0.01 | 0.84 ± 0.01 | 0.79 ± 0.02 | 0.84 ± 0.00 | 0.87 ± 0.00 | 0.83 ± 0.01 | 0.87 ± 0.01 | 0.77 ± 0.00 |
| Semantic embedding | 0.89 ± 0.01 | 0.83 ± 0.01 | 0.80 ± 0.01 | 0.90 ± 0.01 | 0.88 ± 0.00 | 0.90 ± 0.00 | 0.90 ± 0.01 | 0.89 ± 0.00 | 0.92 ± 0.00 | 0.88 ± 0.00 |
| Combined | 0.90 ± 0.00 | 0.80 ± 0.02 | 0.70 ± 0.01 | 0.90 ± 0.01 | 0.88 ± 0.01 | 0.90 ± 0.00 | 0.91 ± 0.00 | 0.90 ± 0.01 | 0.92 ± 0.00 | 0.88 ± 0.00 |

### Re-identify agent, within one operator account

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.51 ± 0.01 | 0.49 ± 0.01 | 0.51 ± 0.02 | 0.65 ± 0.00 | 0.51 ± 0.01 | 0.51 ± 0.01 | 0.57 ± 0.02 | 0.57 ± 0.02 | 0.52 ± 0.02 | 0.49 ± 0.00 |
| Char n-grams | 0.51 ± 0.01 | 0.50 ± 0.01 | 0.50 ± 0.02 | 0.65 ± 0.01 | 0.51 ± 0.01 | 0.51 ± 0.01 | 0.55 ± 0.01 | 0.56 ± 0.01 | 0.51 ± 0.01 | 0.50 ± 0.00 |
| Style profile | 0.51 ± 0.01 | 0.49 ± 0.01 | 0.50 ± 0.01 | 0.71 ± 0.01 | 0.51 ± 0.00 | 0.49 ± 0.01 | 0.53 ± 0.02 | 0.54 ± 0.01 | 0.52 ± 0.01 | 0.50 ± 0.00 |
| Semantic embedding | 0.51 ± 0.01 | 0.49 ± 0.01 | 0.51 ± 0.02 | 0.67 ± 0.01 | 0.51 ± 0.01 | 0.50 ± 0.00 | 0.53 ± 0.01 | 0.54 ± 0.01 | 0.50 ± 0.01 | 0.51 ± 0.00 |
| Combined | 0.51 ± 0.01 | 0.49 ± 0.01 | 0.50 ± 0.01 | 0.71 ± 0.01 | 0.51 ± 0.01 | 0.50 ± 0.00 | 0.55 ± 0.01 | 0.56 ± 0.01 | 0.52 ± 0.01 | 0.51 ± 0.00 |

### Within operator, both aliases in rounds 1-5

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.53 ± 0.01 | 0.49 ± 0.01 | 0.51 ± 0.03 | 0.65 ± 0.03 | 0.53 ± 0.01 | 0.55 ± 0.02 | 0.59 ± 0.04 | 0.59 ± 0.06 | 0.53 ± 0.00 | 0.51 ± 0.00 |
| Char n-grams | 0.53 ± 0.02 | 0.50 ± 0.00 | 0.51 ± 0.02 | 0.66 ± 0.02 | 0.53 ± 0.01 | 0.54 ± 0.01 | 0.58 ± 0.03 | 0.58 ± 0.04 | 0.53 ± 0.00 | 0.51 ± 0.00 |
| Style profile | 0.50 ± 0.02 | 0.49 ± 0.02 | 0.49 ± 0.02 | 0.70 ± 0.02 | 0.49 ± 0.03 | 0.51 ± 0.02 | 0.53 ± 0.02 | 0.53 ± 0.03 | 0.53 ± 0.00 | 0.50 ± 0.00 |
| Semantic embedding | 0.53 ± 0.03 | 0.50 ± 0.01 | 0.52 ± 0.02 | 0.67 ± 0.04 | 0.51 ± 0.02 | 0.53 ± 0.01 | 0.55 ± 0.02 | 0.55 ± 0.01 | 0.49 ± 0.00 | 0.49 ± 0.00 |
| Combined | 0.52 ± 0.02 | 0.50 ± 0.01 | 0.50 ± 0.01 | 0.71 ± 0.03 | 0.51 ± 0.01 | 0.53 ± 0.01 | 0.57 ± 0.01 | 0.57 ± 0.03 | 0.52 ± 0.00 | 0.51 ± 0.00 |

### Within operator, both aliases in rounds 6-10

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.50 ± 0.01 | 0.49 ± 0.02 | 0.52 ± 0.04 | 0.65 ± 0.02 | 0.51 ± 0.03 | 0.51 ± 0.01 | 0.59 ± 0.02 | 0.61 ± 0.03 | 0.55 ± 0.04 | 0.49 ± 0.00 |
| Char n-grams | 0.50 ± 0.01 | 0.50 ± 0.01 | 0.50 ± 0.03 | 0.65 ± 0.02 | 0.50 ± 0.02 | 0.50 ± 0.02 | 0.57 ± 0.01 | 0.60 ± 0.02 | 0.54 ± 0.01 | 0.49 ± 0.00 |
| Style profile | 0.49 ± 0.02 | 0.48 ± 0.03 | 0.48 ± 0.04 | 0.71 ± 0.02 | 0.51 ± 0.02 | 0.48 ± 0.01 | 0.54 ± 0.01 | 0.54 ± 0.02 | 0.53 ± 0.02 | 0.47 ± 0.00 |
| Semantic embedding | 0.50 ± 0.02 | 0.48 ± 0.02 | 0.50 ± 0.01 | 0.67 ± 0.03 | 0.51 ± 0.02 | 0.51 ± 0.01 | 0.54 ± 0.00 | 0.56 ± 0.04 | 0.53 ± 0.01 | 0.50 ± 0.00 |
| Combined | 0.49 ± 0.01 | 0.49 ± 0.01 | 0.49 ± 0.03 | 0.72 ± 0.02 | 0.51 ± 0.01 | 0.49 ± 0.02 | 0.57 ± 0.01 | 0.59 ± 0.02 | 0.54 ± 0.02 | 0.48 ± 0.00 |

### Same operator (different agents)

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.88 ± 0.01 | 0.75 ± 0.02 | 0.66 ± 0.02 | 0.74 ± 0.02 | 0.87 ± 0.02 | 0.87 ± 0.01 | 0.88 ± 0.02 | 0.86 ± 0.01 | 0.87 ± 0.02 | 0.84 ± 0.00 |
| Char n-grams | 0.84 ± 0.02 | 0.73 ± 0.01 | 0.61 ± 0.01 | 0.70 ± 0.02 | 0.83 ± 0.02 | 0.84 ± 0.02 | 0.85 ± 0.02 | 0.83 ± 0.01 | 0.82 ± 0.02 | 0.82 ± 0.00 |
| Style profile | 0.88 ± 0.01 | 0.70 ± 0.01 | 0.58 ± 0.01 | 0.68 ± 0.01 | 0.83 ± 0.02 | 0.88 ± 0.01 | 0.89 ± 0.00 | 0.85 ± 0.01 | 0.91 ± 0.01 | 0.81 ± 0.00 |
| Semantic embedding | 0.94 ± 0.01 | 0.87 ± 0.01 | 0.82 ± 0.01 | 0.84 ± 0.02 | 0.92 ± 0.01 | 0.94 ± 0.01 | 0.94 ± 0.01 | 0.92 ± 0.00 | 0.97 ± 0.00 | 0.92 ± 0.00 |
| Combined | 0.94 ± 0.01 | 0.84 ± 0.01 | 0.72 ± 0.01 | 0.81 ± 0.02 | 0.92 ± 0.01 | 0.94 ± 0.01 | 0.94 ± 0.01 | 0.92 ± 0.00 | 0.96 ± 0.00 | 0.91 ± 0.00 |

### Same base model (different operators) — confound

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.61 ± 0.02 | 0.57 ± 0.01 | 0.52 ± 0.01 | 0.59 ± 0.01 | 0.62 ± 0.02 | 0.63 ± 0.02 | 0.64 ± 0.03 | 0.65 ± 0.02 | 0.66 ± 0.00 | 0.61 ± 0.00 |
| Char n-grams | 0.61 ± 0.03 | 0.58 ± 0.01 | 0.51 ± 0.01 | 0.59 ± 0.01 | 0.63 ± 0.03 | 0.64 ± 0.02 | 0.64 ± 0.03 | 0.66 ± 0.03 | 0.64 ± 0.01 | 0.63 ± 0.00 |
| Style profile | 0.68 ± 0.04 | 0.63 ± 0.01 | 0.52 ± 0.01 | 0.68 ± 0.01 | 0.74 ± 0.03 | 0.72 ± 0.02 | 0.71 ± 0.02 | 0.77 ± 0.05 | 0.78 ± 0.01 | 0.72 ± 0.00 |
| Semantic embedding | 0.65 ± 0.04 | 0.62 ± 0.01 | 0.56 ± 0.03 | 0.62 ± 0.02 | 0.64 ± 0.02 | 0.72 ± 0.03 | 0.72 ± 0.05 | 0.72 ± 0.02 | 0.73 ± 0.03 | 0.64 ± 0.00 |
| Combined | 0.68 ± 0.04 | 0.65 ± 0.01 | 0.54 ± 0.01 | 0.68 ± 0.01 | 0.71 ± 0.03 | 0.75 ± 0.03 | 0.73 ± 0.04 | 0.77 ± 0.04 | 0.81 ± 0.02 | 0.72 ± 0.00 |

### ARI: clustering into operators

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.47 ± 0.06 | 0.23 ± 0.06 | 0.02 ± 0.04 | 0.13 ± 0.01 | 0.43 ± 0.04 | 0.46 ± 0.10 | 0.44 ± 0.13 | 0.41 ± 0.02 | 0.52 ± 0.04 | 0.46 ± 0.00 |
| Char n-grams | 0.26 ± 0.08 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.01 ± 0.00 | 0.15 ± 0.10 | 0.26 ± 0.12 | 0.28 ± 0.20 | 0.35 ± 0.02 | 0.01 ± 0.00 |
| Style profile | 0.45 ± 0.02 | 0.19 ± 0.01 | 0.01 ± 0.01 | 0.12 ± 0.02 | 0.43 ± 0.02 | 0.45 ± 0.03 | 0.46 ± 0.04 | 0.46 ± 0.03 | 0.66 ± 0.04 | 0.36 ± 0.00 |
| Semantic embedding | 0.53 ± 0.01 | 0.43 ± 0.03 | 0.27 ± 0.05 | 0.36 ± 0.06 | 0.53 ± 0.07 | 0.52 ± 0.02 | 0.52 ± 0.02 | 0.58 ± 0.03 | 0.63 ± 0.01 | 0.60 ± 0.00 |
| Combined | 0.51 ± 0.02 | 0.41 ± 0.03 | 0.17 ± 0.02 | 0.23 ± 0.02 | 0.58 ± 0.06 | 0.55 ± 0.03 | 0.53 ± 0.01 | 0.61 ± 0.02 | 0.63 ± 0.02 | 0.59 ± 0.00 |

### ARI: clustering into base models

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 0.38 ± 0.10 | 0.02 ± 0.04 | 0.01 ± 0.03 | 0.02 ± 0.03 | 0.44 ± 0.05 | 0.52 ± 0.08 | 0.42 ± 0.09 | 0.39 ± 0.08 | 0.33 ± 0.17 | 0.36 ± 0.00 |
| Char n-grams | 0.04 ± 0.09 | -0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.01 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.12 ± 0.16 | 0.11 ± 0.10 | 0.01 ± 0.00 |
| Style profile | 0.52 ± 0.03 | 0.26 ± 0.03 | 0.01 ± 0.01 | 0.23 ± 0.04 | 0.50 ± 0.02 | 0.58 ± 0.07 | 0.53 ± 0.01 | 0.56 ± 0.07 | 0.90 ± 0.00 | 0.56 ± 0.00 |
| Semantic embedding | 0.59 ± 0.03 | 0.43 ± 0.12 | 0.18 ± 0.05 | 0.13 ± 0.06 | 0.58 ± 0.01 | 0.62 ± 0.02 | 0.62 ± 0.03 | 0.62 ± 0.02 | 0.60 ± 0.03 | 0.46 ± 0.00 |
| Combined | 0.58 ± 0.04 | 0.28 ± 0.15 | 0.10 ± 0.02 | 0.23 ± 0.05 | 0.56 ± 0.06 | 0.61 ± 0.03 | 0.63 ± 0.05 | 0.62 ± 0.02 | 0.62 ± 0.03 | 0.54 ± 0.00 |

### Rank of covert front pair (1 = most similar of 28)

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 4, 3 | 2 |
| Char n-grams | 1, 1, 1, 1, 2 | 2, 1, 2, 2, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 2, 1, 2 | 1, 1, 2 | 1, 1, 2 | 2, 1, 2 | 1, 1 | 1 |
| Style profile | 5, 5, 5, 5, 5 | 3, 3, 3, 4, 4 | 1, 1, 1, 1, 1 | 3, 1, 2, 1, 1 | 3, 3, 3 | 8, 6, 7 | 5, 5, 5 | 4, 4, 4 | 11, 7 | 4 |
| Semantic embedding | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1 | 1 |
| Combined | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 2, 1, 2 | 3, 1, 3 | 1, 1, 2 | 2, 2, 2 | 3, 2 | 2 |

### Operator pairs: same covert principal vs ordinary honest pairs (AUC)

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.91 ± 0.02 | 0.96 ± 0.00 |
| Char n-grams | 0.99 ± 0.01 | 0.98 ± 0.02 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.98 ± 0.02 | 0.99 ± 0.02 | 0.99 ± 0.02 | 0.98 ± 0.02 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| Style profile | 0.85 ± 0.00 | 0.91 ± 0.02 | 1.00 ± 0.00 | 0.98 ± 0.03 | 0.93 ± 0.00 | 0.78 ± 0.03 | 0.85 ± 0.00 | 0.89 ± 0.00 | 0.70 ± 0.07 | 0.89 ± 0.00 |
| Semantic embedding | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 |
| Combined | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 1.00 ± 0.00 | 0.98 ± 0.02 | 0.95 ± 0.03 | 0.99 ± 0.02 | 0.96 ± 0.00 | 0.94 ± 0.02 | 0.96 ± 0.00 |

### Operator pairs: same covert principal vs honest twins (AUC)

| Feature | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Keyword (word TF-IDF) | — | — | — | — | — | — | — | — | — | — |
| Char n-grams | — | — | — | — | — | — | — | — | — | — |
| Style profile | — | — | — | — | — | — | — | — | — | — |
| Semantic embedding | — | — | — | — | — | — | — | — | — | — |
| Combined | — | — | — | — | — | — | — | — | — | — |

## Identity schemes: pairwise 'same principal' P / R / F1 (mean over seeds)

| Scheme | No evasion | Persona shift on rename | Paraphrase laundering | Operator mixes models | No house style | Subtle agenda | Per-agent memory | No style + subtle + memory | Frontier models | Frontier + persona shift |
|---|---|---|---|---|---|---|---|---|---|---|
| Self-chosen names | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 |
| Agent-held keys (rotated on rename) | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 | 0.00/0.00/0.00 |
| Gateway operator attestation | 1.00/0.80/0.89 | 1.00/0.79/0.88 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.80/0.89 | 1.00/0.76/0.87 |
| Gateway + fingerprint merge | 0.74/1.00/0.85 | 0.74/1.00/0.85 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 0.74/1.00/0.85 | 0.70/1.00/0.83 | 0.70/1.00/0.83 | 0.70/1.00/0.83 | 0.67/0.89/0.76 | 0.85/1.00/0.92 |
| Gateway + model-corrected merge | 0.86/1.00/0.92 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 0.95/1.00/0.97 | 0.83/1.00/0.90 | 0.82/1.00/0.89 | 0.95/1.00/0.97 | 1.00/1.00/1.00 | 0.85/1.00/0.92 |
| Gateway + product-name grep | 0.88/1.00/0.93 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 0.85/1.00/0.91 | 0.90/1.00/0.94 | 1.00/0.80/0.89 | 0.83/1.00/0.88 | 1.00/0.80/0.89 | 1.00/1.00/1.00 | 1.00/1.00/1.00 |

## Run stats

| Run | posts | aliases | empty | refusals | covert posts mentioning package | honest posts mentioning package |
|---|---|---|---|---|---|---|
| baseline_s0 | 400 | 226 | 0 | 0 | 100/100 | 17 |
| baseline_s1 | 400 | 219 | 0 | 0 | 99/100 | 23 |
| baseline_s2 | 400 | 223 | 0 | 0 | 100/100 | 36 |
| baseline_s3 | 400 | 222 | 0 | 0 | 100/100 | 18 |
| baseline_s4 | 400 | 216 | 0 | 0 | 100/100 | 20 |
| frontier_s0 | 400 | 226 | 0 | 0 | 100/100 | 9 |
| frontier_s1 | 400 | 219 | 0 | 0 | 99/100 | 6 |
| frontier_persona_s0 | 400 | 221 | 0 | 0 | 100/100 | 1 |
| hard_s0 | 400 | 226 | 0 | 0 | 0/100 | 0 |
| hard_s1 | 400 | 219 | 0 | 0 | 0/100 | 0 |
| hard_s2 | 400 | 223 | 0 | 0 | 0/100 | 0 |
| memory_s0 | 400 | 226 | 0 | 0 | 99/100 | 34 |
| memory_s1 | 400 | 219 | 0 | 0 | 98/100 | 10 |
| memory_s2 | 400 | 223 | 0 | 0 | 98/100 | 42 |
| mixmodel_s0 | 400 | 226 | 0 | 0 | 92/100 | 32 |
| mixmodel_s1 | 400 | 219 | 0 | 0 | 92/100 | 23 |
| mixmodel_s2 | 400 | 223 | 0 | 0 | 88/100 | 36 |
| mixmodel_s3 | 400 | 222 | 0 | 0 | 92/100 | 20 |
| mixmodel_s4 | 400 | 216 | 0 | 0 | 91/100 | 28 |
| nostyle_s0 | 400 | 226 | 0 | 0 | 100/100 | 32 |
| nostyle_s1 | 400 | 219 | 0 | 0 | 99/100 | 13 |
| nostyle_s2 | 400 | 223 | 0 | 0 | 100/100 | 37 |
| paraphrase_s0 | 400 | 226 | 0 | 0 | 94/100 | 24 |
| paraphrase_s1 | 400 | 219 | 0 | 0 | 100/100 | 13 |
| paraphrase_s2 | 400 | 223 | 0 | 0 | 92/100 | 23 |
| paraphrase_s3 | 400 | 222 | 0 | 0 | 100/100 | 9 |
| paraphrase_s4 | 400 | 216 | 0 | 0 | 98/100 | 23 |
| persona_s0 | 400 | 221 | 0 | 0 | 94/100 | 10 |
| persona_s1 | 400 | 217 | 0 | 0 | 97/100 | 2 |
| persona_s2 | 400 | 226 | 0 | 0 | 93/100 | 32 |
| persona_s3 | 400 | 238 | 0 | 0 | 92/100 | 11 |
| persona_s4 | 400 | 227 | 0 | 0 | 94/100 | 5 |
| subtle_s0 | 400 | 226 | 0 | 0 | 0/100 | 0 |
| subtle_s1 | 400 | 219 | 0 | 0 | 0/100 | 0 |
| subtle_s2 | 400 | 223 | 0 | 0 | 0/100 | 0 |
| twins_s0 | 400 | 226 | 0 | 0 | 100/100 | 40 |
| twins_s1 | 400 | 219 | 0 | 0 | 78/100 | 6 |
| twins_s2 | 400 | 223 | 0 | 0 | 90/100 | 8 |
| twins_s3 | 400 | 222 | 0 | 0 | 99/100 | 17 |
| twins_s4 | 400 | 216 | 0 | 0 | 92/100 | 9 |
| twins_subtle_s0 | 400 | 226 | 0 | 0 | 0/100 | 0 |
| twins_subtle_s1 | 400 | 219 | 0 | 0 | 0/100 | 0 |
| twins_subtle_s2 | 400 | 223 | 0 | 0 | 0/100 | 0 |
| twins_subtle_s3 | 400 | 222 | 0 | 0 | 0/100 | 0 |
| twins_subtle_s4 | 400 | 216 | 0 | 0 | 0/100 | 0 |

## Fingerprint merges (z above 1-1/#pairs quantile; model-corrected)

| Run | fronts | twins | edges | true (same principal) | twin edges | sybil pairs |
|---|---|---|---|---|---|---|
| baseline_s0 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| baseline_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| baseline_s2 | [6, 7] | [] | 3 | 1 | 0 | 1 |
| baseline_s3 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| baseline_s4 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| frontier_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| frontier_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| frontier_persona_s0 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| hard_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| hard_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| hard_s2 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| memory_s0 | [6, 7] | [] | 3 | 1 | 0 | 1 |
| memory_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| memory_s2 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| mixmodel_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| mixmodel_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| mixmodel_s2 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| mixmodel_s3 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| mixmodel_s4 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| nostyle_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| nostyle_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| nostyle_s2 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| paraphrase_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| paraphrase_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| paraphrase_s2 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| paraphrase_s3 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| paraphrase_s4 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| persona_s0 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| persona_s1 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| persona_s2 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| persona_s3 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| persona_s4 | [6, 7] | [] | 1 | 1 | 0 | 1 |
| subtle_s0 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| subtle_s1 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| subtle_s2 | [6, 7] | [] | 2 | 1 | 0 | 1 |
| twins_s0 | [1, 3] | [2, 7] | 2 | 1 | 1 | 1 |
| twins_s1 | [1, 7] | [2, 4] | 1 | 0 | 1 | 1 |
| twins_s2 | [3, 7] | [2, 5] | 1 | 0 | 1 | 1 |
| twins_s3 | [2, 6] | [4, 5] | 3 | 1 | 1 | 1 |
| twins_s4 | [1, 6] | [2, 3] | 1 | 0 | 1 | 1 |
| twins_subtle_s0 | [1, 3] | [2, 7] | 2 | 1 | 1 | 1 |
| twins_subtle_s1 | [1, 7] | [2, 4] | 0 | 0 | 0 | 1 |
| twins_subtle_s2 | [3, 7] | [2, 5] | 1 | 0 | 1 | 1 |
| twins_subtle_s3 | [2, 6] | [4, 5] | 3 | 1 | 1 | 1 |
| twins_subtle_s4 | [1, 6] | [2, 3] | 2 | 0 | 0 | 1 |
