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


from pancoSenpai.path import DATA_FILE
import pickle
import math
from panco.descriptor.curves import RateLatency, TokenBucket
from panco.descriptor.flow import Flow
from panco.descriptor.server import Server
from panco.descriptor.network import Network
from panco.fifo.admTFA import AdmTfa
from panco.fifo.sfaLP import SfaLP
from panco.fifo.fifoLP import FifoLP
from panco.staticpriorities.spFlow import SpFlow
from panco.staticpriorities.spNetwork import SpNetwork

class Graph:
    def __init__(self):
        self.sommets = []   # {"x":..., "y":..., "sc":..., "mr":...}
        self.aretes = []
        self.flows = []
        self.mpl = []
        self.sommet_selectionne = None
        self.flot_selectionne = None
        self.cla = []
        self.num_classes = 3
        self.cla_sel = 0
        self.cla_flo = 0

        self.chemin_en_cours = False
        self.chemin_courant = []
        with open(DATA_FILE, "rb") as f:
            self.default_sc, self.default_ac, self.max_rate, self.ple = pickle.load(f)
        f.close()

    def calcule_aretes(self):
        self.aretes = []
        for f in self.flows:
                for k in range(len(f.path) - 1):
                    if (f.path[k], f.path[k+1]) not in self.aretes:
                        self.aretes += [(f.path[k], f.path[k+1])]

    def apply_modifs_server(self, rate, latency, sha):
        if self.sommet_selectionne is None:
            return
        try:
            # print(self.sommet_selectionne)
            nouveau_taux = int(rate)
            nouveau_latence = int(latency)
            nouveau_sha = int(sha)
            self.sommets[self.sommet_selectionne]["sc"] = RateLatency(nouveau_taux, nouveau_latence)
            self.sommets[self.sommet_selectionne]["mr"] = nouveau_sha
        except ValueError:
            pass  # on ignore si ce n'est pas un nombrepass

    def delete_server(self):
        self.flot_selectionne  = None
        if self.sommet_selectionne is None:
            return
        try:
            # print(self.sommet_selectionne)
            i = self.sommet_selectionne
            self.sommets = [self.sommets[j] for j in range(len(self.sommets)) if not i == j]
            new_flots = []
            for j in range(len(self.flows)):
                if i not in self.flows[j].path:
                    p = []
                    for k in self.flows[j].path:
                        if k < i:
                            p += [k]
                        else:
                            p += [k-1]
                    new_flots += [Flow(self.flows[j].arrival_curve, p)]
            self.flows = new_flots
            self.calcule_aretes()
        except ValueError:
            pass  # on ignore si ce n'est pas un nombre pass

    def delete_flow(self):
        # print("delete")
        if self.flot_selectionne is None:
            # print("flot sel = None")
            return
        try:
            # print("supprimer flot ", self.flot_selectionne)
            j = self.flot_selectionne
            # print(j, len(self.flows), len(self.mpl))
            self.flows = [self.flows[i] for i in range(len(self.flows)) if not i == j]
            self.cla = [self.cla[i] for i in range(len(self.cla)) if not i == j]
            self.mpl = [self.mpl[i] for i in range(len(self.mpl)) if not i == j]
            # print(len(self.flows), len(self.mpl))
            self.flot_selectionne = None
        except ValueError:
            pass


    def end_path(self):
        if len(self.chemin_courant) < 1:
            # print("The path is too short. Please, select at least one server")
            return

        # print("\n=== CHEMIN FINAL ===")
        # print(" → ".join(str(i) for i in self.chemin_courant))
        # print("====================\n")
        text = self.texte_chemin()
        self.chemin_en_cours = False
        return text


    def texte_chemin(self):
        if not self.chemin_en_cours:
            return "chemin vide"
        else:
            text = " → ".join(str(i) for i in self.chemin_courant)
            return text

    def new_path(self):
        self.chemin_en_cours = True
        self.chemin_courant = []
        # print("Début d’un nouveau chemin.")


    def apply_modifs_flow(self, rho, sigma, mpl, cla):
        nouveau_rho = int(rho)
        nouveau_sigma = int(sigma)
        nouveau_mpl = int(mpl)
        nouvelle_classe = int(cla)
        if self.flot_selectionne is not None:
            if self.chemin_courant == []:
                self.chemin_courant = self.flows[self.flot_selectionne].path
                self.end_path()
            j = self.flot_selectionne
            self.flows[j] = Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant)
            self.mpl[j] = nouveau_mpl
            self.cla[j] = nouvelle_classe
        else:
            if self.chemin_courant == []:
                return
            self.flows += [Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant)]
            # print("flot", Flow([TokenBucket(nouveau_sigma, nouveau_rho)], self.chemin_courant))
            self.mpl += [nouveau_mpl]
            self.cla += [nouvelle_classe]
        self.flot_selectionne = None
        self.classe_courante = None
        self.chemin_courant = []
        self.chemin_en_cours = False


    def trouver_sommet(self, x, y):
        for i, s in enumerate(self.sommets):
            if math.dist((x, y), (s["x"], s["y"])) < 15:
                return i
        return None


    def add_vertex(self, x, y):
        self.sommets.append({"x": x, "y": y, "sc": self.default_sc, "mr":self.max_rate})
        self.sommet_selectionne = None

    def afficher_reseau(self, context):
        text_s = "Servers:\n"
        for (i, s) in enumerate(self.sommets):
            text_s += "\t{0}: {1}(t-{2})_+\n".format(i, self.sommets[i]['sc'].rate, self.sommets[i]['sc'].latency)
        text_f = "Flows:\n"
        for (i, f) in enumerate(self.flows):
            if context == 0:
                text_f += "\t{0}: {1}+{2}t\t {3}\t{4}\n".format(i,f.arrival_curve[0].sigma,
                                                f.arrival_curve[0].rho , f.path, self.mpl[i])
            if context == 1:
                text_f += "\t{0}: {1}+{2}t\t {3}\t{4}\n".format(i,f.arrival_curve[0].sigma,
                                                f.arrival_curve[0].rho , f.path, self.cla[i])
        # print(text_f)
        return text_s, text_f


    def analyze_fifo(self, tfa, sfa, plp, elp):
        servers = [Server([self.sommets[i]['sc']],
                          [TokenBucket(0, self.sommets[i]["mr"])]) for i in range(len(self.sommets))]
        network =Network(servers, self.flows)
        for j in range(network.num_servers):
            network.servers[j].max_service_curve[0].sigma = max([0] + [self.mpl[i] for i in network.flows_in_server[j]])
        methods = []
        results_delays = []
        if tfa:
            methods+= ['TFA']
            results_delays +=[AdmTfa(network).all_delays]

        if sfa:
            methods+= ['SFA']
            results_delays +=[SfaLP(network).all_delays]
        if plp:
            methods+= ['PLP']
            results_delays +=[FifoLP(network, polynomial=True, tfa=True, sfa=True).all_delays]

        if elp:
            methods+= ['ELP']
            results_delays +=[FifoLP(network, polynomial=False).all_delays]
        return network, methods, results_delays



    def write_file(self, tfa, sfa, plp, elp, filename):
        servers = [Server([self.sommets[i]['sc']], [TokenBucket(0, self.sommets[i]["mr"])])
                   for i in range(len(self.sommets))]
        # filename = "toy.py"
        file = open(filename, "w")
        network =Network(servers, self.flows)
        file.write("from panco.descriptor.curves import RateLatency, TokenBucket\n")
        file.write("from panco.descriptor.server import Server\n")
        file.write("from panco.descriptor.flow import Flow\n")
        file.write("from panco.descriptor.network import Network\n")
        file.write("from panco.fifo.admTFA import AdmTfa\n")
        file.write("from panco.fifo.sfaLP import SfaLP\n")
        file.write("from panco.fifo.fifoLP import FifoLP\n\n\n")

        file.write("\n\n# Constuction of the network\n\n")
        file.write("flows = []\n")
        for i in range(network.num_flows):
            file.write("flows+= [Flow([TokenBucket({}, {})], {})]\n".format(network.flows[i].arrival_curve[0].sigma,
                                                                            network.flows[i].arrival_curve[0].rho,
                                                                            network.flows[i].path))
        file.write("mpl = []\n")
        for i in range(network.num_flows):
            file.write("mpl+= [{}]\n".format(self.mpl[i]))
        file.write("servers = []\n")
        for i in range(len(self.sommets)):
            file.write("servers+=[Server([RateLatency({},{})], [TokenBucket(0, {})])]\n".format(network.servers[i].service_curve[0].rate,
                                                                 network.servers[i].service_curve[0].latency, self.sommets[i]["mr"]))
        file.write("network = Network(servers, flows)\n")
        file.write("for j in range(network.num_servers):\n")
        file.write("\tnetwork.servers[j].max_service_curve[0].sigma = max([0] + [mpl[i] for i in network.flows_in_server[j]])\n")
        file.write("\n\n# Computation of the bounds\n\n")
        if tfa:
            file.write("print(AdmTfa(network).all_delays)\n")
        if sfa:
            file.write("print(SfaLP(network).all_delays)\n")
        if plp:
            file.write("print(FifoLP(network, polynomial=True, tfa=True, sfa=True).all_delays)\n")
        if elp:
            file.write("print(FifoLP(network, polynomial=False).all_delays)\n")
        file.close()

    def analyze_prio(self):
        servers = [Server([self.sommets[i]['sc']],
                          [TokenBucket(0, self.sommets[i]["mr"])]) for i in range(len(self.sommets))]
        network =Network(servers, self.flows)
        for j in range(network.num_servers):
            network.servers[j].max_service_curve[0].sigma = max([0] + [self.mpl[i] for i in network.flows_in_server[j]])
        spflows = [SpFlow(self.flows[i].arrival_curve, self.flows[i].path, self.mpl[i], self.cla[i])
                 for i in range(len(self.flows))]
        spnet = SpNetwork(network.servers, spflows)
        per_class_nets = spnet.equiv_network(True)
        # print('Les reseaux', per_class_nets)
        prio_networks = per_class_nets
        prio_res_delays =[FifoLP(net, polynomial=True, tfa=True, sfa=True).all_delays for net in per_class_nets]
        return prio_networks, prio_res_delays

    def save_prio(self, filename):
        servers = [Server([self.sommets[i]['sc']], [TokenBucket(0, self.sommets[i]["mr"])])
                   for i in range(len(self.sommets))]
        file = open(filename, "w")
        network =Network(servers, self.flows)
        file.write("from panco.descriptor.curves import RateLatency, TokenBucket\n")
        file.write("from panco.descriptor.server import Server\n")
        file.write("from panco.descriptor.flow import Flow\n")
        file.write("from panco.descriptor.network import Network\n")
        file.write("from panco.fifo.fifoLP import FifoLP\n")
        file.write("from panco.staticpriorities.spFlow import SpFlow\n"
                   "from panco.staticpriorities.spNetwork import SpNetwork\n\n\n")

        file.write("flows = []\n")
        for i in range(network.num_flows):
            file.write("flows+= [Flow([TokenBucket({}, {})], {})]\n".format(network.flows[i].arrival_curve[0].sigma,
                                                                            network.flows[i].arrival_curve[0].rho,
                                                                            network.flows[i].path))
        file.write("mpl = []\n")
        for i in range(network.num_flows):
            file.write("mpl+= [{}]\n".format(self.mpl[i]))
        file.write("cla = []\n")
        for i in range(network.num_flows):
            file.write("cla+= [{}]\n".format(self.cla[i]))
        file.write("servers = []\n")
        for i in range(len(self.sommets)):
            file.write("servers+=[Server([RateLatency({},{})], [TokenBucket(0, {})])]\n".format(network.servers[i].service_curve[0].rate,
                                                                 network.servers[i].service_curve[0].latency, self.sommets[i]["mr"]))
        file.write("network = Network(servers, flows)\n")
        file.write("for j in range(network.num_servers):\n")
        file.write("\tnetwork.servers[j].max_service_curve[0].sigma = max([0] + [mpl[i] for i in network.flows_in_server[j]])\n")
        file.write("spflows = [SpFlow(flows[i].arrival_curve, flows[i].path, mpl[i], cla [i])\n"
                   "           for i in range(network.num_flows)]\n")
        file.write("spnet = SpNetwork(network.servers, spflows)\n")
        file.write("per_class_nets = spnet.equiv_network(True)\n")
        file.write("for net in per_class_nets:\n")
        file.write("\tprint(net)\n\tprint(FifoLP(net, polynomial=True, tfa=True, sfa=True).all_delays)\n")
        file.close()

