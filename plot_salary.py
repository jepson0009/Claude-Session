import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("toy_hr_data.csv")

mean_salary = df["salary"].mean()
median_salary = df["salary"].median()

fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df["salary"], bins=15, color="steelblue", edgecolor="white", alpha=0.85)

ax.axvline(mean_salary, color="red", linewidth=2, linestyle="--", label=f"Mean: ${mean_salary:,.0f}")
ax.axvline(median_salary, color="blue", linewidth=2, linestyle="-", label=f"Median: ${median_salary:,.0f}")

ymax = ax.get_ylim()[1]
ax.text(mean_salary, ymax * 0.95, f"Mean\n${mean_salary:,.0f}",
        color="red", ha="center", va="top", fontsize=9, fontweight="bold")
ax.text(median_salary, ymax * 0.83, f"Median\n${median_salary:,.0f}",
        color="blue", ha="center", va="top", fontsize=9, fontweight="bold")

ax.set_xlabel("Salary ($)", fontsize=12)
ax.set_ylabel("Number of Employees", fontsize=12)
ax.set_title("Distribution of Employee Salaries", fontsize=14)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("salary_distribution.png", dpi=150)
print(f"Mean: ${mean_salary:,.0f}  |  Median: ${median_salary:,.0f}")
