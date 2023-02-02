#Radmil Hrbek
#version 0.0.1

class Podsit:
    nazev: str
    pocet_adres: int
    maska: int
    adresa_site: int
    def __init__(self, podsite):
        try:
            self.nazev = str(input("Zadej název sítě: "))
            self.pocet_adres = podsite
            self.maska = 256 - podsite
            self.adresa_site = int(input("Zadej adresu sítě: "))
        except ValueError:
            print("Není vhodný input.")



def HostCalculator():
    while True:
        try:
            pocet_hostu = int(input("Zadej kolik hostů má síť {}.".format(i+1)))
            if pocet_hostu > 1 and pocet_hostu < 256:
                break
            else:
                continue
        except ValueError:
            print("Není celé číslo.")
            continue
    pocet_pouzitych_adres = pocet_hostu+2
    match pocet_pouzitych_adres:
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 4:
            return 4
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 8:
            return 8
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 16:
            return 16
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 32:
            return 32
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 64:
            return 64
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 128:
            return 128
        case pocet_pouzitych_adres if pocet_pouzitych_adres <= 256:
            return 256

print("program na podsítě\n")
pocet_podsiti = int(input("Zadej kolik potřebuješ podsítí: "))
podsite = []
podsite_informace = {}

for i in range(0, pocet_podsiti):
    podsite.append(HostCalculator())
    podsite.sort(reverse=True)

print(podsite)

for i in range(0, len(podsite)):
    informace = Podsit(podsite[i])
    index = i
    data = [informace.nazev, informace.pocet_adres, informace.maska, informace.adresa_site]
    podsite_informace[i] = data

print("Podsítě vytvořeny.\n\n")
while True:
    index_podsite = int(input("Zadej index podsítě ze které chceš data: "))
    if index_podsite > len(podsite_informace) or index_podsite < 0:
        print("Nevhodné číslo, zadej znova.")
    else:
        print(podsite_informace.get(index_podsite))