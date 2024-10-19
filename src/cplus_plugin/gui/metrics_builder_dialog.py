# -*- coding: utf-8 -*-
"""
Wizard for customizing custom activity metrics table.
"""

import os
import re
import typing

from qgis.core import (
    Qgis,
    QgsColorRamp,
    QgsFillSymbolLayer,
    QgsGradientColorRamp,
    QgsMapLayerProxyModel,
    QgsRasterLayer,
)
from qgis.gui import QgsGui, QgsMessageBar

from qgis.PyQt import QtCore, QtGui, QtWidgets

from qgis.PyQt.uic import loadUiType

from ..conf import Settings, settings_manager

from ..definitions.defaults import ICON_PATH, USER_DOCUMENTATION_SITE
from .metrics_builder_model import MetricColumnListItem, MetricColumnListModel
from ..models.base import Activity
from ..models.report import MetricColumn
from ..utils import FileUtils, log, generate_random_color, open_documentation, tr

WidgetUi, _ = loadUiType(
    os.path.join(os.path.dirname(__file__), "../ui/activity_metrics_builder_dialog.ui")
)


class ActivityMetricsBuilder(QtWidgets.QWizard, WidgetUi):
    """Wizard for customizing custom activity metrics table."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        QgsGui.enableAutoGeometryRestore(self)

        # Setup notification bars
        self._column_message_bar = QgsMessageBar()
        self.vl_column_notification.addWidget(self._column_message_bar)

        self._column_list_model = MetricColumnListModel()

        # Add the default area column
        area_metric_column = MetricColumn(
            "Area", tr("Area (Ha)"), "", auto_calculated=True
        )
        self._column_list_model.add_new_column(area_metric_column)

        # Initialize wizard
        ci_icon = FileUtils.get_icon("cplus_logo.svg")
        ci_pixmap = ci_icon.pixmap(64, 64)
        self.setPixmap(QtWidgets.QWizard.LogoPixmap, ci_pixmap)

        help_button = self.button(QtWidgets.QWizard.HelpButton)
        help_icon = FileUtils.get_icon("mActionHelpContents_green.svg")
        help_button.setIcon(help_icon)

        self.currentIdChanged.connect(self.on_page_id_changed)
        self.helpRequested.connect(self.on_help_requested)

        # Intro page
        banner = FileUtils.get_pixmap("metrics_illustration.svg")
        self.lbl_banner.setPixmap(banner)
        self.lbl_banner.setScaledContents(True)

        # Columns page
        add_icon = FileUtils.get_icon("symbologyAdd.svg")
        self.btn_add_column.setIcon(add_icon)
        self.btn_add_column.clicked.connect(self.on_add_column)

        remove_icon = FileUtils.get_icon("symbologyRemove.svg")
        self.btn_delete_column.setIcon(remove_icon)
        self.btn_delete_column.setEnabled(False)
        self.btn_delete_column.clicked.connect(self.on_remove_column)

        move_up_icon = FileUtils.get_icon("mActionArrowUp.svg")
        self.btn_column_up.setIcon(move_up_icon)
        self.btn_column_up.setEnabled(False)
        self.btn_column_up.clicked.connect(self.on_move_up_column)

        move_down_icon = FileUtils.get_icon("mActionArrowDown.svg")
        self.btn_column_down.setIcon(move_down_icon)
        self.btn_column_down.setEnabled(False)
        self.btn_column_down.clicked.connect(self.on_move_down_column)

        self.splitter.setStretchFactor(0, 25)
        self.splitter.setStretchFactor(1, 75)

        self.cbo_column_expression.setAllowEmptyFieldName(True)
        self.cbo_column_expression.setAllowEvalErrors(False)
        self.cbo_column_expression.setExpressionDialogTitle(
            tr("Column Expression Builder")
        )

        self.lst_columns.setModel(self._column_list_model)
        self.lst_columns.selectionModel().selectionChanged.connect(
            self.on_column_selection_changed
        )

        self.txt_column_name.textChanged.connect(self._on_column_header_changed)
        self.cbo_column_alignment.currentIndexChanged.connect(
            self._on_column_alignment_changed
        )
        self.cbo_column_expression.fieldChanged.connect(
            self._on_column_expression_changed
        )

    def on_page_id_changed(self, page_id: int):
        """Slot raised when the page ID changes.

        :param page_id: ID of the new page.
        :type page_id: int
        """
        # Update title
        window_title = (
            f"{tr('Activity Metrics Wizard')} - "
            f"{tr('Step')} {page_id + 1} {tr('of')} "
            f"{len(self.pageIds())!s}"
        )
        self.setWindowTitle(window_title)

    def on_help_requested(self):
        """Slot raised when the help button has been clicked.

        Opens the online help documentation in the user's browser.
        """
        open_documentation(USER_DOCUMENTATION_SITE)

    def push_column_message(
        self,
        message: str,
        level: Qgis.MessageLevel = Qgis.MessageLevel.Warning,
        clear_first: bool = False,
    ):
        """Push a message to the notification bar in the
        columns wizard page.

        :param message: Message to the show in the notification bar.
        :type message: str

        :param level: Severity of the message. Warning is the default.
        :type level: Qgis.MessageLevel

        :param clear_first: Clear any current messages in the notification
        bar, default is False.
        :type clear_first: bool
        """
        if clear_first:
            self._column_message_bar.clearWidgets()

        self._column_message_bar.pushMessage(message, level, 5)

    def on_add_column(self):
        """Slot raised to add a new column."""
        label_text = (
            f"{tr('Specify the name of the column.')}<br>"
            f"<i>{tr('Any special characters will be removed.')}"
            f"</i>"
        )
        column_name, ok = QtWidgets.QInputDialog.getText(
            self,
            tr("Set Column Name"),
            label_text,
        )

        if ok and column_name:
            # Remove special characters
            clean_column_name = re.sub("\W+", " ", column_name)
            column_exists = self._column_list_model.column_exists(clean_column_name)
            if column_exists:
                QtWidgets.QMessageBox.warning(
                    self,
                    tr("Duplicate Column Name"),
                    tr("There is an already existing column name"),
                )
                return

            self._column_list_model.add_new_column(clean_column_name)

            item = self._column_list_model.item_from_name(column_name)
            if item is None:
                return

            # Select item
            self.select_column(item.row())

    def on_remove_column(self):
        """Slot raised to remove the selected column."""
        selected_items = self.selected_column_items()
        for item in selected_items:
            self._column_list_model.remove_column(item.name)

    def on_move_up_column(self):
        """Slot raised to move the selected column one level up."""
        selected_items = self.selected_column_items()
        if len(selected_items) == 0:
            return

        item = selected_items[0]
        row = self._column_list_model.move_column_up(item.row())
        if row == -1:
            return

        # Maintain selection
        self.select_column(row)

    def on_move_down_column(self):
        """Slot raised to move the selected column one level down."""
        selected_items = self.selected_column_items()
        if len(selected_items) == 0:
            return

        item = selected_items[0]
        row = self._column_list_model.move_column_down(item.row())
        if row == -1:
            return

        # Maintain selection
        self.select_column(row)

    def select_column(self, row: int):
        """Select the column item in the specified row.

        :param row: Column item in the specified row number to be selected.
        :type row: int
        """
        index = self._column_list_model.index(row, 0)
        if not index.isValid():
            return

        selection_model = self.lst_columns.selectionModel()
        selection_model.select(index, QtCore.QItemSelectionModel.ClearAndSelect)

    def load_column_properties(self, column_item: MetricColumnListItem):
        """Load the properties of the column item in the corresponding
        UI controls.

        :param column_item: Column item whose properties are to be loaded.
        :type column_item: MetricColumnListItem
        """
        # Set column properties
        self.txt_column_name.blockSignals(True)
        self.txt_column_name.setText(column_item.header)
        self.txt_column_name.blockSignals(False)

        # Load alignment options
        self.cbo_column_alignment.blockSignals(True)

        self.cbo_column_alignment.clear()

        left_icon = FileUtils.get_icon("mIconAlignLeft.svg")
        self.cbo_column_alignment.addItem(left_icon, tr("Left"), QtCore.Qt.AlignLeft)

        right_icon = FileUtils.get_icon("mIconAlignRight.svg")
        self.cbo_column_alignment.addItem(right_icon, tr("Right"), QtCore.Qt.AlignRight)

        center_icon = FileUtils.get_icon("mIconAlignCenter.svg")
        self.cbo_column_alignment.addItem(
            center_icon, tr("Center"), QtCore.Qt.AlignHCenter
        )

        justify_icon = FileUtils.get_icon("mIconAlignJustify.svg")
        self.cbo_column_alignment.addItem(
            justify_icon, tr("Justify"), QtCore.Qt.AlignJustify
        )

        alignment_index = self.cbo_column_alignment.findData(column_item.alignment)
        if alignment_index != -1:
            self.cbo_column_alignment.setCurrentIndex(alignment_index)

        self.cbo_column_alignment.blockSignals(False)

        self.cbo_column_expression.blockSignals(True)

        if column_item.auto_calculated:
            self.cbo_column_expression.setEnabled(False)
        else:
            self.cbo_column_expression.setEnabled(True)

        self.cbo_column_expression.setExpression(column_item.expression)

        self.cbo_column_expression.blockSignals(False)

    def on_column_selection_changed(
        self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection
    ):
        """Slot raised when selection in the columns view has changed.

        :param selected: Current item selection.
        :type selected: QtCore.QItemSelection

        :param deselected: Previously selected items that have been
        deselected.
        :type deselected: QtCore.QItemSelection
        """
        self.btn_delete_column.setEnabled(True)
        self.btn_column_up.setEnabled(True)
        self.btn_column_down.setEnabled(True)

        selected_columns = self.selected_column_items()
        if len(selected_columns) != 1:
            self.btn_delete_column.setEnabled(False)
            self.btn_column_up.setEnabled(False)
            self.btn_column_down.setEnabled(False)

            self.clear_column_properties()

        else:
            # List view is set to single selection hence this
            # condition will be for one item selected.
            self.load_column_properties(selected_columns[0])

    def selected_column_items(self) -> typing.List[MetricColumnListItem]:
        """Returns the selected column items in the column list view.

        :returns: A collection of the selected column items.
        :rtype: list
        """
        selection_model = self.lst_columns.selectionModel()
        idxs = selection_model.selectedRows()

        return [self._column_list_model.item(idx.row()) for idx in idxs]

    def _on_column_header_changed(self, header: str):
        """Slot raised when the header label has changed.

        :param header: New header label text.
        :type header: str
        """
        self.save_column_properties()

    def _on_column_alignment_changed(self, index: int):
        """Slot raised when the column alignment has changed.

        :param index: Current index of the selected alignment.
        :type index: int
        """
        self.save_column_properties()

    def _on_column_expression_changed(self, field_name: str):
        """Slot raised when the column expression changes.

        :param field_name: The field that has changed.
        :type field_name: str
        """
        self.save_column_properties()

    def save_column_properties(self):
        """Updates the properties of the metric column based on the
        values of the UI controls for the current selected column
        item.
        """
        selected_columns = self.selected_column_items()
        if len(selected_columns) == 0:
            return

        current_column = selected_columns[0]
        current_column.header = self.txt_column_name.text()
        current_column.alignment = self.cbo_column_alignment.itemData(
            self.cbo_column_alignment.currentIndex()
        )
        current_column.expression = self.cbo_column_expression.currentText()