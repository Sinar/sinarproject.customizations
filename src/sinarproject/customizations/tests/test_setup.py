# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sinarproject.customizations.testing import (  # noqa: E501
    SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING,
)

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that sinarproject.customizations is properly installed."""

    layer = SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if sinarproject.customizations is installed."""
        self.assertTrue(
            self.installer.is_product_installed("sinarproject.customizations")
        )

    def test_browserlayer(self):
        """Test that ISinarprojectCustomizationsLayer is registered."""
        from plone.browserlayer import utils
        from sinarproject.customizations.interfaces import (
            ISinarprojectCustomizationsLayer,
        )

        self.assertIn(ISinarprojectCustomizationsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("sinarproject.customizations")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if sinarproject.customizations is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("sinarproject.customizations")
        )

    def test_browserlayer_removed(self):
        """Test that ISinarprojectCustomizationsLayer is removed."""
        from plone.browserlayer import utils
        from sinarproject.customizations.interfaces import (
            ISinarprojectCustomizationsLayer,
        )

        self.assertNotIn(ISinarprojectCustomizationsLayer, utils.registered_layers())
