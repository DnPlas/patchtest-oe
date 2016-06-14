# variables
PASS='PASS'
FAIL='FAIL'

#
# Execute patchtest and compare current result with expected result.
#
exec_patchtest() {
    local TESTDIR=$1
    local TESTID=$2
    local TESTMBOX=$3
    local EXPECTED=$4
    local BRANCH=$5

    if [ -z "$BRANCH" ]; then
	BRANCH="master"
    fi

    # in case of failure, this RESULT will be blank
    RESULT=$(patchtest --test-dir $TESTDIR -m $TESTMBOX --no-patch --branch $BRANCH | \
	sed -n -e "/$TESTID/p" | \
	sed -n -e "/$EXPECTED/p")
    [ -z "${RESULT}" ] && { echo "$TESTDIR $TESTID $EXPECTED"; }
}

