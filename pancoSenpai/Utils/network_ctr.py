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


from pancoSenpai.path import DATA_FILE
import pickle
import math
from panco.descriptor.curves import RateLatency, TokenBucket
from panco.descriptor.flow import Flow

class Graphe:
    def __init__(self):
        self.sommets = []   # {"x":..., "y":..., "sc":..., "mr":...}
        self.aretes = []
        self.flows = []
        self.mpl = []
        self.sommet_selectionne = None
        self.flot_selectionne = None
        self.cla = []
        self.num_classes = 3
        self.cla_sel = 0

        self.chemin_en_cours = False
        self.chemin_courant = []
        with open(DATA_FILE, "rb") as f:
            self.default_sc, self.default_ac, self.max_rate, self.ple = pickle.load(f)
        f.close()

    def calcule_aretes(self):
        self.aretes = []
        for f in self.flows:
                for k in range(len(f.path) - 1):
                    if (f.path[k], f.path[k+1]) not in self.aretes:
                        self.aretes += [(f.path[k], f.path[k+1])]

    def apply_modifs_server(self, rate, latency, sha):
        if self.sommet_selectionne is None:
            return
        try:
            # print(self.sommet_selectionne)
            nouveau_taux = int(rate)
            nouveau_latence = int(latency)
            nouveau_sha = int(sha)
            self.sommets[self.sommet_selectionne]["sc"] = RateLatency(nouveau_taux, nouveau_latence)
            self.sommets[self.sommet_selectionne]["mr"] = nouveau_sha
        except ValueError:
            pass  # on ignore si ce n'est pas un nombrepass

    def texte_chemin(self):
        if not self.chemin_en_cours:
            return "chemin vide"
        else:
            text = " → ".join(str(i) for i in self.chemin_courant)
            return text

    def add_path_f(self):
        self.chemin_en_cours = True
        self.chemin_courant = []
        # print("Début d’un nouveau chemin.")


    def apply_modifs_flot(self, rho, sigma, mpl, cla):
        nouveau_rho = int(rho)
        # print("rho")
        nouveau_sigma = int(sigma)
        nouveau_mpl = int(mpl)
        nouvelle_classe = int(cla)
        # print("sigma")
        if self.flot_selectionne is not None:
            j = self.flot_selectionne
            self.flows[j] = Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant)
            self.mpl[j] = nouveau_mpl
            self.cla[j] = nouvelle_classe
        else:
            self.flows += [Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant)]
            # print("flot", Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant))
            self.mpl += [nouveau_mpl]
            self.cla += [nouvelle_classe]
        self.flot_selectionne = None
        self.chemin_courant = []
        self.chemin_en_cours = False

    def trouver_sommet(self, x, y):
        for i, s in enumerate(self.sommets):
            if math.dist((x, y), (s["x"], s["y"])) < 15:
                return i
        return None
