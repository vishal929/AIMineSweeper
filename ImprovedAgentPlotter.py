# file serves to plot our results with matplotlib

# This serves as a driver to generate a plot for Strategy1 using matplotlib

# calls strategy1 probability helper function and uses it to generate a plot

import ImprovedProbabilityHelper
from ImprovedKnowledgeBase import ImprovedKnowledgeBase
import matplotlib.pyplot as plt


result = ImprovedProbabilityHelper.improvedProbabilityHelper(50,25,ImprovedKnowledgeBase.randomCellToQuery)
# now performing matplotlib logic to generate the graph


#including data points

plt.scatter(*zip(*result))
plt.plot(*zip(*result))
plt.title("Average Success vs Mine Density (on 50x50 board)")
plt.xlabel("Mine Density")
plt.ylabel("Average Success (from 25 trials)")
plt.xticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.yticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.show()