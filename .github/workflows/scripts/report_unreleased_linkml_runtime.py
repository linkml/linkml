#!/usr/bin/env python

import json
import os
import subprocess
import sys

summary_header = "Tests with 'unreleased linkml-runtime'"


def format_results_message(total_tests, passed_count, failed_tests):
    """Format the results message for the PR comment"""

    server_url = os.environ.get("GITHUB_SERVER_URL", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")

    # Construct the job URL
    job_url = f"{server_url}/{repository}/actions/runs/{run_id}"

    if not failed_tests:
        lines = [
            f"## ✨ 🧪 {summary_header} ([View Details]({job_url})) ✨\n",
            f"- Total Tests: {total_tests}",
            f"- ✅ Passed: {passed_count}",
            "\n✨ All tests passed!",
        ]
    else:
        lines = [
            f"## ⚠️ 🧪 {summary_header} ([View Details]({job_url})) ⚠️\n",
            f"- Total Tests: {total_tests}",
            f"- ✅ Passed: {passed_count}",
        ]
        failed_count = len(failed_tests)
        lines.extend(
            [
                f"- ❌ Failed: {failed_count}\n",
                "### Failed Tests",
                "| File | Test Name |",
                "|------|-----------|",
            ]
        )
        for (
            filename,
            test_name,
        ) in failed_tests:
            lines.append(f"| {filename} | {test_name} |")

    return "\n".join(lines)


def write_job_summary(total_tests, passed_count, failed_tests):
    """Write a markdown summary to the GitHub Actions job summary"""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(f"## 🧪 {summary_header}\n\n")
            f.write(f"- Total Tests: {total_tests}\n")
            f.write(f"- ✅ Passed: {passed_count}\n")
            if failed_tests:
                f.write(f"- ❌ Failed: {len(failed_tests)}\n\n")
                f.write("### Failed Tests\n\n")
                for filename, test_name in failed_tests:
                    f.write(f"- {filename} - {test_name}\n")


def run_tests_and_report():
    # Get user provided arguments first
    test_cli = sys.argv[1:]

    # Always ensure we have the JSON report arguments
    json_report_args = ["--json-report", "--json-report-file=report.json"]

    # Combine arguments (user args first, then JSON report args)
    full_command = test_cli + json_report_args

    # Run pytest and stream output
    subprocess.run(full_command, stdout=sys.stdout, stderr=sys.stderr)

    # Process the results
    with open("report.json") as f:
        report = json.load(f)

    print(f"::group::{summary_header}", file=sys.stderr)

    failed_tests = []
    for test in report["tests"]:
        if test["outcome"] == "failed":
            filename = test["nodeid"].split("::")[0]
            test_name = test["nodeid"].split("::")[1] if "::" in test["nodeid"] else test["nodeid"]
            failed_tests.append((filename, test_name))
            print(f"::warning file={filename}::Failing Test: {filename} - {test_name}", file=sys.stderr)

    total_tests = len(report["tests"])
    failed_count = len(failed_tests)
    passed_count = total_tests - failed_count

    print(f"Total Tests: {total_tests}", file=sys.stderr)
    print(f"✅ Passed: {passed_count}", file=sys.stderr)
    if failed_count > 0:
        print(f"❌ Failed: {failed_count}", file=sys.stderr)
        print(f"::notice::Test Summary: {failed_count} test{'s' if failed_count > 1 else ''} failed", file=sys.stderr)

    print("::endgroup::", file=sys.stderr)

    # Write job summary
    write_job_summary(total_tests, passed_count, failed_tests)

    # Write the results to test-results_unreleased-linkml-runtime.md
    with open("test-results_unreleased-linkml-runtime.md", "w", encoding="utf-8") as f:
        f.write(format_results_message(total_tests, passed_count, failed_tests))

    os.remove("report.json")
    return 0


if __name__ == "__main__":
    sys.exit(run_tests_and_report())
