import random

def gen_nom_alea():
    nom_base = ("Andromeda","Proxima", "Alpha", "Kepler", "list2")
    suffixe = ("dd", "hh", "HD", "Thug", "de l\'EI", "KSP", "MDR")
    return random.choice(nom_base) + "-pd-" + random.choice(suffixe) + str(random.randint(0,99))

def dist_eucl(x1, x2, y1, y2):
    return ((x2-x1)**2 + (y2-y1)**2) ** 0.5

def gen_univ(nbre_sys_solaire, taille_x, taille_y, facteur_alea=1):

    univers = list()
    dist_univers = dist_eucl(taille_x, 0, taille_y, 0)
    while len(univers) < nbre_sys_solaire:
        x = round(random.uniform(0, taille_x))
        y = round(random.uniform(0, taille_y))
        if len(univers) == 0:
            univers.append([x, y, gen_nom_alea()])
        else:
            compteur_mauvaise_planete = 0
            for systeme in univers:
                distance = dist_eucl (x, systeme[0], y, systeme[1])
                seuil = 0.10
                if distance/dist_univers < seuil * facteur_alea:
                    compteur_mauvaise_planete +=1

            if compteur_mauvaise_planete == 0:
                univers.append([x, y, gen_nom_alea()])

    return univers
