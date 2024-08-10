from ast import arg
import threading
import time
class MyThread(threading.Thread):
  def __init__(self, func, args0, args1):
    super(MyThread, self).__init__()
    self.func = func
    self.args0 = args0
    self.args1 = args1

  def run(self):
    self.result = self.func(self.args0, self.args1)

  def get_result(self):
    try:
      return self.result
    except Exception:
      return None
  
def func1(txt, txt2):
  print('here!')
  time.sleep(1)
  # print(str(txt)+str(txt2)+'not return')
  return(str(txt)+str(txt2)+'return')

if __name__ == '__main__':
  txt = '123'
  txt2 = '456'
  t = MyThread(func=func1, args0=txt, args1=txt2)
  t.setDaemon(True)
  t.start()
  

  t.join(timeout=3)
  # assert not (t.get_result() == None)
  print(t.get_result())
  print('over!')