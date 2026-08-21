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
from pancoSenpai.Utils.colors import Cyan


class MainView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None  # sera injecté après
        self.configure(fg_color=Cyan.bg)

        ctk.CTkLabel(self, text="Welcome on PancoSenpai! the graphical tool to help you with Panco.",
                     text_color=Cyan.tx, font= ("Arial", 15)).pack(side="top", pady=10)
        ctk.CTkLabel(self, text="").pack(pady=5)
        ctk.CTkLabel(self, text="Choose the default parameters for your service curve \n"
                                "(service rate, latency and shaping rate) " 
                                 "and \narrival curve (burst, arrival rate and maximum packet length)",
                     text_color=Cyan.tx).pack( pady=5)
        self.btn_default = ctk.CTkButton(
            self,
            text="Default parameters",
            command=lambda:self.controller.open_default(),
            fg_color=Cyan.btn,
            hover_color=Cyan.hov,
            text_color=Cyan.tx,
            corner_radius=10,
        )
        self.btn_default.pack(pady=5)
        ctk.CTkLabel(self, text="").pack(pady=5)
        ctk.CTkLabel(self, text="Draw, analyze and generate the code of a small FIFO network",
        # (burst, arrival rate and maximum packet length)",
                     text_color=Cyan.tx).pack( pady=5)
        self.btn_toy = ctk.CTkButton(
            self,
            text="Toy FIFO network",
            command=lambda: self.controller.open_fifo_small(),
            fg_color=Cyan.btn,
            hover_color=Cyan.hov,
            text_color=Cyan.tx,
            corner_radius=10,
        )
        self.btn_toy.pack(pady=5)
        ctk.CTkLabel(self, text="").pack(pady=5)

        ctk.CTkLabel(self, text="Draw, analyze and generate the code of a \nsmall network with several priority classes",
        # (burst, arrival rate and maximum packet length)",
                     text_color=Cyan.tx).pack( pady=5)
        self.btn_prio = ctk.CTkButton(
            self,
            text="Toy network with priorities",
            command=lambda: self.controller.open_prio_small(),
            fg_color=Cyan.btn,
            hover_color=Cyan.hov,
            text_color=Cyan.tx,
            corner_radius=10,
        )
        (self.btn_prio.pack(pady=5))
        ctk.CTkLabel(self, text="").pack(pady=5)
        self.btn_quit = ctk.CTkButton(
            self,
            text="Quit",
            command=lambda:self.controller.quitter(),
            fg_color=Cyan.btn,
            hover_color=Cyan.hov,
            text_color=Cyan.tx,
            corner_radius=10,
        )
        self.btn_quit.pack(pady=5)


