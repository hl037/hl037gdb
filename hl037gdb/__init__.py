
import re
import click
import gdb
import shlex
from click.exceptions import Exit, Abort, ClickException
import click

def invoke_click_cmd(cmd, name, args, **extra):
  try :
    ctx = cmd.make_context(name, args, parent = None, **extra)
    cmd.invoke(ctx)
  except Exit : 
    pass
  except ClickException as exc : 
    raise

cur_cmd = None
def dont_repeat():
  cur_cmd.dont_repeat()
  
class CMD(gdb.Command):
  def __init__(self, name, click_cmd):
    self.name = name
    self.click_cmd = click_cmd
    super().__init__(name, gdb.COMMAND_USER)

  def invoke(self, argument, from_tty):
    cur_cmd = self
    invoke_click_cmd(self.click_cmd, self.name, shlex.split(argument))

def gdb_cmd(f):
  _f = click.command()(f)
  CMD(f.__name__, _f)
  return _f



def common_vxb_vbits(is_addr, obj, size):
  if len(size) == 0 :
    size = None
  else :
    size, = size
    size = str(int(size, 0))
    
  if is_addr :
    addr = hex(int(obj, 0))
  else :
    v = gdb.parse_and_eval(obj)
    t = v.type
    if v.type.code != gdb.TYPE_CODE_PTR:
      v = v.address
      if v is None :
        raise RuntimeError('Non addressable object')
      t = v.type
    addr = v.format_string(format='x')
    if size is None :
      size = str(t.target().sizeof)
  return addr, size
  


@gdb_cmd
@click.option('-a', '--is_addr', help="The first argument is an address")
@click.argument('obj')
@click.argument('size', nargs=-1)
def vxb(*args, **kwargs):
  addr, size = common_vxb_vbits(*args, **kwargs)
  gdb.execute(f'mo xb {addr} {size}')


@gdb_cmd
@click.option('-a', '--is_addr', help="The first argument is an address")
@click.argument('obj')
@click.argument('size', nargs=-1)
def vbits(*args, **kwargs):
  addr, size = common_vxb_vbits(*args, **kwargs)
  gdb.execute(f'mo get_vbits {addr} {size}')
  


