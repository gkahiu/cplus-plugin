# -*- coding: utf-8 -*-
"""
    Definitions for all defaults settings
"""

import os
import json

from pathlib import Path

PILOT_AREA_EXTENT = {
    "type": "Polygon",
    "coordinates": [30.743498637, 32.069186664, -25.201606226, -23.960197335],
}

PLUGIN_MESSAGE_LOG_TAB = "qgis_cplus"
SCENARIO_LOG_FILE_NAME = "processing.log"

QGIS_MESSAGE_LEVEL_DICT = {
    0: "INFO",
    1: "WARNING",
    2: "CRITICAL",
    3: "SUCCESS",
    4: "NOLEVEL",
}

DEFAULT_CRS_ID = 4326

DOCUMENTATION_SITE = "https://conservationinternational.github.io/cplus-plugin"
USER_DOCUMENTATION_SITE = (
    "https://conservationinternational.github.io/cplus-plugin/user/guide"
)
ABOUT_DOCUMENTATION_SITE = (
    "https://conservationinternational.github.io/cplus-plugin/about/ci"
)
REPORT_DOCUMENTATION = "https://conservationinternational.github.io/cplus-plugin/user/guide/#report-generating"

BASE_PLUGIN_NAME = "CPLUS"
# Title in the QGIS settings. Leave it like this for now incase title needs to change
OPTIONS_TITLE = BASE_PLUGIN_NAME
GENERAL_OPTIONS_TITLE = "General"
REPORT_OPTIONS_TITLE = "Reporting"
LOG_OPTIONS_TITLE = "Logs"
ICON_PATH = ":/plugins/cplus_plugin/icon.svg"
REPORT_SETTINGS_ICON_PATH = str(
    os.path.normpath(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + "/icons/report_settings.svg"
    )
)
LOG_SETTINGS_ICON_PATH = str(
    os.path.normpath(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + "/icons/log_settings.svg"
    )
)
ICON_PDF = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    + "/icons/mActionSaveAsPDF.svg"
)
ICON_LAYOUT = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    + "/icons/mActionNewLayout.svg"
)
ICON_REPORT = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    + "/icons/mIconReport.svg"
)
ICON_HELP = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    + "/icons/mActionHelpContents_green.svg"
)

ADD_LAYER_ICON_PATH = ":/plugins/cplus_plugin/cplus_left_arrow.svg"
REMOVE_LAYER_ICON_PATH = ":/plugins/cplus_plugin/cplus_right_arrow.svg"

SCENARIO_OUTPUT_FILE_NAME = "cplus_scenario_output"
SCENARIO_OUTPUT_LAYER_NAME = "scenario_result"

PILOT_AREA_SCENARIO_SYMBOLOGY = {
    "Agroforestry": {"val": 1, "color": "#d80007"},
    "Alien Plant Removal": {"val": 2, "color": "#6f6f6f"},
    "Applied Nucleation": {"val": 3, "color": "#81c4ff"},
    "Assisted Natural Regeneration": {"val": 4, "color": "#e8ec18"},
    "Avoided Deforestation and Degradation": {"val": 5, "color": "#ff4c84"},
    "Avoided Wetland Conversion/Restoration": {"val": 6, "color": "#1f31d3"},
    "Bioproducts": {"val": 7, "color": "#67593f"},
    "Bush Thinning": {"val": 8, "color": "#30ff01"},
    "Direct Tree Seeding": {"val": 9, "color": "#bd6b70"},
    "Livestock Market Access": {"val": 10, "color": "#6c0009"},
    "Livestock Rangeland Management": {"val": 11, "color": "#ffa500"},
    "Natural Woodland Livestock Management": {"val": 12, "color": "#007018"},
    "Sustainable Crop Farming & Aquaponics": {"val": 13, "color": "#781a8b"},
}

ACTIVITY_COLOUR_RAMPS = {
    "Agroforestry": "Reds",
    "Alien Plant Removal": "Greys",
    "Alien_Plant_Removal": "Greys",
    "Applied Nucleation": "PuBu",
    "Applied_Nucleation": "PuBu",
    "Assisted Natural Regeneration": "YlOrRd",
    "Assisted_Natural_Regeneration": "YlOrRd",
    "Avoided Deforestation and Degradation": "RdPu",
    "Avoided_Deforestation_and_Degradation": "RdPu",
    "Avoided Wetland Conversion/Restoration": "Blues",
    "Avoided_Wetland_Conversion_Restoration": "Blues",
    "Bioproducts": "BrBG",
    "Bush Thinning": "BuGn",
    "Bush_Thinning": "BuGn",
    "Direct Tree Seeding": "PuRd",
    "Direct_Tree_Seeding": "PuRd",
    "Livestock Market Access": "Rocket",
    "Livestock_Market_Access": "Rocket",
    "Livestock Rangeland Management": "YlOrBr",
    "Livestock_Rangeland_Management": "YlOrBr",
    "Natural Woodland Livestock Management": "Greens",
    "Natural_Woodland_Livestock_Management": "Greens",
    "Sustainable Crop Farming & Aquaponics": "Purples",
    "Sustainable_Crop_Farming_&_Aquaponics": "Purples",
}

