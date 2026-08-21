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

class PrioView(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None  # will be injected afterward
        self.renderer = GraphRenderer()
        self.title("Drawing and analyzing a toy network with a few priority classes")
        self.geometry("1000x600")
        self.grid_rowconfigure((0, 1), weight=1)   # Canvas s'étire
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.per_class=ctk.BooleanVar()
        self.delays=ctk.BooleanVar()
        self.num_classes = 3


        # Colonne 1
        self.menu_s = ctk.CTkFrame(self, fg_color="#EDE6FF")
        self.menu_s.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(self.menu_s, text="Priority classes", text_color=col1.tx, fg_color=col1.bg,
                     font= ("Arial", 15)).pack()

        row_ncl = ctk.CTkFrame(self.menu_s, fg_color=col1.bg    )
        row_ncl.pack(fill="x", pady=0)
        ctk.CTkLabel(row_ncl ,text="Number of classes:", fg_color=col1.bg,
                     text_color=col1.tx, anchor="w", justify="left",
                     corner_radius=10).pack(side="left", padx=5, pady=0)
        self.entree_ncl = ctk.CTkEntry(row_ncl, width=30)
        self.entree_ncl.pack(side="left", padx=1, pady=1)
        ctk.CTkButton(row_ncl, text="OK", fg_color=col1.btn, text_color=col1.tx, hover_color=col1.hov,  width=40,
                      command=lambda: self.controller.set_ncl()).pack(side="right", padx=1, pady=1)
        self.entree_rate, self.entree_latency, self.entree_sha =  (
            server_view(self.menu_s, col1,
                        lambda:self.controller.appliquer_modifs_server(),
                        lambda:self.controller.supprimer_server()))

        # Colonne 2
        self.menu_f = ctk.CTkFrame(self, fg_color=col2.bg)
        self.menu_f.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.entree_sigma, self.entree_rho, self.entree_ple, self.label_chemin, self.bouton_class = (
            flow_view(self.menu_f, 1, col2, lambda: self.controller.add_flow(),
                      lambda: self.controller.appliquer_modifs_flot(),
                      lambda value: self.controller.cla_selection(value)))

        #Colonne 3 : Information supplementaire

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
        # Colonne 4 bas (calcul, generation de code)

        self.comp2 = ctk.CTkFrame(self, fg_color=col5.bg)
        self.comp2.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(self.comp2, text="Compute", fg_color=col5.bg, text_color=col5.tx,
                     font= ("Arial", 15)).pack()
        ctk.CTkCheckBox(self.comp2, text="Per-class network", variable=self.per_class, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)
        ctk.CTkCheckBox(self.comp2, text="end-to-end delays", variable=self.delays, fg_color="green",
                        text_color=col5.tx).pack(anchor="w", padx=5, pady=5)


        ctk.CTkButton(self.comp2, text="See results", fg_color=col5.btn, text_color=col5.tx, hover_color=col5.hov,
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

    def dessiner_sommet(self, x, y, couleur, i, s):
        self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=couleur)
        self.canvas.create_text(x, y, text=str(i))
        self.canvas.create_text(x, y-15, text=str(s["sc"]))

    def dessiner_arete(self, s1, s2):
        self.canvas.create_line(s1["x"], s1["y"], s2["x"], s2["y"], width=2, arrow="last", arrowshape=(12, 15, 5))

    def get_per_class(self):
        return self.per_class.get()

    def get_delays(self):
        return self.delays.get()

    def update_menu_class(self, n_c):
        text = ["{}".format(i)for i in range(n_c)]
        self.bouton_class.configure(values=text)
        # print(n_c)

    def update_menu_flot(self, n_f):
        text = ["{}".format(i)for i in range(n_f)]
        self.bouton_flot.configure(values=text)
        # print(n_f)
