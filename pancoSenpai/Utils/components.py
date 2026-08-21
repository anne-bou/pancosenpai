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
from pancoSenpai.Utils.colors import Color

def make_line(view, text, color: Color, tk_var, placeholder=""):
    line = ctk.CTkFrame(view, fg_color=color.bg)
    line.pack(fill="x", pady=4)

    label = ctk.CTkLabel(line, text=text, fg_color=color.bg, text_color=color.tx)
    label.pack(side="left", padx=5)
    label.pack(side="left", padx=5)

    entry = ctk.CTkEntry(line, width=50)
    entry.pack(side="right", padx=5)

    # --- Placeholder manuel ---
    entry.insert(0, placeholder)
    entry._placeholder_text = placeholder
    entry._is_placeholder = True

    def on_focus_in(event):
        if entry._is_placeholder:
            entry.delete(0, "end")
            entry._is_placeholder = False

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, entry._placeholder_text)
            entry._is_placeholder = True

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    # --- Synchronization with the  variable ---
    def update_var(event):
        if not entry._is_placeholder:
            tk_var.set(entry.get())

    entry.bind("<KeyRelease>", update_var)

    return line, label, entry


