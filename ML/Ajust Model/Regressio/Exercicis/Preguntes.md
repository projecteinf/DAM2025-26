# Metodologia de treball de la pràctica

Aquesta pràctica s’ha de realitzar de manera progressiva, seguint l’ordre dels scripts proporcionats.
L’objectiu no és només executar el codi, sinó **entendre què fa el model en cada pas i per què el resultat canvia**.

Per a cada script, s’ha de seguir exactament el mateix procediment.

---

## 1. Anàlisi del codi

Abans d’executar el script:

* Llegeix el codi amb atenció.
* Identifica:
  * quines dades s’utilitzen (variables d’entrada),
  * quin model s’està fent servir,
  * quina informació s’està intentant predir.
* Relaciona el codi amb els conceptes teòrics treballats a classe.

* No passis directament a executar el programa.
    * Entendre el codi abans d’executar-lo és part fonamental de la pràctica.

## 2. Execució del script

* Executa el script en el teu entorn de treball.
* Observa el resultat obtingut
* Comprova que el resultat té sentit en funció de les dades utilitzades.

## 3. Anàlisi del resultat

Després de l’execució:

* Analitza el valor de l’error:
* Reflexiona sobre el motiu del resultat:
* No es tracta de jutjar si el resultat és “bo” o “dolent”, sinó d’entendre per què és així.

## 4. Resposta a les preguntes

* Respon les preguntes associades a cada script utilitzant.
* Les respostes han d’estar **raonades**, no només descrites.
* No n’hi ha prou amb dir *“perquè el model és millor”*; cal explicar **què ha canviat i per què**.

### 5. Continuïtat entre scripts

Cada script parteix del coneixement adquirit en l’anterior:

* No són exercicis independents.
* Les conclusions d’un script t’han de servir per entendre el següent.

### 6. Script final (millora del model)

En l’últim script, hauràs d’aplicar el mateix mètode de treball, però modificant el codi per millorar la predicció:

* Cal justificar els canvis realitzats i el seu impacte en el resultat.

---


# Script 1
1. Després de mirar el script, quin model s'està utilitzant?
1. Per quin motiu l'error és tan elevat?
1. Com es pot millorar la precisió de la predicció?

---

# Script 2
1. Per quin motiu l’error ha disminuït respecte a l’script 1?

---

# Script 3
1. Quins factors fan que, en aquest dataset, afegir l’any de construcció tingui un impacte limitat en l’error del model?

---

# Script 4
1. L’error ha augmentat després d’afegir una nova variable. Per quin motiu?

---

# Script 5
1. Modifica el codi del script 3 per millorar la predicció actuant sobre les dades utilitzades pel model (sense canviar l’algoritme).

---


# Codificació

## Script 1
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Dataset
X = np.array([[50], [70], [90], [110]])
y = np.array([120000, 160000, 210000, 260000])

# Model
model = LinearRegression()
model.fit(X, y)

# Predicció
superficie = np.array([[80]])
pred = model.predict(superficie)[0]

# Error
preu_real = 220000  # L'immoble està en una zona bona => preu més elevat. 

error = abs(preu_real - pred)

print("Predicció:", int(pred))
print("Preu real:", preu_real)
print("Error:", int(error))

```


## Script 2
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

def zonaNumericaSerie(zona_series):
    return zona_series.map({
        "Normal": 0,
        "Bona": 1
    })

def zonaNumericaValor(zona):
    return {
        "Normal": 0,
        "Bona": 1
    }[zona]

# Dataset
df = pd.DataFrame({
    "superficie": [80, 80, 100, 100],
    "zona": ["Normal", "Bona", "Normal", "Bona"],
    "preu": [170000, 230000, 210000, 280000]
})

# Model
df["zona_num"] = zonaNumericaSerie(df["zona"])

X = df[["superficie", "zona_num"]]
y = df["preu"]

model = LinearRegression()
model.fit(X, y)

# Predicció
superficie = 80
zona = "Bona"
zona_num = zonaNumericaValor(zona)

test = pd.DataFrame({
    "superficie": [superficie],
    "zona_num": [zona_num]
})

pred = model.predict(test)[0]
preu_real = 220000

error = abs(preu_real - pred)

print("Predicció:", int(pred))
print("Preu real:", preu_real)
print("Error:", int(error))
```


## Script 3
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

def zonaNumericaSerie(zona_series):
    return zona_series.map({
        "Normal": 0,
        "Bona": 1
    })

def zonaNumericaValor(zona):
    return {
        "Normal": 0,
        "Bona": 1
    }[zona]

# Dataset
df = pd.DataFrame({
    "superficie": [80, 80, 100, 100],
    "zona": ["Normal", "Bona", "Normal", "Bona"],
    "any": [1965, 2005, 1965, 2005],
    "preu": [170000, 230000, 210000, 280000]
})

# Conversió zona
df["zona_num"] = zonaNumericaSerie(df["zona"])

# Variables
X = df[["superficie", "zona_num", "any"]]
y = df["preu"]

# Model
model = LinearRegression()
model.fit(X, y)

# Predicció
superficie = 80
zona = "Bona"
any_construccio = 2005

zona_num = zonaNumericaValor(zona)

test = pd.DataFrame({
    "superficie": [superficie],
    "zona_num": [zona_num],
    "any": [any_construccio]
})

pred = model.predict(test)[0]
preu_real = 220000
error = abs(preu_real - pred)

print("Predicció:", int(pred))
print("Preu real:", preu_real)
print("Error:", int(error))

```

## Script 4
```python
import pandas as pd
from sklearn.linear_model import LinearRegression

def zonaNumericaSerie(zona_series):
    return zona_series.map({
        "Normal": 0,
        "Bona": 1
    })

def zonaNumericaValor(zona):
    return {
        "Normal": 0,
        "Bona": 1
    }[zona]

# Dataset (mateix que script 3 + nova variable)
df = pd.DataFrame({
    "superficie": [80, 80, 100, 100],
    "zona": ["Normal", "Bona", "Normal", "Bona"],
    "any": [1965, 2005, 1965, 2005],
    "numero_porta": [12, 87, 34, 56],  # variable inútil però plausible
    "preu": [170000, 220000, 210000, 280000]
})

# Conversió zona
df["zona_num"] = zonaNumericaSerie(df["zona"])

X = df[["superficie", "zona_num", "any", "numero_porta"]]
y = df["preu"]

model = LinearRegression()
model.fit(X, y)

# Predicció
test = pd.DataFrame({
    "superficie": [80],
    "zona_num": [1],
    "any": [2005],
    "numero_porta": [50]
})

pred = model.predict(test)[0]
preu_real = 220000
error = abs(preu_real - pred)

print("Predicció:", int(pred))
print("Preu real:", preu_real)
print("Error:", int(error))

```

