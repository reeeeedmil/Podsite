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
        while True:
            if ctvrty >= 256:
                treti += 1
                ctvrty -= 256
            else: break
        
        while True:
            if treti >= 256:
                druhy += 1
                treti -= 256
            else: break
        
        while True:
            if druhy >= 256:
                prvni += 1
                druhy -= 256
            else: break
            
        self.prvni_byte = prvni
        self.druhy_byte = druhy
        self.treti_byte = treti
        self.ctvrty_byte = ctvrty
            
    def update_broadcast(self, pocet_hostu):
        zvyseni_prvniho_bytu, zvyseni_druheho_bytu, zvyseni_tretiho_bytu = 0, 0, 0
        prvni_byte = self.prvni_byte
        druhy_byte = self.druhy_byte
        treti_byte = self.treti_byte
        ctvrty_byte = pocet_hostu+self.ctvrty_byte
        pouzite_byty = 0
        posledni_zvetseni = 0
    
        while ctvrty_byte >= 256:
            ctvrty_byte -= 256
            zvyseni_tretiho_bytu += 1
        treti_byte += zvyseni_tretiho_bytu
    
        while treti_byte >= 256:
            treti_byte -= 256
            zvyseni_druheho_bytu += 1
        druhy_byte += zvyseni_druheho_bytu
    
        while druhy_byte >= 256:
            druhy_byte -= 256
            zvyseni_prvniho_bytu += 1
        prvni_byte += zvyseni_prvniho_bytu

        if prvni_byte != self.prvni_byte:
            posledni_zvetseni = 1
        elif druhy_byte != self.druhy_byte:
            posledni_zvetseni = 2
        elif treti_byte != self.treti_byte:
            posledni_zvetseni = 3
        else:
            posledni_zvetseni = 4
        
        
        match posledni_zvetseni:
            case 4: ctvrty_byte-=1
            case 3: treti_byte-=1; ctvrty_byte=255 
            case 2: druhy_byte-=1; treti_byte=255; ctvrty_byte=255
            case 1: prvni_byte-=1; druhy_byte=255; treti_byte=255; ctvrty_byte=255
        
        
        self.prvni_byte_broadcast = prvni_byte
        self.druhy_byte_broadcast = druhy_byte
        self.treti_byte_broadcast  = treti_byte
        self.ctvrty_byte_broadcast = ctvrty_byte
        
    def update_prefix(self, prefix, pocet_hostu):
        self.prefix = prefix
        self.pocet_hostu = pocet_hostu
        
    def update_maska(self):
        prvni_byte_masky = 255
        druhy_byte_masky = 255
        treti_byte_masky = 255
        ctvrty_byte_masky = 255
        soucet_pouzitych_cisel_prefixu = 0
    
        if self.prefix < 8:
            mocnina = 8-self.prefix-soucet_pouzitych_cisel_prefixu
            prvni_byte_masky = 255-(2**mocnina)+1
            soucet_pouzitych_cisel_prefixu += mocnina
        
    
        if self.prefix < 16:
            mocnina = 16-self.prefix-soucet_pouzitych_cisel_prefixu
            druhy_byte_masky = 255-(2**mocnina)+1
            soucet_pouzitych_cisel_prefixu += mocnina
        
        
        if self.prefix < 24:
            mocnina = 24-self.prefix-soucet_pouzitych_cisel_prefixu
            treti_byte_masky = 255-(2**mocnina)+1
            soucet_pouzitych_cisel_prefixu += mocnina
        
    
        if self.prefix < 32:
            mocnina = 32-self.prefix-soucet_pouzitych_cisel_prefixu
            ctvrty_byte_masky = 255-(2**mocnina)+1
            soucet_pouzitych_cisel_prefixu += mocnina
        
                      
        self.prvni_byte_masky = prvni_byte_masky
        self.druhy_byte_masky = druhy_byte_masky
        self.treti_byte_masky = treti_byte_masky
        self.ctvrty_byte_masky = ctvrty_byte_masky
        
    def update_wildcard_maska(self):
        prvni_byte_wildcard_masky = 0
        druhy_byte_wildcard_masky = 0
        treti_byte_wildcard_masky = 0
        ctvrty_byte_wildcard_masky = 0
        soucet_pouzitych_cisel_prefixu = 0
    
        if self.prefix < 8:
            mocnina = 8-self.prefix-soucet_pouzitych_cisel_prefixu
            prvni_byte_wildcard_masky = 0+(2**mocnina)-1
            soucet_pouzitych_cisel_prefixu += mocnina
        
    
        if self.prefix < 16:
            mocnina = 16-self.prefix-soucet_pouzitych_cisel_prefixu
            druhy_byte_wildcard_masky = 0+(2**mocnina)-1
            soucet_pouzitych_cisel_prefixu += mocnina
        
        
        if self.prefix < 24:
            mocnina = 24-self.prefix-soucet_pouzitych_cisel_prefixu
            treti_byte_wildcard_masky = 0+(2**mocnina)-1
            soucet_pouzitych_cisel_prefixu += mocnina
        
    
        if self.prefix < 32:
            mocnina = 32-self.prefix-soucet_pouzitych_cisel_prefixu
            ctvrty_byte_wildcard_masky = 0+(2**mocnina)-1
            soucet_pouzitych_cisel_prefixu += mocnina
        
                      
        self.prvni_byte_wildcard_masky = prvni_byte_wildcard_masky
        self.druhy_byte_wildcard_masky = druhy_byte_wildcard_masky
        self.treti_byte_wildcard_masky = treti_byte_wildcard_masky
        self.ctvrty_byte_wildcard_masky = ctvrty_byte_wildcard_masky 
        
        

