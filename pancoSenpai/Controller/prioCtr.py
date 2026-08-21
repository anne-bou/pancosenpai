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


from pancoSenpai.View.resPrioView import ResPrioView
from pancoSenpai.Controller.graphCtr import Graph


class PrioCtr:
    def __init__(self, view):
        self.view = view
        self.view.controller = self
        self.graph = Graph()

    def appliquer_modifs_server(self):
        rate = self.view.entree_rate.get()
        latency = self.view.entree_latency.get()
        sha= self.view.entree_sha.get()
        self.graph.apply_modifs_server(rate, latency, sha)
        self.dessiner()
        text_s, text_f = self.graph.afficher_reseau(1)
        self.view.affiche_texte_reseau(text_s, text_f)

    def dessiner(self):
        self.graph.calcule_aretes()
        if self.graph.flot_selectionne  is not None:
            path = self.graph.flows[self.graph.flot_selectionne].path
        else:
            path = []
        if self.graph.sommet_selectionne is None:
            ssel = -1
        else:
            ssel = self.graph.sommet_selectionne
        self.view.renderer.draw_network(self.view.canvas, self.graph.sommets, self.graph.aretes, path, ssel)

    def afficher_reseau(self):
        text_s, text_f = self.graph.afficher_reseau(1)
        self.view.affiche_texte_reseau(text_s, text_f)

    def afficher_chemin(self):
        text = self.graph.texte_chemin()
        self.view.label_chemin.configure(text=text)

    def terminer_chemin(self):
        text = self.graph.end_path()
        self.view.label_chemin.configure(text=text)
        self.dessiner()

    def supprimer_server(self):
        self.graph.delete_server()
        self.dessiner()
        self.afficher_reseau()
        self.view.update_menu_flot(len(self.graph.flows))

    def modifier_flot(self):
        if self.graph.flot_selectionne is None:
            return
        try:

            # print("modifier flot ", self.graph.flot_selectionne)
            j = self.graph.flot_selectionne
            self.view.vider_flot()
            self.view.entree_sigma.insert(0, str(self.graph.flows[j].arrival_curve[0].sigma))
            self.view.entree_rho.insert(0, str(self.graph.flows[j].arrival_curve[0].rho))
            self.view.entree_ple.insert(0, str(self.graph.mpl[j]))
            self.graph.chemin_en_cours = True
            self.graph.chemin_courant = []
        except ValueError:
            pass

    def supprimer_flot(self):
        # print("Suppression")
        self.graph.delete_flow()

        self.dessiner()
        self.afficher_reseau()
        self.view.update_menu_flot(len(self.graph.flows))

    def add_flow(self):
        ac = self.graph.default_ac
        ple = self.graph.ple
        self.view.vider_flot()
        self.view.entree_rho.insert(0, str(ac.rho))
        self.view.entree_sigma.insert(0, str(ac.sigma))
        self.view.entree_ple.insert(0, str(ple))
        self.graph.chemin_en_cours = True
        self.graph.chemin_courant = []
        # print("Début d’un nouveau chemin.")
        self.afficher_chemin()

    def appliquer_modifs_flot(self):
        self.graph.apply_modifs_flow(self.view.entree_rho.get(), self.view.entree_sigma.get(),
                                     self.view.entree_ple.get(), self.graph.cla_sel)
        self.view.update_menu_flot(len(self.graph.flows))
        self.dessiner()
        self.afficher_reseau()

    def flot_selection(self, value):
        self.graph.flot_selectionne = int(value)
        # print("flot selectionne:", value)
        self.dessiner()

    def classe_donnee(self, value):
        self.graph.cla_sel = int(value)
        # print("classe courante:", value)

    def cla_selection(self, value):
        self.graph.cla_sel = int(value)
        # print("classe affectee:", value)

    def ajouter_ou_selectionner(self, event):
        index = self.graph.trouver_sommet(event.x, event.y)
        if index is None:
            # Ajouter un sommet
            # print("ajout sommet")
            self.graph.add_vertex(event.x, event.y)
            self.view.vider_service()
            self.afficher_reseau()
        else:
            # Sélectionner un sommet
            # print('sommet selectionne:', index)
            self.graph.sommet_selectionne = index
            self.view.vider_service()
            self.view.entree_rate.insert(0, str(self.graph.sommets[index]["sc"].rate))
            self.view.entree_latency.insert(0, str(self.graph.sommets[index]["sc"].latency))
            self.view.entree_sha.insert(0, str(self.graph.sommets[index]["mr"]))

            if self.graph.chemin_en_cours:
                self.graph.chemin_courant.append(index)
                # print("Sommet ajouté au chemin :", index)
                self.afficher_chemin()
        self.dessiner()

    def analyser(self):
        prio_networks, prio_res_delays = self.graph.analyze_prio()
        ResPrioView(self.view, prio_networks, prio_res_delays)

    def save(self):
        self.graph.save_prio("toyprio.py")

    def define_num_classes(self):
        self.graph.num_classes = self.view.cn.get()
        # print("Number of classes: {}".format(self.num_classes))
        self.view.update_menu_class(self.num_classes)

    def quitter(self):
        self.view.destroy()

    def set_ncl(self):
        self.graph.num_classes = int(self.view.entree_ncl.get())
        self.view.update_menu_class(self.graph.num_classes)
        # print("Number of classes: {}".format(self.graph.num_classes))
