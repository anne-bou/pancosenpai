# ============================================================
# PancoSenpai Project — https://github.com/anne-bou/pancosenpai
# Copyright (C) 2026 Anne Bouillard
# License: BSD-3-Clause
#
# This file is part of the PancoSenpai project.
# Redistribution must retain this copyright notice and license.
# ============================================================

__author__ = "Anne Bouillard"
__email__ = "anne.bouillard@ens.fr"
__license__ = "BSD-3-Clause"


import customtkinter as ctk
from pancoSenpai.Utils.colors import Mauve, Blue, Orange, Green, Red
from pancoSenpai.Utils.network_view import server_view, flow_view, flow_modif, print_network, vider_champs
from pancoSenpai.View.rendererView import GraphRenderer

col1 = Mauve
col2 = Green
col3 = Orange
col4 = Blue
col5 = Red


class ToyView(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None  # will be injected afterward
        self.renderer = GraphRenderer()
        self.title("Drawing and analyzing a toy network")
        self.geometry("1000x600")

        self.grid_rowconfigure((0, 1), weight=1)   # Canvas s'étire
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)


        self.tfa=ctk.BooleanVar()
        self.sfa=ctk.BooleanVar()
        self.plp=ctk.BooleanVar()
        self.elp=ctk.BooleanVar()

         # Colonne 1
        self.menu_s = ctk.CTkFrame(self, fg_color=col1.bg)
        self.menu_s.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.entree_rate, self.entree_latency, self.entree_sha =  (
            server_view(self.menu_s, col1,
                        lambda:self.controller.appliquer_modifs_server(),
                        lambda:self.controller.supprimer_server()))

        # Colonne 2
        self.menu_f = ctk.CTkFrame(self, fg_color=col2.bg)
        self.menu_f.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.entree_sigma, self.entree_rho, self.entree_ple, self.label_chemin = (
            flow_view(self.menu_f, 0, col2, lambda: self.controller.add_flow(),
                      lambda: self.controller.appliquer_modifs_flot(),
                      lambda value: self.controller.cla_selection(value)))

        # Colonne 3
        self.menu_select_f = ctk.CTkFrame(self, fg_color=col3.bg)
        self.menu_select_f.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.bouton_flot = flow_modif(self.menu_select_f,col3, lambda value: self.controller.flot_selection(value),
                                      lambda: self.controller.modifier_flot(), lambda: self.controller.supprimer_flot())

        # Colonne 4

        self.desc = ctk.CTkFrame(self, fg_color=col4.bg)
        self.desc.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        self.label_servers, self.label_flows = print_network(self.desc, col4)

        #Bas de la fenetre
        self.canvas = ctk.CTkCanvas(self, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew", columnspan=3, padx=5, pady=5)

        # Bind clic
        self.canvas.bind("<Button-1>", lambda event: self.controller.ajouter_ou_selectionner(event))

        # Colonne 4 bas (calcul, gerneration de code)

        self.comp2 = ctk.CTkFrame(self, fg_color=col5.bg)
        self.comp2.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(self.comp2, text="End-to-end delays with", fg_color=col5.bg, text_color=col5.tx,
                     font= ("Arial", 15)).pack()
        ctk.CTkCheckBox(self.comp2, text="TFA method", variable=self.tfa, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)
        ctk.CTkCheckBox(self.comp2, text="SFA method", variable=self.sfa, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)
        ctk.CTkCheckBox(self.comp2, text="PLP method", variable=self.plp, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)
        ctk.CTkCheckBox(self.comp2, text="ELP method", variable=self.elp, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)

        ctk.CTkButton(self.comp2, text="Compute bounds", fg_color=col5.btn, text_color=col5.tx, hover_color=col5.hov,
                      command=lambda: self.controller.analyser()).pack(padx=1, pady=1)

        ctk.CTkButton(self.comp2, text="Save File", fg_color=col5.btn, text_color=col5.tx, hover_color=col5.hov,
                      command=lambda: self.controller.save()).pack( padx=1, pady=1)

        self.btn_quit = ctk.CTkButton(
            self.comp2,
            text="Quit",
            command=lambda:self.controller.quitter(),
            fg_color=col5.btn,
            hover_color=col5.hov,
            text_color=col5.tx,
        )
        self.btn_quit.pack(pady=10)


    def vider_service(self):
        vider_champs(self.entree_rate, self.entree_latency, self.entree_sha)

    def vider_flot(self):
        vider_champs(self.entree_sigma, self.entree_rho, self.entree_ple)

    def affiche_texte_reseau(self, text_s, text_f):
        self.label_servers.configure(text=text_s)
        self.label_flows.configure(text=text_f)

    def get_tfa(self):
        return self.tfa.get()

    def get_sfa(self):
        return self.sfa.get()

    def get_plp(self):
        return self.plp.get()

    def get_elp(self):
        return self.elp.get()

    def update_menu_flot(self, n_f):
        text = ["{}".format(i)for i in range(n_f)]
        self.bouton_flot.configure(values=text)
        # print(n_f)
