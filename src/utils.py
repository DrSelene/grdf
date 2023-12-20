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


def write_to_excel(data: pd.DataFrame, path: str):
    '''Writes dict to excel file
    Args:
        - data , panda dataframe w columns id_pce, consommation, date_debut, date_fin
        - path: full path to output file e.g. "output.xslx"'''
    # Create a Pandas DataFrame from the list of dictionaries
    print("im in")
    print(data["id_pce"].unique())
    # Create an Excel writer with Pandas
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        # Iterate over unique id_pce values
        for id_pce in data["id_pce"].unique():
            # Filter DataFrame for each id_pce
            df_id_pce = data[data["id_pce"] == id_pce]
            print(df_id_pce)

            # Write the DataFrame to the Excel file
            df_id_pce.to_excel(writer, sheet_name=f"pce {id_pce}", index=False)