QGIS_GDAL_PROVIDER = "gdal"

DEFAULT_LOGO_PATH = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/icons/ci_logo.png"
)
CPLUS_LOGO_PATH = str(
    os.path.normpath(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + "/icons/cplus_logo.svg"
    )
)
CI_LOGO_PATH = str(
    os.path.normpath(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + "/icons/ci_logo.svg"
    )
)

# Default template file name
SCENARIO_ANALYSIS_TEMPLATE_NAME = "scenario_analysis_default.qpt"
SCENARIO_ANALYSIS_METRICS_TEMPLATE_NAME = "scenario_analysis_metrics.qpt"
SCENARIO_COMPARISON_TEMPLATE_NAME = "scenario_comparison.qpt"

# Minimum sizes (in mm) for repeat items in the template
MINIMUM_ITEM_WIDTH = 100
MINIMUM_ITEM_HEIGHT = 100

# Report font
REPORT_FONT_NAME = "Proxima Nova"

# Report colours
REPORT_COLOR_TREEFOG = "#bad636"
REPORT_COLOR_RAINFOREST = "#357d57"

# Activity character limits
MAX_ACTIVITY_NAME_LENGTH = 50
MAX_ACTIVITY_DESCRIPTION_LENGTH = 225

# IDs for the given tables in the report template
ACTIVITY_AREA_TABLE_ID = "activity_area_table"
PRIORITY_GROUP_WEIGHT_TABLE_ID = "assigned_weights_table"
AREA_COMPARISON_TABLE_ID = "comparison_table"

# IDs for items in the metrics report template
METRICS_HEADER_BACKGROUND = "metrics_header_background"
METRICS_FOOTER_BACKGROUND = "metrics_footer_background"
METRICS_TABLE_HEADER = "metrics_table_header"
METRICS_LOGO = "metrics_ci_logo"
METRICS_PAGE_NUMBER = "metrics_page_number"
METRICS_ACCREDITATION = "metrics_accreditation_text"

ONLINE_DEFAULT_PREFIX = "cplus://"


# Initializing the plugin default data as found in the data directory
priority_layer_path = (
    Path(__file__).parent.parent.resolve()
    / "data"
    / "default"
    / "priority_weighting_layers.json"
)

with priority_layer_path.open("r") as fh:
    priority_layers_dict = json.load(fh)
PRIORITY_LAYERS = priority_layers_dict["layers"]


PRIORITY_GROUPS = [
    {
        "uuid": "dcfb3214-4877-441c-b3ef-8228ab6dfad3",
        "name": "Biodiversity",
        "description": "Placeholder text for biodiversity",
    },
    {
        "uuid": "21a30a80-eb49-4c5e-aff6-558123688e09",
        "name": "Climate",
        "description": "Placeholder text for climate",
    },
    {
        "uuid": "3a66c845-2f9b-482c-b9a9-bcfca8395ad5",
        "name": "Finance",
        "description": "Placeholder text for finance",
    },
]

DEFAULT_REPORT_DISCLAIMER = (
    "The boundaries, names, and designations "
    "used in this report do not imply official "
    "endorsement or acceptance by Conservation "
    "International Foundation, or its partner "
    "organizations and contributors."
)
DEFAULT_REPORT_LICENSE = (
    "Creative Commons Attribution 4.0 International " "License (CC BY 4.0)"
)
BASE_API_URL = "https://stage.cplus.earth/api/v1"
IRRECOVERABLE_CARBON_API_URL = f"{BASE_API_URL}/reference_layer/carbon_calculation/"

DEFAULT_BASE_COMPARISON_REPORT_NAME = "Scenario Comparison Report"
MAXIMUM_COMPARISON_REPORTS = 10

NPV_EXPRESSION_DESCRIPTION = (
    "Calculates the financial NPV of the current "
    "activity. This returns the equivalent of the "
    "area of the current activity (in hectares) "
    "and multiplies it by the NPV rate (US$/ha) "
    "for each pathway that constitutes the activity. "
    "The NPV pathways are those defined via the NPV PWL "
    "Manager.<br><b>NOTE: If the NPV is not defined "
    "then the function will return -1.0.</b>"
)

PWL_IMPACT_EXPRESSION_DESCRIPTION = (
    "Calculates the impact of the "
    "current activity by multiplying "
    "the area of the NCS pathways (in hectares) of "
    "the current activity by a user-defined number "
    "of jobs created per hectare. The area of the NCS "
    "pathways in the activity will be automatically "
    "populated during the computation."
)

MEAN_BASED_IRRECOVERABLE_CARBON_EXPRESSION_DESCRIPTION = (
    "Calculates the total irrecoverable carbon (tons C) of "
    "protect NCS pathways in an activity using the mean "
    "reference irrecoverable carbon dataset. This dataset "
    "needs to be defined in the CPLUS settings for this "
    "expression to be evaluated.<br><b>NOTE: A value of -1.0 "
    "will be returned if an error is encountered, or 0.0 if "
    "there are no protect NCS pathways in the activity or "
    "no overlapping pixels with the reference layer in the "
    "area of interest.</b>"
)
