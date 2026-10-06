import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

""" This plot was generated with google gemini. The data was extracted by Group 7 by using the blender program from the CLI """
# Load the dataset
df = pd.read_csv("render_benchmark.csv")

# Create a figure with 1 row and 2 columns
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), facecolor='#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

colors = ['#2c3e50', '#1a7f64']
samples = sorted(df["Samples"].unique())

# Loop through each sample group and plot them on their respective axes
for idx, sample_val in enumerate(samples):
    ax = axes[idx]
    ax.set_facecolor('#f8f9fa')
    sns.despine(ax=ax, top=True, right=True)
    
    # Filter data for the current subplot
    subset = df[df["Samples"] == sample_val]
    
    # Render standalone Boxplot
    sns.boxplot(
        x="Samples", 
        y="TotalRenderTime_Seconds", 
        data=subset,
        width=0.4,
        color=colors[idx],
        showfliers=True,  # Keeps standard outliers visible if there are any
        linewidth=2,
        ax=ax
    )
    
    # Styling and Labels
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#cccccc')
    ax.xaxis.grid(False)
    ax.set_xlabel("")
    
    # Only show the Y-axis label on the left-most plot
    if idx == 0:
        ax.set_ylabel("Total Render Time (Seconds)", fontsize=11, fontweight='semibold', color='#2b2b2b', labelpad=12)
    else:
        ax.set_ylabel("")
    
    x_label = f"{sample_val} Samples\nN = {len(subset)} runs"
    ax.set_xticklabels([x_label], fontsize=11, fontweight='semibold', color='#2b2b2b')
    
    # Dynamically scale the Y-axis for each subplot independently based on its own variance
    data_min = subset["TotalRenderTime_Seconds"].min()
    data_max = subset["TotalRenderTime_Seconds"].max()
    padding = (data_max - data_min) * 0.5
    if padding == 0: padding = 0.05
    ax.set_ylim(data_min - padding, data_max + padding * 2.5)
    
    # Median Annotations
    median = subset["TotalRenderTime_Seconds"].median()
    ax.text(
        0, 
        median + padding * 0.6, 
        f"Median: ~{median:.2f}s", 
        ha='center', 
        va='bottom', 
        fontsize=11.5, 
        fontweight='bold', 
        color='#222222'
    )
    
    ax.tick_params(axis='both', which='major', labelsize=10.5)

# Overall Figure Titles
plt.suptitle("Blender GPU Benchmark: Render Time Distribution", fontsize=16, fontweight='bold', color='#111111', y=1.02)
fig.text(0.5, 0.95, "Evaluating performance consistency across 25 independent runs for 32 vs 64 sample workloads", ha='center', fontsize=11, color='#555555')

plt.tight_layout()
plt.savefig("render_benchmark_split_no_scatters.png", dpi=300, bbox_inches="tight")
plt.show()
