# this is to show we can handle litmus tests
# let's begin with SC
# this is a library that handles test format

import unroll
import litmus.litmusParse as lmt

class litmusTestAdaptor(object):
    def __init__(self, instCols):
        self.num_cores = instCols.num_cores
        
        self.NoThread = [1] * instCols.num_cores
        self.TemplateProgram , self.localStates = instCols.unroller_get_templateProgram_local_state()
        self.SysSharedState = instCols.unroller_get_sharedStates()

        self.Unroller = unroll.unroller(NoThread = self.NoThread, localStates = self.localStates, 
            TemplateProgram = self.TemplateProgram, SysSharedState = self.SysSharedState)
        
        Unroller = self.Unroller # alias

        Unroller.unroll()

        # add co/fr relations
        rf_force = {}
        for tp,gid1,gid2 in instCols.set_of_rel:
            neid1 = instCols.unroller_gid2instName_and_eid(gid1)
            neid2 = instCols.unroller_gid2instName_and_eid(gid2)


            relTuple1 = Unroller.litmus_getRelRefTuple(*neid1)
            relTuple2 = Unroller.litmus_getRelRefTuple(*neid2)
            if tp == 'rf':
                write = relTuple1
                read  = relTuple2 # w -> r
                assert read not in rf_force
                rf_force[read] = write
            else: # fr,co
                Unroller.enforce_CO_or_FR(tp, relTuple1, relTuple2)

        # add fence instructions
        for instName in instCols.set_of_fences:
            neid = instCols.unroller_instName2Name_and_eid(instName)
            fence_tuple = Unroller.litmus_getRelRefTuple(*neid)
            Unroller.litmus_makeTsLocalFence(fence_tuple)

        # add read asserts
        for instName,cond in instCols.set_of_read_assert.items():
            frameCond = lambda ts,instName=instName:ts.inst.name == instName
            Unroller.addPropertyOnSingleFrames( runProperty = cond, frameCond = frameCond )

        # add last frame assertions
        for endingAssert in instCols.endingAsserts:
            Unroller.addPropertyOnEnding(endingAssert)

        # do the final Pi
        Unroller.finalizePiFun(rf_force)

    def run(self): # string of sat unsat
        self.Unroller.buildRunProp() # func = z3.And by default
        self.Unroller.pushInstConstraintAndCheck()
        return str(self.Unroller.solve())


def runOneAlternative(altblk): # return a newly created unroller
    lmtAdaptor = litmusTestAdaptor(altblk)
    result = lmtAdaptor.run()
    print result,'vs.',altblk.outcome,
    if (result == 'unsat' and altblk.outcome == 'Forbidden') or (result == 'sat' and altblk.outcome == 'Permitted'):
        print ' okay'
        return True
    else:
        print ' !inconsistent'
        return False
        

# run one litmus test
def runLitmusTest(testname):
    lmt.parseLitmusTest(testname)
    if not lmt.AlterLists:
        print 'Parsing Error:',testname
        raw_input()
        return
    # is what we got, list of instruction
    resultOk = False
    for altblk in lmt.AlterLists:
        resultOk = resultOk or runOneAlternative(altblk)
    if not resultOk:
        assert False

SC_tests = """
amd3.test        n4.test        rfi006.test        safe006.test  safe021.test
co-iriw.test     n5.test        rfi011.test        safe007.test  safe022.test
co-mp.test       n6.test        rfi012.test        safe008.test  safe026.test
iriw.test        n7.test        rfi013.test        safe009.test  safe027.test
iwp23b.test      podwr000.test  rfi014.test        safe010.test  safe029.test
iwp24a.test      podwr001.test  rfi015.test        safe011.test  safe030.test
iwp24.test       rfi000.test    rwc-unfenced.test  safe012.test  sb2.test
lb.test          rfi001.test    safe000.test       safe014.test  sb.test
mp+staleld.test  rfi002.test    safe001.test       safe016.test  ssl.test
mp.test          rfi003.test    safe002.test       safe017.test  wrc.test
n1.test          rfi004.test    safe003.test       safe018.test
n2.test          rfi005.test    safe004.test       safe019.test
"""

TSO_nofence = """
amd3.test        n2.test        rfi005.test        safe004.test  safe019.test
co-iriw.test     n4.test        rfi006.test        safe006.test  safe021.test
co-mp.test       n5.test        rfi011.test        safe007.test  safe022.test
iriw.test        n6.test        rfi012.test        safe008.test  safe026.test
iwp23b.test      n7.test        rfi013.test        safe009.test  safe027.test
iwp24a.test      podwr000.test  rfi014.test        safe010.test  safe029.test
iwp24.test       podwr001.test  rfi015.test        safe011.test  safe030.test
lb.test          rfi000.test    rwc-unfenced.test  safe012.test  sb2.test
rfi001.test    safe000.test       safe014.test  sb.test
mp+staleld.test  rfi002.test    safe001.test       safe016.test  ssl.test
mp.test          rfi003.test    safe002.test       safe017.test  wrc.test
n1.test          rfi004.test    safe003.test       safe018.test
"""

def TestSCLitmusTest():
    for name in SC_tests.split():
        fullPath = 'litmus/SC_tests/'+name
        print '== Running:'+name+' =='
        runLitmusTest(fullPath)

def TestTSOLitmusTest():
    for name in TSO_nofence.split():
        fullPath = 'litmus/TSO_tests/'+name
        print '== Running:'+name+' =='
        runLitmusTest(fullPath)


if __name__ == '__main__':
    TestSCLitmusTest()
    #runLitmusTest('litmus/TSO_tests/rfi011.test')


