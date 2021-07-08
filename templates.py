# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the specification of Graphol ontologies  #
#  Copyright (C) 2015 Daniele Pantaleone <danielepantaleone@me.com>      #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
#  #####################                          #####################  #
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Ingegneria Informatica, Automatica e Gestionale       #
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it  #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Daniele Pantaleone <pantaleone@dis.uniroma1.it>                  #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################



from PyQt5 import QtCore
from PyQt5 import QtWidgets

from eddy.core.datatypes.graphol import Item, Identity
from eddy.core.items.nodes.facet import FacetNode
from eddy.core.plugin import AbstractPlugin


class ItemSetPlugin(AbstractPlugin):
    """
    This plugin provides the Zoom control used to scale the MDI area.
    """

    def __init__(self, spec, session):
        """
        Initialize the plugin.
        :type spec: PluginSpec
        :type session: session
        """
        super().__init__(spec, session)
        self.actions = set()

    #############################################
    #   SLOTS
    #################################

    @QtCore.pyqtSlot()
    def doAddHigherarchy(self):
        """
        Update the state of the zoom controls according to the active diagram.
        """
        self.placeHigherarchy()

    @QtCore.pyqtSlot()
    def doAddAttributes(self):
        """
        Increase the main view zoom level.
        :type _: bool
        """
        self.placeAttributes()

    @QtCore.pyqtSlot()
    def doAddRelationship(self):
        """
        Decrese the main view zoom level.
        :type _: bool
        """
        self.placeRelationship()

    #############################################
    #   INTERFACE
    #################################

    def placeHigherarchy(self):
        """
        Adds a higherarchy to a concept node
        """
        diagram = self.session.mdi.activeDiagram()
        if diagram:
            concepts = diagram.selectedNodes(filter_on_nodes=lambda i: i.identity() is Identity.Concept)
            if len(concepts) == 0:
                return
            if len(concepts) > 1:
                print("Hai selezionato più di un concetto!!!")
                return
            for item in concepts:
                if item.identity() is Identity.Concept:
                    node = Item.FacetNode
                    diagram.addItem(node)
                    node.paint()
                    print("L'item è in posizione ({}, {})".format(item.pos().x(), item.pos().y()))

    def placeAttributes(self):
        """
        Refresh the status of the Zoom controls
        :type enabled: bool
        """
        print("att")

    def placeRelationship(self):
        """
        Set the zoom level according to the given value.
        :type level: float
        """
        print("rel")

    #############################################
    #   HOOKS
    #################################

    def dispose(self):
        """
        Executed whenever the plugin is going to be destroyed.
        """

        # UNINSTALL THE PALETTE DOCK WIDGET
        self.debug('Uninstalling zoom controls from "view" toolbar')
        for action in self.actions:
            self.session.widget('view_toolbar').removeAction(action)


    def start(self):
        """
        Perform initialization tasks for the plugin.
        """
        # INITIALIZE THE WIDGETS
        self.debug('test')

        self.addWidget(QtWidgets.QToolButton(
            text='H', clicked=self.doAddHigherarchy,
            objectName='button_higherarchy'))
        self.addWidget(QtWidgets.QToolButton(
            text='A', clicked=self.doAddAttributes,
            objectName='button_attributes'))
        self.addWidget(QtWidgets.QToolButton(
            text='R', clicked=self.doAddRelationship,
            objectName='button_relationship'))

        # CREATE VIEW TOOLBAR BUTTONS
        self.debug('Installing zoom controls in "view" toolbar')
        self.actions.add(self.session.widget('view_toolbar').addSeparator())
        self.actions.add(self.session.widget('view_toolbar').addWidget(self.widget('button_higherarchy')))
        self.actions.add(self.session.widget('view_toolbar').addWidget(self.widget('button_attributes')))
        self.actions.add(self.session.widget('view_toolbar').addWidget(self.widget('button_relationship')))
