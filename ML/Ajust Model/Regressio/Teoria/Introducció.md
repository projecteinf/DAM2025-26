#  ML esquema (Repàs / esquema general)

```
                        Machine Learning
                                |
        ------------------------------------------------
        |                                              |
 Aprenentatge supervisat                    Aprenentatge no supervisat
        |                                              |
   --------------                              --------------------
   |            |                              |                  |
Classificació  Regressió                  Clustering     Reducció dimensional


```

## Conceptes

- Aprenentatge supervisat → les dades estan etiquetades.

    - Classificació  → el model prediu un valor discret (categoria).

        - Exemple:  

            - Classificar una imatge com gos o gat.  

    - Regressió → el model prediu un valor numèric continu.

        - Exemple:  

            - Determinar el preu de venda d’un immoble: les dades (superfície, situació, etc.) inclouen el preu.

- Aprenentatge no supervisat → les dades no incorporen la dada objectiu (NO etiquetes).

---

# Regressió

## Cas pràctic

Volem predir el preu d’un immoble només a partir de la superfície.

- Dades reals d’habitatges venuts:

| Superfície (m²) | Preu real (€) |
| --------------- | ------------- |
| 50              | 120.000       |
| 70              | 160.000       |
| 90              | 210.000       |
| 110             | 260.000       |

El model “aprèn”  -> com més superfície, més preu

### Predicció

- Quant valdrà un pis de 80 m²?

    * **Predicció:** 180.000 €

- Realitat 

    * **Preu real:** 195.000 €

### Error

- Error = 195.000 − 180.000 = 15.000 €

- Problema

    - La superfície no és l'única dada que determina el preu!  

        * barri
        * estat del pis
        * orientació
        * etc

### Objectiu

- Reduir al màxim l'error amb la informació disponible.  

## Representació gràfica

![Gràfica regressió](./Images/Gràfica%20regressió.png)

- Eixos

    * Eix horitzontal → **superfície (m²)**  

    * Eix vertical → **preu (€)**  

- Punts

    * Pis venut (sabem a quin preu s'ha venut cada pis!)

- Interpretació  
    
    - “Aquest pis tenia X m² i es va vendre per Y €”

- La línia

    * Millor aproximació possible del model per explicar la relació entre superfície i preu.  

        - S’aproxima el màxim possible a tots els punts.  

    * Ens permet predir el preu de l'immoble (segons la seva superfície)

        - Exemple 

            - Quin preu li correspon a un immoble amb una superfície de 90 m²? i de 70 m²?

- Error

    - Distància vertical entre el punt (immoble) i la línia (model/predicció).  

        - Menor distància => menor error!

## Realitat (més dades).  

- El model no és bo només amb la dada de superfície!

- Afegim una nova dada (zona ubicació del immoble: normal / bona)

| Superfície (m²) | Zona   | Preu real (€) |
| --------------- | ------ | ------------- |
| 80              | Normal | 170.000       |
| 80              | Bona   | 220.000       |
| 100             | Normal | 210.000       |
| 100             | Bona   | 280.000       |

![Dades immobles amb la seva zona](./Images/Dades%20immobles%20amb%20zona.png)

- La zona és rellevant per a determinar el preu del immoble!  

### Model

- El model continua essent una línia, tot i que ara ja comença a mostrar les seves limitacions.
  
![Model amb la zona](./Images/Dades%20immobles%20amb%20zona%20-%20Model.png)  

- Interpretació gràfica.  

    - La línia és el que el model ha après.  

    - Per cada superfície, ens diu quin preu espera el model.  

    - Els punts són la realitat. La línia és una aproximació.  

### Reflexió

- “No seria millor una línia que passi exactament per tots els punts?”

- Resposta: en aquest cas, el model s’adaptaria massa a aquestes dades i no generalitzaria bé a nous immobles.

# Underfitting i Overfitting  

- Conceptes ja treballats amb classificació. No varien per a regressió

## Underfitting (model massa simple)

- El model és massa simple per representar la relació entre les dades.

- No captura bé el patró real.

    - L’error és alt tant amb dades conegudes com amb dades noves.

### Exemple 

- Predir el preu d’un immoble utilitzant només la superfície, quan en realitat el preu depèn de més factors (zona, estat, orientació…).

    - El model no aprèn prou de les dades.  

## Overfitting (model massa ajustat)

- El model s’adapta massa a les dades d’entrenament.

- Intenta passar exactament per tots els punts.

- L’error és molt baix amb dades conegudes però alt amb dades noves.

### Exemple

- Un model que passa exactament per tots els punts del dataset però no funciona bé amb nous immobles.

    - El model aprèn el soroll en lloc del patró general.

# Objectiu del model

- No fer un model massa simple.

- No fer un model massa complex.

- Trobar un equilibri que permeti reduir l’error i generalitzar bé.