#!/bin/bash
set -x

declare -r TEST_LIST
declare -r ONE_TEST
declare -r URL
declare -r PORT

if [ "X$TEST_LIST" != "X" ] && [ "X$ONE_TEST" != "X" ]; then
	echo "Should only provide one of the two options. Either TEST_LIST or ONE_TEST to run."
	exit 1
fi

if [ "X$TEST_LIST" != "X" ]; then
    echo ""
    echo "Running ./run_master.py --url $URL --port $PORT --tests-list $TEST_LIST"
    echo ""
    ./run_master.py --url "$URL" --port "$PORT" --tests-list "$TEST_LIST"
elif [ "X$ONE_TEST" != "X" ]; then
    echo ""
    echo "Running ./run_master.py --url $URL --port $PORT --tests $ONE_TEST"
    echo ""
    ./run_master.py --url "$URL" --port "$PORT" --tests "$ONE_TEST"
fi
# Return success or failure ( 0 - success )
EXIT_STATUS=$?

if [ -f report.html ]; then
	echo "COPYING report.html TO result DIRECTORY"
	cp report.html result
fi
if [ -f result.xml ]; then
	echo "COPYING result.xml TO result DIRECTORY"
	cp result.xml result
fi
if [ -d assets ]; then
	echo "COPYING assets DIRECTORY TO result DIRECTORY"
	cp -r assets result
fi

chmod -R 777 result
if [ "$EXIT_STATUS" -eq 0 ]; then
	PASSED=true
else
	PASSED=false
fi
$PASSED
