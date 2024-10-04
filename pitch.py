import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

figure, axes = plt.subplots()
center_circle = plt.Circle((0, 2400), 800, facecolor='None', edgecolor='white', lw=2)
center_point = plt.Circle((0, 2400), 25, facecolor='None', edgecolor='white', lw=2.5)
penatly_point = plt.Circle((3500, 2400), 25, facecolor='None', edgecolor='white', lw=2.5)

axes.set_facecolor('forestgreen')
axes.set_aspect(1)
axes.add_artist(center_circle)
axes.add_artist(center_point)
axes.add_artist(penatly_point)

plt.gca().add_patch(Rectangle((3000,1000),1500,2800,
                    edgecolor='white',
                    facecolor='none',
                    lw=2))

plt.gca().add_patch(Rectangle((4000,1700),500,1400,
                    edgecolor='white',
                    facecolor='none',
                    lw=2))

plt.plot([0,0],[0,4800], color="white")
plt.plot([0,4500],[4800,4800], color="white")
plt.plot([4500,4500],[4800,0], color="white")
plt.plot([4500,0],[0,0], color="white")
plt.plot([4500,4500],[0,4800], color="white")

plt.xticks([])
plt.yticks([])

plt.xlim(-100,4600)
plt.ylim(-100,4900)

plt.savefig('pitch.png', bbox_inches='tight', dpi=1200)
# plt.show()