def menu_hlavni():
    zakladni_adresa = None
    vyber = -1
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
            except:
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
    vyber = -1
    podsite = None
    while vyber != 0:
        print('''
0 - Předchozí menu
1 - Zadání podsítí podle počtu hostů
2 - Zadání podsítí podle prefixů: ''')
        while True:
            try:
                vyber = int(input("Zadej výběr: "))
            except:
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
    try:
        print("0 - Předchozí menu \nZadej 1 až {0} na zobrazení podsítě, 1 je největší síť.".format(len(adresy_podsite)))
    except:
        print("Neexistující rozsah.")
        return
    while True:
        try:
            vyber = int(input("Zadej číslo: "))
        except:
            print(ERROR_ZNAK)
        if vyber == 0:
            break
        elif vyber >= 1 and vyber <= len(adresy_podsite):
            vyber-=1
            print('''
                  
Síť {0}.
Adresa sítě: {1}.{2}.{3}.{4} /{5}
Adresa broadcast: {6}.{7}.{8}.{9} /{5}
Počet adres: {10}
Počet hostů: {11}
Maska: {12}.{13}.{14}.{15}
Wildcard maska: {16}.{17}.{18}.{19}
'''.format(
    vyber+1,
    adresy_podsite[vyber].prvni_byte, adresy_podsite[vyber].druhy_byte, adresy_podsite[vyber].treti_byte, adresy_podsite[vyber].ctvrty_byte,
    adresy_podsite[vyber].prefix,
    
    adresy_podsite[vyber].prvni_byte_broadcast, adresy_podsite[vyber].druhy_byte_broadcast,
    adresy_podsite[vyber].treti_byte_broadcast, adresy_podsite[vyber].ctvrty_byte_broadcast,
    
    adresy_podsite[vyber].pocet_hostu,
    adresy_podsite[vyber].pocet_hostu-2,
    adresy_podsite[vyber].prvni_byte_masky, adresy_podsite[vyber].druhy_byte_masky,
    adresy_podsite[vyber].treti_byte_masky, adresy_podsite[vyber].ctvrty_byte_masky,
    
    adresy_podsite[vyber].prvni_byte_wildcard_masky, adresy_podsite[vyber].druhy_byte_wildcard_masky,
    adresy_podsite[vyber].treti_byte_wildcard_masky, adresy_podsite[vyber].ctvrty_byte_wildcard_masky
))

def kombinace_zakladni_adresy_a_podsiti(zakladni_adresa, podsite):
    if zakladni_adresa == None:
        zakladni_adresa = Sit()
    adresy_siti = []
    soucet_ctvrtych_bytu = 0
    
    for cislo_site in range(0, len(podsite)):
        adresa = Sit()
        
        adresa.update_bytes(zakladni_adresa.prvni_byte, zakladni_adresa.druhy_byte, zakladni_adresa.treti_byte, soucet_ctvrtych_bytu)
        soucet_ctvrtych_bytu += podsite[cislo_site]
        
        adresa.update_prefix(pocet_hostu_na_prefix(podsite[cislo_site]), podsite[cislo_site])
        
        adresa.update_maska()
        
        adresa.update_wildcard_maska()
        
        
        
        adresa.update_broadcast(podsite[cislo_site])
        
        adresy_siti.append(adresa)
        
    return adresy_siti

