# Diagnòstic sobre la diabetis

Cal fer una anàlisi completa amb dades reals del dataset Pima Indians Diabetes "(https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv)".

L’objectiu és construir un model per predir si una persona tindrà diabetis (1 = sí, 0 = no), analitzar els resultats i treure conclusions sobre la qualitat del model.

Hauràs de:
- carregar el dataset real
- entrenar un Decision Tree
- generar la matriu de confusió
- calcular Accuracy, Precision, Recall i F1-score
- analitzar quin tipus d’error (FP o FN) és més important en aquest problema
- justificar si el model està ben ajustat (train vs test)
- escriure conclusions finals

Per a carregar el dataset utilitza el següent codi

```python
df = pd.read_csv("https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv", header=None)

X = df.iloc[:, :-1]   # 8 variables
y = df.iloc[:, -1]    # classe (0 = no diabètic, 1 = diabètic)
```
