import numpy
import matplotlib.pyplot as plt
import pandas as pd

data_AAPL = numpy.loadtxt(fname='./results/latency_AAPL.csv').transpose()
data_MSFT = numpy.loadtxt(fname='./results/latency_MSFT.csv').transpose()
data_NFLX = numpy.loadtxt(fname='./results/latency_NFLX.csv').transpose()

#my_dict = {'AAPL': data_AAPL, 'MSFT': data_MSFT, 'NFLX': data_NFLX}
my_dict = {'AAPL': data_AAPL, 'MSFT': data_MSFT, 'NFLX': data_NFLX}

fig, ax = plt.subplots()
ax.boxplot(my_dict.values(), meanline=True, showmeans=True)
ax.set_xticklabels(my_dict.keys())
plt.title('Complex Flood Approach')
plt.xlabel('Subscriber Topic(s)')
plt.ylabel('Time (ms)')
plt.ylim((0, 4.0))
plt.savefig('./results/complex_flooding.png')

plt.show()