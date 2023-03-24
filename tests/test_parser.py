import pytest

from launch_moos.parser import (
    assign_statement_line, processconfig, process_config_run_line, global_section, comment_line, moos_file
)


def test_comments() -> None:
    r = comment_line.parse_string("// NAME: M. Benjamin, MIT CSAIL\n", parse_all=True)
    assert len(r) == 0

    comments_test = """//-------------------------------------------------
        // NAME: M. Benjamin, MIT CSAIL
        // FILE: alpha.moos
        //-------------------------------------------------
    """

    # r = comment_line.parse_string(comments_test, parse_all=True)
    # assert len(r) == 0


def test_parse_globals() -> None:
    r = assign_statement_line.parse_string("ServerHost   = localhost\n", parse_all=True)
    assert r[0]['name'] == "ServerHost"
    assert r[0]['value'] == "localhost"

    r = assign_statement_line.parse_string("  absolute_time_gap = 1   // In Seconds, Default is 4\n", parse_all=True)
    assert r[0]['name'] == "absolute_time_gap"
    assert r[0]['value'].strip() == "1"

    r = assign_statement_line.parse_string("  GRID_CONFIG = pts={-100,-200: 200,-200: 200,25: -100,25}\n", parse_all=True)
    assert r[0]['name'] == 'GRID_CONFIG'
    assert r[0]['value'] == 'pts={-100,-200: 200,-200: 200,25: -100,25}'

    moos_globals1 = """//-------------------------------------------------
// NAME: M. Benjamin, MIT CSAIL
// FILE: alpha.moos
//-------------------------------------------------

ServerHost   = localhost
ServerPort   = 9000
Community    = alpha
MOOSTimeWarp = 1

// Forest Lake
LatOrigin  = 43.825300 
LongOrigin = -70.330400 

// MIT Sailing Pavilion (use this one)
// LatOrigin  = 42.358456 
// LongOrigin = -71.087589
"""

    r = global_section.parse_string(moos_globals1, parse_all=True)
    assert len(r) == 6


def test_parse_antler_block() -> None:
    r = process_config_run_line.parse_string("  Run = MOOSDB          @ NewConsole = false\n", parse_all=True)
    assert r['executable'] == "MOOSDB"
    assert r['params'][0]['name'] == "NewConsole"
    assert r['params'][0]['value'] == "false"

    r = process_config_run_line.parse_string("Run = pHelmIvP	@ NewConsole = true, ExtraProcessParams=HParams\n", parse_all=True)
    assert r['executable'] == "pHelmIvP"
    assert r['params'][0]['name'] == "NewConsole"
    assert r['params'][0]['value'] == "true"
    assert r['params'][1]['name'] == "ExtraProcessParams"
    assert r['params'][1]['value'] == "HParams"

    r = process_config_run_line.parse_string("Run = uTimerScript       @ NewConsole = false ~uTimerScript_SensorConfig\n", parse_all=True)
    assert r['executable'] == "uTimerScript"
    assert r['params'][0]['name'] == "NewConsole"
    assert r['params'][0]['value'] == "false"
    assert r['moosname'] == "uTimerScript_SensorConfig"

    antler_moos1 = """Processconfig = ANTLER
{
  MSBetweenLaunches = 100

  Run = MOOSDB          @ NewConsole = false
  Run = pLogger         @ NewConsole = false
  Run = uProcessWatch   @ NewConsole = false

  Run = pMarineViewer   @ NewConsole = false

  Run = pHostInfo       @ NewConsole = false
  Run = pShare          @ NewConsole = false
  Run = uFldShoreBroker @ NewConsole = false
  Run = uFldNodeComms   @ NewConsole = false
  Run = uTimerScript    @ NewConsole = false

  Run = uFldCTDSensor       @ NewConsole = false
  Run = pFrontGridRender    @ NewConsole = false
  Run = pGradeFrontEstimate @ NewConsole=false
}
"""

    r = processconfig.parse_string(antler_moos1, parse_all=True)
    pass

def test_parse_processconfig_block() -> None:
    proc_block_2 = """ProcessConfig = pGradeFrontEstimate
{
  AppTick=1
  CommsTick=1

}
"""
    r = processconfig.parse_string(proc_block_2, parse_all=True)

    assert r['processconfig_name'] == "pGradeFrontEstimate"
    assert r[2]['name'] == "AppTick"
    assert r[2]['value'] == "1"
    assert r[3]['name'] == "CommsTick"
    assert r[3]['value'] == "1"


# def test_moos_file():
    # moos_file_ex1 = open("moos_files/s15_pedi_alpha.moos", "rt").read()
    # r = moos_file.parse_string(moos_file_ex1, parse_all=True)
