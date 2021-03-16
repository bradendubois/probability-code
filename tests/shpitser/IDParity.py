#!/usr/bin/env python

#########################################################
#                                                       #
#   IDParity                                            #
#                                                       #
#   Author: Braden Dubois (braden.dubois@usask.ca)      #
#   Written for: Dr. Eric Neufeld                       #
#                                                       #
#########################################################

import os

from do.probability.shpitser.identification.IDAlgorithm import ID
from do.probability.shpitser.identification.IDProcessing import parse_shpitser
from do.probability.shpitser.latent.LatentProjection import latent_projection
from do.probability.shpitser.structures.Distribution import Distribution

from do.probability.structures.CausalGraph import CausalGraph
from do.probability.structures.VariableStructures import Outcome, Intervention

from do.util.helpers import power_set
from do.util.ModelLoader import parse_model


# A runnable test to ensure / prove the equivalence of results generated by the backdoor-criterion with the
#   expressions generated by Shpitser & Pearl's Identification algorithm

def id_parity():

    def parity(cg: CausalGraph, y: set, x: set):

        latent = latent_projection(cg.graph, cg.latent)

        identification = ID(y, x, Distribution(cg.tables), latent)
        result_identification = parse_shpitser(identification, cg, dict())

        head = [Outcome(v, cg.outcomes[v][0]) for v in y]
        print(x)
        body = [Intervention(v, cg.outcomes[v][0]) for v in x if v]

        result_do = cg.probability_query(head, body)

        return result_identification, result_do

    loc = "./graphs/full"

    graph_files = [f for f in os.listdir(loc) if os.path.isfile(os.path.join(loc, f))]

    corr = 0
    fail = 0

    for graph_file in [f for f in graph_files if not f.endswith("L.json")]:

        # Skip this graph as it is from testing some ideas and can't be used
        if graph_file == 'causal_graph_4.json':
            continue

        graph = CausalGraph(**parse_graph_file_data(loc + "/" + graph_file))

        for y in power_set(graph.variables, False):

            for x in power_set(set(graph.variables.keys()) - set(y)):

                res_id, res_do = parity(graph, set(y), set(x))

                if res_id and res_do:
                    assert res_id - res_do < 0.00000001
                    corr += 1
                else:
                    fail += 1

    print(corr, fail, corr + fail)