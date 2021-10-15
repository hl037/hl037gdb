define printr
  call (void)operator<<(std::cout, $arg0)
  printf "\n"
end

define vgdb
  target remote | vgdb
end

set history save on
set history filename ~/.cache/gdb_history

focus cmd

python import hl037gdb


