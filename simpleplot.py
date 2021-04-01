import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('./results/sfMSFT.csv', na_values='.')
#data = pd.read_csv('./results/latency_MSFT.csv', na_values='.')
#data = pd.read_csv('./results/latency_AAPL.csv', na_values='.')
#data = pd.read_csv('./results/latency_IBM.csv', na_values='.')

print(data)

# plt.figure(figsize=(4, 3))
plt.boxplot(data)
plt.xticks((1,), ('MSFT',))
plt.title('Simple Flood Approach')
plt.xlabel('Broker Topic(s)')
plt.ylabel('Time (ms)')
plt.ylim((0, 1.5))
plt.savefig('./results/simple_flooding.png')
plt.show()