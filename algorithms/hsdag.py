#!/usr/bin/env python
import logging
import multiprocessing as mp

from algorithms import quickxplain
from common import utils

logging.basicConfig(level=logging.DEBUG)

solver_path = "solver_apps/choco4solver.jar"
numCores = mp.cpu_count()
maxNumGenCC = numCores - 1
currentNumGenCC = 0

counter_constructed_nodes = 0

maxNumberOfDiagnoses = -1
maxNumberOfConflicts = -1

nodeLabels = []
pathLabels = []

root = None
openNodes = []
label_nodesMap = {}
nodes_lookup = {}


def getConflicts():
    return nodeLabels


def getDiagnoses():
    return pathLabels


def construct(B, C):
    # generate root if there is none
    if createRoot(B, C):
        createNodes()


def createRoot(B, C):
    global root, openNodes, counter_constructed_nodes

    hasRootLabel = True

    if not hasRoot():
        labels = computeLabel(C, B)

        if len(labels) == 0:
            hasRootLabel = False
        else:  # create root node
            label = selectLabel(labels)
            root = Node(None, None, B, C)
            root.label = label
            counter_constructed_nodes = counter_constructed_nodes + 1

            openNodes.append(root)

            addNodeLabels(labels)  # to reuse labels
            addItemToLabelNodesMap(label, root)

            # log.debug("{}(HSTree-construct) Created root node [root={}]", LoggerUtils.tab(), root);
    return hasRootLabel


def createNodes():
    while hasNodesToExpand():
        node = getNextNode()

        if not node.isRoot():
            if skipNode(node):
                continue

            # log.debug("{}(HSTree-createNodes) Processing [node={}]", LoggerUtils.tab(), node);
            # LoggerUtils.indent();

            label(node)

            if shouldStopConstruction():
                # LoggerUtils.outdent();
                break

        if node.status == "Open":
            expand(node)

        # if not node.isRoot():
        # LoggerUtils.outdent();


def label(node):
    # Reusing labels - H(node) ∩ S = {}, then label node by S
    labels = getReusableLabels(node)

    # compute labels if there are none to reuse
    if len(labels) == 0:
        labels = computeLabel(node.C, node.B)

        processLabels(labels)

    if len(labels) > 0 and len(labels[0]) > 0:
        label = selectLabel(labels)

        node.label = label
        addItemToLabelNodesMap(label, node)

        # log.debug("{}(HSTree-label) Node [node={}] has label [label={}]", LoggerUtils.tab(), node, label);
    else:  # found a path label
        foundAPathLabelAtNode(node)


def expand(nodeToExpand):
    global counter_constructed_nodes, openNodes
    # log.debug("{}(HSTree-expand) Generating the children nodes of [node={}]", LoggerUtils.tab(), nodeToExpand);
    # LoggerUtils.indent();

    for arcLabel in nodeToExpand.label:
        B, C = nodeToExpand.create_parameter(arcLabel)

        # rule 1.a - reuse node
        node = getReusableNode(nodeToExpand.pathLabel, arcLabel)
        if node is not None:
            node.addparent(nodeToExpand)
        else:  # rule 1.b - generate a new node
            node = Node(nodeToExpand, arcLabel, B, C)
            nodes_lookup[utils.get_hashcode(node.pathLabel)] = node
            counter_constructed_nodes = counter_constructed_nodes + 1

            if not canPrune(node):
                openNodes.append(node)
                # log.debug("{}(HSTree-expand) Created [node={}]", LoggerUtils.tab(), node);


def shouldStopConstruction():
    # when the number of already identified diagnoses is greater than the limit, stop the computation
    condition1 = (maxNumberOfDiagnoses != -1 and maxNumberOfDiagnoses <= len(getDiagnoses()))
    # OR when the number of already identified conflicts is greater than the limit, stop the computation
    condition2 = (maxNumberOfConflicts != -1 and maxNumberOfConflicts <= len(getConflicts()))

    return condition1 or condition2


def addItemToLabelNodesMap(label, node):
    global label_nodesMap

    hashcode = utils.get_hashcode(label)
    if hashcode in label_nodesMap:
        label_nodesMap[hashcode].append(node)
    else:
        label_nodesMap[hashcode] = [node]


def computeLabel(C, B):
    return [quickxplain.quickXplain(C, B)]


def addNodeLabels(labels):
    global nodeLabels
    for label in labels:
        nodeLabels.append(label.copy())


def foundAPathLabelAtNode(node):
    node.status = "Checked"
    pathLabel = node.pathLabel.copy()

    addPathLabel(pathLabel)


def addPathLabel(pathLabel):
    global pathLabels
    pathLabels.append(pathLabel)


def selectLabel(labels):
    return labels.pop(0)


def hasNodesToExpand():
    return len(openNodes) > 0


def getNextNode():
    global openNodes
    if len(openNodes) > 0:
        return openNodes.pop(0)
    else:
        return None


def hasRoot():
    return root is not None


