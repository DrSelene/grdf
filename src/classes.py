"""Creates classes for the project"""
from utils import env, token_uri
import requests
import time
from requests.exceptions import RequestException, HTTPError
import json
import re
from typing import Dict, List, Tuple, Union
import pandas as pd


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
        self.access_token = ""

    def get_token(self):
        payload = {
            "grant_type": "client_credentials",
            "scope": env[self.running_env]["scope"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.request("POST", token_uri, data=payload)
        self.access_token = response.json()["access_token"]

        return self.access_token

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

        error_counter = 0
        for count in range(0, len(id_pce)):
            # Make one request per PCE
            url = f"{env[self.running_env]['uri_data']}pce/{id_pce[count]}/droit_acces"
            try:
                response = requests.request(
                    "PUT", url=url, headers=headers, json=pce_parameters[count]
                )
                return response.text

            except HTTPError as e:
                if e.response.status_code == 403 and error_counter <= 5:
                    error_counter += 1
                    print("Forbidden access. Regenerating a token now and retrying...")
                    self.get_token()
                    self.declarer_droit_access(id_pce, pce_parameters)
                elif e.response.status_code == 403 and error_counter > 5:
                    print("Retied 5 times. Stop retrying now")
                else:
                    print(f"HTTPError: {e.response.status_code} - {e.response.reason}")

            except RequestException as e:
                # Handle network-related issues, HTTP errors, timeouts, etc.
                print(f"Request failed: {e}")
                return e

            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"An unexpected error occurred: {e}")
                return e

            finally:
                time.sleep(0.2)

    def consulter_droit_acces(self) -> Tuple[Dict[str, str], List[str]]:
        """Gets all droit access for all PCE with their status,
        returns:
            - sorted_pce_with_status (Dict) {pce_id: status (str)}, sorted so that Active pce appear first
            - pce_with_active_status (list): list of active pces"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }

        url = f"{env[self.running_env]['uri_data']}droits_acces"

        response = requests.request("GET", url=url, headers=headers)

        # Lookup what you need in that weird text response
        # Find all matches of the energie_pattern in the response text
        all_pce = re.compile(r'"id_pce":"([^"]+)"', re.DOTALL).findall(response.text)
        all_access_status = re.compile(r'"etat_droit_acces":"([^"]+)"').findall(
            response.text
        )

        # Combine the lists into a list of tuples
        combined_data = list(zip(all_pce, all_access_status))

        # Remove duplicates based on the pce values
        unique_pce_with_status = {pce: status for pce, status in set(combined_data)}

        # Sort the dictionary based on the values (statuses)
        sorted_pce_with_status = dict(
            sorted(
                unique_pce_with_status.items(),
                key=lambda item: (item[1] != "Active", item),
            )
        )

        # Filter PCEs with a status of 'Active'
        pce_with_active_status = {
            pce: status
            for pce, status in sorted_pce_with_status.items()
            if status == "Active"
        }

        return sorted_pce_with_status, pce_with_active_status

    def get_conso_data(
        self, id_pce: list[str], date_debut: str, date_fin: str
    ) -> Union[pd.DataFrame, str]:
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

        pce_data = []
        for pce in id_pce:
            url = f"{env[self.running_env]['uri_data']}pce/{pce}/donnees_consos_informatives"

            try:
                response = requests.request(
                    "GET", url=url, headers=headers, params=params
                )

                # Regular expression pattern to match the 'energie' values, and beg and end date
                matches_energy = re.compile(r'"energie":\s*(\d+),').findall(
                    response.text
                )

                matches_start_date = re.compile(
                    r'"date_debut_consommation":"([^"]+)"'
                ).findall(response.text)

                matches_end_date = re.compile(
                    r'"date_fin_consommation":"([^"]+)"'
                ).findall(response.text)

                matches_type_conso = re.compile(
                    r'"type_qualif_conso":"([^"]+)"'
                ).findall(response.text)
                matches_status_msg = re.compile(r'"message":"([^"]+)"').findall(
                    response.text
                )

                if matches_status_msg:
                    return f"erreur: {matches_status_msg}"

                if matches_energy:
                    pce_data.append(
                        pd.DataFrame(
                            {
                                "id_pce": pce,
                                "consommation (kWh)": matches_energy,
                                "date_debut": matches_start_date,
                                "date_fin": matches_end_date,
                                "type_qualif_conso": matches_type_conso,
                            }
                        )
                    )

            except HTTPError as e:
                if e.response.status_code == 403 and error_counter <= 5:
                    error_counter += 1
                    print("Forbidden access. Regenerating a token now and retrying...")
                    self.get_token()
                    self.get_conso_data(id_pce, date_debut, date_fin)
                elif e.response.status_code == 403 and error_counter > 5:
                    print("Retied 5 times. Stop retrying now")
                else:
                    print(f"HTTPError: {e.response.status_code} - {e.response.reason}")

            except RequestException as e:
                # Handle network-related issues, HTTP errors, timeouts, etc.
                print(f"Request failed: {e}")
                return f"erreur: {e}"

            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"An unexpected error occurred: {e}")
                return f"erreur: {e}"

        pce_data = pd.concat(pce_data)
        return pce_data
