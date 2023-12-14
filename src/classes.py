"""Creates classes for the project"""
from utils import env, token_uri
import requests
import time
from requests.exceptions import RequestException
import json
import re


class Grdf_Api:
    def __init__(
        self, client_id: str, client_secret: str, running_env: str = "prod"
    ) -> None:
        """Args:
        - running_env: bas or prod
        client_id and client_secret, ID (str)"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.running_env = running_env

    def get_token(self):
        payload = {
            "grant_type": "client_credentials",
            "scope": env[self.running_env]["scope"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.request("POST", token_uri, data=payload)
        self.access_token = response.json()["access_token"]

    def declarer_droit_access(self, id_pce: list[str], pce_parameters: list[dict]):
        """Uses Put to declare droit d'acces
        Args:
            - id_pce (list) list of pce ids (str)
            - pce_parameters (list). For each PCE, list of params (dict) to send to API
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }

        for count in range(0, len(id_pce)):
            # Make one request per PCE
            url = f"{env[self.running_env]['uri_data']}{id_pce[count]}/droit_acces"
            try:
                response = requests.request(
                    "PUT", url=url, headers=headers, json=pce_parameters[count]
                )

            except RequestException as e:
                # Handle network-related issues, HTTP errors, timeouts, etc.
                print(f"Request failed: {e}")

            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"An unexpected error occurred: {e}")

            time.sleep(0.2)  #

    def get_conso_data(self, id_pce: list[str], date_debut: str, date_fin: str):
        """Get conso data for a PCE and one or more meters
        Args:
            - id_pce (list of str): list of pce for which you want data
            - date_debut et date_fin: str format "yyyy-mm-dd"
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }

        params = {"date_debut": date_debut, "date_fin": date_fin}

        output = []
        for pce in id_pce:
            print(pce)
            url = (
                f"{env[self.running_env]['uri_data']}{pce}/donnees_consos_informatives"
            )

            try:
                response = requests.request(
                    "GET", url=url, headers=headers, params=params
                )

                # Regular expression pattern to match the 'energie' values
                energie_pattern = re.compile(r'"energie":\s*(\d+),')
                print(response.text)
                # Find all matches of the energie_pattern in the response text
                matches = energie_pattern.findall(response.text)
                if matches:
                    print(matches)

                    # Sum up the 'energie' values
                    total_energie = sum(int(match) for match in matches)
                else:
                    total_energie = "NaN"

                output.append(
                    {
                        "id_pce": pce,
                        "consommation": total_energie,
                        "date_debut": date_debut,
                        "date_fin": date_fin,
                    }
                )

            except RequestException as e:
                # Handle network-related issues, HTTP errors, timeouts, etc.
                print(f"Request failed: {e}")

            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"An unexpected error occurred: {e}")

        return output