class Node(object):
    generatedNodeId = -1

    def __init__(self, parent, arcLabel, B, C):
        Node.generatedNodeId = Node.generatedNodeId + 1
        self.id = Node.generatedNodeId
        self.status = "Open"
        if parent is None:
            self.level = 0
            self.parents = None
            self.pathLabel = []
        else:
            self.level = parent.level + 1
            self.parents = []
            parent.addChild(arcLabel, self)
            if len(parent.pathLabel) > 0:
                self.pathLabel = parent.pathLabel.copy()
            else:
                self.pathLabel = []
            self.pathLabel.append(arcLabel)
        self.B = B
        self.C = C
        self.arcLabel = arcLabel
        self.label = None

        self.children = {}

    def isRoot(self):
        return self.parents is None

    def addParent(self, parent):
        if not self.isRoot():
            self.parents.append(parent)

    def addChild(self, arcLabel, child):
        if arcLabel is not None:
            self.children[utils.get_hashcode([arcLabel])] = child
            child.addParent(self)

    def create_parameter(self, arcLabel):
        newC = self.C.copy()
        newC.remove(arcLabel)

        newB = self.B.copy()

        return newB, newC

    def __str__(self):
        return "Node: " + str(self.id) + ", level= " + str(self.level) + ", status: " + self.status + ", label= " \
               + str(self.label) + ", B= " + str(self.B) + ", C= " + str(self.C) + ", arcLabel= " + str(self.arcLabel) \
               + ", pathLabels: " + str(self.pathLabel)


# Pruning engine
def skipNode(node):
    return node.status != "Open" or canPrune(node)


def canPrune(node):
    # 3.i - if n is checked, and n'' is such that H(n) ⊆ H(n'), then close the node n''
    # n is a diagnosis
    for pathLabel in pathLabels:
        if all(elem in pathLabel for elem in node.pathLabel):
            # if node.pathLabel.containsAll(pathLabel):
            node.status = "Closed"
            # incrementCounter(COUNTER_CLOSE_1);

            # log.debug("{}(HSTreePruningEngine-canPrune_3i) Closed [node={}]", LoggerUtils.tab(), node);

            return True

    # 3.ii - if n has been generated and node n'' is such that H(n') = H(n), then close node n''
    for n in openNodes:
        if len(n.pathLabel) == len(node.pathLabel) and len(utils.diff(n.pathLabel, node.pathLabel)) == 0:
            node.status = "Closed"
            # incrementCounter(COUNTER_CLOSE_2);

            # log.debug("{}(HSTreePruningEngine-canPrune_3i) Closed [node={}]", LoggerUtils.tab(), node);

            return True
    return False


def getReusableLabels(node: Node):
    labels = []
    for label in nodeLabels:
        # H(node) ∩ S = {}
        if not utils.hasIntersection(node.pathLabel, label):
            labels.append(label)
            # incrementCounter(COUNTER_REUSE_LABELS);
            # log.debug("{}(HSTreePruningEngine-getReusableLabels) Reuse [label={}, node={}]", LoggerUtils.tab(), label, node);

    return labels


def getReusableNode(pathLabels, arcLabel):
    h = pathLabels.copy()
    h.append(arcLabel)
    hashcode = utils.get_hashcode(h)
    return nodes_lookup.get(hashcode)


def processLabels(labels):
    if len(labels) > 0 and len(labels[0]) > 0:
        # stop(TIMER_NODE_LABEL);
        # check existing and obtained labels for subset-relations
        nonMinLabels = []

        for fs in nodeLabels:
            if utils.contains(nonMinLabels, fs):
                continue

            for cs in labels:
                if utils.contains(nonMinLabels, cs):
                    continue

                if len(fs) > len(cs):
                    greater = fs
                    smaller = cs
                else:
                    smaller = cs
                    greater = fs

                if utils.containsAll(greater, smaller):
                    nonMinLabels.append(greater)

                    if len(greater) > len(smaller):
                        # update the DAG
                        hashcode = utils.get_hashcode(greater)
                        nodes = label_nodesMap.get(hashcode)
                        # log.trace("{}(HSDAGPruningEngine-processLabels) updating [nodes={}]", LoggerUtils.tab(), nodes);

                        if nodes is not None:
                            for nd in nodes:
                                if nd.status == "Open":
                                    nd.label = smaller  # relabel the node with smaller
                                    # log.trace("{}(HSDAGPruningEngine-processLabels) reSetLabel [node={}]", LoggerUtils.tab(), nd);
                                    addItemToLabelNodesMap(smaller, nd)  # add new label to the map

                                    delete = utils.diff(greater, smaller)
                                    for label in delete:
                                        child = nd.children.get(label)

                                        if child is not None:
                                            # incrementCounter(COUNTER_PRUNING);
                                            child.parents.remove(nd)
                                            nd.children.remove(label)
                                            cleanUpNodes(child)

        # remove the known non - minimal conflicts
        for label in nonMinLabels:
            nodeLabels.remove(label)

            hashcode = utils.get_hashcode(label)
            del label_nodesMap[hashcode]
            # labels.removeAll(nonMinLabels)
            # nonMinLabels.forEach(label_nodesMap::remove)

        # add new labels to the list of labels
        addNodeLabels(labels)
        # hsdag.addNodeLabels(labels)


def cleanUpNodes(node):
    hashcode = utils.get_hashcode(node.pathLabel)
    del nodes_lookup[hashcode]
    # log.debug("{}(HSDAGPruningEngine-cleanUpNodes) removed pathLabel from nodesLookup [pathLabel={}]", LoggerUtils.tab(), node.getPathLabel());

    if node.status == "Open":
        node.status = "Pruned"
        # incrementCounter(COUNTER_CLEANED_NODES);

        # log.debug("{}(HSDAGPruningEngine-cleanUpNodes) pruned [node={}]", LoggerUtils.tab(), node);

    # downward clean up
    for arcLabel in node.children.keys():
        child = node.children.get(arcLabel)
        if child is not None:
            cleanUpNodes(child)
