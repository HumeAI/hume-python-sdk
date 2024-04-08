import semver

from hume import __version__


class TestVersion:
    def test_version(self) -> None:
        version = semver.VersionInfo.parse(__version__)
        assert version.major == 0
        assert version.minor > 0
