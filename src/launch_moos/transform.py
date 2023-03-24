from launch.actions import ExecuteProcess


def antler_run_statement_to_action(statement):
    assert statement["executable"] == "pHelmIvP"

    for param in statement["params"]:
        param["name"] == "NewConsole"
        param["value"] == "true"

    assert r["params"][1]["name"] == "ExtraProcessParams"
    assert r["params"][1]["value"] == "HParams"
    assert statement["moosname"] == "uTimerScript_SensorConfig"
