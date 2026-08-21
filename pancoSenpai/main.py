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
from pancoSenpai.Controller.mainCtr import MainController
from pancoSenpai.View.mainView import MainView
from panco.descriptor.curves import RateLatency, TokenBucket
import os
import pickle
from pancoSenpai.path import DATA_FILE


def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        def_sc = RateLatency(10,1)

        def_ac = TokenBucket(2, 1)
        def_max_rate = 15
        def_ple = 1

        with open(DATA_FILE, "wb") as f:
            pickle.dump((def_sc, def_ac, def_max_rate, def_ple), f)

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PancoSenpai")
        self.geometry("500x500")
        # Vue principale
        self.view = MainView(self)
        # Controller principal
        self.controller = MainController(self.view)

        # On relie la vue au controller
        self.view.controller = self.controller

        self.view.pack(fill="both", expand=True)


def main():
    ensure_data_file()
    app = Main()
    app.mainloop()

if __name__ == "__main__":
    main()