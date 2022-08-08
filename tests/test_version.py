import semver

from hume import __version__


class TestVersion:
    def test_version(self):
        semversion = semver.VersionInfo.parse(__version__)
        assert semversion.major == 0
        assert semversion.minor > 0
