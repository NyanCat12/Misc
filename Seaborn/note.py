"""
Grouped violinplots with split violins
======================================

_thumb: .5, .47
Seaborn version 0.7.1
"""
import seaborn as sns
sns.set(style="whitegrid", palette="pastel", color_codes=True)

# Load the example tips dataset
tips = sns.load_dataset("tips")
print (tips)
# Draw a nested violinplot and split the violins for easier comparison
sns_plot = sns.violinplot(x="day", y="total_bill", hue="sex", data=tips, split=True,
               inner="quart", palette={"Male": "b", "Female": "y"})
sns_pair = sns.pairplot(data=tips, hue = 'sex', diag_kind = 'kde')

sns.despine(left=True)
sns.plt.show()

fig = sns_plot.get_figure()
fig.savefig('a.jpg')

#PairGrid类图像保存
fig2 = sns_pair.fig
fig2.savefig('b.jpg')
