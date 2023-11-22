import csv
import pandas as pd
import re

# Lire le fichier CSV
df0 = pd.read_csv('nba2k-full.csv', encoding='utf-8')  # ancien utile pour comparaison

# Remplacez les valeurs NaN par une chaîne vide (ou une autre valeur par défaut)
df = df0.fillna('')

# Configurez pandas pour afficher toutes les colonnes sans troncature
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

print(df)
# colonne_a_afficher = df[['keywords', 'categories description']]
# print(colonne_a_afficher)
