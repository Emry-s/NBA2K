import mysql.connector  # Importe la bibliothèque pour interagir avec MySQL
import xml.etree.ElementTree as XML_TREE  # Importe la bibliothèque pour manipuler des arbres XML
from xml.dom.minidom import parseString  # Importe les outils pour traiter les fichiers XML au format DOM
import psycopg2  # Importe la bibliothèque pour interagir avec PostgreSQL
import pandas as pd  # Importe la bibliothèque pour la manipulation et l'analyse de données
from lxml import etree  # Importe la bibliothèque pour manipuler des documents XML et HTML de manière efficace


# Fonction pour extraire les données de la base MySQL
def extract_data_from_mysql():
    connection_to_mysql = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Isib",
        database="nba2k_ratings"
    )
    cursor = connection_to_mysql.cursor()
    # création d'un curseur afin d'exécuter des requêtes SQL
    cursor.execute("SELECT * FROM player_ratings")
    raw_data = cursor.fetchall()
    # raw_data contient les résultats de la requête sous forme de liste de tuples.

    # Modifications des datas
    # Création d'une df pandas pour manipuler les datas
    df = pd.DataFrame(raw_data)
    # Obtiens le nom des colonnes
    df.columns = [i[0] for i in cursor.description]

    df = df.drop_duplicates(subset='full_name', keep='first')
    df['rating'] = df['rating'].astype(str) + "%"  # conversion du rating en str obligée
    df['jersey'] = df['jersey'].str.replace('#', '')
    df = df.drop('version', axis=1)  # axis=1 = supp la colonne
    cursor.close()
    connection_to_mysql.close()
    return df


# Fonction pour créer une table spécifique
# Création de la table "Table1" avec tri par position
def create_table(root, formatted_data, table_name, columns):
    table_root = XML_TREE.SubElement(root, table_name)

    if table_name == "Best_player_by_position":
        # Créez un ordre personnalisé pour la colonne "position"
        custom_order = ["G", "G-F", "F-G", "F", "F-C", "C-F", "C"]
        formatted_data["position"] = pd.Categorical(formatted_data["position"], categories=custom_order, ordered=True)
        formatted_data = formatted_data.sort_values(by=["position", "rating"], ascending=[True, False])

    # parcours les lignes = 1 player chaque fois
    for _, row in formatted_data.iterrows():
        player = XML_TREE.SubElement(table_root, "Player")
        # parcours les colonnes de la ligne
        for column in columns:
            value = row[column]
            # créer la balise 'column'
            field = XML_TREE.SubElement(player, column)
            # met la valeur dedans
            field.text = str(value)


# Fonction pour créer le fichier XML bien formaté
def create_formatted_xml(formatted_data):
    root = XML_TREE.Element("NBA_Data")

    create_table(root, formatted_data, "Best_player_by_position", ["position", "full_name", "rating", "team"])
    create_table(root, formatted_data, "In_depth_player_review",
                 ["full_name", "jersey", "team", "height", "weight", "b_day", "salary", "country", "college"])
    create_table(root, formatted_data, "Draft_info", ["full_name", "draft_year", "draft_round", "draft_peak", "college"]
                 )

    xml_string = XML_TREE.tostring(root, encoding="utf-8")  # convertir l'objet XML root en une chaîne de caractères
    dom = parseString(xml_string)  # transforme en un objet DOM (Document Object Model), Le DOM est une
    # représentation hiérarchique des éléments d'un document XML → meilleure manipulation
    pretty_xml = dom.toprettyxml()  # ajoute des retraits, des espaces et des sauts de ligne pour rendre le XML plus
    # lisible.

    with open("nba_data_formatted.xml", "w") as f:
        f.write(pretty_xml)


# Fonction pour transférer les données vers PostgresSQL
def transfer_to_postgresql():
    connection_to_pg = psycopg2.connect(
        host="localhost",
        database="nba2k_ratings",
        user="postgres",
        password="isib"
    )
    cursor = connection_to_pg.cursor()

    tables = {
        "best_by_position": ["position", "full_name", "rating", "team"],
        "players_description": ["full_name", "jersey", "team", "height", "weight", "b_day",
                                "salary", "country", "college"],
        "draft_info": ["full_name", "draft_year", "draft_round", "draft_peak", "college"]
    }

    for table_name, table_columns in tables.items():
        column_definitions = [f"{col} TEXT" for col in table_columns]
        # cette ligne crée une chaîne de texte avec le nom de la colonne suivi de "TEXT" (= type)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})")

        tree = XML_TREE.parse('nba_data_formatted.xml')  # Charge le fichier XML
        root = tree.getroot()  # obtient la racine de l'XML

        for player in root.findall(".//Player"):  # recherche tous les éléments <Player> dans le fichier XML
            values = [player.find(col).text if player.find(col) is not None else "" for col in table_columns]
            # Cette ligne crée une liste 'values' contenant les valeurs des colonnes pour un joueur donné. Elle vérifie
            # si chaque colonne existe pour le joueur avant de récupérer sa valeur.
            placeholders = ', '.join(['%s' for _ in values])
            # Une liste de %s séparés par des virgules. Cette chaîne sera utilisée dans l'instruction SQL pour
            # spécifier les emplacements des valeurs à insérer dans la base de données
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(table_columns)}) VALUES ({placeholders})",
                           tuple(values))

    connection_to_pg.commit()
    connection_to_pg.close()
    print("Le fichier XML a été transféré avec succès dans la base de données PostgresSQL.")


def transform_into_html():
    # Charger le fichier XML
    xml_file = etree.parse('nba_data_formatted.xml')

    # Charger la feuille de style XSLT
    xslt_style = etree.parse('nba.xslt')
    # Créer un transformateur à partir du fichier XSLT
    transformer = etree.XSLT(xslt_style)

    # Appliquer la transformation XSLT sur le document XML
    result = transformer(xml_file)

    # Convertir le résultat en une chaîne de caractères avec une belle présentation
    pretty_html = etree.tostring(result, pretty_print=True)

    # Enregistrer le résultat dans un fichier HTML bien formaté avec des sauts de ligne
    with open('result.html', 'wb') as output_file:
        output_file.write(pretty_html)

    print("Résultat enregistré dans 'result.html'")


def main():
    # Extraction des données depuis MySQL
    formatted_data = extract_data_from_mysql()
    print("Extraction des données terminée")
    # Création du fichier XML
    create_formatted_xml(formatted_data)
    print("Création du fichier XML terminée")
    # Valider le fichier XML par rapport au schéma XSD
    xsd_schema = etree.XMLSchema(file='nba.xsd')
    xml_to_validate = etree.parse('nba_data_formatted.xml')
    if xsd_schema.validate(xml_to_validate):
        print("Le fichier XML est conforme au schéma XSD.")
    else:
        return print("Le fichier XML n'est pas conforme au schéma XSD.")
    # Transfert des données vers PostgresSQL
    transfer_to_postgresql()
    transform_into_html()


if __name__ == "__main__":
    main()
