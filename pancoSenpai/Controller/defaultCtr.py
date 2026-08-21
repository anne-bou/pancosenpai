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

from panco.descriptor.curves import RateLatency, TokenBucket
from pancoSenpai.path import DATA_FILE
import pickle

def get_entry_value(entry):
    value = entry.get()
    if entry._is_placeholder:
        return entry._placeholder_text
    return value


class DefaultCtr:
    def __init__(self, view):
        self.view = view

    def save_close(self):
        def_sc = RateLatency(int(get_entry_value(self.view.default_rate)),
                             int(get_entry_value(self.view.default_latency)))

        def_ac = TokenBucket(int(get_entry_value(self.view.default_sigma)),
                             int(get_entry_value(self.view.default_rho  )))
        def_max_rate = max(int(get_entry_value(self.view.default_max_rate)), def_sc.rate)
        def_ple = int(get_entry_value(self.view.default_ple))
        filename = DATA_FILE
        with open(filename, "wb") as f:
            pickle.dump((def_sc, def_ac, def_max_rate, def_ple), f)
        f.close()
        self.view.destroy()