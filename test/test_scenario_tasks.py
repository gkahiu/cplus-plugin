# coding=utf-8
"""Tests for the plugin processing tasks

"""

import unittest

import os
import uuid
import processing
import datetime

from processing.core.Processing import Processing

from qgis.core import Qgis, QgsRasterLayer, QgsVectorLayer, QgsWkbTypes

from cplus_plugin.conf import settings_manager, Settings

from cplus_plugin.tasks import ScenarioAnalysisTask
from cplus_plugin.models.base import Scenario, NcsPathway, Activity


class ScenarioAnalysisTaskTest(unittest.TestCase):
    def setUp(self):
        Processing.initialize()

    def test_scenario_pathways_weighting(self):
        """Test the weighting of NCS pathways"""
        pathway_layer_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "pathways", "layers"
        )

        pathway_layer_path = os.path.join(pathway_layer_directory, "test_pathway_1.tif")

        priority_layers_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "priority", "layers"
        )

        priority_layer_path_1 = os.path.join(
            priority_layers_directory, "test_priority_1.tif"
        )

        test_priority_group = {
            "uuid": "a4f76e6c-9f83-4a9c-b700-fb1ae04860a4",
            "name": "test_priority_group",
            "description": "test_priority_group_description",
            "value": 1,
        }

        priority_layer_1 = {
            "uuid": "c931282f-db2d-4644-9786-6720b3ab206a",
            "name": "test_priority_layer",
            "description": "test_priority_layer_description",
            "selected": False,
            "path": priority_layer_path_1,
            "groups": [test_priority_group],
        }

        settings_manager.save_priority_group(test_priority_group)
        settings_manager.save_priority_layer(priority_layer_1)

        test_pathway = NcsPathway(
            uuid=uuid.uuid4(),
            name="test_pathway",
            description="test_description",
            path=pathway_layer_path,
            priority_layers=[],
        )

        test_layer = QgsRasterLayer(test_pathway.path, test_pathway.name)

        test_extent = test_layer.extent()

        test_activity = Activity(
            uuid=uuid.uuid4(),
            name="test_activity",
            description="test_description",
            pathways=[test_pathway],
        )

        scenario = Scenario(
            uuid=uuid.uuid4(),
            name="Scenario",
            description="Scenario description",
            activities=[test_activity],
            extent=test_extent,
            priority_layer_groups=[],
        )

        analysis_task = ScenarioAnalysisTask(
            "test_scenario_pathways_weighting",
            "test_scenario_pathways_weighting_description",
            [test_activity],
            [],
            test_layer.extent(),
            scenario,
        )

        extent_string = (
            f"{test_extent.xMinimum()},{test_extent.xMaximum()},"
            f"{test_extent.yMinimum()},{test_extent.yMaximum()}"
            f" [{test_layer.crs().authid()}]"
        )

        base_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "pathways",
        )

        scenario_directory = os.path.join(
            f"{base_dir}",
            f'scenario_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
            f"_{str(uuid.uuid4())[:4]}",
        )

        analysis_task.scenario_directory = scenario_directory

        settings_manager.set_value(Settings.BASE_DIR, base_dir)
        settings_manager.set_value(Settings.PATHWAY_SUITABILITY_INDEX, 0.5)

        past_stat = test_layer.dataProvider().bandStatistics(1)

        self.assertEqual(past_stat.minimumValue, 1.0)
        self.assertEqual(past_stat.maximumValue, 10.0)

        results = analysis_task.run_pathways_weighting(
            [test_activity],
            [test_priority_group],
            extent_string,
            temporary_output=True,
        )

        self.assertTrue(results)

        result_layer = QgsRasterLayer(test_pathway.path, test_pathway.name)

        stat = result_layer.dataProvider().bandStatistics(1)

        self.assertEqual(stat.minimumValue, 0.5)
        self.assertEqual(stat.maximumValue, 5.0)

    def test_scenario_activities_creation(self):
        pathway_layer_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "pathways", "layers"
        )

        pathway_layer_path_1 = os.path.join(
            pathway_layer_directory, "test_pathway_1.tif"
        )

        first_test_pathway = NcsPathway(
            uuid=uuid.uuid4(),
            name="first_test_pathway",
            description="first_test_description",
            path=pathway_layer_path_1,
        )

        pathway_layer_path_2 = os.path.join(
            pathway_layer_directory, "test_pathway_2.tif"
        )

        second_test_pathway = NcsPathway(
            uuid=uuid.uuid4(),
            name="second_test_pathway",
            description="second_test_description",
            path=pathway_layer_path_2,
        )

        first_test_layer = QgsRasterLayer(
            first_test_pathway.path, first_test_pathway.name
        )
        second_test_layer = QgsRasterLayer(
            second_test_pathway.path, second_test_pathway.name
        )

        test_extent = first_test_layer.extent()

        test_activity = Activity(
            uuid=uuid.uuid4(),
            name="test_activity",
            description="test_description",
            pathways=[first_test_pathway, second_test_pathway],
        )

        scenario = Scenario(
            uuid=uuid.uuid4(),
            name="Scenario",
            description="Scenario description",
            activities=[test_activity],
            extent=test_extent,
            priority_layer_groups=[],
        )

        analysis_task = ScenarioAnalysisTask(
            "test_scenario_activities_creation",
            "test_scenario_activities_creation_description",
            [test_activity],
            [],
            test_extent,
            scenario,
        )

        extent_string = (
            f"{test_extent.xMinimum()},{test_extent.xMaximum()},"
            f"{test_extent.yMinimum()},{test_extent.yMaximum()}"
            f" [{first_test_layer.crs().authid()}]"
        )

        base_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "pathways",
        )

        scenario_directory = os.path.join(
            f"{base_dir}",
            f'scenario_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
            f"_{str(uuid.uuid4())[:4]}",
        )

        analysis_task.scenario_directory = scenario_directory

        settings_manager.set_value(Settings.BASE_DIR, base_dir)
        settings_manager.set_value(Settings.PATHWAY_SUITABILITY_INDEX, 1.0)

        first_layer_stat = first_test_layer.dataProvider().bandStatistics(1)
        second_layer_stat = second_test_layer.dataProvider().bandStatistics(1)

        self.assertEqual(first_layer_stat.minimumValue, 1.0)
        self.assertEqual(first_layer_stat.maximumValue, 10.0)

        self.assertEqual(second_layer_stat.minimumValue, 7.0)
        self.assertEqual(second_layer_stat.maximumValue, 10.0)

        results = analysis_task.run_activities_analysis(
            [test_activity],
            extent_string,
            temporary_output=True,
        )

        self.assertTrue(results)

        result_layer = QgsRasterLayer(test_activity.path, test_activity.name)

        stat = result_layer.dataProvider().bandStatistics(1)

        self.assertEqual(stat.minimumValue, 1.0)
        self.assertEqual(stat.maximumValue, 19.0)

    def test_scenario_activities_masking(self):
        activities_layer_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "activities", "layers"
        )

        mask_layers_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "mask", "layers"
        )

        activity_layer_path_1 = os.path.join(
            activities_layer_directory, "test_activity_1.tif"
        )
        mask_layer_path_1 = os.path.join(mask_layers_directory, "test_mask_1.shp")

        test_activity = Activity(
            uuid=uuid.uuid4(),
            name="test_activity",
            description="test_description",
            pathways=[],
            path=activity_layer_path_1,
            mask_paths=[mask_layer_path_1],
        )

        settings_manager.save_activity(test_activity)

        activity_layer = QgsRasterLayer(test_activity.path, test_activity.name)

        test_extent = activity_layer.extent()

        scenario = Scenario(
            uuid=uuid.uuid4(),
            name="Scenario",
            description="Scenario description",
            activities=[test_activity],
            extent=test_extent,
            priority_layer_groups=[],
        )

        analysis_task = ScenarioAnalysisTask(
            "test_scenario_activities_masking",
            "test_scenario_activities_masking_description",
            [test_activity],
            [],
            test_extent,
            scenario,
        )

        extent_string = (
            f"{test_extent.xMinimum()},{test_extent.xMaximum()},"
            f"{test_extent.yMinimum()},{test_extent.yMaximum()}"
            f" [{activity_layer.crs().authid()}]"
        )

        base_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data",
            "activities",
        )

        scenario_directory = os.path.join(
            f"{base_dir}",
            f'scenario_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
            f"_{str(uuid.uuid4())[:4]}",
        )

        analysis_task.scenario_directory = scenario_directory

        settings_manager.set_value(Settings.BASE_DIR, base_dir)

        # Before masking, check if the activity layer stats are correct
        activity_layer = QgsRasterLayer(test_activity.path, test_activity.name)
        first_layer_stat = activity_layer.dataProvider().bandStatistics(1)

        self.assertEqual(first_layer_stat.minimumValue, 1.0)
        self.assertEqual(first_layer_stat.maximumValue, 19.0)

        results = analysis_task.run_internal_activities_masking(
            [test_activity], extent_string, temporary_output=True
        )

        self.assertTrue(results)

        self.assertIsInstance(results, bool)
        self.assertTrue(results)

        self.assertIsNotNone(test_activity.path)

        result_layer = QgsRasterLayer(test_activity.path, test_activity.name)

        result_stat = result_layer.dataProvider().bandStatistics(1)
        self.assertEqual(result_stat.minimumValue, 1.0)
        self.assertEqual(result_stat.maximumValue, 18.0)

        self.assertTrue(result_layer.isValid())

    def tearDown(self):
        pass
