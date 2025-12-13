# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import sinarproject.customizations


class SinarprojectCustomizationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=sinarproject.customizations)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "sinarproject.customizations:default")


SINARPROJECT_CUSTOMIZATIONS_FIXTURE = SinarprojectCustomizationsLayer()


SINARPROJECT_CUSTOMIZATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SINARPROJECT_CUSTOMIZATIONS_FIXTURE,),
    name="SinarprojectCustomizationsLayer:IntegrationTesting",
)


SINARPROJECT_CUSTOMIZATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SINARPROJECT_CUSTOMIZATIONS_FIXTURE,),
    name="SinarprojectCustomizationsLayer:FunctionalTesting",
)
