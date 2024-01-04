import tkinter as tk
from tkinter import ttk
from classes import Grdf_Api  # Import your Grdf_Api class
from utils import write_to_excel
import pandas as pd
import os
import sys


class AppGui:
    def __init__(self, master):
        self.master = master
        self.master.title("GRDF API")

        self.myapi = Grdf_Api(
            client_id="", client_secret="", running_env=""
        )  # Initialize with dummy values

        self.notebook = ttk.Notebook(master)

        # Create tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Générer un token")
        self.notebook.add(self.tab2, text="Voir les droits d'accès")
        self.notebook.add(self.tab3, text="Obtenir données de conso")
        self.notebook.add(self.tab4, text="Déclarer droits d'accès")

        self.property_label = ttk.Label(
            master,
            text="Copyright © 2023 VB Solutions. All rights reserved",
            font=("Helvetica", 8),
        )
        self.property_label.pack(side=tk.BOTTOM, pady=5)

        # Set up tab 1
        self.setup_tab1()

        # Set up tab 2
        self.setup_tab2()

        # Set up tab 4
        self.setup_tab4()

        self.notebook.pack()

    def setup_tab1(self):
        self.client_id_label_tab1 = ttk.Label(self.tab1, text="Client ID:")
        self.client_id_entry_tab1 = ttk.Entry(self.tab1)

        self.client_secret_label_tab1 = ttk.Label(self.tab1, text="Client Secret:")
        self.client_secret_entry_tab1 = ttk.Entry(self.tab1, show="*")

        # self.running_env_label_tab1 = ttk.Label(self.tab1, text="Running Environment:")
        # self.running_env_entry_tab1 = ttk.Entry(self.tab1)

        self.submit_button_tab1 = ttk.Button(
            self.tab1, text="Générer un token", command=self.submit_tab1
        )

        self.result_label_tab1 = ttk.Label(self.tab1, text="Résultat:")
        self.result_text_tab1 = tk.Text(self.tab1, height=2, width=40, wrap="word")

        self.client_id_label_tab1.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.client_id_entry_tab1.grid(row=0, column=1, padx=5, pady=5)
        self.client_secret_label_tab1.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.client_secret_entry_tab1.grid(row=1, column=1, padx=5, pady=5)
        # self.running_env_label_tab1.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        # self.running_env_entry_tab1.grid(row=2, column=1, padx=5, pady=5)
        self.submit_button_tab1.grid(row=3, column=0, columnspan=2, pady=10)
        self.result_label_tab1.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.result_text_tab1.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def submit_tab1(self):
        # Update the instance with new values
        self.myapi.client_id = self.client_id_entry_tab1.get()
        self.myapi.client_secret = self.client_secret_entry_tab1.get()
        self.myapi.running_env = "prod"

        try:
            # Call the Grdf_Api method to generate token
            result = self.myapi.get_token()
            result = "Token généré"
        except Exception as e:
            result = f"Erreur: {str(e)}"

        # Display the result in the Tkinter window
        self.result_text_tab1.delete("1.0", tk.END)  # Clear previous content
        self.result_text_tab1.insert(tk.END, result)

        # Set up tab 3 now that you have a token
        self.setup_tab3()

    def setup_tab2(self):
        self.submit_button_tab2 = ttk.Button(
            self.tab2, text="Voir les droits d'accès", command=self.submit_tab2
        )

        self.result_label_tab2 = ttk.Label(self.tab2, text="Result:")
        self.result_text_tab2 = tk.Text(self.tab2, height=10, width=40, wrap="word")

        self.submit_button_tab2.grid(row=0, column=0, columnspan=2, pady=10)
        self.result_label_tab2.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.result_text_tab2.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def submit_tab2(self):  #
        tous_droits_access, _ = self.myapi.consulter_droit_acces()

        # Call the Grdf_Api method to get droits d'accès
        try:
            tous_droits_access, _ = self.myapi.consulter_droit_acces()
            result = str(tous_droits_access)
        except Exception as e:
            result = f"Erreur: {str(e)}"

        # Display the result in the Tkinter window
        self.result_text_tab2.delete("1.0", tk.END)  # Clear previous content
        self.result_text_tab2.insert(tk.END, result)

    def setup_tab3(self):
        _, possible_values = self.myapi.consulter_droit_acces()

        self.id_pce_label_tab3 = ttk.Label(self.tab3, text="Selectionner PCEs:")
        self.id_pce_label_tab3.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        # Create a tk.Listbox with scrollbars
        self.id_pce_listbox_tab3 = tk.Listbox(
            self.tab3, selectmode=tk.MULTIPLE, height=5
        )
        self.scrollbar_tab3 = tk.Scrollbar(self.tab3, orient=tk.VERTICAL)

        for value in possible_values:
            self.id_pce_listbox_tab3.insert(tk.END, value)

        self.id_pce_listbox_tab3.config(yscrollcommand=self.scrollbar_tab3.set)
        self.scrollbar_tab3.config(command=self.id_pce_listbox_tab3.yview)
        self.id_pce_listbox_tab3.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.scrollbar_tab3.grid(row=0, column=2, pady=5, sticky="ns")

        self.date_debut_label_tab3 = ttk.Label(self.tab3, text="Date Debut:")
        self.date_debut_entry_tab3 = ttk.Entry(self.tab3)
        self.date_debut_label_tab3.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.date_debut_entry_tab3.grid(row=1, column=1, padx=5, pady=5)

        self.date_fin_label_tab3 = ttk.Label(self.tab3, text="Date Fin:")
        self.date_fin_entry_tab3 = ttk.Entry(self.tab3)
        self.date_fin_label_tab3.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.date_fin_entry_tab3.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button_tab3 = ttk.Button(
            self.tab3, text="Récupérer les données", command=self.submit_tab3
        )
        self.submit_button_tab3.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label_tab3 = ttk.Label(self.tab3, text="Résultat:")
        self.result_text_tab3 = tk.Text(self.tab3, height=10, width=40, wrap="word")
        self.result_label_tab3.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.result_text_tab3.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def submit_tab3(self):
        # Get the selected PCEs
        selected_pces = [
            self.id_pce_listbox_tab3.get(index)
            for index in self.id_pce_listbox_tab3.curselection()
        ]

        script_dir = os.path.dirname(sys.argv[0])

        path_to_file = os.path.join(
            script_dir,
            f"{self.date_debut_entry_tab3.get()} à {self.date_fin_entry_tab3.get()} {'_'.join(selected_pces)}.xlsx",
        )

        # Call the Grdf_Api method to get conso data
        conso_data = self.myapi.get_conso_data(
            id_pce=selected_pces,
            date_debut=self.date_debut_entry_tab3.get(),
            date_fin=self.date_fin_entry_tab3.get(),
        )

        if isinstance(conso_data, pd.DataFrame):
            write_to_excel(data=conso_data, path=path_to_file)

            print_result = f"Fichier sauvegardé: {path_to_file}"
        else:
            print_result = conso_data

        # Display the result in the Tkinter window
        self.result_text_tab3.delete("1.0", tk.END)  # Clear previous content
        self.result_text_tab3.insert(tk.END, print_result)

    def setup_tab4(self):
        self.submit_button_tab4 = ttk.Button(
            self.tab4, text="Déclarer droits d'accès", command=self.submit_tab4
        )

        self.result_label_tab4 = ttk.Label(self.tab4, text="Result:")
        self.result_text_tab4 = tk.Text(self.tab4, height=10, width=40, wrap="word")
        labels_tab4 = labels_tab4 = [
            "id_pce",
            "role_tiers",
            "raison_sociale",
            "nom_titulaire",
            "code_postal",
            "courriel_titulaire",
            "numero_telephone_mobile_titulaire",
            "date_debut_droit_acces",
            "date_fin_droit_acces",
            "perim_donnees_conso_debut",
            "perim_donnees_conso_fin",
            "perim_donnees_contractuelles",
            "perim_donnees_techniques",
            "perim_donnees_informatives",
            "perim_donnees_publiees",
        ]
        self.entries_tab4 = {}

        for i, label_text in enumerate(labels_tab4):
            label = ttk.Label(self.tab4, text=label_text)
            entry = ttk.Entry(self.tab4, width=50)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries_tab4[label_text] = entry

        self.entries_tab4["role_tiers"].insert(0, "AUTORISE_CONTRAT_FOURNITURE")

        self.submit_button_tab4.grid(
            row=len(labels_tab4), column=0, columnspan=2, pady=10
        )
        self.result_label_tab4.grid(
            row=len(labels_tab4) + 1, column=0, sticky="w", padx=5, pady=5
        )
        self.result_text_tab4.grid(
            row=len(labels_tab4) + 2, column=0, columnspan=2, padx=5, pady=5
        )

    def submit_tab4(self):
        # Collect values from the entries
        params_tab4 = {label: entry.get() for label, entry in self.entries_tab4.items()}

        try:
            # Call the Grdf_Api method to declare droits d'accès
            new_droit_acces_resp = self.myapi.declarer_droit_access(
                id_pce=[params_tab4["id_pce"]], pce_parameters=[params_tab4]
            )
            result_tab4 = f"Droits d'accès déclarés\n{new_droit_acces_resp}"
        except Exception as e:
            result_tab4 = f"Erreur: {str(e)}"

        # Display the result in the Tkinter window
        self.result_text_tab4.delete("1.0", tk.END)  # Clear previous content
        self.result_text_tab4.insert(tk.END, result_tab4)


def main():
    root = tk.Tk()
    app = AppGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
