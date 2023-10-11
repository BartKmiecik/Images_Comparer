import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV data into a DataFrame
navara = pd.read_csv('Navara.csv', header=0, index_col=0)
juke = pd.read_csv('Juke.csv', header=0, index_col=0)
qashqai = pd.read_csv('Qashqai.csv', header=0, index_col=0)
pathfinder = pd.read_csv('Pathfinder.csv', header=0, index_col=0)

# plt.figure(figsize=(10, 8))
# sns.set(font_scale=1.2)  # Adjust font size
# sns.heatmap(navara, cmap='YlGnBu', linewidths=1, square=True, cbar_kws={'label': 'Values'})
# plt.title('Heatmap of CSV Data')
# # plt.xticks(rotation=45)
# plt.show()

fig, axes = plt.subplots(1, 4, figsize=(12, 6))

# First heatmap on the left
plt.sca(axes[0])
ax = sns.heatmap(navara, cmap='YlGnBu', linewidths=1, square=True)
plt.ylim(0,36)
plt.xlim(0,6)
plt.title('Navara')
# plt.xticks(rotation=45)


# Second heatmap on the right
plt.sca(axes[1])
sns.heatmap(juke, cmap='YlGnBu', linewidths=1, square=True)
plt.ylim(0,36)
plt.xlim(0,6)
plt.title('Juke')
# plt.xticks(rotation=45)

plt.sca(axes[2])
sns.heatmap(qashqai, cmap='YlGnBu', linewidths=1, square=True)
plt.ylim(0,36)
plt.xlim(0,6)
plt.title('Qashqai')
# plt.xticks(rotation=45)

plt.sca(axes[3])
sns.heatmap(qashqai, cmap='YlGnBu', linewidths=1, square=True, cbar_kws={'label': 'MSE'})
plt.ylim(0,36)
plt.xlim(0,6)
plt.title('Pathfinder')
# plt.xticks(rotation=45)

# Adjust spacing between subplots
plt.tight_layout()

plt.show()
