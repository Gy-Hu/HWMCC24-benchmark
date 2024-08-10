import z3



class Instruction(object):
    def __init__(self,name, decodeFunc):
        self.name = name
        self.decodeFunc = decodeFunc
        self.updateDict = {}
    def setUpdateToState(self,stateName,func):
        self.updateDict[stateName] = func
    def setILA_st(self,stlocal):
        self.stlocal = stlocal
    def setEntity(self,entity):
        self.entity = entity


ACTION_WRITE = 1
ACTION_CLEAR = 0

GOOD_IMAGE = 1
BAD_IMAGE  = 2
IMImageAddr = 3
SMImageAddr = 4


# this is just a place holder

#--------------------------------------------------------------
# Driver single-thread-behavior
SendResetDevice = Instruction('SendResetDevice', lambda state: state('DriPC') == 0) # MMIO
SendResetDevice.setUpdateToState('ResetCMDAddress',lambda state: ACTION_WRITE ) 
SendResetDevice.setUpdateToState('DriPC',lambda state: 1 ) 

WriteSMImage = Instruction('WriteSMImage', lambda state: state('DriPC') == 1)
WriteSMImage.setUpdateToState('SMImageAddr',lambda state: z3.If( z3.Int('badImage'+state('__tid_suffix__')) == 0,  GOOD_IMAGE, BAD_IMAGE  ) ) 
WriteSMImage.setUpdateToState('DriPC',lambda state: 2 ) 

SendLoadFw = Instruction('SendLoadFw', lambda state: state('DriPC') == 2) # MMIO
SendLoadFw.setUpdateToState('LoadFWAddress',lambda state: ACTION_WRITE ) 
SendLoadFw.setUpdateToState('DriPC',lambda state: 3 ) 

ReceiveReportSts = Instruction('ReceiveReportSts', lambda state: z3.And( state('DriPC') == 3 , state('ProcIntBitAddress') == ACTION_WRITE ) )
ReceiveReportSts.setUpdateToState('ProcIntBitAddress',lambda state: ACTION_CLEAR ) 
ReceiveReportSts.setUpdateToState('DriPC',lambda state: 4 ) 

ProcInst = [SendResetDevice, WriteSMImage, SendLoadFw, ReceiveReportSts ]
ProcState= ['DriPC']

[inst.setILA_st(ProcState) for inst in ProcInst]
[inst.setEntity('driver:') for inst in ProcInst]

#--------------------------------------------------------------
# Device one thread


ReceiveReset = Instruction('ReceiveReset', lambda state: state('ResetCMDAddress') == ACTION_WRITE)
ReceiveReset.setUpdateToState('ResetCMDAddress', lambda state: ACTION_CLEAR )
ReceiveReset.setUpdateToState('DevIdx1', lambda state: 0 )
ReceiveReset.setUpdateToState('DevIdx2', lambda state: 0 )

ReceiveLoadFw = Instruction('ReceiveLoadFw', lambda state: state('LoadFWAddress') == ACTION_WRITE)
ReceiveLoadFw.setUpdateToState('LoadFWAddress', lambda state: ACTION_CLEAR )
ReceiveLoadFw.setUpdateToState('DevIdx1', lambda state: 1 )

CopyFwFromSMtoIM = Instruction('CopyFwFromSMtoIM', lambda state: state('DevIdx1') == 1)
CopyFwFromSMtoIM.setUpdateToState('IMImageAddr', lambda state: state('SMImageAddr') )
CopyFwFromSMtoIM.setUpdateToState('DevIdx1', lambda state: 2 )

SendAuthReq = Instruction('SendAuthReq', lambda state: state('DevIdx1') == 2)
SendAuthReq.setUpdateToState('AuthReqAddress', lambda state: ACTION_WRITE )
SendAuthReq.setUpdateToState('DevIdx1', lambda state: 3 )

ReceiveAuthResp = Instruction('ReceiveAuthResp', lambda state: state('RecvAuthRespAddress') == ACTION_WRITE)
ReceiveAuthResp.setUpdateToState('RecvAuthRespAddress', lambda state: ACTION_CLEAR )
ReceiveAuthResp.setUpdateToState('DevIdx2', lambda state: 4 )

ReadCheckSts = Instruction('ReadCheckSts', lambda state: state('DevIdx2') == 4 )
ReadCheckSts.setUpdateToState('DeviceStsAddress', lambda state: state('CEStsAddress') )
ReadCheckSts.setUpdateToState('DevIdx2', lambda state: 5 )

SendReportSts = Instruction('SendReportSts', lambda state: state('DevIdx2') == 5 )
SendReportSts.setUpdateToState('ProcIntBitAddress', lambda state: ACTION_WRITE )
SendReportSts.setUpdateToState('DevIdx2', lambda state: 6 )

JumpToIM = Instruction('JumpToIM', lambda state: state('DevIdx2') == 6 )
JumpToIM.setUpdateToState('DevPC', lambda state: z3.If(state('DeviceStsAddress') == GOOD_IMAGE , IMImageAddr , 0 )  )
JumpToIM.setUpdateToState('DevIdx2', lambda state: 7 )


DevInst = [ReceiveReset, ReceiveLoadFw, CopyFwFromSMtoIM, SendAuthReq, ReceiveAuthResp, ReadCheckSts, SendReportSts, JumpToIM ]
DevState= ['DevIdx1', 'DevIdx2', 'DevPC']

[inst.setILA_st(DevState) for inst in DevInst]
[inst.setEntity('device:') for inst in DevInst]
#--------------------------------------------------------------
# CE one thread

ReceiveAuthReq = Instruction('ReceiveAuthReq', lambda state: state('AuthReqAddress') == ACTION_WRITE)
ReceiveAuthReq.setUpdateToState('AuthReqAddress', lambda state: ACTION_CLEAR )
ReceiveAuthReq.setUpdateToState('CEIdx', lambda state: 1)

VerifyFwSignatureInIM = Instruction('VerifyFwSignatureInIM', lambda state: state('CEIdx') == 1)
VerifyFwSignatureInIM.setUpdateToState('CEStsAddress', lambda state: state('IMImageAddr'))
VerifyFwSignatureInIM.setUpdateToState('CEIdx', lambda state: 2 )

SendAuthRespSts = Instruction('SendAuthRespSts', lambda state: state('CEIdx') == 2)
SendAuthRespSts.setUpdateToState('RecvAuthRespAddress' , lambda state: ACTION_WRITE )
SendAuthRespSts.setUpdateToState('CEIdx', lambda state: 3 )

CEInst = [ReceiveAuthReq, VerifyFwSignatureInIM, SendAuthRespSts]
CEState= ['CEIdx']


[inst.setILA_st(CEState) for inst in CEInst]
[inst.setEntity('ce:') for inst in CEInst]

SysSharedState = ['ResetCMDAddress', 'SMImageAddr', 'LoadFWAddress', 'ProcIntBitAddress','IMImageAddr', 'SMImageAddr','AuthReqAddress',
    'RecvAuthRespAddress', 'DeviceStsAddress', 'CEStsAddress']