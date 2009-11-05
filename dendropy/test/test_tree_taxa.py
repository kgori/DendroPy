#! /usr/bin/env python

###############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2009 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
Tests composition and traversal of trees.
"""

import unittest
import sys

from dendropy.utility import messaging
from dendropy.test import support
from dendropy.dataobject import tree as treeobj
from dendropy.dataobject import taxon as taxonobj

_LOG = messaging.get_logger(__name__)

class TreeTaxonSettingTest(unittest.TestCase):

    def build_tree_from_labels(self, tax_labels):
        """
        (0, (1, (2, 3)));
        """
        _LOG.info("Getting new tree: %s" % tax_labels)
        tree = treeobj.Tree()
        leaf_nodes = []
        for tax_label in tax_labels[:4]:
            t = tree.taxon_set.require_taxon(label=tax_label)
            leaf_nodes.append(treeobj.Node(taxon=t))
        self.assertEquals(len(tree.taxon_set), 4)
        tree.seed_node.add_child(node=leaf_nodes[0])
        n = tree.seed_node.new_child()
        n.add_child(node=leaf_nodes[1])
        n = n.add_child(treeobj.Node())
        n.add_child(node=leaf_nodes[2])
        n.add_child(node=leaf_nodes[3])
        return tree

    def testTreeTaxonSetting(self):
        t1 = self.build_tree_from_labels(["a1", "a2", "a3", "a4"])
        for i, nd in enumerate(t1.leaf_iter()):
            nd.old_taxon = nd.taxon
            nd.taxon.label = "b%d" % i
        tx_old = t1.taxon_set
        tx_new = taxonobj.TaxonSet()
        t1.reindex_taxa(tx_new)
        for i, taxon in enumerate(tx_new):
            expected = "b%d" % i
            self.assertEquals(taxon.label, expected,
                "Expecting '%s', but found '%s'" % (expected, taxon.label))
        for i, nd in enumerate(t1.leaf_iter()):
            assert nd.old_taxon is not nd.taxon
            assert nd.old_taxon in tx_old
            assert nd.taxon in tx_new

    def testTreeListTaxonSetting(self):

        # add trees with identical taxon labels, but different `Taxon`
        # objects
        tree_coll = treeobj.TreeList()
        for i in xrange(10):
            t = self.build_tree_from_labels(['b1', 'b2', 'b3', 'b4'])
            t.old_taxa = t.taxon_set
            tree_coll.append(t)
        self.assertEquals(len(tree_coll), 10)
        for t in tree_coll:
            assert t.taxon_set is tree_coll.taxon_set
            assert t.taxon_set is not t.old_taxa

if __name__ == "__main__":
    unittest.main()