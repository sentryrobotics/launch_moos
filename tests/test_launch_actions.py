"""Tests for the MOOSApp Action."""

from pathlib import Path
import asyncio

from launch import LaunchContext
from launch.actions import IncludeLaunchDescription

from launch_moos.actions.moosapp import MOOSApp
from launch_moos import MOOSMissionFileDescriptionSource

import pytest


def test_moosapp_args():
    lc = LaunchContext()
    lc._set_asyncio_loop(asyncio.get_event_loop())

    moosdb_app = MOOSApp(executable="echo",
                         mission_file="the_moos_file.moos",
                         output='screen')

    moosdb_app.execute(lc)
    assert moosdb_app.process_details['cmd'] == ['echo', 'the_moos_file.moos']


def test_moosapp_args_2():
    lc = LaunchContext()
    lc._set_asyncio_loop(asyncio.get_event_loop())

    moos_app = MOOSApp(executable="echo",
                         alias="pHelmIvP",
                         mission_file="the_moos_file.moos",
                         output='screen')

    moos_app.execute(lc)
    assert moos_app.process_details['cmd'] == ['echo', 'the_moos_file.moos', 'pHelmIvP']


def test_moosapp_generate_mission_file():
    lc = LaunchContext()
    lc._set_asyncio_loop(asyncio.get_event_loop())

    helmivp_app = MOOSApp(executable="pHelmIvP",
                          alias="pHelmIvP",
                          global_config=[
                              ("ServerHost", "localhost"),
                              ("ServerPort", 9000),
                              ("Community", "alpha"),
                              ("MOOSTimeWarp", 1),
                              ("LatOrigin", 43.825300),
                              ("LongOrigin", -70.330400),
                          ],
                          config=[
                              ("AppTick", 4),
                              ("CommsTick", 4),
                              ("behaviors", "alpha.bhv"),
                              ("domain", "course:0:359:360"),
                              ("domain", "speed:0:4:41"),
                          ])

    helmivp_app.execute(lc)
    moos_file = helmivp_app.process_details['cmd'][1]
    assert helmivp_app.mission_file == moos_file

    assert Path(moos_file).is_file()
    assert Path(moos_file).read_text() == """ServerHost = localhost
ServerPort = 9000
Community = alpha
MOOSTimeWarp = 1
LatOrigin = 43.8253
LongOrigin = -70.3304

ProcessConfig = pHelmIvP
{
  AppTick = 4
  CommsTick = 4
  behaviors = alpha.bhv
  domain = course:0:359:360
  domain = speed:0:4:41
}
"""


def test_include_mission_file():
    desc = MOOSMissionFileDescriptionSource("alpha.moos")
