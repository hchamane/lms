import pytest

from lms.domains import FeatureSwitch


@pytest.mark.usefixtures("wipe_feature_switch_table")
class TestFeatureSwitch:
    def test_feature_switch_init(self) -> None:
        feature_switch = FeatureSwitch(name="test_feature_switch")
        assert feature_switch.name == "test_feature_switch"

    def test_feature_switch_create(self) -> None:
        feature_switch = FeatureSwitch.create(name="test_feature_switch")
        assert feature_switch.name == "test_feature_switch"
        assert feature_switch.active == 0

    def test_feature_switch_create_and_set_value(self) -> None:
        feature_switch = FeatureSwitch.create(name="test_feature_switch")
        assert feature_switch.name == "test_feature_switch"
        assert feature_switch.active == 0

        feature_switch.set_value(1)
        assert feature_switch.active == 1
