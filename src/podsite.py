ERROR_ZNAK = "Neplatný znak";
ERROR_CISLO = "Nevhodné číslo";
ERROR_ROZSAH = "Jsi mimo rozsah!";


class Sit:
    def __init__(self):
        self.prefix = 24
        self.prvni_byte = 0
        self.druhy_byte = 0
        self.treti_byte = 0
        self.ctvrty_byte = 0
        
    def update_bytes(self, prvni, druhy, treti, ctvrty):
        self.prvni_byte = prvni
        self.druhy_byte = druhy
        self.treti_byte = treti
        self.ctvrty_byte = ctvrty
        
    def update_prefix(self, prefix, pocet_hostu):
        self.prefix = prefix
        self.pocet_hostu = pocet_hostu
        


def menu_hlavni():
    zakladni_adresa = None
    vyber = None
    podsite = None
    adresy_podsite = None
    print("HLAVNÍ MENU")
    while vyber != 0:
        print('''
0 - Konec programu
1 - Zadání základní IPv4 adresy
2 - Zadání podsítí
3 - Zobrazení podsítí
4 - Zapsání do Adresace.txt''')
        while True:
            try:
                vyber = int(input("Zadej výběr: "))
            except ValueError():
                print(ERROR_ZNAK)
            if vyber >= 0 and vyber <= 4:
                break
            else:
                print(ERROR_CISLO)
        match vyber:
            case 0: exit()
            case 1: zakladni_adresa = kontrola_pritomnosti(input_zakladni_ipv4_adresy(), zakladni_adresa) 
            case 2: adresy_podsite = kontrola_pritomnosti(menu_zadani_podsiti(zakladni_adresa), adresy_podsite)
            case 3: zobrazeni_podsiti(adresy_podsite)
            case 4: zapsani_do_txt(adresy_podsite)

def menu_zadani_podsiti(zakladni_adresa=None):
    vyber = None
    podsite = None
    while vyber != 0:
        print('''
0 - Předchozí menu
1 - Zadání podsítí podle počtu hostů
2 - Zadání podsítí podle prefixů: ''')
        while True:
            try:
                vyber = int(input("Zadej výběr: "))
            except ValueError():
                print(ERROR_ZNAK)
            if vyber >= 0 and vyber <= 2:
                break
            else:
                print(ERROR_CISLO)
        match vyber:
            case 0: break
            case 1: podsite = vytvoreni_podsiti_podle_poctu_hostu()
            case 2: podsite = vytvoreni_podsiti_podle_prefixu()
        
        return kombinace_zakladni_adresy_a_podsiti(zakladni_adresa, podsite)

def zobrazeni_podsiti(adresy_podsite):
    print("0 - Předchozí menu \nZadej 1 až {0} na zobrazení podsítě, 1 je největší síť.".format(len(adresy_podsite)))
    while True:
        try:
            vyber = int(input("Zadej číslo: "))
        except ValueError():
            print(ERROR_ZNAK)
        if vyber == 0:
            break
        elif vyber >= 1 and vyber <= len(adresy_podsite):
            vyber-=1
            print('''
Síť {0}.
Adresa sítě: {1}.{2}.{3}.{4} /{5}
Adresa broadcast: {1}.{2}.{3}.{6} /{5}
Počet adres: {7}
Počet hostů: {8}'''.format(
    vyber+1,
    adresy_podsite[vyber].prvni_byte, adresy_podsite[vyber].druhy_byte, adresy_podsite[vyber].treti_byte, adresy_podsite[vyber].ctvrty_byte,
    adresy_podsite[vyber].prefix,
    (adresy_podsite[vyber].ctvrty_byte+adresy_podsite[vyber].pocet_hostu-1),
    adresy_podsite[vyber].pocet_hostu,
    adresy_podsite[vyber].pocet_hostu-2
))
            

def vypocet_adresy_site(cislo_site, podsite):
    soucet_hostu = 0
    zvyseni_tretiho_bytu = 0
    for i in range(0, cislo_site):
        soucet_hostu += podsite[i]
        if soucet_hostu >= 256:
            soucet_hostu -= 256
            zvyseni_tretiho_bytu += 1
    return soucet_hostu, zvyseni_tretiho_bytu
        

def kombinace_zakladni_adresy_a_podsiti(zakladni_adresa, podsite):
    if zakladni_adresa == None:
        zakladni_adresa = Sit()
    adresy_siti = []
    for cislo_site in range(0, len(podsite)):
        adresa_site, zvyseni_tretiho_bytu = vypocet_adresy_site(cislo_site, podsite)
        adresa = Sit()
        adresa.update_bytes(zakladni_adresa.prvni_byte, zakladni_adresa.druhy_byte, zakladni_adresa.treti_byte+zvyseni_tretiho_bytu, adresa_site)
        adresa.update_prefix(pocet_hostu_na_prefix(podsite[cislo_site]), podsite[cislo_site])
        
        
        adresy_siti.append(adresa)
    return adresy_siti

def pocet_hostu_na_prefix(pocet_hostu):
    pocet_hostu = 256-pocet_hostu
    pocet_hostu = str(bin(pocet_hostu))
    prefix = 24
    pocet_jednicek = 0
    for cislo in pocet_hostu:
        if cislo == '1':
            pocet_jednicek += 1
    prefix += pocet_jednicek
    return prefix

def prefix_na_pocet_hostu(prefix):
    posledni_byte_prefixu = 32-prefix
    pocet_adres = 0
    for mocnina in range(0, posledni_byte_prefixu):
        pocet_adres += 2**mocnina
    return pocet_adres+1



