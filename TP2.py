"""
TP2 : Gestion d'une base de données d'un hôpital

Groupe de laboratoire : 02
Numéro d'équipe :  02
Noms et matricules : Nom1 (Matricule1), Nom2 (Matricule2)
"""

import csv
import statistics


########################################################################################################## 
# PARTIE 1 : Initialisation des données (2 points)
##########################################################################################################

def load_csv(csv_path, patients_dict = {}):
    """
    Fonction python dont l'objectif est de venir créer un dictionnaire "patients_dict" à partir d'un fichier csv

    Paramètres
    ----------
    csv_path : chaîne de caractères (str)
        Chemin vers le fichier csv (exemple: "/home/data/fichier.csv")
    
    Résultats
    ---------
    patients_dict : dictionnaire python (dict)
        Dictionnaire composé des informations contenues dans le fichier csv
    """

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ID = row['participant_id']
            if ID not in patients_dict:
                patients_dict[ID] = {key: value for key, value in row.items() if key != 'participant_id'}

    return patients_dict

########################################################################################################## 
# PARTIE 2 : Fusion des données (3 points)
########################################################################################################## 

def load_multiple_csv(csv_path1, csv_path2):
    """
    Fonction python dont l'objectif est de venir créer un unique dictionnaire "patients" à partir de deux fichier csv

    Paramètres
    ----------
    csv_path1 : chaîne de caractères (str)
        Chemin vers le premier fichier csv (exemple: "/home/data/fichier1.csv")
    
    csv_path2 : chaîne de caractères (str)
        Chemin vers le second fichier csv (exemple: "/home/data/fichier2.csv")
    
    Résultats
    ---------
    patients_dict : dictionnaire python (dict)
        Dictionnaire composé des informations contenues dans les deux fichier csv SANS DUPLICATIONS
    """
    return load_csv(csv_path2, load_csv(csv_path1))

########################################################################################################## 
# PARTIE 3 : Changements de convention (4 points)
########################################################################################################## 

def update_convention(old_convention_dict):
    """
    Fonction pour mettre à jour la convention des dates et des valeurs 'n/a' dans un dictionnaire de patients.
    
    Paramètres
    ----------
    old_convention_dict : dict
        Dictionnaire contenant les informations des patients selon l'ancienne convention
    
    Résultats
    ---------
    new_convention_dict : dict
        Dictionnaire mis à jour avec les nouvelles conventions
    """
    new_convention_dict = {}
    for participant_id, patient_data in old_convention_dict.items():
        updated_data = {}
        for key, value in patient_data.items():
            updated_data[key] = None if value == "n/a" else value.replace("-", "/") if "-" in value else value
        new_convention_dict[participant_id] = updated_data
            
    return new_convention_dict

########################################################################################################## 
# PARTIE 4 : Recherche de candidats pour une étude (5 points)
########################################################################################################## 

def fetch_candidates(patients_dict):
    """
    Fonction python dont l'objectif est de venir sélectionner des candidats à partir d'un dictionnaire patients et 3 critères:
    - sexe = femme
    - 25 <= âge <= 32
    - taille > 170

    Paramètres
    ----------
    patients_dict : dictionnaire python (dict)
        Dictionnaire contenant les informations des "patients"
    
    Résultats
    ---------
    candidates_list : liste python (list)
        Liste composée des `participant_id` de l'ensemble des candidats suivant les critères
    """

    return [participant_id for participant_id, patient_data in patients_dict.items() if patient_data.get('sex') == 'F' and  (25 <= int(patient_data['age']) <= 32) and (int(patient_data['height']) > 170)]

    

########################################################################################################## 
# PARTIE 5 : Statistiques (6 points)
########################################################################################################## 

def moyenne(liste):
    return round(statistics.mean([float(item) for item in liste if item != 'n/a' and item != None]), 1)

def std(liste):
    return round(statistics.stdev(([float(item) for item in liste if item != 'n/a' and item != None])), 1)

