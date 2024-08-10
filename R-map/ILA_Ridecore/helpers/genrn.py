tmpl = """
    "s0_r{0}"  : "RTL.pipe.aregfile.regfile.mem[{0}] @ robexit",
    "s1_r{0}"  : "(#cmt1# && #wen1# && (#wrf1# == {0})) ? #wdata1# : #s0_r{0}#",
    "s2_r{0}"  : "(#cmt2# && #wen2# && (#wrf2# == {0})) ? #wdata2# : #s1_r{0}#",
    "pre_r{0}" : "rob_match2 ? s1_r{0} : s0_r{0}",
    "post_r{0}": "rob_match2 ? s2_r{0} : s1_r{0}","""

for idx in range(1,32):
  print (tmpl.format(idx))
