#!/usr/bin/env python

import optparse
import os
import sys
import pytest

MasterScriptDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(MasterScriptDir, "src"))

print("SYSTEM PATH : {}".format(str(sys.path)))

# add options
usage = "%prog[options]"
parser = optparse.OptionParser(usage=usage)

parser.add_option("--url", action="store", dest="url", help="websocket url", metavar="[URL]", default="ws://localhost")
parser.add_option("--port", action="store", dest="port", help="port to connect", metavar="[PORT]", default="4444")
parser.add_option("--tests", action="append", dest="tests",
                  help="Path to test suite to be run", metavar="[PATH TO TEST SUITE(S)]")
parser.add_option("--tests-list", action="store", dest="testslist", help="list containing the test suites to be run",
                  metavar="[PATH TO A LIST OF TEST SUITES TO BE RUN]")
parser.add_option("--mark-test", action="store", dest="marktest", help="Mark a test function with custom metadata",
                  metavar="[RUN MARKED TESTS]")

(options, args) = parser.parse_args()
pytest_parameters = []

if options.marktest:
    pytest_parameters.append("-m " + options.marktest)
pytest_parameters.append("-v")
pytest_parameters.append("--junitxml=result.xml")
pytest_parameters.append("--show-capture=no")
pytest_parameters.append("-ra")
pytest_parameters.append("--tb=short")
pytest_parameters.append("--disable-pytest-warnings")
pytest_parameters.append("--html=report.html")

# URL
if options.url:
    pytest_parameters.append("--url={}".format(options.url))
    print("URL : {}".format(options.url))
    print("--------" + len(options.url) * "-" + "\n")
else:
    print("URL needs to be set. Exiting.")
    sys.exit(1)
# port
if options.port:
    pytest_parameters.append("--port={}".format(options.port))
    print("PORT : {}".format(options.port))
    print("---------" + len(options.port) * "-" + "\n")

# passing a file containing the test suite(s)
if options.tests is not None:
    pytest_parameters.extend(options.tests)
elif options.testslist is not None:
    test_list = []
    # we got a test file that needs to be parsed
    for line in open(options.testslist, 'r'):
        if not line.startswith('#'):
            test_list.append(line.rstrip())
    pytest_parameters.extend(test_list)
else:
    print("There are no tests to run. Exiting.")
    sys.exit(1)

print(pytest_parameters)

print("\n#############################")
print("####### RUNNING TESTS #######")
print("#############################\n")
print(pytest_parameters)
exit_code = pytest.main(pytest_parameters)
exit(exit_code)
