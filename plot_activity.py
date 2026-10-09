import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("activity_over_time.csv")

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.dropna().sort_values("Year")
df["Year"] = df["Year"].astype(int)

plt.figure(figsize=(9, 4.5))
plt.plot(df["Year"], df["Commits"], marker="o", linewidth=2, color="#2c3e50")
plt.fill_between(df["Year"], df["Commits"], color="#3498db", alpha=0.15)

plt.title("Blender Development Activity Over Time (Annual Commits)", fontsize=13, weight="bold")
plt.xlabel("Year", fontsize=11)
plt.ylabel("Commits per Year", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.5)

plt.xticks(df["Year"][::2], rotation=45)
plt.tight_layout()

plt.savefig("activity_over_time.png", dpi=300)
print("Graph saved as activity_over_time.png")
