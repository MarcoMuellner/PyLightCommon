import pytest

from PyLightCommon.updater import updater
from PyLightCommon.updater import compareVersions

def testCompareVersions():
    assert compareVersions('v0.1.0','v1.0.0')
    assert compareVersions('v1.0.0','v1.0.1')
    assert compareVersions('v0.1.0','v0.2.0')
    assert compareVersions('v0.2.0', 'v0.2.1')

    assert not compareVersions('v1.0.0', 'v0.1.0')
    assert not compareVersions('v1.0.1', 'v1.0.0')
    assert not compareVersions('v0.2.0', 'v0.1.0')
    assert not compareVersions('v0.2.1', 'v0.2.0')