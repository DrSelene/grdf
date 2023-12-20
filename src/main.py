from classes import Grdf_Api
import pandas as pd
from utils import write_to_excel


def main():
    myapi = Grdf_Api(
        client_id="grdf_adict_bas", client_secret="wGe0MW13k", running_env="bas"
    )

    myapi.get_token()
    print(myapi.access_token)

    myapi.declarer_droit_access(
        id_pce=["GI999001", "11300000000000"],
        pce_parameters=[
            {
                "role_tiers": "AUTORISE_CONTRAT_FOURNITURE",
                "raison_sociale": "BabaTech",
                "nom_titulaire": "",
                "code_postal": "77900",
                "courriel_titulaire": "robert.dupont@dupont.fr",
                "numero_telephone_mobile_titulaire": "0699999999",
                "date_debut_droit_acces": "2019-07-05",
                "date_fin_droit_acces": "2024-01-31",
                "perim_donnees_conso_debut": "2018-01-01",
                "perim_donnees_conso_fin": "2023-12-31",
                "perim_donnees_contractuelles": "Faux",
                "perim_donnees_techniques": "Faux",
                "perim_donnees_informatives": "Faux",
                "perim_donnees_publiees": "Vrai",
            },
            {
                "role_tiers": "AUTORISE_CONTRAT_FOURNITURE",
                "raison_sociale": "",
                "nom_titulaire": "MICHOU",
                "code_postal": "77900",
                "courriel_titulaire": "Mathilde.MICHOU@MICHOU.fr",
                "numero_telephone_mobile_titulaire": "0699999999",
                "date_debut_droit_acces": "2019-07-05",
                "date_fin_droit_acces": "2024-01-31",
                "perim_donnees_conso_debut": "2018-01-01",
                "perim_donnees_conso_fin": "2023-12-31",
                "perim_donnees_contractuelles": "Faux",
                "perim_donnees_techniques": "Faux",
                "perim_donnees_informatives": "Faux",
                "perim_donnees_publiees": "Vrai",
            },
        ],
    )

    tous_droits_access = myapi.consulter_droit_acces()

    # conso = myapi.get_conso_data(
    #     id_pce=["11300000000001"], date_debut="2020-01-01", date_fin="2020-01-03"
    # )

    # print(conso)

    # write_to_excel(data = conso, path = 'output.xlsx')


if __name__ == "__main__":
    main()
