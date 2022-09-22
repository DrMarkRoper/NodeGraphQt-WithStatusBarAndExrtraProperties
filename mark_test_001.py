#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget,
    constants,
)


from MTRU import custom_mtru_default_node

sys.path.append('../../gui_testbed')
import test_database

def mtru_create_node(graph, node_type_id):
    node_type_details = test_database.get_node_type(node_type_id)
    new_node = graph.create_node(
        'nodes.custom.ports.CustomMTRUDefaultNode', 
        name=node_type_details['Name'])
    node_type_connectors = test_database.list_node_types_connectors_by_node_type_id(node_type_id)
    for connector in node_type_connectors:
        connector_name = connector['ConnectionTypeName']
        if connector['Instance'] > 1: 
            connector_name = connector_name + ' (' + str(connector['Instance']) + ')'
        if connector['InputOutputType'] == 1 or connector['InputOutputType'] == 3:
            new_port = new_node.add_input(connector_name)
            new_port.create_property('connector_type', str(connector['ConnectionTypeId']))
            #new_port.set_connector_type(connector['ConnectionTypeId'])
        if connector['InputOutputType'] == 2 or connector['InputOutputType'] == 3:
            new_port = new_node.add_output(connector_name)
            new_port.create_property('connector_type', str(connector['ConnectionTypeId']))
            #new_port.set_connector_type(connector['ConnectionTypeId'])
    
    # Node type details
    new_node.create_property(name='Node Type Id', value=node_type_details['NodeTypeId'], widget_type=constants.NODE_PROP_QLABEL, tab='Node Type Details')
    new_node.create_property(name='Name', value=node_type_details['Name'], widget_type=constants.NODE_PROP_QLABEL, tab='Node Type Details')
    new_node.create_property(name='Description', value=node_type_details['Description'], widget_type=constants.NODE_PROP_QLABEL, tab='Node Type Details')
    new_node.create_property(name='Default Command', value=node_type_details['CommandString'], widget_type=constants.NODE_PROP_QLABEL, tab='Node Type Details')

    node_type_attributes = test_database.list_node_types_attributes_details_by_node_type_id(node_type_id)
    for attribute in node_type_attributes:
        if attribute['DisplayMode'] == 0:
            new_node.create_property(name=attribute['Name'], value=attribute['DefaultValue'], widget_type=constants.NODE_PROP, tab='Node Attributes')
        elif attribute['ReadonlyMode'] == 0:
            new_node.create_property(name=attribute['Name'], value=attribute['DefaultValue'], widget_type=constants.NODE_PROP_QLABEL, tab='Node Attributes')
        elif attribute['ValueType'] == 1:
            new_node.create_property(name=attribute['Name'], value=0, widget_type=constants.NODE_PROP_INT, tab='Node Attributes')
        # elif attribute['ValueType'] == 2:
        #     print(attribute['name'])
        #     new_node.create_property(name=attribute['Name'], value=attribute['DefaultValue'], widget_type=constants.NODE_PROP_FLOAT, tab='Node Attributes')
        else:
            new_node.create_property(name=attribute['Name'], value=attribute['DefaultValue'], widget_type=constants.NODE_PROP_QTEXTEDIT, tab='Node Attributes')

        # TODO: allowed values dropdown

def node_compute(graph, node):
    node.compute(graph)

def test_func(graph, node):
    print('ToDo: node menu item')

if __name__ == '__main__':
    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication([])

    # create graph controller.
    graph = NodeGraph()

    # registered example nodes.
    graph.register_nodes([
        custom_mtru_default_node.CustomMTRUDefaultNode,
    ])

    # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.resize(1100, 800)
    graph_widget.show()

    # auto layout nodes.
    graph.auto_layout_nodes()

    # fit node selection to the viewer.
    graph.fit_to_selection()


    # create a node properties bin widget.
    properties_bin = PropertiesBinWidget(node_graph=graph)
    properties_bin.setWindowFlags(QtCore.Qt.Tool)

    # example show the node properties bin widget when a node is double clicked.
    def display_properties_bin(node):
        properties_bin.hide()
        properties_bin.show()

    # wire function to "node_double_clicked" signal.
    graph.node_double_clicked.connect(display_properties_bin)
    #graph.node_selected.connect(display_properties_bin)
 
    # Build the create node menu
    graph_menu = graph.get_context_menu('graph')
    edit_menu = graph_menu.add_menu('&Create Node')
    # Need to know which pipeline type we are on
    pipeline_type_id = 2 #'Process Timer'
    # Load in Categories and node types for this pipeline_type
    node_types = test_database.list_node_types_categories_by_pipeline_type_id(pipeline_type_id) # -> [PipelineTypeCategoryName], [NodeTypeName], [NodeTypeId]
    current_cat = ""
    for node_type in node_types:
        if current_cat != node_type['PipelineTypeCategoryName']:
            cat_menu = edit_menu.add_menu(node_type['PipelineTypeCategoryName'])
            current_cat = node_type['PipelineTypeCategoryName']
        cat_menu.add_command(node_type['NodeTypeName'], lambda x, y=node_type['NodeTypeId']: mtru_create_node(x, y))

    nodes_menu = graph.get_context_menu('nodes')
    nodes_menu.add_command('Compute', func=node_compute, node_type='nodes.custom.ports.CustomMTRUDefaultNode')
    nodes_menu.add_command('Open Folder', func=test_func, node_type='nodes.custom.ports.CustomMTRUDefaultNode')
    nodes_menu.add_separator()
    nodes_menu.add_command('Duplicate Node', func=test_func, node_type='nodes.custom.ports.CustomMTRUDefaultNode')
    nodes_menu.add_command('Remove Node', func=test_func, node_type='nodes.custom.ports.CustomMTRUDefaultNode')
    nodes_menu.add_separator()
    nodes_menu.add_command('Delete Data', func=test_func, node_type='nodes.custom.ports.CustomMTRUDefaultNode')


    app.exec_()