def fetch_statistics(patients_dict):
    """
    Fonction python dont l'objectif est de venir calculer et ranger dans un nouveau dictionnaire "metrics" la moyenne et 
    l'écart type de l'âge, de la taille et de la masse pour chacun des sexes présents dans le dictionnaire "patients_dict".

    Paramètres
    ----------
    patients_dict : dictionnaire python (dict)
        Dictionnaire contenant les informations des "patients"
    
    Résultats
    ---------
    metrics : dictionnaire python (dict)
        Dictionnaire à 3 niveaux contenant:
            - au premier niveau: le sexe --> metrics.keys() == ['M', 'F']
            - au deuxième niveau: les métriques --> metrics['M'].keys() == ['age', 'height', 'weight'] et metrics['F'].keys() == ['age', 'height', 'weight']
            - au troisième niveau: la moyenne et l'écart type --> metrics['M']['age'].keys() == ['mean', 'std'] ...
    
    """
    metrics, midMetricsM, midMetricsF= {'M':{"age": {'mean' : 0, 'std' : 0}, "height": {'mean' : 0, 'std' : 0}, "weight" : {'mean' : 0, 'std' : 0}}, 'F': {"age": {'mean' : 0, 'std' : 0}, "height": {'mean' : 0, 'std' : 0}, "weight" : {'mean' : 0, 'std' : 0}}}, {'age':[], 'height':[], 'weight':[]}, {'age':[], 'height':[], 'weight':[]}

    for data in patients_dict.values(): 
        if data["sex"] == "M" : 
            midMetricsM['age'].append(data['age'])
            midMetricsM['height'].append(data['height'])
            midMetricsM['weight'].append(data['weight']) 
        else: 
            midMetricsF['age'].append(data['age']) 
            midMetricsF['height'].append(data['height']) 
            midMetricsF['weight'].append(data['weight'])

    #mean hommes
    metrics['M']['age']['mean'], metrics['M']['height']['mean'], metrics['M']['weight']['mean'] = moyenne(midMetricsM['age']), moyenne(midMetricsM['height']), moyenne(midMetricsM['weight'])
    #mean femmes
    metrics['F']['age']['mean'], metrics['F']['height']['mean'], metrics['F']['weight']['mean'] = moyenne(midMetricsF['age']), moyenne(midMetricsF['height']), moyenne(midMetricsF['weight'])
    #std hommes
    metrics['M']['age']['std'], metrics['M']['height']['std'], metrics['M']['weight']['std'] = std(midMetricsM['age']), std(midMetricsM['height']), std(midMetricsM['weight'])
    #std femmes
    metrics['F']['age']['std'], metrics['F']['height']['std'], metrics['F']['weight']['std'] = std(midMetricsF['age']), std(midMetricsF['height']), std(midMetricsF['weight'])

    return metrics

########################################################################################################## 
# PARTIE 6 : Bonus (+2 points)
########################################################################################################## 

def listOfLists(dict):
    print([[k] + list(v.values()) for k, v in dict.items()])
    return [[k] + list(v.values()) for k, v in dict.items()]

def create_csv(metrics):
    """
    Fonction python dont l'objectif est d'enregister le dictionnaire "metrics" au sein de deux fichier csv appelés
    "F_metrics.csv" et "M_metrics.csv" respectivement pour les deux sexes.

    Paramètres
    ----------
    metrics : dictionnaire python (dict)
        Dictionnaire à 3 niveaux généré lors de la partie 5
    
    Résultats
    ---------
    paths_list : liste python (list)
        Liste contenant les chemins des deux fichiers "F_metrics.csv" et "M_metrics.csv"
    """

    paths_list = ["F_metrics.csv", "M_metrics.csv"]

    return paths_list

########################################################################################################## 
# TESTS : Le code qui suit permet de tester les différentes parties 
########################################################################################################## 

if __name__ == '__main__':
    ######################
    # Tester la partie 1 #
    ######################

    # Initialisation de l'argument
    csv_path = "subjects.csv"

    # Utilisation de la fonction
    patients_dict = load_csv(csv_path)

    # Affichage du résultat
    print("Partie 1: \n\n", patients_dict, "\n")

    ######################
    # Tester la partie 2 #
    ######################

    # Initialisation des arguments
    csv_path1 = "subjects.csv"
    csv_path2 = "extra_subjects.csv"

    # Utilisation de la fonction
    patients_dict_multi = load_multiple_csv(csv_path1=csv_path1, csv_path2=csv_path2)

    # Affichage du résultat
    print("Partie 2: \n\n", patients_dict_multi, "\n")

    ######################
    # Tester la partie 3 #
    ######################

    # Utilisation de la fonction
    new_patients_dict = update_convention(patients_dict)

    # Affichage du résultat
    print("Partie 3: \n\n", new_patients_dict, "\n")

    ######################
    # Tester la partie 4 #
    ######################

    # Utilisation de la fonction
    patients_list = fetch_candidates(patients_dict)

    # Affichage du résultat
    print("Partie 4: \n\n", patients_list, "\n")

    ######################
    # Tester la partie 5 #
    ######################

    # Utilisation de la fonction
    metrics = fetch_statistics(new_patients_dict)

    # Affichage du résultat
    print("Partie 5: \n\n", metrics, "\n")

    ######################
    # Tester la partie 6 #
    ######################

    # Initialisation des arguments
    dummy_metrics = {'M':{'age':{'mean':0,'std':0}, 'height':{'mean':0,'std':0}, 'weight':{'mean':0,'std':0}}, 
                     'F':{'age':{'mean':0,'std':0}, 'height':{'mean':0,'std':0}, 'weight':{'mean':0,'std':0}}}
    
    # Utilisation de la fonction
    paths_list = create_csv(metrics)

    # Affichage du résultat
    print("Partie 6: \n\n", paths_list, "\n")

