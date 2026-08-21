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


class GraphRenderer:
    @staticmethod
    def draw_node(canvas, x: int, y: int, s, i, couleur):
        canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill=couleur)
        canvas.create_text(x, y, text=str(i))
        canvas.create_text(x, y-15, text=str(s["sc"]))

    @staticmethod
    def draw_edge(canvas, s1, s2, couleur):
        canvas.create_line(s1["x"], s1["y"], s2["x"], s2["y"], width=2, arrow="last", arrowshape=(12, 15, 5),
                                fill=couleur)

    def draw_network(self, canvas, sommets, aretes, path, ssel):
        canvas.delete("all")
        # Aretes
        for (i, j) in aretes:
            s1 = sommets[i]
            s2 = sommets[j]
            self.draw_edge(canvas, s1, s2, "black")
        if path  is not None:
            for k in range(len(path)-1):
                self.draw_edge(canvas, sommets[path[k]], sommets[path[k + 1]], "red")
        # Sommets
        for i, s in enumerate(sommets):
            x, y = s["x"], s["y"]
            couleur = "orange" if i == ssel else "skyblue"
            self.draw_node(canvas, x, y, s, i, couleur)



