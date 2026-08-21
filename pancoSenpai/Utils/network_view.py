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
import tkinter as tk
from pancoSenpai.Utils.colors import Color
from pancoSenpai.Utils.components import make_line

def server_view(frame, col:Color, on_save, on_delete):
    ctk.CTkLabel(frame  , text="Define/modify a server", fg_color=col.bg,
                 text_color=col.tx,  font=("Arial", 15)).pack(pady=5)
    ctk.CTkLabel(frame, text="Click on the white rectangle \nto create a server\nClick"
                                       "on a sever to select and \nmodify/delete it", fg_color=col.bg,
                     text_color=col.tx,  font=("Arial", 10)).pack(pady=1)
    _, _, rate = make_line(frame, "Service rate:", col, tk.StringVar(), placeholder="")
    _, _, latency = make_line(frame, "Latency:", col, tk.StringVar(), placeholder="")
    _, _, sha = make_line(frame, "Shaping rate:", col, tk.StringVar(), placeholder="")
    bouton_update_sc = ctk.CTkButton(frame,fg_color=col.btn, text_color=col.tx, hover_color = col.hov,
                                     text="Save service curve", command=on_save)
    bouton_update_sc.pack(pady=1)

    bouton_delete_server = ctk.CTkButton(frame,fg_color=col.btn, text_color=col.tx, hover_color = col.hov,
                                         text="Delete server", command=on_delete)
    bouton_delete_server.pack(pady=1)
    return rate, latency, sha

def flow_view(frame, context, col:Color, on_add, on_apply, on_class):
        ctk.CTkLabel(frame, text="Define/modify a flow", text_color=col.tx, font= ("Arial", 15)).pack(pady=1)
        new_flow = ctk.CTkButton(frame,fg_color=col.btn, hover_color = col.hov, text="New flow",
                                      text_color=col.tx,
                                      command=on_add)
        new_flow.pack(pady=1)
        _, _, rho = make_line(frame, "Arrival rate:", col, tk.StringVar(), placeholder="")
        _, _, sigma = make_line(frame, "Burst:", col, tk.StringVar(),
                                              placeholder="")
        _, _, ple = make_line(frame, "Max. Packet length:", col, tk.StringVar(),
                                              placeholder="")
        if context == 1:
            bouton_class = ctk.CTkComboBox(frame, values=["0", "1", "2"], text_color=col.tx,
                                           fg_color=col.bg,
                        button_color=col.btn, border_color=col.btn,
                        command = on_class,
                        )
            bouton_class.pack(pady=1)

        bouton_appliquer = ctk.CTkButton(frame, fg_color=col.btn, hover_color = col.hov, text="Apply",
                                              text_color=col.tx, command=on_apply)
        bouton_appliquer.pack(pady=1)

        zone_chemin = ctk.CTkFrame(frame, fg_color=col.bg, height=150)
        zone_chemin.pack(side="bottom", fill="x", pady=10)

        ctk.CTkLabel(zone_chemin, text="Path :", fg_color=col.bg, text_color=col.tx,
                     font=("Arial", 15)).pack(anchor="w")

        label_chemin = ctk.CTkLabel(zone_chemin, text="(empty)", fg_color=col.bg, text_color=col.tx,
                                         justify="left")
        label_chemin.pack(anchor="w", padx=5, pady=5)
        if context == 1:
            return rho, sigma, ple, label_chemin, bouton_class
        return rho, sigma, ple, label_chemin

def flow_modif(frame, col:Color, on_select, on_modif, on_delete):
    ctk.CTkLabel(frame, text="Select/delete a flow", text_color=col.tx,
                     font= ("Arial", 15)).pack(pady=1)
    ctk.CTkLabel(frame, text="Choose the flow you want to modify", text_color=col.tx).pack(pady=1)
    bouton_flot = ctk.CTkComboBox(frame, values=[""], text_color=col.tx, fg_color=col.bg, button_color=col.btn,
                                  border_color=col.btn, command = on_select)
    bouton_flot.pack(pady=1)

    ctk.CTkButton(frame,text="Modify flow", text_color=col.tx, fg_color=col.btn, hover_color=col.hov,
                      command=on_modif).pack(pady=1)
    ctk.CTkButton(frame,text="Delete flow", text_color=col.tx, fg_color=col.btn, hover_color=col.hov,
                      command=on_delete).pack(pady=1)
    return bouton_flot

def print_network(frame, col:Color):
    ctk.CTkLabel(frame, text="Network description", text_color=col.tx, fg_color=col.bg,
                     font= ("Arial", 15)).pack()
    # tk.Label(self.print_s, text=str(self.sommets[0]["sc"]))

    label_servers = ctk.CTkLabel(frame, text="No server or flow defined yet",
                                          text_color=col.tx, fg_color=col.bg, justify="left")
    label_servers.pack(anchor="w", padx=5, pady=5)
    label_flows = ctk.CTkLabel(frame, text="", text_color=col.tx, fg_color=col.bg, justify="left")
    label_flows.pack(anchor="w", padx=5, pady=5)
    return label_servers, label_flows

def vider_champs(*widgets):
    for w in widgets:
        w.delete(0, "end")



