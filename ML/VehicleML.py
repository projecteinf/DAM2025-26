""" 
INSTRUCCIONS PREVIES

sudo apt install python3-pip
sudo apt install python3.13-venv
python3 -m venv venv
source venv/bin/activate
python3 VehicleML.py 4 200

"""

# Executar source venv/bin/activate per testejar el programa
import argparse
from sklearn.tree import DecisionTreeClassifier

"""
scikit-learn -> llibreria 
    Proporciona molts “models d’intel·ligència”.
    Li facilitem les dades -> fa treball d'aprendre patrons.
    Nosaltres triem quin model volem -> DecisionTree => Quin tipus d'intel·ligència vull utilitzar
"""

# --- Dades d'entrenament ---
# Característiques: [número de rodes, pes en kg]
X = [[2, 50], [2, 100], [2, 150], [2, 125],
     [4, 400], [4, 500], [4, 300], [4, 200],
	[3,200]]
y = ["Bicicleta", "Bicicleta", "Motocicleta", "Motocicleta",
     "Cotxe familiar", "Cotxe familiar", "Cotxe Turisme", "Cotxe Turisme","Tricicle"]


model = DecisionTreeClassifier()    # Funció de sklearn -> Creem un model buit
model.fit(X, y)                     # Entrenem el model amb les dades que tenim.
                                    

# --- Arguments per consola ---
parser = argparse.ArgumentParser(description="Classificador de vehicles amb ML")
parser.add_argument("rodes", type=int, help="Número de rodes (2 o 4)")
parser.add_argument("pes", type=int, help="Pes del vehicle (kg)")
args = parser.parse_args()

# --- Predicció ---
prediccio = model.predict([[args.rodes, args.pes]])
print(f"Predicció: {prediccio[0]}")