def input_zakladni_ipv4_adresy():
    zakladni_adresa = Sit()
    while True:
        try:
            prvni_byte = int(input("Zadej první byte: "))
        except ValueError():
            print(ERROR_ZNAK)
        if prvni_byte >= 0 and prvni_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue


    while True:
        try:
            druhy_byte = int(input("Zadej druhý byte: "))
        except ValueError():
            print(ERROR_ZNAK)
        if druhy_byte >= 0 and druhy_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue
        
        
    while True:
        try:
            treti_byte = int(input("Zadej třetí byte: "))
        except ValueError():
            print(ERROR_ZNAK)
        if treti_byte >= 0 and treti_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue
        
        
    while True:
        try:
            ctvrty_byte = int(input("Zadej čtvrtý byte: "))
        except ValueError():
            print(ERROR_ZNAK)
        if ctvrty_byte > 0 and ctvrty_byte <= 255:
            print("Jsi si jistý, že chceš čtvrtý byte jiný než 0? (A/N)")
            
            try:
                vyber = str(input("Zadej znak: "))
            except ValueError():
                print(ERROR_ZNAK)
            
            if vyber == 'A':
                break
            elif vyber == 'N':
                continue
            else:
                print(ERROR_ZNAK)
                continue
                
        elif ctvrty_byte == 0:
            break            

        else:
            print(ERROR_ROZSAH)
            continue
        
        
    zakladni_adresa.update_bytes(prvni_byte, druhy_byte, treti_byte, ctvrty_byte)
    print("{0}.{1}.{2}.{3}".format(
        zakladni_adresa.prvni_byte,
        zakladni_adresa.druhy_byte,
        zakladni_adresa.treti_byte,
        zakladni_adresa.ctvrty_byte,
    ))
    return zakladni_adresa

def vytvoreni_podsiti_podle_prefixu():
    print("Zadávej prefixy v rozsahu 24-30, pro ukončení zadej 0.")
    list_hostu = input_podle_prefixu()
    return list_hostu

def input_podle_prefixu():
    zakladni_prefix = 24
    index_zadavani = 1
    list_hostu = []
    while True:
        
        while True:
            try:
                prefix = int(input("Zadej prefix pro {0}. síť: ".format(index_zadavani)))
            except ValueError():
                print(ERROR_ZNAK)
                continue
            if prefix == 0:
                break
            elif prefix < 24 or prefix > 30:
                print(ERROR_ROZSAH)
                continue
            else:
                break
        if prefix == 0:
            break
        pocet_hostu = prefix_na_pocet_hostu(prefix)
        list_hostu.append(pocet_hostu)
        index_zadavani += 1
    
    list_hostu.sort()
    list_hostu.reverse()
    print(list_hostu)
    return list_hostu        
    

def vytvoreni_podsiti_podle_poctu_hostu():
    print("Zadávej počet hostů v síti, pro ukončení zadej 0.")
    list_hostu = input_podle_hostu() 
    return list_hostu
        
def input_podle_hostu():
    pocet_hostu = -1
    index_zadavani = 1
    list_hostu = []
    while True:

        while True:
            try:
                pocet_hostu = int(input("Zadej počet hostů pro {0}. síť: ".format(index_zadavani)))
            except ValueError():
                print(ERROR_ZNAK)
                continue
            if pocet_hostu == 0:
                break
            elif pocet_hostu <= 1 or pocet_hostu >= 254:
                print(ERROR_ROZSAH)
                continue
            else:
                break
            
        if pocet_hostu == 0:
            break    
        pocet_hostu = standardizace_velikosti(pocet_hostu)
        list_hostu.append(pocet_hostu)
        index_zadavani += 1
    
    list_hostu.sort()
    list_hostu.reverse() 
    print(list_hostu)
    return list_hostu

        
def standardizace_velikosti(velikost_site):
    puvodni_velikost = velikost_site+2
    index = 0
    while True:
        velikost_site = puvodni_velikost
        velikost_site -= 2**index
        index += 1
        if velikost_site <= 0:
            return (2**(index-1))
        
        
def kontrola_pritomnosti(kontrolovana_data, predchozi_data=None):
    if kontrolovana_data != None and predchozi_data != None and predchozi_data != kontrolovana_data:
        print("Chcete přepsat data? (A/N)")
        while True:
            try:
                vyber = str(input("Zadejte znak: "))
            except ValueError():
                print(ERROR_ZNAK)
                continue
            
            if vyber == 'A':
                return kontrolovana_data
            elif vyber == 'N':
                return predchozi_data
            else:
                print(ERROR_ZNAK)
                continue
                
    elif kontrolovana_data != None and predchozi_data == None:
        return kontrolovana_data
    
    elif kontrolovana_data == None and predchozi_data != None:
        return predchozi_data
    
    else:
        return kontrolovana_data


def zapsani_do_txt(site):
    textak=open('Adresace.txt', "w+", encoding="utf=16")
    for index in range(0, len(site)):
        textak.write('''Síť {0}.
Adresa sítě: {1}.{2}.{3}.{4} /{5}
Adresa broadcast: {1}.{2}.{3}.{6} /{5}
Počet adres: {7}
Počet hostů: {8}

'''.format(
    index+1,
    site[index].prvni_byte, site[index].druhy_byte, site[index].treti_byte, site[index].ctvrty_byte,
    site[index].prefix,
    (site[index].ctvrty_byte+site[index].pocet_hostu-1),
    site[index].pocet_hostu,
    site[index].pocet_hostu-2))
    textak.close()




        

# MAIN
print("Program na podsítě")
menu_hlavni()
