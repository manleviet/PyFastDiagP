#!/usr/bin/env python
from algorithms import quickxplain
from common import utils
import logging

logging.basicConfig(level=logging.DEBUG)

counter_constructed_nodes = 0

maxNumberOfDiagnoses = -1
maxNumberOfConflicts = -1

nodeLabels = {}
pathLabels = {}

root = None
openNodes = []
label_nodesMap = {}

def getConflicts():
    return nodeLabels

def getDiagnoses():
    return pathLabels

def construct(B, C):
    # generate root if there is none
    if createRoot(B, C):
        createNodes()
    stopConstruction()

def createRoot(B, C):
    global root, openNodes

    hasRootLabel = true

    if not hasRoot():
        labels = quickxplain.quickXplain(C, B)

        if len(labels) == 0 or label == "No Conflict":
            hasRootLabel = false
        else:  # create root node
            label = selectLabel(labels)
            root = Node(None, None, B, C)
            #incrementCounter(COUNTER_CONSTRUCTED_NODES)

            openNodes.append(root)

            addNodeLabels(labels)  # to reuse labels
            addItemToLabelNodesMap(label, root)

            # log.debug("{}(HSTree-construct) Created root node [root={}]", LoggerUtils.tab(), root);
    return hasRootLabel

def stopConstruction():
    # log.debug("{}<<< return [conflicts={}]", LoggerUtils.tab(), getConflicts());
    # log.debug("{}<<< return [diagnoses={}]", LoggerUtils.tab(), getDiagnoses());

    # stop(TIMER_HS_CONSTRUCTION_SESSION);
    # stop(TIMER_PATH_LABEL, false);

    # if (log.isTraceEnabled()) {
    #     HSUtils.printInfo(root, getConflicts(), getDiagnoses());
    # }

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
                break;

        if (node.getStatus() == NodeStatus.Open) {
            expand(node);
        }

        System.gc();
        if (!node.isRoot()) {
            LoggerUtils.outdent();

def label(node):
    # Reusing labels - H(node) ∩ S = {}, then label node by S
    labels = getReusableLabels(node)

    # compute labels if there are none to reuse
    if len(labels) == 0:
        labels = computeLabel(node)

        processLabels(labels)

    if len(labels) > 0:
        label = selectLabel(labels)

        node.label = label
        addItemToLabelNodesMap(label, node)

        # log.debug("{}(HSTree-label) Node [node={}] has label [label={}]", LoggerUtils.tab(), node, label);
    else:  # found a path label
        foundAPathLabelAtNode(node);

        # stop(TIMER_PATH_LABEL);
        # start(TIMER_PATH_LABEL);

def expand(nodeToExpand):
    global counter_constructed_nodes, openNodes
    # log.debug("{}(HSTree-expand) Generating the children nodes of [node={}]", LoggerUtils.tab(), nodeToExpand);
    # LoggerUtils.indent();

    for arcLabel in nodeToExpand.label:
        B = nodeToExpand.B
        C = nodeToExpand.C

        node = Node(nodeToExpand, arcLabel, B, C)
        counter_constructed_nodes = counter_constructed_nodes + 1
        # incrementCounter(COUNTER_CONSTRUCTED_NODES);

        if not canPrune(node):
            openNodes.add(node);
            # log.debug("{}(HSTree-expand) Created [node={}]", LoggerUtils.tab(), node);

def shouldStopConstruction():
    # when the number of already identified diagnoses is greater than the limit, stop the computation
    condition1 = (maxNumberOfDiagnoses != -1 and maxNumberOfDiagnoses <= getDiagnoses().size())
    # OR when the number of already identified conflicts is greater than the limit, stop the computation
    condition2 = (maxNumberOfConflicts != -1 and maxNumberOfConflicts <= getConflicts().size())

    return condition1 or condition2

def addItemToLabelNodesMap(label, node):
    global label_nodesMap
    label_nodesMap[label].add(node)

def computeLabel(node):
    B = node.B
    C = node.C

    return quickxplain.quickXplain(C, B)

def addNodeLabels(labels):
    global nodeLabels
    for label in labels:
        nodeLabels.add(label)

def foundAPathLabelAtNode(node):
    node.status = "Checked"
    pathLabel = node.pathLabel.copy()

    addPathLabel(pathLabel)

def addPathLabel(pathLabel):
    global pathLabels
    pathLabels.add(pathLabel)

def selectLabel(labels):
    return labels.pop()

def hasNodesToExpand():
    return len(openNodes) > 0

def getNextNode():
    global openNodes
    return openNodes.pop()

def hasRoot():
    return root != None

class Node(object):
    generatedNodeId = -1

    def __init__(self, parent, arcLabel, B, C):
        generatedNodeId = generatedNodeId + 1
        self.id = generatedNodeId
        self.status = "Open"
        if parent == None:
            self.level = 0
            self.parents = None
            self.pathLabel = []
        else:
            self.level = parent.level + 1
            self.parents = [parent]
            parent.addChild(arcLabel, self)
            self.pathLabel = parent.pathLabel.copy()
        self.B = B
        self.C = C
        self.arcLabel = arcLabel
        self.label = None

        self.pathLabel.append(arcLabel)

        self.children = {}

    def isRoot():
        return self.parents == None

    def addParent(self, parent):
        if not isRoot():
            self.parents = [parent]

    def addChild(self, arcLabel, child):
        self.children[arcLabel] = child
        child.addParent(self)

    def create_parameter(self, arcLabel):
        C = self.C.copy()
        del C[arcLabel]

        B = self.B.copy()

        return B, C

    # def getLabel(self):
    #     self.label = quickXplain(self.C, self.B)

    def __str__(self):
        return "Node: " + str(self.id) + ", level= " + str(self.level) + ", status: " + self.status 
        + ", label= " + str(self.label) + ", B= " + str(self.B) + ", C= " + str(self.C) 
        + ", arcLabel= " + str(self.arcLabel) + ", pathLabels: " + str(self.pathLabel)

# Pruning engine
def skipNode(node):
    return node.status != "Open" || canPrune(node);

def canPrune(node):
    # 3.i - if n is checked, and n' is such that H(n) ⊆ H(n'), then close the node n'
    # n is a diagnosis
    for pathLabel in pathLabels:
        if node.pathLabel.containsAll(pathLabel):
            node.status = "Closed"
            # incrementCounter(COUNTER_CLOSE_1);

            # log.debug("{}(HSTreePruningEngine-canPrune_3i) Closed [node={}]", LoggerUtils.tab(), node);

            return true;

    # 3.ii - if n has been generated and node n' is such that H(n') = H(n), then close node n'
    for n in openNodes:
        if len(n.pathLabel) == len(node.pathLabel)
                and len(utils.diff(n.pathLabel, node.pathLabel)) == 0:
            node.status = "Closed"
            # incrementCounter(COUNTER_CLOSE_2);

            # log.debug("{}(HSTreePruningEngine-canPrune_3i) Closed [node={}]", LoggerUtils.tab(), node);

            return true;
    return false;

def getReusableLabels(node : Node):
    labels = []
    for label in nodeLabels:
        # H(node) ∩ S = {}
        if not hasIntersection(node.pathLabel, label)):
            labels.add(label);
            # incrementCounter(COUNTER_REUSE_LABELS);
            # log.debug("{}(HSTreePruningEngine-getReusableLabels) Reuse [label={}, node={}]", LoggerUtils.tab(), label, node);

    return labels;

def processLabels(labels):
    if len(labels) > 0:
        # stop(TIMER_NODE_LABEL);

        addNodeLabels(labels)
    # else:
        # stop TIMER_NODE_LABEL without saving the time
        # stop(TIMER_NODE_LABEL, false);