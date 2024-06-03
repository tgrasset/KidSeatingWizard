import random
import argparse

def read_file(file):
    kids = []
    try:
        with open(file, 'r') as file:
            for line in file:
                if not line.strip() or line.strip().startswith('#'):
                    continue
                data = [element.strip() for element in line.strip().split(',')]
                name = data[0]
                age = data[1]
                chair = data[2]
                conditions = data[3:]
                kids.append({'name': name, 'age': age, 'chair': chair, 'conditions': conditions})
    except Exception as e:
        print(f"{e}")
        exit()
    return kids

def sit_leading_pairs(kids, tables):
    leading_pairs = []
    for kid in kids:
        for condition in kid['conditions']:
            if condition.startswith('&'):
                partner_name = condition[1:]
                partner = next((k for k in kids if k['name'] == partner_name), None)
                if partner and ((kid, partner) not in leading_pairs and (partner, kid) not in leading_pairs):
                    leading_pairs.append((kid, partner))
                    break
    for table in tables:
        if len(table) == 0 and leading_pairs:
            pair = leading_pairs.pop(0)
            table.extend(pair)
            kids = [kid for kid in kids if kid['name'] != pair[0]['name'] and kid['name'] != pair[1]['name']]
    return kids

def map_tables(kids, adult_nb):
    table_nb = (len(kids) + adult_nb) // 7
    if (len(kids) + adult_nb) % 7 != 0:
        table_nb += 1
    tables = [[] for _ in range(table_nb)]
    for i in range(min(adult_nb, table_nb)):
        tables[i].append({'name': 'Adulte' + str(i + 1), 'age': 'adulte', 'chair' : 'autre', 'conditions': []})
    kids = sit_leading_pairs(kids, tables)

    kids_with_adults = [kid for kid in kids if 'avec_adulte' in kid['conditions']]
    other_kids = [kid for kid in kids if kid not in kids_with_adults]

    indexes = list(range(len(kids_with_adults)))
    random.shuffle(indexes)

    for i in indexes:
        tables.sort(key=len)
        placed = False
        for table in tables:
            if table and table[0]['age'] == 'adulte' and len(table) < 7 and all('!'+kids_with_adults[i]['name'] not in kid['conditions'] for kid in table):
                table.append(kids_with_adults[i])
                placed = True
                break
        if not placed:
            print("Oups, ", kids_with_adults[i]['name'], " n'a pas de place, par manque d'adultes ou conditions affinitaires trop restrictives")

    indexes = list(range(len(other_kids)))
    random.shuffle(indexes)
    for i in indexes:
        tables.sort(key=len)
        placed = False
        for table in tables:
            if len(table) < 7 and all('!'+other_kids[i]['name'] not in k['conditions'] for k in table):
                table.append(other_kids[i])
                placed = True
                break
        if not placed:
            print("Oups, ", other_kids[i]['name'], " n'a pas de place, par manque d'adultes ou conditions affinitaires trop restrictives") 
    return tables

def pair_kids(kids):
    primaires = [kid for kid in kids if kid['age'] == 'primaire']
    maternelles = [kid for kid in kids if kid['age'] == 'maternelle']
    pairs = []
    random.shuffle(primaires)
    random.shuffle(maternelles)
    while primaires and maternelles:
        mat = maternelles[0]
        found_pair = False
        for prim in primaires:
            if '!'+prim['name'] in mat['conditions']:
                continue
            pairs.append([mat, prim])
            primaires.remove(prim)
            maternelles.remove(mat)
            found_pair = True
            break
        if found_pair == False:
            break
    while primaires:
        kid1 = primaires.pop(0)
        for prim in primaires:
            if '!'+prim['name'] not in kid1['conditions']:
                pairs.append([kid1, prim])
                primaires.remove(prim)
                break
        else:
            pairs.append([kid1])
    while maternelles:
        kid1 = maternelles.pop(0)
        for mat in maternelles:
            if '!'+mat['name'] not in kid1['conditions']:
                pairs.append([kid1, mat])
                maternelles.remove(mat)
                break
        else:
            pairs.append([kid1])

    return pairs

def print_result(tables, pairs, adult_nb):
    total_veg = 0
    total_no_pork = 0
    total_normal = 0
    total_primaire = 0
    total_maternelle = 0
    for i, table in enumerate(tables, start=1):
        veg = sum(1 for member in table if 'veg' in member['conditions'])
        no_pork = sum(1 for member in table if 'sans_porc' in member['conditions'])
        primaires = sum(1 for member in table if member['age'] == "primaire")
        maternelles = sum(1 for member in table if member['age'] == "maternelle")
        normal = len(table) - veg - no_pork
        if table[0]['age'] == 'adulte':
            normal -= 1
        small_chairs = sum(1 for member in table if member['chair'] == 'petite_chaise')
        big_chairs = sum(1 for member in table if member['chair'] == 'grande_chaise')
        print("Table", i, " : ", [member['name'] for member in table])
        print("            Chaises: ", small_chairs, " petite(s) et ", big_chairs, " grande(s)")
        if table[0]['age'] == 'adulte':
            print("            Adulte: 1")
        else:
            print("            Adulte: 0")
        print("")
        total_veg += veg
        total_no_pork += no_pork
        total_normal += normal 
        total_maternelle += maternelles
        total_primaire += primaires
        
    print("TOTAL: ")
    print("REPARTITION : ",total_maternelle, " maternelle(s), ", total_primaire, " primaire(s), ", adult_nb, " adulte(s).")
    print("MENUS ENFANTS : ", total_no_pork, " sans porc, ", total_veg, " vegetarien(s), ", total_normal, " ordinaire(s). ")
    print("")
    print("Rang : ")
    for pair in pairs:
        if len(pair) == 2:
            print(pair[0]['name'], pair[1]['name'])
        else:
            print(pair[0]['name'])

def main():
    parser = argparse.ArgumentParser(description="Plan de table pour les kids")
    parser.add_argument("data_file", type=str, help="Chemin vers le fichier de data")
    parser.add_argument("adult_nb", type=int, help="Nombre d'adultes encadrants")
    args = parser.parse_args()

    kids = read_file(args.data_file)
    tables= map_tables(kids, args.adult_nb)
    pairs = pair_kids(kids)

    print_result(tables, pairs, args.adult_nb)

if __name__ == "__main__":
    main()
