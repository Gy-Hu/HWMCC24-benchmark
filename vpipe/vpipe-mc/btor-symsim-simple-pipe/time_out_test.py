from ast import arg
import threading
import time
class MyThread(threading.Thread):
  def __init__(self, func, args):
    super(MyThread, self).__init__()
    self.func = func
    self.args = args

  def run(self):
    self.result = self.func(self.args)

  def get_result(self):
    try:
      return self.result
    except Exception:
      return None
  
def func1(txt):
  time.sleep(4)
  print(str(txt)+'not return')
  return(str(txt)+'return')

if __name__ == '__main__':
  txt = '123'
  t = MyThread(func=func1, args=(txt))
  t.setDaemon(True)
  t.start()

  t.join(timeout=3)
  
  print(t.get_result())
  print('over!')