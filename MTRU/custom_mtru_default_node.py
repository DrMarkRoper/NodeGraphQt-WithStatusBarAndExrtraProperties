#!/usr/bin/python
from Qt import QtCore, QtGui

from NodeGraphQt import BaseNode
from NodeGraphQt.constants import (
    NodeEnum
)

def draw_triangle_port(painter, rect, info):
    """
    Custom paint function for drawing a Triangle shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))

    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


def draw_square_port(painter, rect, info):
    """
    Custom paint function for drawing a Square shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    # mouse over port color.
    if info['hovered']:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35, 255)
    # port connected color.
    elif info['connected']:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info['color'])
        border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()





class CustomMTRUDefaultNode(BaseNode):
    """
    MTRU default node with custom shaped ports.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.custom.ports'

    # set the initial default node name.
    NODE_NAME = 'node'

    def __init__(self):
        super(CustomMTRUDefaultNode, self).__init__()
        # No default input/outputs
        # create input and output port.
        # self.add_input('in', color=(200, 10, 0))
        # self.add_output('default')
        # self.add_output('square', painter_func=draw_square_port)
        # self.add_output('triangle', painter_func=draw_triangle_port)
        self.status = 0
        self.view._text_item.set_locked(True)
        self.model.text_color = (238, 238, 238)
        self.model.color = (68, 68, 68)

    # def add_output(self, connector_name):
    #     return super(CustomMTRUDefaultNode, self).add_output(connector_name, painter_func=draw_square_circle)

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        self.status = new_status
        if new_status == NodeEnum.STATUS_VALUE_PENDING:
            self.view.status_color = NodeEnum.STATUS_COLOR_PENDING.value
        elif new_status == NodeEnum.STATUS_VALUE_RUNNING:
            self.view.status_color = NodeEnum.STATUS_COLOR_RUNNING.value
        elif new_status == NodeEnum.STATUS_VALUE_DONE:
            self.view.status_color = NodeEnum.STATUS_COLOR_DONE.value
        elif new_status == NodeEnum.STATUS_VALUE_ERROR:
            self.view.status_color = NodeEnum.STATUS_COLOR_ERROR.value
        elif new_status == NodeEnum.STATUS_VALUE_WARNING:
            self.view.status_color = NodeEnum.STATUS_COLOR_WARNING.value
        else:
            self.view.status_color = NodeEnum.STATUS_COLOR_PENDING.value

    def compute(self, graph):
        self.view.status_display_mode = NodeEnum.STATUS_DISPLAY_MODE_BLOCKS
        self.view.status_block_count = 5
        self.view.status_blocks = []
        #self.view.status_percent = 0
        self.set_status(NodeEnum.STATUS_VALUE_RUNNING)
        print('Clicked on node: {}'.format(self.name()))
        print('Node Type Id: {}'.format(str(self.get_property(name='Node Type Id'))))
        print('Node Status: {}'.format(str(self.get_status())))
        input_connections = self.connected_input_nodes()
        for port, nodes in input_connections.items():
            print('Connector: {}'.format(port.name()))
            for input_node in nodes:
                input_node.compute(graph)
        self.set_status(NodeEnum.STATUS_VALUE_DONE)
        #self.view.status_percent = 50
        self.view.status_blocks = [NodeEnum.STATUS_COLOR_WARNING.value, NodeEnum.STATUS_COLOR_ERROR.value, NodeEnum.STATUS_COLOR_DONE.value, NodeEnum.STATUS_COLOR_DONE.value, NodeEnum.STATUS_COLOR_DONE.value, NodeEnum.STATUS_COLOR_ERROR.value]
