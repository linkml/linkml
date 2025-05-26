#!/usr/bin/env python

import json
import os
import subprocess
import sys


def run_tests_and_report():
    # Get all command line arguments except the script name
    test_cli = sys.argv[1:]

    # Always ensure we have the JSON report arguments
    json_report_args = ["--json-report", "--json-report-file=report.json"]

    # Combine base arguments with user provided arguments
    full_command = test_cli + json_report_args

    # Run pytest with all arguments
    subprocess.run(full_command)

    # Read the JSON report
    with open("report.json") as f:
        report = json.load(f)

    # Process failed tests
    for test in report["tests"]:
        if test["outcome"] == "failed":
            filename = test["nodeid"].split("::")[0]
            test_name = test["nodeid"].split("::")[1] if "::" in test["nodeid"] else test["nodeid"]
            line = test.get("call", {}).get("crash_line", "1")
            print(f"::warning file={filename},line={line},col=1::Failing Test: {test_name}")

    # Cleanup
    os.remove("report.json")


if __name__ == "__main__":
    run_tests_and_report()
