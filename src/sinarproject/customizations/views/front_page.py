# -*- coding: utf-8 -*-

# from sinarproject.customizations import _
from Products.Five.browser import BrowserView
from plone import api
from zope.interface import implementer
from zope.interface import Interface
from datetime import datetime

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFrontPage(Interface):
    """Marker Interface for IFrontPage"""


@implementer(IFrontPage)
class FrontPage(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('front_page.pt')

    update_types = ["pressstatement", "newsmedia", "updates"]

    def __call__(self):
        # Implement your own actions:
        return self.index()

    def updates(self):

        items = api.content.find(portal_type='Resource',
                                 sort_on='effective',
                                 sort_order='descending',
                                 )

        updates = [item for item in items if item.resource_type in
                   self.update_types]

        return updates[:3]

    def events(self):

        items = api.content.find(portal_type='Activity',
                                 start={'query': datetime.now(), 'range': 'min'},
                                 sort_on='start',
                                 sort_order='ascending',
                                 sort_limit=3,
                                 )[:3]
        return items
