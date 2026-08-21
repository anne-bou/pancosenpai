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
from pancoSenpai.Utils.colors import  Mauve, Blue, Green, Orange, Red

colors = [Mauve, Orange, Green, Red, Blue]

class ResPrioView(ctk.CTkToplevel):
    def __init__(self, parent, prio_networks, delays):
        super().__init__(parent)
        self.prio_networks = prio_networks
        self.delays = delays
        self.title("Results for the priority network")

        for c in range(len(self.prio_networks)):
            self.net_frame = ctk.CTkFrame(self, fg_color=colors[c].bg)
            self.net_frame.grid(row=0, column=c % 5, sticky="nsew", padx=5, pady=5)

            ctk.CTkLabel(self.net_frame, text='class {} network\n\n'.format(c) +
                                str(self.prio_networks[c])).pack(side="left", fill="x", padx=5, pady=5)
            self.del_frame=ctk.CTkFrame(self, fg_color=colors[c].bg)
            self.del_frame.grid(row=1, column=c, sticky="nsew", padx=5, pady=5)

            seq_del = ["flow {0}\t{1}\n".format(i, j) for (i, j) in enumerate(self.delays[c])]
            text_del = ""
            for d in seq_del:
                text_del += d
            ctk.CTkLabel(self.del_frame, text=text_del).pack()
