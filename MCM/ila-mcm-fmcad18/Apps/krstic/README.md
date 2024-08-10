## Krstic Example 

To run it, type
    
    python unroll.py
  
The SoC design without the lock mechanism is defined in `soc.py`
The SoC design with the lock mechanism is defined in `OoO.py`

In the subdirectory `mmodel`, there are two memory consistency model defined: TSO and SC.

If there is a satisfiable program that satisfies 
the property (defined [here](https://github.com/zhanghongce/ila-mcm-fmcad18/blob/ff48d6a3ab9beb16691424f785fc61d66b129f4c/Apps/krstic/unroll.py#L606))
it will be stored in the subdirectory `log` with the name `unroll.log`

