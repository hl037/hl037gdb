
This is my personal GDB configuration.

As of today, it provides the following commands :

  - `vgdb` : performs `target remote | vgdb` providing a shortcut to debug valgrind'ed programs
  - `vxb [-a] obj [size]` : provides a shortcut to `mo xb obj size`. if `-a` is specified, then obj is a passed as is to `mo xb`, else, its address is passed. If size is not specified, it is guessed from the size of the type of obj.
  - `vbits [-a] obj [size]` same as `vxb` but with `mo get_vbits`.


