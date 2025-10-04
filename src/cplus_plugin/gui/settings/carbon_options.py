# coding=utf-8

"""Plugin carbon settings."""

import os
import typing

import qgis.core

from qgis.gui import QgsFileWidget, QgsMessageBar, QgsOptionsPageWidget
from qgis.gui import QgsOptionsWidgetFactory
from qgis.PyQt import uic
from qgis.PyQt import QtCore
from qgis.PyQt.QtGui import (
    QIcon,
    QShowEvent,
    QPixmap,
)

from qgis.PyQt.QtWidgets import QButtonGroup, QWidget

from ...api.base import ApiRequestStatus
from ...api.carbon import (
    start_irrecoverable_carbon_download,
    get_downloader_task,
)

from ...conf import (
    settings_manager,
    Settings,
)
from ...definitions.constants import CPLUS_OPTIONS_KEY, CARBON_OPTIONS_KEY
from ...definitions.defaults import (
    OPTIONS_TITLE,
    CARBON_OPTIONS_TITLE,
    CARBON_SETTINGS_ICON_PATH,
)
from ...models.base import DataSourceType
from ...utils import FileUtils, tr


Ui_CarbonSettingsWidget, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "../../ui/carbon_settings.ui")
)


class CarbonSettingsWidget(QgsOptionsPageWidget, Ui_CarbonSettingsWidget):
    """Carbon settings widget."""

    def __init__(self, parent=None):
        QgsOptionsPageWidget.__init__(self, parent)
        self.setupUi(self)

        self.message_bar = QgsMessageBar(self)
        self.layout().insertWidget(0, self.message_bar)

        tif_file_filter = tr("GeoTIFF (*.tif *.tiff *.TIF *.TIFF)")

        # Irrecoverable carbon
        self.gb_ic_reference_layer.toggled.connect(
            self._on_irrecoverable_group_box_toggled
        )

        self._irrecoverable_group = QButtonGroup(self)
        self._irrecoverable_group.addButton(self.rb_local, DataSourceType.LOCAL.value)
        self._irrecoverable_group.addButton(self.rb_online, DataSourceType.ONLINE.value)
        self._irrecoverable_group.idToggled.connect(
            self._on_irrecoverable_button_group_toggled
        )

        self.fw_irrecoverable_carbon.setDialogTitle(
            tr("Select Irrecoverable Carbon Dataset")
        )
        self.fw_irrecoverable_carbon.setRelativeStorage(
            QgsFileWidget.RelativeStorage.Absolute
        )
        self.fw_irrecoverable_carbon.setStorageMode(QgsFileWidget.StorageMode.GetFile)
        self.fw_irrecoverable_carbon.setFilter(tif_file_filter)

        self.cbo_irrecoverable_carbon.layerChanged.connect(
            self._on_irrecoverable_carbon_layer_changed
        )
        self.cbo_irrecoverable_carbon.setFilters(
            qgis.core.QgsMapLayerProxyModel.Filter.RasterLayer
        )

        self.fw_save_online_file.setDialogTitle(
            tr("Specify Save Location of Irrecoverable Carbon Dataset")
        )
        self.fw_save_online_file.setRelativeStorage(
            QgsFileWidget.RelativeStorage.Absolute
        )
        self.fw_save_online_file.setStorageMode(QgsFileWidget.StorageMode.SaveFile)
        self.fw_save_online_file.setFilter(tif_file_filter)

        # self.lbl_url_tip.setPixmap(FileUtils.get_pixmap("info_green.svg"))
        # self.lbl_url_tip.setScaledContents(True)

        self.btn_ic_download.setIcon(FileUtils.get_icon("downloading_svg.svg"))
        self.btn_ic_download.clicked.connect(self.on_download_irrecoverable_carbon)

        # Use the task to get real time updates on the download progress
        self._irrecoverable_carbon_downloader = None
        self._configure_irrecoverable_carbon_downloader_updates()

        # Stored carbon
        self.fw_biomass.setDialogTitle(tr("Select Biomass Dataset"))
        self.fw_biomass.setRelativeStorage(QgsFileWidget.RelativeStorage.Absolute)
        self.fw_biomass.setStorageMode(QgsFileWidget.StorageMode.GetFile)
        self.fw_biomass.setFilter(tif_file_filter)

        self.cbo_biomass.layerChanged.connect(self._on_biomass_layer_changed)
        self.cbo_biomass.setFilters(qgis.core.QgsMapLayerProxyModel.Filter.RasterLayer)

    def apply(self) -> None:
        """This is called on OK click in the QGIS options panel."""
        self.save_settings()

    def save_settings(self) -> None:
        """Saves the settings."""
        # Irrecoverable carbon
        settings_manager.set_value(
            Settings.IRRECOVERABLE_CARBON_LOCAL_SOURCE,
            self.fw_irrecoverable_carbon.filePath(),
        )
        settings_manager.set_value(
            Settings.IRRECOVERABLE_CARBON_ONLINE_SOURCE, self.txt_ic_url.text()
        )
        settings_manager.set_value(
            Settings.IRRECOVERABLE_CARBON_ONLINE_LOCAL_PATH,
            self.fw_save_online_file.filePath(),
        )

        if self.rb_local.isChecked():
            settings_manager.set_value(
                Settings.IRRECOVERABLE_CARBON_SOURCE_TYPE, DataSourceType.LOCAL.value
            )
        elif self.rb_online.isChecked():
            settings_manager.set_value(
                Settings.IRRECOVERABLE_CARBON_SOURCE_TYPE, DataSourceType.ONLINE.value
            )

        settings_manager.set_value(
            Settings.IRRECOVERABLE_CARBON_ENABLED,
            self.gb_ic_reference_layer.isChecked(),
        )

        # Stored carbon
        settings_manager.set_value(
            Settings.STORED_CARBON_BIOMASS_PATH,
            self.fw_biomass.filePath(),
        )

    def load_settings(self):
        """Loads the settings and displays it in the UI."""
        # Irrecoverable carbon
        irrecoverable_carbon_enabled = settings_manager.get_value(
            Settings.IRRECOVERABLE_CARBON_ENABLED, default=False
        )
        if irrecoverable_carbon_enabled:
            self.gb_ic_reference_layer.setChecked(True)
        else:
            self.gb_ic_reference_layer.setChecked(False)

        # Local path
        self.fw_irrecoverable_carbon.setFilePath(
            settings_manager.get_value(
                Settings.IRRECOVERABLE_CARBON_LOCAL_SOURCE, default=""
            )
        )

        # Online config
        self.txt_ic_url.setText(
            settings_manager.get_value(
                Settings.IRRECOVERABLE_CARBON_ONLINE_SOURCE, default=""
            )
        )
        self.fw_save_online_file.setFilePath(
            settings_manager.get_value(
                Settings.IRRECOVERABLE_CARBON_ONLINE_LOCAL_PATH, default=""
            )
        )

        source_type_int = settings_manager.get_value(
            Settings.IRRECOVERABLE_CARBON_SOURCE_TYPE,
            default=DataSourceType.ONLINE.value,
            setting_type=int,
        )
        if source_type_int == DataSourceType.LOCAL.value:
            self.rb_local.setChecked(True)
            self.sw_irrecoverable_carbon.setCurrentIndex(0)
        elif source_type_int == DataSourceType.ONLINE.value:
            self.rb_online.setChecked(True)
            self.sw_irrecoverable_carbon.setCurrentIndex(1)

        self.validate_current_irrecoverable_data_source()

        self.reload_irrecoverable_carbon_download_status()

        # Stored carbon
        self.fw_biomass.setFilePath(
            settings_manager.get_value(Settings.STORED_CARBON_BIOMASS_PATH, default="")
        )

    def showEvent(self, event: QShowEvent) -> None:
        """Show event being called. This will display the plugin settings.
        The saved settings will be loaded.

        :param event: Event that has been triggered.
        :type event: QShowEvent
        """
        super().showEvent(event)
        self.load_settings()

    def reload_irrecoverable_carbon_download_status(self):
        """Fetch the latest download status of the irrecoverable carbon
        dataset from the online source if applicable.
        """
        status = settings_manager.get_value(
            Settings.IRRECOVERABLE_CARBON_ONLINE_DOWNLOAD_STATUS, None, int
        )
        if status is None:
            return

        # Set notification icon
        path = ""
        status_type = ApiRequestStatus.from_int(status)
        if status_type == ApiRequestStatus.COMPLETED:
            path = FileUtils.get_icon_path("mIconSuccess.svg")
        elif status_type == ApiRequestStatus.ERROR:
            path = FileUtils.get_icon_path("mIconWarning.svg")
        elif status_type == ApiRequestStatus.NOT_STARTED:
            path = FileUtils.get_icon_path("mIndicatorTemporal.svg")
        elif status_type == ApiRequestStatus.IN_PROGRESS:
            path = FileUtils.get_icon_path("progress-indicator.svg")
        elif status_type == ApiRequestStatus.CANCELED:
            path = FileUtils.get_icon_path("mTaskCancel.svg")

        self.lbl_download_status_tip.svg_path = path

        # Set notification description
        description = settings_manager.get_value(
            Settings.IRRECOVERABLE_CARBON_ONLINE_STATUS_DESCRIPTION, "", str
        )
        self.lbl_ic_download_status.setText(description)

    def _configure_irrecoverable_carbon_downloader_updates(self):
        """Get current downloader and connect the signals of the
        task in order to update the UI.
        """
        # Use the task to get real time updates on the download progress
        self._irrecoverable_carbon_downloader = get_downloader_task()

        if self._irrecoverable_carbon_downloader is None:
            return

        self._irrecoverable_carbon_downloader.started.connect(
            self.reload_irrecoverable_carbon_download_status
        )
        self._irrecoverable_carbon_downloader.canceled.connect(
            self.reload_irrecoverable_carbon_download_status
        )
        self._irrecoverable_carbon_downloader.completed.connect(
            self.reload_irrecoverable_carbon_download_status
        )
        self._irrecoverable_carbon_downloader.error_occurred.connect(
            self.reload_irrecoverable_carbon_download_status
        )

    def validate_irrecoverable_carbon_url(self) -> bool:
        """Checks if the irrecoverable data URL is valid.

        :returns: True if the link is valid else False if the
        URL is empty, points to a local file or if not
        well-formed.
        :rtype: bool
        """
        dataset_url = self.txt_ic_url.text()
        if not dataset_url:
            self.message_bar.pushWarning(
                tr("CPLUS - Irrecoverable carbon dataset"), tr("URL not defined")
            )
            return False

        url_checker = QtCore.QUrl(dataset_url, QtCore.QUrl.StrictMode)
        if url_checker.isLocalFile():
            self.message_bar.pushWarning(
                tr("CPLUS - Irrecoverable carbon dataset"),
                tr("Invalid URL referencing a local file"),
            )
            return False
        else:
            if not url_checker.isValid():
                self.message_bar.pushWarning(
                    tr("CPLUS - Irrecoverable carbon dataset"),
                    tr("URL is invalid."),
                )
                return False

        return True

    def on_download_irrecoverable_carbon(self):
        """Slot raised to check download link and initiate download
        process of the irrecoverable carbon data.

        The function will check and save the currently defined local
        save as path for the reference dataset as this will be required
        and fetched by the background download process.

        """
        valid_url = self.validate_irrecoverable_carbon_url()
        if not valid_url:
            tr_title = tr("CPLUS - Online irrecoverable carbon dataset")
            tr_msg = tr("URL for downloading irrecoverable carbon data is invalid.")
            self.message_bar.pushWarning(tr_title, tr_msg)

            return

        if not self.fw_save_online_file.filePath():
            tr_title = tr("CPLUS - Online irrecoverable carbon dataset")
            tr_msg = tr(
                "File path for saving downloaded irrecoverable "
                "carbon dataset not defined"
            )
            self.message_bar.pushWarning(tr_title, tr_msg)

            return

        # Check if the local path has been saved in settings or varies from
        # what already is saved in settings
        download_save_path = self.fw_save_online_file.filePath()
        if (
            settings_manager.get_value(
                Settings.IRRECOVERABLE_CARBON_ONLINE_LOCAL_PATH,
                default="",
                setting_type=str,
            )
            != download_save_path
        ):
            settings_manager.set_value(
                Settings.IRRECOVERABLE_CARBON_ONLINE_LOCAL_PATH, download_save_path
            )

        # (Re)initiate download
        start_irrecoverable_carbon_download()

        # Get downloader for UI updates
        self._configure_irrecoverable_carbon_downloader_updates()

    def validate_current_irrecoverable_data_source(self):
        """Checks if the currently selected irrecoverable data source
        is valid.
        """
        self.message_bar.clearWidgets()

        if self.rb_local.isChecked():
            local_path = self.fw_irrecoverable_carbon.filePath()
            if not os.path.exists(local_path):
                tr_msg = tr("CPLUS - Local irrecoverable carbon dataset not found")
                self.message_bar.pushWarning(tr_msg, local_path)
        elif self.rb_online.isChecked():
            _ = self.validate_irrecoverable_carbon_url()
            if not self.fw_save_online_file.filePath():
                tr_msg = tr("CPLUS - Online irrecoverable carbon dataset")
                self.message_bar.pushWarning(
                    tr_msg, tr("File path for saving dataset not defined")
                )

    def _on_irrecoverable_button_group_toggled(self, button_id: int, toggled: bool):
        """Slot raised when a button in the irrecoverable
        button group has been toggled.

        :param button_id: Button identifier.
        :type button_id: int

        :param toggled: True if the button is checked else False
        if unchecked.
        :type toggled: bool
        """
        if button_id == DataSourceType.LOCAL.value and toggled:
            self.sw_irrecoverable_carbon.setCurrentIndex(0)
        elif button_id == DataSourceType.ONLINE.value and toggled:
            self.sw_irrecoverable_carbon.setCurrentIndex(1)

    def _on_irrecoverable_group_box_toggled(self, toggled: bool):
        """Slot raised when the irrecoverable group box has
        been toggled.

        :param toggled: True if the button is checked else
        False if unchecked.
        :type toggled: bool
        """
        settings_manager.set_value(Settings.IRRECOVERABLE_CARBON_ENABLED, toggled)

    def _on_irrecoverable_carbon_layer_changed(self, layer: qgis.core.QgsMapLayer):
        """Sets the file path of the currently selected irrecoverable
        layer in the corresponding file input widget.

        :param layer: Currently selected layer.
        :type layer: QgsMapLayer
        """
        if layer is not None:
            self.fw_irrecoverable_carbon.setFilePath(layer.source())

    def _on_biomass_layer_changed(self, layer: qgis.core.QgsMapLayer):
        """Sets the file path of the currently selected biomass
        layer in the corresponding file input widget.

        :param layer: Currently selected layer.
        :type layer: QgsMapLayer
        """
        if layer is not None:
            self.fw_biomass.setFilePath(layer.source())


