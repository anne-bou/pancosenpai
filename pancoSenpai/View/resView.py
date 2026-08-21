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

from tkinter import ttk
import tkinter as tk


class ResView(tk.Toplevel):
    def __init__(self, parent, network, methods, results_delays):
        super().__init__(parent)
        self.network = network
        self.methods = methods
        self.results_delays = results_delays
        self.num_servers = self.network.num_servers
        self.num_flows = self.network.num_flows
        self.title("Results")
        columns = ["flow"] + self.methods
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        for c in columns:
            self.table.heading(c,  text=c)
        self.table.pack(fill="both", expand=True)
        self.delays = self.results_delays
        for i in range(self.network.num_flows):
            self.table.insert('', 'end', values=[str(i)]+ [str(self.delays[j][i]) for j in range(len(columns)-1)])
