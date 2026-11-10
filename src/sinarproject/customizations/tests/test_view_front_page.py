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

    def test_front_page_view_hides_byline(self):
        # The front-page view template should not show the document byline
        # (#section-byline), rendered by the plone.belowcontenttitle
        # viewlet manager in the main template.
        doc = self.portal["front-page"]
        request = self.portal.REQUEST
        view = getMultiAdapter((doc, request), name="front-page")
        # ZPublisher sets request['PUBLISHED'] to the view before calling it.
        request["PUBLISHED"] = view
        result = view()
        self.assertNotIn("section-byline", result)

    def test_byline_still_shown_for_other_views(self):
        # Only the front-page view suppresses the byline; other views of
        # the same document keep it.
        doc = self.portal["front-page"]
        request = self.portal.REQUEST
        other_view = getMultiAdapter((doc, request), name="view")
        request["PUBLISHED"] = other_view
        result = other_view()
        self.assertIn("section-byline", result)


class ViewsFunctionalTest(unittest.TestCase):

    layer = SINARPROJECT_CUSTOMIZATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