class CarbonOptionsFactory(QgsOptionsWidgetFactory):
    """Factory for defining CPLUS carbon settings."""

    def __init__(self) -> None:
        super().__init__()

        # Check version for API compatibility for managing items in
        # options tree view.
        version = qgis.core.Qgis.versionInt()
        if version >= 33200:
            self.setKey(CARBON_OPTIONS_KEY)

        self.setTitle(tr(CARBON_OPTIONS_TITLE))

    def icon(self) -> QIcon:
        """Returns the icon which will be used for the carbon settings item.

        :returns: An icon object which contains the provided custom icon
        :rtype: QIcon
        """
        return QIcon(CARBON_SETTINGS_ICON_PATH)

    def path(self) -> typing.List[str]:
        """
        Returns the path to place the widget page at.

        This instructs the registry to place the carbon options tab under the
        main CPLUS settings.

        :returns: Path name of the main CPLUS settings.
        :rtype: list
        """
        version = qgis.core.Qgis.versionInt()
        if version < 33200:
            return [OPTIONS_TITLE]

        return [CPLUS_OPTIONS_KEY]

    def createWidget(self, parent: QWidget) -> CarbonSettingsWidget:
        """Creates a widget for carbon settings.

        :param parent: Parent widget
        :type parent: QWidget

        :returns: Widget for defining carbon settings.
        :rtype: CarbonSettingsWidgetSettingsWidget
        """
        return CarbonSettingsWidget(parent)
