# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import os, sys
import json

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory






# TEMPLATE: D3 PACK HIERARCHY
# http://mbostock.github.io/d3/talk/20111116/pack-hierarchy.html
# https://github.com/d3/d3/wiki/Pack-Layout
# http://bl.ocks.org/nilanjenator/4950148





class D3PackHierarchyViz(VizFactory):
    """
    D3 PackHierarchyViz

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(D3PackHierarchyViz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/d3-v3", "libs/jquery"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        jsontree_classes = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayer)
        c_total = len(self.ontospy_graph.classes)


        if len(self.ontospy_graph.toplayer) == 1:
            # the first element can be the single top level
            JSON_DATA_CLASSES = json.dumps(jsontree_classes[0])
        else:
            # hack to make sure that we have a default top level object
            JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'owl:Thing',})


        extra_context = {
                        "ontograph": self.ontospy_graph,
    					"TOTAL_CLASSES": c_total,
    					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
                        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate("d3/d3_packHierarchy.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        return main_url




# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = D3PackHierarchyViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e





# ===========
# June 20, 2016 : notes
# ===========
# ....
#
#
#
# def run(graph, save_on_github=False, main_entity=None ):
# 	"""
# 	"""
# 	try:
# 		ontology = graph.ontologies[0]
# 		uri = ontology.uri
# 	except:
# 		ontology = None
# 		uri = ";".join([s for s in graph.sources])
#
# 	# ontotemplate = open("template.html", "r")
# 	ontotemplate = open(ONTODOCS_VIZ_TEMPLATES + "d3_packHierarchy.html", "r")
# 	t = Template(ontotemplate.read())
#
# 	jsontree_classes = build_D3treeStandard(0, 99, 1, graph.toplayer)
# 	c_total = len(graph.classes)
#
#
# 	if len(graph.toplayer) == 1:
# 		# the first element can be the single top level
# 		JSON_DATA_CLASSES = json.dumps(jsontree_classes[0])
# 	else:
# 		# hack to make sure that we have a default top level object
# 		JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'owl:Thing',})
#
# 	c = Context({
# 					"ontology": ontology,
# 					"main_uri" : uri,
# 					"STATIC_PATH": ONTODOCS_VIZ_STATIC,
# 					"save_on_github" : save_on_github,
# 					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
# 					"TOTAL_CLASSES": c_total,
# 				})
#
# 	rnd = t.render(c)
#
# 	return safe_str(rnd)
#
#
#
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
# 	import sys
# 	try:
# 		# script for testing - must launch this module
# 		# >python -m viz.viz_packh
#
# 		func = locals()["run"] # main func dynamically
# 		run_test_viz(func)
#
# 		sys.exit(0)
#
# 	except KeyboardInterrupt as e: # Ctrl-C
# 		raise e