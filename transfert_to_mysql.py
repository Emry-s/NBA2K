import pandas as pd
from sqlalchemy import create_engine

"""
Transfert de données vers une base de données MySQL
"""

# Configuration de la connexion à la base de données MySQL grâce à la classe create_engine
# Format : type_of_db+connector://db_user:password@host/database_name
engine = create_engine("mysql+mysqlconnector://root:Isib@127.0.0.1/nba2k_ratings")

# Chargement du fichier CSV dans un DataFrame pandas
df = pd.read_csv('nba2k-full.csv')

# Nom de la table MySQL
# table_name = 'player_ratings'

# Insérer les données du DataFrame dans la table MySQL
df.to_sql(name='player_ratings', con=engine, if_exists='replace', index=False)
# index=False : Cela indique de ne pas inclure la colonne d'index du DataFrame dans la table MySQL.

print("Transfert vers la base de données MySql terminé ")
