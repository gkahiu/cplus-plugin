# -*- coding: utf-8 -*-
"""
Unit tests for base data models.
"""

from unittest import TestCase

from model_data_for_testing import (
    get_activity,
    get_invalid_ncs_pathway,
    get_valid_ncs_pathway,
    VALID_NCS_UUID_STR,
)


class TestNcsPathway(TestCase):
    def setUp(self):
        self.ncs = get_valid_ncs_pathway()
        self.invalid_ncs = get_invalid_ncs_pathway()

    def test_to_map_layer(self):
        """Confirm that the map layer is not None."""
        map_layer = self.ncs.to_map_layer()
        self.assertIsNotNone(map_layer)

    def test_ncs_is_valid(self):
        """Confirm NCS item is valid."""
        self.assertTrue(self.ncs.is_valid())

    def test_ncs_is_not_valid(self):
        """Confirm NCS item is not valid."""
        self.assertFalse(self.invalid_ncs.is_valid())


class TestActivity(TestCase):
    def setUp(self):
        self.ncs = get_valid_ncs_pathway()
        self.invalid_ncs = get_invalid_ncs_pathway()

    def test_add_valid_ncs_pathway(self):
        """Assert a valid NCS pathway can be added to the model."""
        activity = get_activity()
        result = activity.add_ncs_pathway(self.ncs)
        self.assertTrue(result)

    def test_to_map_layer(self):
        """Confirm that the map layer is not None."""
        activity = get_activity()
        map_layer = activity.to_map_layer()
        self.assertIsNotNone(map_layer)

    def test_add_invalid_ncs_pathway(self):
        """Assert an invalid NCS pathway cannot be added to the activity."""
        activity = get_activity()
        result = activity.add_ncs_pathway(self.invalid_ncs)
        self.assertFalse(result)

    def test_contains_ncs_pathway(self):
        """Assert activity contains an NcsPathway object."""
        activity = get_activity()
        _ = activity.add_ncs_pathway(self.ncs)
        result = activity.contains_pathway(VALID_NCS_UUID_STR)
        self.assertTrue(result)

    def test_remove_ncs_pathway(self):
        """Assert removal of an NcsPathway object."""
        activity = get_activity()
        _ = activity.add_ncs_pathway(self.ncs)
        result = activity.remove_ncs_pathway(VALID_NCS_UUID_STR)
        self.assertTrue(result)

    def test_get_ncs_pathway_by_uuid(self):
        """Assert retrieval of an NcsPathway object using its UUID."""
        activity = get_activity()
        _ = activity.add_ncs_pathway(self.ncs)
        ncs = activity.pathway_by_uuid(VALID_NCS_UUID_STR)
        self.assertIsNotNone(ncs)
