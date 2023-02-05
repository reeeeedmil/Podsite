#Radmil Hrbek
#version 0.2.3

ERROR1 = "Neplatný znak"
PRIKAZY = {"1":"\nHostname zařízení:\n\nenable\nconfigure terminal\nhostname (název zařízení)",
"2a":'''
Zabezpečení routeru:

enable
configure terminal
enable secret cisco
line console 0
password cisco
login
line vty 0 4
password cisco
login
line aux 0
password cisco
login
service password-encryption
end''',

"3":'''
Nastavení DHCP na routeru:

enable
configure terminal
ip dhcp pool (název DHCP skupiny)
network (adresa sítě) (maska)
defaultr-router (default-gateway adresa)
dns-server (adresa DNS serveru)
exit
ip dhcp excluded-address (první ip adresa) (poslední ip adresa) ((rozsah adres, které nebudou přiřazeny))
end''',
            
"2b":'''
Zabezpečení switche:

enable
configure terminal
interface vlan 1
ip address (adresa switche) (maska)
ip default-gateway (default-gateway adresa)
exit
enable secret cisco
line console 0
password cisco
login
line vty 0 4
password cisco
login
line aux 0
password cisco
login
end''',

}

podsite = []
podsite_informace = {}
pocet_zvetseni = 0

def HostCalculator():
    while True:
        try:
            pocet_hostu = int(input("Zadej kolik hostů má síť {}.: ".format(i+1)))
            if pocet_hostu > 1 and pocet_hostu < 256:
                break
            else:
                print("Neplatný počet hostů.")
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


def Adresa_site_Calculator(podsite, y, zvetseni):
    for i in range(0, len(podsite)):
        adresa_site = 0
        x = 0
        while True:
            if y == 0:
                return 0
            elif x < y:
                adresa_site += podsite[x]
                while adresa_site >= 256:
                    adresa_site -= 256
                x += 1
                if x == y:
                    return adresa_site
                else: continue
            else:
                break

def Data_podsiti(posledni):
    print("Zadej číslo sítě (1 je největší síť, {} je nejmenší síť, 0 tě vrátí do menu)".format(posledni))
    while True:
        try:
            index_podsite = int(input("Číslo sítě: "))-1
        except ValueError:
            print(ERROR1 + "\n")
            continue
        if index_podsite+1 == 0:
            break
        elif index_podsite > len(podsite_informace)-1 or index_podsite < 0:
            print("Nevhodné číslo, zadej znova. \n")
        else:
            data_podsiti_vysledek = (podsite_informace.get(index_podsite))
            print('''
Název sítě: {}
Počet adres: {}
Maska: 255.255.255.{}
Adresa sítě: {}.{}.{}.{}

'''.format(
                data_podsiti_vysledek[0],
                data_podsiti_vysledek[1],
                data_podsiti_vysledek[2],
                data_podsiti_vysledek[3],
                data_podsiti_vysledek[4],
                data_podsiti_vysledek[5],
                data_podsiti_vysledek[6]
                ))

def Prikazy():
    print("\n\nZadáním znaků dostaneš příkazy (0 tě vrátí do menu): ")
    print('''\"1\" pro hostname
\"2a\" pro zabezpečení routeru
"2b\" pro zabezpečení
\"3\" pro DHCP na routeru\'''')

    while True:
        try:
            prikaz = str(input("\nZadej znaky: "))
        except ValueError:
            print(ERROR1)
            continue
        if prikaz == "0":
            break
        else:
            try:
                print(PRIKAZY.get(prikaz))
            except ValueError:
                print(ERROR1)

def Smerovaci_protokoly():
    print("0. tě vrátí do menu\n1. OSPF")
    vyber_protoklu = None
    while vyber_protoklu != 0:
        try:
            vyber_protoklu = int(input("Zadej číslo nabídky: "))
        except ValueError:
            print(ERROR1)
        match vyber_protoklu:
            case vyber_protoklu if vyber_protoklu == 0:
                continue
            case vyber_protoklu if vyber_protoklu == 1:
                OSPF()

