import os
import time
import threading
import tempfile
from collections import defaultdict


class DiskIOBenchmark:
    def __init__(self):
        self.size = 1
        self.benchmarks = defaultdict(list)
        self._setup()

    def _setup(self):
        self.fp = open("./test.txt", "wb")
        self.is_open = True
        self.bytes_written = 0
        self.duration = 2

    def compute_throughput(self):
        for _ in range(self.duration):
            time.sleep(1)
            self.benchmarks[self.size].append(self.bytes_written)
            self.bytes_written = 0
        self.is_open = False

    def write(self):
        bs = bytearray(os.urandom(self.size))
        while self.is_open:
            self.fp.write(bs)
            self.bytes_written += self.size

    def benchmark(self):
        for size in range(1, 8192, 1000):
            self.size = size
            self._setup()
            print("benchmarking for size", self.size)
            
            try:
                t1 = threading.Thread(target=self.compute_throughput)
                t2 = threading.Thread(target=self.write)
                
                t1.start()
                t2.start()

                t1.join()
                t2.join()
            except Exception as e:
                raise e
            finally:
                self.fp.close()

    def print_benchmarks(self):
        for size, throughputs in self.benchmarks.items():
            print(size, sum(throughputs)/len(throughputs))


bm = DiskIOBenchmark()
bm.benchmark()
bm.print_benchmarks()