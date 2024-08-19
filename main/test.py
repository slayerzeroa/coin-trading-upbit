# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from multiprocessing import Process, Queue
# import multiprocessing as mp
# import datetime
# import timer
# import time
#
#
# def producer(q):
#     proc = mp.current_process()
#     print(proc.name)
#
#     while True:
#         now = datetime.datetime.now()
#         data = str(now)
#         q.put(data)
#         time.sleep(1)
#
#
# class Consumer(QThread):
#     poped = pyqtSignal(str)
#
#     def __init__(self, q):
#         super().__init__()
#         self.q = q
#
#     def run(self):
#         while True:
#             if not self.q.empty():
#                 data = q.get()
#                 self.poped.emit(data)
#
#
# class MyWindow(QMainWindow):
#     def __init__(self, q):
#         super().__init__()
#         self.setGeometry(200, 200, 300, 200)
#
#         # thread for data consumer
#         self.consumer = Consumer(q)
#         self.consumer.poped.connect(self.print_data)
#         self.consumer.start()
#
#
#     @pyqtSlot(str)
#     def print_data(self, data):
#         self.statusBar().showMessage(data)
#
#
# if __name__ == "__main__":
#     q = Queue()
#
#     # producer process
#     p = Process(name="producer", target=producer, args=(q, ), daemon=True)
#     p.start()
#
#     # Main process
#     app = QApplication(sys.argv)
#     mywindow = MyWindow(q)
#     mywindow.show()
#     app.exec_()



import multiprocessing as mp
import time

def worker():
    proc = mp.current_process()
    print(proc.name)
    print(proc.pid)
    time.sleep(5)
    print("SubProcess End")


if __name__ == "__main__":
    # main process
    proc = mp.current_process()
    print(proc.name)
    print(proc.pid)

    # process spawning
    p = mp.Process(name="SubProcess", target=worker)
    p.start()

    print("MainProcess End")
