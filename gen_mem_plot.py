import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

""" Disclaimer: This code was generated with google gemini."""

# Load the data from your csv
df = pd.read_csv('render_benchmark.csv')

# Create a single figure canvas
plt.figure(figsize=(8, 5))

# Scatter plot showing memory stability across all runs
sns.scatterplot(
    data=df, x='Run', y='PeakMemory_MB', hue='Samples', 
    palette=['#4C72B0', '#DD8452']
)

plt.title('Peak Memory Usage per Run')
plt.ylabel('Peak Memory (MB)')
plt.xlabel('Run Number')
plt.ylim(435, 455) # Zoomed in to show the flat line clearly

plt.tight_layout()
plt.savefig('PeakMemUsage.png', dpi=300)
plt.show()
