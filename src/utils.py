import pandas as pd

env = {
    "bas": {
        "scope": "/adict/bas/v5",
        "uri_data": "https://api.grdf.fr/adict/bas/v5/",
    },
    "prod": {"scope": "/adict/v2", "uri_data": "https://api.grdf.fr/adict/v2/"},
}

token_uri = (
    "https://sofit-sso-oidc.grdf.fr/openam/oauth2/realms/externeGrdf/access_token"
)

variable_declarer_pce = {
    "id_pce": "ID PCE, séparés par virgule",
    "role_tiers": "Role Tiers",
    "raison_sociale": "Raison Sociale",
    "nom_titulaire": "Nom Titulaire",
    "code_postal": "Code Postal",
    "courriel_titulaire": "Courriel Titulaire",
    "numero_telephone_mobile_titulaire": "Numéro Téléphone Mobile Titulaire",
    "date_debut_droit_acces": "Date Début Droit Accès (yyyy-mm-dd)",
    "date_fin_droit_acces": "Date Fin Droit Accès (yyyy-mm-dd)",
    "perim_donnees_conso_debut": "Périm Données Conso Début (yyyy-mm-dd)",
    "perim_donnees_conso_fin": "Périm Données Conso Fin (yyyy-mm-dd)",
    "perim_donnees_contractuelles": "Périm Données Contractuelles (Vrai/Faux)",
    "perim_donnees_techniques": "Périm Données Techniques (Vrai/Faux)",
    "perim_donnees_informatives": "Périm Données Informatives (Vrai/Faux)",
    "perim_donnees_publiees": "Périm Données Publiées (Vrai/Faux)",
}

def write_to_excel(data: pd.DataFrame, path: str):
    '''Writes dict to excel file
    Args:
        - data , panda dataframe w columns id_pce, consommation, date_debut, date_fin
        - path: full path to output file e.g. "output.xslx"'''

    # Create an Excel writer with Pandas
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        # Iterate over unique id_pce values
        for id_pce in data["id_pce"].unique():
            # Filter DataFrame for each id_pce
            df_id_pce = data[data["id_pce"] == id_pce]

            # Write the DataFrame to the Excel file
            df_id_pce.to_excel(writer, sheet_name=f"pce {id_pce}", index=False)