def OSPF():
    print("\nSměrovací protokol OSPF")
    OSPF_cislo = int(input("Zadej číslo OSPF procesu: "))
    area = int(input("Zadej číslo tvé area: "))
    print("Zadej číslo sítě (1 je největší síť, {} je nejmenší síť, 0 tě vrátí do menu)".format(len(podsite)))
    while True:
        try:
            index_podsite = int(input("Číslo sítě: "))-1
        except ValueError:
            print(ERROR1 + "\n")
            continue
        if index_podsite+1 == 0:
            break
        elif index_podsite > len(podsite_informace)-1 or index_podsite < 0:
            print("Nevhodné číslo, zadej znova. \n")
        else:
            data_podsiti_vysledek = (podsite_informace.get(index_podsite))
            wildcard = 255 - data_podsiti_vysledek[2]
            print('''

Název sítě: {}
Počet adres v síti: {}
Adresa sítě: {}.{}.{}.{}
Wildcard maska: 0.0.0.{}

enable
configure terminal
router ospf {}
network {}.{}.{}.{} 0.0.0.{} area {}\n'''.format(data_podsiti_vysledek[0], data_podsiti_vysledek[1],
                                                data_podsiti_vysledek[3], data_podsiti_vysledek[4],
                                                data_podsiti_vysledek[5], data_podsiti_vysledek[6],
                                                wildcard, OSPF_cislo,
                                                data_podsiti_vysledek[3], data_podsiti_vysledek[4],
                                                data_podsiti_vysledek[5], data_podsiti_vysledek[6],
                                                wildcard, area))




















print("program na podsítě\n")

nabidka = None
while nabidka != 0:
    while True:
        print("0. Ukončí program\n1. Vytvoření podsítí\n2. Data o podsítích\n3. Příkazy\n4. Směrovací protokoly\n")
        try:
            nabidka = int(input("Zadej číslo nabídky: "))
            if nabidka < 0 or nabidka > 4:
                continue
        except ValueError:
            print(ERROR1)
        match nabidka:
            case nabidka if nabidka == 0:
                exit()
            case nabidka if nabidka == 1:
                zvetseni_tretiho_bytu = 0
                #Zadání prvních 3 bytů adresy
                podsite.clear()
                podsite_informace.clear()
                while True:
                    try:
                        prvni_byte = int(input("Zadej první byte adresy: "))
                        druhy_byte = int(input("Zadej druhý byte adresy: "))
                        treti_byte = int(input("Zadej třetí byte adresy: "))
                        if prvni_byte < 256 and druhy_byte < 256 and treti_byte < 256:
                            break
                        else: 
                            print("Jeden z bytů je neplatný.")
                            continue
                    except ValueError:
                        print(ERROR1)
                        continue
                #Zadání počtu podsítí
                while True:
                    try:
                        pocet_podsiti = int(input("Zadej kolik potřebuješ podsítí: "))
                        break
                    except ValueError:
                        print(ERROR1)
                        continue

                #Zadání velikostí podsítí do listu podsite
                for i in range(0, pocet_podsiti):
                    podsite.append(HostCalculator())
                    podsite.sort(reverse=True)
                print(podsite)
                #Zadání informací o samostatných podsítí do dict podsite_informace
                for i in range(0, len(podsite)):
                    soucet = 0
                    while True:
                        try:
                            nazev = str(input("Zadej název sítě (počet adres = {}): ".format(podsite[i])))
                            break
                        except ValueError:
                            continue
                    pocet_adres = podsite[i]
                    maska = 256 - podsite[i]
                    data = []
                    data.extend((nazev, pocet_adres, maska, prvni_byte, druhy_byte))
                    
                    for ii in range(0, i):
                        if i != ii:
                            soucet += podsite[ii]
                            if soucet >= 256:
                                soucet -= 256
                                zvetseni_tretiho_bytu += 1
                                pocet_zvetseni += 1
                    adresa_site = Adresa_site_Calculator(podsite, i, pocet_zvetseni)
                    data.append(treti_byte+zvetseni_tretiho_bytu)
                    zvetseni_tretiho_bytu = 0
                    data.append(adresa_site)
                    podsite_informace[i] = data
                    
                    
                    
                print("Podsítě vytvořeny.\n\n")

                f=open("Adresace.txt", "w+", encoding='utf=16')
                for i in range(0, len(podsite)):
                            data_podsiti_vysledek = (podsite_informace.get(i))
                            data_1 = str(data_podsiti_vysledek[0])
                            data_2 = str(data_podsiti_vysledek[1])
                            data_3 = str(data_podsiti_vysledek[2])
                            data_4 = str(data_podsiti_vysledek[3])
                            data_5 = str(data_podsiti_vysledek[4])
                            data_6 = str(data_podsiti_vysledek[5])
                            data_7 = str(data_podsiti_vysledek[6])
                            f.write('''
                Název sítě: ''' 
                + data_1 +
                '''\nPočet adres: '''
                + data_2 +
                '''\nMaska: 255.255.255.''' 
                + data_3 + 
                '''\nAdresa sítě: ''' + data_4 + "." + data_5 + "." + data_6 + "." + data_7 + "\n")
                f.close()

            case nabidka if nabidka == 2:
                Data_podsiti(len(podsite))
            case nabidka if nabidka == 3:
                Prikazy()
            case nabidka if nabidka == 4:
                if bool(podsite_informace):
                    Smerovaci_protokoly()
                else:
                    print("\nNejsou vytvořeny podsítě.\n")