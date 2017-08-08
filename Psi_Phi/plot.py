import matplotlib.pyplot as plt
plt.switch_backend('agg')
import seaborn as sns



sns_plot = \
(sns.jointplot(psi, phi, size=12, space=0, xlim=(-190, 190), ylim=(-190, 190)).plot_joint(sns.kdeplot, zorder=0,
                                                                                         n_levels=6))

# sns_plot = sns.jointplot(psi_list_numpy, phi_list_numpy, kind="hex", color="#4CB391")  # stat_func=kendalltau
# sns_plot.ylim(-180, 180)
print "plotting: ", pfam
sns_plot.savefig("Ramachandranplot_scatter/ramachandranplot_" + pfam + ".png")