import xml.etree.ElementTree as ET
from os.path import exists
import matplotlib.pyplot as plt
from itertools import chain
from statistics import mean
from operator import itemgetter

year_range = range(2008,2023)
y1 = [y + (6/12) for y in year_range]
y2 = [y + (11/12) for y in year_range]
y = list(chain.from_iterable(zip(y1, y2)))[:-1] # Slice off November 2022

# key: country name
# value: list, index: timestep
#              value: list, index: input order
#                           value: efficiency
efficiency = dict()
i = 0
for year in year_range:
    for month in ['06', '11']:
        fp = 'data/TOP500_' + str(year) + month + '_all.xml'
        if not exists(fp):
            print("File not found: " + fp)
            continue

        fh = open(fp)
        tree = ET.parse(fh)
        root = tree.getroot()
        ns = {'top500': 'http://www.top500.org/xml/top500/1.0'}

        for site in root:
            country = site.find('top500:country', ns).text
            rmax = float(site.find('top500:r-max', ns).text)
            power = site.find('top500:power', ns).text
            if power:
                power = float(power)
                if float(power) > 0:
                    if country not in efficiency:
                        efficiency[country] = [None] * len(y)
                    if efficiency[country][i] is None:
                        efficiency[country][i] = []
                    efficiency[country][i].append(rmax / float(power))

        i += 1

# key: country name
# value: list, index: timestep
#              value: max or avg
best = dict()
avg = dict()
best_single = dict()
for country, values in efficiency.items():
    best[country] = [0] * len(y)
    avg[country] = [0] * len(y)
    for i in range(len(y)):
        if values[i]:
            best[country][i] = max(values[i])
            avg[country][i] = mean(values[i])
    best_single[country] = max(best[country])

# N = 5
# best_single = dict(sorted(best_single.items(), key = itemgetter(1), reverse = True)[:N])

figure, axis = plt.subplots(2)
axis[0].set_title("Best Single Site")
axis[0].set_yscale('log')
axis[0].set_ylabel('Power Effeciency (MFlops/Watt)')
axis[1].set_title("Average Site")
axis[1].set_ylabel('Power Effeciency (MFlops/Watt)')
axis[1].set_yscale('log')

for country in ['United States', 'China', 'Russia', 'Japan', 'Finland', 'France']:
    axis[0].plot(y, best[country], label=country)
    axis[1].plot(y, avg[country], label=country)

axis[0].legend()
axis[1].legend()
plt.show()