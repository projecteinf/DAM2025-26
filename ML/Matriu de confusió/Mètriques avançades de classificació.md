# Ajust del model - Mètriques avançades 

## Introducció: Accuracy és insuficient!

- Accuracy (Repàs)

    - L'accuracy ens diu el percentatge d'encerts totals.

    - Fòrmula

```
             Encerts
Accuracy = ───────────
              Total
```

    - Fins ara l'hem utilitzat per avaluar models i detectar underfitting/overfitting.

- Problema accuray

    - Enganyós quan les classes estan desbalancejades.

        - Les dades del model ens diu

    - Necessitem mètriques que tinguin en compte els diferents tipus d'errors.

### Exemple 

[Exemple Problema Accuracy - Detecció de fraus - dades no reals](../../Exemples/Accuracy%20problem.py)

```
$ python3 "Accuracy problem.py"

DEMOSTRACIÓ: PROBLEMES DE L'ACCURACY AMB DADES DESBALANCEJADES
======================================================================
Distribució inicial:
- Transaccions normals: 1900 (95.0%)
- Transaccions fraudulentes: 100 (5.0%)

Després de train/test split:
Train: 1400 instàncies (70 fraus)
Test: 600 instàncies (30 fraus)

======================================================================
MODEL : DECISION TREE

Accuracy Train: 0.9879
Accuracy Test:  0.9783

 Anàlisi de detecció de frau:
- Fraus reals en test: 30
- Fraus detectats: 18
- Fraus no detectats (s'han colat): 12
- Tasa de detecció: 60.0%

======================================================================

```

En l'exemple anterior tenim només un 60% de detecció del cas realment important!


# Ajust del model. Precisió i Recall

1. Entendre el problema
1. Definir tipus d'error més important (casos erròniament detectats / casos no detectats / ambdós)
1. Construir matriu de confusió
1. Escollir mètrica o mètriques a utilitzar.
1. Obtenir valors mètriques.
1. Validació de les mètriques.

## Matriu de confusió
  
|      |      | PREDICCIÓ  | PREDICCIÓ  |
| ---: | ---: | ---:       | ---:       |
|      |      |    NO      |   SI       |
|REAL  |  NO  |    TN      |   FP       |
|REAL  |  SI  |    FN      |   TP       |

- En el exemple de detecció de fraus

    - True Positive (TP): El model diu "SI" i és correcte (18)
    - True Negative (TN): El model diu "NO" i és correcte (569) 
    - False Positive (FP): El model diu "SI" però s'equivoca (falsa alarma) (1)
    - False Negative (FN): El model diu "NO" però s'equivoca (cas que s'escapa) (12)

![Matriu de confusió - Detecció de fraus - Dades no reals](../Images/Matriu%20de%20confusió%20Detecció%20Fraus%20-%20Dades%20no%20reals.png)

## Definicir tipus d'error important. 

- Quan calculem l'eficiència d'un model ho hem de fer en relació al problema que s'està tractant.

- Exemple

    - Detecció de frau amb targetes de crèdit.  

        - Precisió: Interessa minimitzar els falsos positius (detecta que es fa frau amb la targeta i és fals => client emprenyat!)

    - Detecció de malalties.  

        - Recall: Interessa minimitzar els falsos negatius (es prediu que no té la malaltia i realment la té)

## Precisió 

- Falsos positius són greus.

- Quan el model diu "SI" quantes vegades és "SI".

### Fórmula 
```
             TP (Encerts "SI")
Precisió = ──────────────────────
            TP + FP (Tots els "SI")
```
## Recall 

- Falsos negatius són greus.

- Dels casos que realment són sí, quants n'ha detectat el model.

### Fórmula visual:
```
             TP (Encerts "SI")
Recall = ──────────────────────
            TP + FN (Tots els "SI" reals)
```

## F1-Score

- La importància dels falsos positius i dels falsos negatius és semblant.

- Combina precisió i recall en un únic valor.

- Útil quan la classe està desbalancejada

### Fórmula

```
              2 x (Precisió x Recall)
F1-Score = ────────────────────────────────
                 Precisió + Recall
```

## Importància matriu de confusió

    - Entendre per què la mètrica surt baixa o alta

    - Analitzar el tipus d’error (FP o FN)

    - Detecció de problemes de biaix

        - TN i FN molt alts
        - TP i FP molt baixos
        
            - El model només sap dir NO.
        
        - TP i FP molt alts
        - TN i FN molt baixos
        
            - El model només sap dir SÍ.
---

# Exemple real

## Detecció càncer de pit

[Codi - Càncer de pit](../../Exemples/Canc<!--  -->erDePit.py)

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

# 1. Càrrega de dades reals
data = load_breast_cancer()
X = data.data
y = data.target  # 0 = malignant, 1 = benign

# 2. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 3. Model: Decision Tree amb fondària 4
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)

# 4. Prediccions
y_train_pred = model.predict(X_train) 
y_test_pred = model.predict(X_test)


# 5. Mètriques
acc_train = accuracy_score(y_train, y_train_pred)
prec_train = precision_score(y_train, y_train_pred)
rec_train = recall_score(y_train, y_train_pred)
f1_train = f1_score(y_train, y_train_pred)

acc_test = accuracy_score(y_test, y_test_pred)
prec_test = precision_score(y_test, y_test_pred)
rec_test = recall_score(y_test, y_test_pred)
f1_test = f1_score(y_test, y_test_pred)




print("===== ACCURACY =====")
print(f"Train:  {acc_train:.4f}")
print(f"Test:  {acc_test:.4f}")
print("===== PRECISION =====")
print(f"Train:  {prec_train:.4f}")
print(f"Test:  {prec_test:.4f}")
print("===== RECALL =====")
print(f"Train:    {rec_train:.4f}")
print(f"Test:    {rec_test:.4f}")
print("===== F1-SCORE =====")
print(f"Train:  {f1_train:.4f}")
print(f"Test:  {f1_test:.4f}")

# 6. Matriu de confusió (valor numèric)
cm = confusion_matrix(y_test, y_test_pred)
print("\nMatriu de confusió:")
print(cm)

# 7. Representació gràfica
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=data.target_names)
disp.plot(cmap="Blues")
plt.title("Matriu de Confusió — Breast Cancer (Decision Tree)")
plt.show()


```

## Resultats 

```
===== ACCURACY =====
Train:  0.9953
Test:  0.9510
===== PRECISION =====
Train:  0.9926
Test:  0.9659
===== RECALL =====
Train:    1.0000
Test:    0.9551
===== F1-SCORE =====
Train:  0.9963
Test:  0.9605

Matriu de confusió:
[[51  3]
 [ 4 85]]

```

![Matriu Confusió - Càncer de pit](../Images/Matriu%20Confusió%20-%20CancerDePit.png)

## Anàlisi

No hi ha underfitting ni overfitting per a cada model. Els valors de train i de test són semblants.

Tots els valors d'ajust del model són elevats i vàlids si la temàtica no fos mèdica. En temes mèdics, es considera un bon model quan l'error és inferior al 2%

La dada més important és la de Recall: 

Quants diagnòstics han detectat com a benigne un tumor que era maligne (FN), 3 per un total de 54 que representa un 5.5% 

En aquest cas, s'hauria de provar si els resultats milloren augmentant la profunditat o utilitzant un model diferent.