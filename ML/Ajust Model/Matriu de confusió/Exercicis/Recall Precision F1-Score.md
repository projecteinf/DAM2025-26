# EXERCICI 1 — Sistema antispam 

Matriu de confusió:

|             | Pred NO | Pred SI |
| ----------- | ------- | ------- |
| Real NO | 9150    | 270     |
| Real SI | 180     | 400     |

“SI” => SPAM.

## Preguntes

1. Quin tipus d’error és més greu: FP o FN?

1. Quina mètrica és prioritària a maximitzar (Precisió, Recall o F1)?

1. Justifica la resposta.

---

# EXERCICI 2 — Detecció de frau bancari 

Matriu:

|             | Pred NO | Pred SI |
| ----------- | ------- | ------- |
| Real NO | 1900    | 120     |
| Real SI | 45      | 135     |

## Preguntes

1. Quin error és més greu?

1. Cal mirar només precisió o només recall?

1. Quina mètrica recomanaries?

---

# EXERCICI 3 — Diagnòstic de COVID 

Matriu:

|             | Pred NO | Pred SI |
| ----------- | ------- | ------- |
| Real NO | 890     | 130     |
| Real SI | 15      | 65      |

## Preguntes

1. Quin error és més greu?

1. Quina mètrica és prioritària?

1. Els resultats del model són acceptables?


---

# EXERCICI 4 — Reconeixement facial 

Matriu:

|             | Pred NO | Pred SI |
| ----------- | ------- | ------- |
| Real NO | 4800    | 200     |
| Real SI | 190     | 410     |

SI -> Identificació correcte

## Preguntes

1. Quin error és més greu en un aeroport?

1. Quin error és més greu en una porta d’empresa?

1. Quina mètrica prioritzar en cada cas?

---

# EXERCICI 5 — Sistema de recomanació 

Matriu de confusió:

|             | Pred NO | Pred SI |
| ----------- | ------- | ------- |
| Real NO | 7000    | 1400    |
| Real SI | 900     | 1700    |

SI -> Anunci interessant

## Preguntes

1. Quin error molesta més al client?
1. Quin tipus d’error no és especialment greu?
1. Quina mètrica prioritzar?
1. Per què els FN són poc importants?

---

# EXERCICI 6 — Classificador d’imatges (gats vs gossos)**

Matriu de confusió:

|              | Pred GOS | Pred GAT |
| ------------ | -------- | -------- |
| **Real GOS** | 460      | 40       |
| **Real GAT** | 50       | 450      |

## Preguntes

1. Calcula l’**accuracy** del model.
2. El dataset està balancejat?
3. Els errors FP i FN tenen el mateix impacte en aquest problema?
4. És correcte utilitzar l’accuracy com a mètrica principal?
5. Segons l’accuracy, el model és bo?

---

### ✔️ **Solució**

**1. Accuracy**

Total encerts = 460 + 450 = **910**
Total mostres = 1000

```
Accuracy = 910 / 1000 = 0.91 → 91%
```

**2. Dataset balancejat?**
Sí: 500 gats / 500 gossos → classes iguals.

**3. FP i FN tenen el mateix cost?**
Sí, confondre un gat amb un gos o a l’inrevés **no té conseqüències especials**.

**4. És correcte usar Accuracy?**
**Sí**:

* dataset balancejat
* errors FP i FN simètrics
* cap error és crític

**5. El model és bo segons l’Accuracy?**
Sí, 91% és un valor alt i adequat per aquest context.

---


# EXERCICI 6 — Classificador d’imatges (gats vs gossos)

Matriu de confusió:

|              | Pred GOS | Pred GAT |
| ------------ | -------- | -------- |
| Real GOS | 460      | 40       |
| Real GAT | 50       | 450      |

## Preguntes

1. Calcula l’accuracy del model.
2. El dataset està balancejat?
3. Els errors FP i FN tenen el mateix impacte en aquest problema?
4. És correcte utilitzar l’accuracy com a mètrica principal?
5. Segons l’accuracy, el model és bo?

---

# EXERCICI 7 — Predicció d’avaries en màquines industrials

Un model prediu si una màquina fallarà (*FAIL*) o no (*OK*).

Distribució real:

* 90% OK
* 10% FAIL

Matriu de confusió:

|               | Pred OK | Pred FAIL |
| ------------- | ------- | --------- |
| Real OK   | 880     | 20        |
| Real FAIL | 50      | 50        |

## Preguntes

1. Calcula l’accuracy.
2. És un bon model segons l’accuracy?
3. Quin tipus d’error és més greu en aquest context: FP o FN?
4. L’accuracy és una mètrica adequada aquí?
5. Quina mètrica seria millor utilitzar?

---
