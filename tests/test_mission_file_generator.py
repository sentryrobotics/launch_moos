"""Tests for the MOOS Mission File Generator."""

import pytest

from launch_moos.moosfile_generator import evaluate_template


@pytest.mark.skip  # empy has troubles with this
def test_moosapp_generate_mission_file(capsys) -> None:
    output = evaluate_template(
        {
            "process_name": "pHelmIvP",
            "global_variables": [
                ("ServerHost", "localhost"),
                ("ServerPort", 9000),
                ("Community", "alpha"),
                ("MOOSTimeWarp", 1),
                ("LatOrigin", 43.8253001),
                ("LongOrigin", -70.3304001),
            ],
            "process_variables": [
                ("AppTick", 4),
                ("CommsTick", 4),
                ("behaviors", "alpha.bhv"),
                ("domain", "course:0:359:360"),
                ("domain", "speed:0:4:41"),
            ],
        }
    )

    assert (
        output
        == """ServerHost = localhost
ServerPort = 9000
Community = alpha
MOOSTimeWarp = 1
LatOrigin = 43.8253001
LongOrigin = -70.3304001

ProcessConfig = pHelmIvP
{
  AppTick = 4
  CommsTick = 4
  behaviors = alpha.bhv
  domain = course:0:359:360
  domain = speed:0:4:41
}
"""
    )
