#!/bin/bash
echo "* Remove prior results..."
rm -f *.btor2 *.vcd __yosys*.txt
echo "* Parsing input..."
yosys -s gen_btor.ys > __yosys_exec_result.txt
echo "* Run Pono to check refinement..."
pono --vcd cex.vcd -e ind  --property-file property.smt2  problem.btor2 
RfResult=$?
echo "* Parsing sanity check input..."
yosys -s gen_sanity_prop.ys > __yosys_exec_result.sanity.txt
echo "* Run Pono to check assumption sanity..."
pono --vcd cex.vcd -e ind  --property-file property.smt2  sanity.btor2 
SanityResult=$?
CoverResult=3

function show_result () {
    RfError=""
    SanityError=""
    CoverError=""

    if test $RfResult = 0; then RfMsg=" (* buggy)";
    elif test $RfResult = 1; then RfMsg=" (passed)";
    elif test $RfResult = 2; then RfMsg=" (* checker error)";
    elif test $RfResult = 3; then RfMsg=" (skipped)";
    elif test $RfResult = 255; then RfMsg=" (unknown)";
    else echo "UNKNOWN PONO RESULT: " $RfResult; RfMsg=" (* terminated)"; RfResult=2
    fi

    if   test $SanityResult = 0;   then SanityMsg=" (* sanity violation)";
    elif test $SanityResult = 1;   then SanityMsg=" (sanity is proved to hold)";
    elif test $SanityResult = 2;   then SanityMsg=" (* checker error)";
    elif test $SanityResult = 3;   then SanityMsg=" (skipped)";
    elif test $SanityResult = 255; then SanityMsg=" (no sanity violation within bound)";
    else echo "UNKNOWN PONO RESULT: " $SanityResult; SanityMsg=" (* terminated)"; SanityResult=2
    fi

    if   test $CoverResult = 0;   then CoverMsg=" (covered)";
    elif test $CoverResult = 1;   then CoverMsg=" (* not reachable)";
    elif test $CoverResult = 2;   then CoverMsg=" (* checker error)";
    elif test $CoverResult = 3;   then CoverMsg=" (skipped)";
    elif test $CoverResult = 255; then CoverMsg=" (* not yet reachable)";
    else echo "UNKNOWN PONO RESULT: " $CoverResult; CoverMsg=" (* terminated)"; CoverResult=2;
    fi

    echo '============ SUMMARY ============'
    echo 'Refinement Check:' $RfResult $RfMsg
    echo 'Santiy Check:' $SanityResult $SanityMsg
    echo 'Cover Check:' $CoverResult $CoverMsg
    echo '============ END OF SUMMARY ============'
    echo ""

    if [ $RfResult = 2 ] || [ $SanityResult = 2 ] ||  [ $CoverResult = 2 ]; then
        return 2
    fi

    if test $RfResult = 0; then return 0;
    elif test $SanityResult = 0; then return 0;
    elif test $CoverResult = 1; then return 0;
    elif test $CoverResult = 255; then return 255;
    else return $RfResult;
    fi
}

show_result
exit $?


