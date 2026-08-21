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
import pickle
import tkinter as tk
import pancoSenpai.Utils.components as ct
from pancoSenpai.Utils.colors import Green, Mauve
from pancoSenpai.path import DATA_FILE
fg_col = "#bbbbbb"

class DefaultView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None  # will be injected afterward

        self.title('Set Default Parameters')
        self.geometry("200x500")

        self.default_rate = ctk.StringVar()
        self.default_rate = ctk.StringVar()

        f = DATA_FILE
        with open(file=f, mode="rb") as f:
            sc, ac, max_rate, ple = pickle.load(f)      
        f.close()
        ctk.CTkLabel(self, text="Enter the default \nparameters for your network \n(it will be possible \n"
                                "to modify them afterwards).").pack(pady=1)
        ctk.CTkLabel(self, text="Server Parameters", fg_color=Mauve.btn, font=("Arial", 15), text_color=Mauve.tx,
                     corner_radius=10).pack(pady=1)

        _, _, self.default_rate = ct.make_line(self, "Service rate:", Mauve,ctk.StringVar(),
                                               placeholder=str(sc.rate))
        _, _, self.default_latency = ct.make_line(self, "Service latency:", Mauve,ctk.StringVar(),
                                                  placeholder="{}".format(sc.latency))
        _, _, self.default_max_rate = ct.make_line(self, "Max. Service rate:", Mauve,ctk.StringVar(),
                                           placeholder="{}".format(max_rate))

        ctk.CTkLabel(self, text="Flow Parameters", fg_color=Green.btn, font=("Arial", 15), text_color=Green.tx,
                     corner_radius=10).pack(pady=10)
        _, _, self.default_rho = ct.make_line(self, "Arrival rate: ", Green, tk.StringVar(),
                                              placeholder="{}".format(ac.rho))
        _, _, self.default_sigma = ct.make_line(self, "Burst", Green ,tk.StringVar(),
                                                placeholder="{}".format(ac.sigma))
        _, _, self.default_ple = ct.make_line(self, "Max Packet length:", Green, tk.StringVar(),
                                              placeholder="{}".format(ple))


        ctk.CTkButton(self, text="Save and close",
                      command=lambda: self.controller.save_close(), corner_radius=10).pack(pady=1)
