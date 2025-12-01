import argparse

def classifica_vehicle(rodes, pes):
    if rodes == 2 and pes < 100:
        return "Bicicleta"
    elif rodes == 2:
        return "Motocicleta"
    elif rodes == 4 and pes < 350:
        return "Cotxe turisme"
    else:
        return "Cotxe familiar"

parser = argparse.ArgumentParser("")

parser.add_argument("totalRodes", help="Número de rodes que té el vehicle 2 o 4", type=int)
parser.add_argument("pes", help="Pes del vehicle amb kgs", type=int)

args = parser.parse_args()

rodes = args.totalRodes
pes = args.pes

print("Vehicle: ",classifica_vehicle(rodes,pes))
