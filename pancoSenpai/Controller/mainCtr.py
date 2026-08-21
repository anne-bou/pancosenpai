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


from pancoSenpai.View.defaultView import DefaultView
from pancoSenpai.Controller.defaultCtr import DefaultCtr
from pancoSenpai.View.toyView import ToyView
from pancoSenpai.Controller.toyCtr import ToyCtr
from pancoSenpai.Controller.prioCtr import PrioCtr
from pancoSenpai.View.prioView import PrioView


class MainController:
    def __init__(self, view):
        self.view = view

    def open_fifo_small(self):
        toy_view = ToyView(self.view)
        toy_ctrl = ToyCtr(toy_view)
        toy_view.controller = toy_ctrl


    def open_prio_small(self):
        prio_view = PrioView(self.view)
        prio_ctrl = PrioCtr(prio_view)
        prio_view.controller = prio_ctrl

    def open_default(self):
        def_view = DefaultView(self.view)
        def_ctrl = DefaultCtr(def_view)
        def_view.controller = def_ctrl

    def quitter(self):
        self.view.master.destroy()
