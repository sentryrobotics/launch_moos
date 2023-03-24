#!/usr/bin/env python3

import os
import platform
import sys
from typing import cast

import launch  # noqa: E402
import launch.actions  # noqa: E402
import launch.events  # noqa: E402
import launch.substitutions  # noqa: E402
from launch import LaunchDescription  # noqa: E402
from launch import LaunchIntrospector  # noqa: E402
from launch import LaunchService  # noqa: E402

from launch_moos.actions import IncludeMOOSMission
from launch_moos.actions import MOOSApp


# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # noqa


def main(argv=sys.argv[1:]):
    """Run Counter via launch."""
    # Configure rotating logs.
    # launch.logging.launch_config.log_handler_factory = \
    #     lambda path, encoding=None: launch.logging.handlers.RotatingFileHandler(
    #         path, maxBytes=1024, backupCount=3, encoding=encoding)

    # moos_file = IncludeMOOSMission("alpha.moos")

    moos_globals = [
        ("ServerHost", "localhost"),
        ("ServerPort", 9000),
        ("Community", "alpha"),
        ("MOOSTimeWarp", 1),
        ("LatOrigin", 43.825300),
        ("LongOrigin", -70.330400),
    ]

    moosdb_app = MOOSApp(
        executable="MOOSDB", name="MOOSDB", global_config=moos_globals, output="screen"
    )

    helmivp_app = MOOSApp(
        executable="pHelmIvP",
        alias="pHelmIvP",
        global_config=moos_globals,
        config=[
            ("AppTick", 4),
            ("CommsTick", 4),
            ("behaviors", "alpha.bhv"),
            ("domain", "course:0:359:360"),
            ("domain", "speed:0:4:41"),
        ],
        output="screen",
    )

    ld = LaunchDescription([moosdb_app, helmivp_app])

    # # Unset launch prefix to prevent other process from getting this setting.
    # ld.add_action(launch.actions.SetLaunchConfiguration('launch-prefix', ''))
    #
    # # Run the counting program, with default options.
    # counter_action = launch.actions.ExecuteProcess(cmd=[sys.executable, '-u', './counter.py'])
    # ld.add_action(counter_action)
    #
    # # Setup an event handler for just this process which will exit when `Counter: 4` is seen.
    # def counter_output_handler(event):
    #     target_str = 'Counter: 4'
    #     if target_str in event.text.decode():
    #         return launch.actions.EmitEvent(event=launch.events.Shutdown(
    #             reason="saw '{}' from '{}'".format(target_str, event.process_name)
    #         ))
    #
    # ld.add_action(launch.actions.RegisterEventHandler(launch.event_handlers.OnProcessIO(
    #     target_action=counter_action,
    #     on_stdout=counter_output_handler,
    #     on_stderr=counter_output_handler,
    # )))
    #
    # # Run the counter a few more times, with various options.
    # ld.add_action(launch.actions.ExecuteProcess(
    #     cmd=[sys.executable, '-u', './counter.py', '--ignore-sigint']
    # ))
    # ld.add_action(launch.actions.ExecuteProcess(
    #     cmd=[sys.executable, '-u', './counter.py', '--ignore-sigint', '--ignore-sigterm']
    # ))
    #
    # # Add our own message for when shutdown is requested.
    # ld.add_action(launch.actions.RegisterEventHandler(launch.event_handlers.OnShutdown(
    #     on_shutdown=[launch.actions.LogInfo(msg=[
    #         'Launch was asked to shutdown: ',
    #         launch.substitutions.LocalSubstitution('event.reason'),
    #     ])],
    # )))

    print("Starting introspection of launch description...")
    print("")

    print(LaunchIntrospector().format_launch_description(ld))

    print("")
    print("Starting launch of launch description...")
    print("")

    # ls = LaunchService(argv=argv, debug=True)  # Use this instead to get more debug messages.
    ls = LaunchService(argv=argv)
    ls.include_launch_description(ld)
    return ls.run()


if __name__ == "__main__":
    sys.exit(main())
