# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from sinarproject.customizations.testing import (
    SINARPROJECT_CUSTOMIZATIONS_FUNCTIONAL_TESTING,
)
from sinarproject.customizations.testing import (
    SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING,
)
from sinarproject.customizations.views.front_page import IFrontPage
from zope.component import getMultiAdapter

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_front_page_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="front-page"
        )
        self.assertTrue(IFrontPage.providedBy(view))

    def test_front_page_view_registered_for_all_content(self):
        # The front-page view is registered with for="*", so it is
        # resolvable for any content type, including the front-page
        # document itself.
        view = getMultiAdapter(
            (self.portal["front-page"], self.portal.REQUEST), name="front-page"
        )
        self.assertTrue(IFrontPage.providedBy(view))


class ViewsFunctionalTest(unittest.TestCase):

    layer = SINARPROJECT_CUSTOMIZATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