def pocet_hostu_na_prefix(pocet_hostu):
    prefix = 32
    puvodni_velikost = pocet_hostu
    mocnina = 0
    while True:
        pocet_hostu = puvodni_velikost
        pocet_hostu -= 2**mocnina
        if pocet_hostu <= 0:
            break
        mocnina += 1
        
    prefix -= mocnina
    return prefix

def prefix_na_pocet_hostu(prefix):
    posledni_byte_prefixu = 32-prefix
    pocet_adres = 0
    for mocnina in range(0, posledni_byte_prefixu):
        pocet_adres += 2**mocnina
    return pocet_adres+1


        
    return prvni_byte, druhy_byte, treti_byte, ctvrty_byte


def input_zakladni_ipv4_adresy():
    zakladni_adresa = Sit()
    prvni_byte = -1
    druhy_byte = -1
    treti_byte = -1
    ctvrty_byte = -1
    while True:
        try:
            prvni_byte = int(input("Zadej první byte: "))
        except:
            print(ERROR_ZNAK)
        if prvni_byte >= 0 and prvni_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue

 
    while True:
        try:
            druhy_byte = int(input("Zadej druhý byte: "))
        except:
            print(ERROR_ZNAK)
        if druhy_byte >= 0 and druhy_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue
        
        
    while True:
        try:
            treti_byte = int(input("Zadej třetí byte: "))
        except:
            print(ERROR_ZNAK)
        if treti_byte >= 0 and treti_byte <= 255:
            break
        else:
            print(ERROR_ROZSAH)
            continue
        
        
    while True:
        try:
            ctvrty_byte = int(input("Zadej čtvrtý byte: "))
        except:
            print(ERROR_ZNAK)
        if ctvrty_byte > 0 and ctvrty_byte <= 255:
            print("Jsi si jistý, že chceš čtvrtý byte jiný než 0? (A/N)")
            
            try:
                vyber = str(input("Zadej znak: "))
            except:
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
    print("Zadávej prefixy v rozsahu 1-30, pro ukončení zadej 0.")
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
            except:
                print(ERROR_ZNAK)
                continue
            if prefix == 0:
                break
            elif prefix < 0 or prefix > 30:
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
            except:
                print(ERROR_ZNAK)
                continue
            if pocet_hostu == 0:
                break
            elif pocet_hostu <= 1 or pocet_hostu >= 2147483645:
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
            except:
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
    try:
        print("0 - Předchozí menu \nZadej 1 až {0} na zobrazení podsítě, 1 je největší síť.".format(len(adresy_podsite)))
    except:
        print("Neexistující rozsah.")
        return
    textak=open('Adresace.txt', "w+", encoding="utf=16")
    for index in range(0, len(site)):
        textak.write('''Síť {0}.
Adresa sítě: {1}.{2}.{3}.{4} /{5}
Adresa broadcast: {6}.{7}.{8}.{9} /{5}
Počet adres: {10}
Počet hostů: {11}
Maska: {12}.{13}.{14}.{15}
Wildcard maska: {16}.{17}.{18}.{19}

'''.format(
    index+1,
    site[index].prvni_byte, site[index].druhy_byte, site[index].treti_byte, site[index].ctvrty_byte,
    site[index].prefix,
    
    site[index].prvni_byte_broadcast, site[index].druhy_byte_broadcast,
    site[index].treti_byte_broadcast, site[index].ctvrty_byte_broadcast,
    
    site[index].pocet_hostu,
    site[index].pocet_hostu-2,
    site[index].prvni_byte_masky, site[index].druhy_byte_masky,
    site[index].treti_byte_masky, site[index].ctvrty_byte_masky,
    
    site[index].prvni_byte_wildcard_masky, site[index].druhy_byte_wildcard_masky,
    site[index].treti_byte_wildcard_masky, site[index].ctvrty_byte_wildcard_masky))
    textak.close()
    print("Zapsání úspěšné.\n")


# MAIN
print("Program na podsítě")
menu_hlavni()
