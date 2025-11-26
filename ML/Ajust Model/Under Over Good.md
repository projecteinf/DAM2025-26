# Carrega del dataset.  

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv", header=None)

df.columns = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigree", "Age", "Outcome"
]

df.head()
```

---

# Separació Train/Test.  

```python
from sklearn.model_selection import train_test_split

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

---

# Entrenament

Prova els models amb els paràmetres proposats per a obtenir la precisió del model en entrenament i test

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# "Decision Tree (max_depth=1)": DecisionTreeClassifier(max_depth=2, random_state=42)
# "Decision Tree (max_depth=10)": DecisionTreeClassifier(max_depth=10, random_state=42)
# "Logistic Regression": LogisticRegression(max_iter=200)
# "kNN (k=3)": KNeighborsClassifier(n_neighbors=3)
# "kNN (k=15)": KNeighborsClassifier(n_neighbors=15)
# "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42)

```

---

# Resultats

- Modifica el codi anterior per a imprimir per pantalla la capçalera i les primeres 5 files (head) del nostre dataset.

- Percentatge de dades.

| Tipus        | Percentatge | 
| :---         |:---         | 
| Entrenament  | ?           | 
| Test         | ?           | 

Omple la següent taula:

| Model                    | Train Acc | Test Acc | Diagnòstic                           |
| ------------------------ | --------- | -------- | ------------------------------------ |
| Decision Tree (depth=2)  | ?         | ?        | Underfitting / Overfitting / Ajustat |
| Decision Tree (depth=10) | ?         | ?        | …                                    |
| Logistic Regression      | ?         | ?        | …                                    |
| kNN (k=3)                | ?         | ?        | …                                    |
| kNN (k=15)               | ?         | ?        | …                                    |
| Random Forest            | ?         | ?        | …                                    |

---

1. Quin model pateix UNDERFITTING? Per què?

2. Quin model pateix OVERFITTING? Per què?

3. Quin model està BEN AJUSTAT?

4. Quin és el millor model de tots segons test accuracy?

5. Creus que amb un model més avançat (SVM, XGBoost) podries superar el 80%? Per què?

6. Si diversos models diferents obtenen precisions similars (0.72–0.77), què significa això sobre el dataset?

7. Quin és el límit pràctic d’accuracy que es pot assolir amb aquest dataset?

8. Què indica això sobre la qualitat de les dades?
