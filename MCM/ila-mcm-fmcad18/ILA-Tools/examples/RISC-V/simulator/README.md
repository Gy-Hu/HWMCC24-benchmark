RISC-V ISA Simulator
======================

Author  : Andrew Waterman, Yunsup Lee

Date    : June 19, 2011

Version : (under version control)

About
-------------

The RISC-V ISA Simulator implements a functional model of one or more
RISC-V processors.

Build Steps
---------------

We assume that the RISCV environment variable is set to the RISC-V tools
install path, and that the riscv-fesvr package is installed there.

    $ mkdir build
    $ cd build
    $ ../configure --prefix=$RISCV --with-fesvr=$RISCV
    $ make
    $ [sudo] make install

Compiling and Running a Simple C Program
-------------------------------------------

Install spike (see Build Steps), riscv-gnu-toolchain, and riscv-pk.

Write a short C program and name it hello.c.  Then, compile it into a RISC-V
ELF binary named hello:

    $ riscv64-unknown-elf-gcc -o hello hello.c

Now you can simulate the program atop the proxy kernel:

    $ spike pk hello

Per-Instruction Simulator
----------------------------------------

Modified: Hongce Zhang (hongcez@princeton.edu)

After you build the simulator, under the directory $RISCV/bin/ you
can find an executable called "spike_sim_inst". It takes in assign.in. 
The format is described in the following section. The simulator generates 
result.out. 

    $ ./spike_sim_inst
    
for runing the simulator with default options.
	
The default ISA is RV32, if you would like to like to simulate 64-bit
RISC-V, please run with

    $ ./spike_sim_inst --isa=RV64

More options can be found by 

    $ ./spike_sim_inst -h

I/O Format of Per-Instruction Simulator
----------------------------------------

The format of assign.in is listed here:

	line 1:  instruction (hex)
	line 2:  x0 value-of-x0 (hex) (x0 must be zero!)
	line 3:  x1 value-of-x1 (hex)
	line ...
	line 33: pc value-of-pc (hex)
	line 34: .CSR_BEGIN
	line 35: .CSR_END 
	
Note: if you are not controlling CSRs, you don't need
to fill anthing between .CSR_BEGIN and .CSR_END.
Especially, if you don't assign Priv, it will be set
to USER_LEVEL automatically.

Starting here is the content of memory. Because memory
can be very large, it is not feasible to list them all.
You can assign a default value and only care about the 
ones that are not default.

In line 36, two values. The first is the number of bytes
that are not equal to the default value , the second is
the default value.

	line 36: #-of-bytes(dec) default-value(hex)
	line 37-end:
			all items in address(hex) data(hex) pair,
			use space to split the two fields and use 
			newline to split items.


The format of result.out is listed here:

	x0 0
	x1 ? (hex)
	x2 ? (hex)
	...
	pc ?
	.CSR_BEGIN
		CSRs (Probably you are not interested)
	.CSR_END
	Content of memory, similar format as in assign.in


An example of assign.in:

5081b3 is the instruction: ADD x3, x1, x5

	5081b3
	x0 0
	x1 1
	x2 2
	x3 3
	x4 4
	x5 5
	x6 6
	x7 7
	x8 8
	x9 9
	x10 a
	x11 b
	x12 c
	x13 d
	x14 e
	x15 f
	x16 10
	x17 11
	x18 12
	x19 13
	x20 14
	x21 15
	x22 16
	x23 17
	x24 18
	x25 19
	x26 1a
	x27 1b
	x28 1c
	x29 1d
	x30 1e
	x31 1f
	pc 4000
	.CSR_BEGIN
	.CSR_END
	0 0



Simulating a New Instruction
------------------------------------

Adding an instruction to the simulator requires two steps:

  1.  Describe the instruction's functional behavior in the file
      riscv/insns/<new_instruction_name>.h.  Examine other instructions
      in that directory as a starting point.

  2.  Add the opcode and opcode mask to riscv/opcodes.h.  Alternatively,
      add it to the riscv-opcodes package, and it will do so for you:

         $ cd ../riscv-opcodes
         $ vi opcodes       // add a line for the new instruction
         $ make install

  3.  Rebuild the simulator.

Interactive Debug Mode
---------------------------

To invoke interactive debug mode, launch spike with -d:

    $ spike -d pk hello

To see the contents of an integer register (0 is for core 0):

    : reg 0 a0

To see the contents of a floating point register:

    : fregs 0 ft0

or:

    : fregd 0 ft0

depending upon whether you wish to print the register as single- or double-precision.

To see the contents of a memory location (physical address in hex):

    : mem 2020

To see the contents of memory with a virtual address (0 for core 0):

    : mem 0 2020

You can advance by one instruction by pressing <enter>. You can also
execute until a desired equality is reached:

    : until pc 0 2020                   (stop when pc=2020)
    : until mem 2020 50a9907311096993   (stop when mem[2020]=50a9907311096993)

Alternatively, you can execute as long as an equality is true:

    : while mem 2020 50a9907311096993

You can continue execution indefinitely by:

    : r

At any point during execution (even without -d), you can enter the
interactive debug mode with `<control>-<c>`.

To end the simulation from the debug prompt, press `<control>-<c>` or:

    : q

Debugging With Gdb
------------------

An alternative to interactive debug mode is to attach using gdb. When invoked
with '--gdb-port <port>' spike will listen on the given TCP port.  It's
possible to attach with gdb (that has riscv support compiled in) by entering
`target remote localhost:<port>` in gdb. For example, in one shell run:
```
spike --gdb-port 9824 pk tests/debug
```

Then in a second shell you may do something like:
```
tnewsome@compy-vm:~/SiFive/riscv-isa-sim$ $RISCV/bin/riscv64-unknown-elf-gdb tests/debug
GNU gdb (GDB) 7.11.50.20160212-git
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "--host=x86_64-pc-linux-gnu --target=riscv64-unknown-elf".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from tests/debug...done.
(gdb) target remote localhost:9824
Remote debugging using localhost:9824
0x00000000000101f0 in main ()
    at /home/tnewsome/SiFive/riscv-isa-sim/tests/debug.c:20
20          while (i)
(gdb) p i
$1 = 42
(gdb) list
15          volatile int i = 42;
16          const char *text = "constant\n";
17          int threshold = 7;
18
19          // Wait for the debugger to get us out of this loop.
20          while (i)
21              ;
22
23          printf("%s", text);
24          for (int y=0; y < 10; y++) {
(gdb) p i=0
$2 = 0
(gdb) b print_row
Breakpoint 1 at 0x10178: file /home/tnewsome/SiFive/riscv-isa-sim/tests/debug.c, line 7.
(gdb) c
Continuing.

Breakpoint 1, print_row (length=0)
    at /home/tnewsome/SiFive/riscv-isa-sim/tests/debug.c:7
7           for (int x=0; x<length; x++) {
(gdb) c
Continuing.

Breakpoint 1, print_row (length=1)
    at /home/tnewsome/SiFive/riscv-isa-sim/tests/debug.c:7
7           for (int x=0; x<length; x++) {
(gdb) delete breakpoints
Delete all breakpoints? (y or n) y
(gdb) c
Continuing.
Remote connection closed
(gdb)
```
