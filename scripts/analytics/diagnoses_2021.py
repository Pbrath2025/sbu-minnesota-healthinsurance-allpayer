import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Load the dataset (modify the filename if needed)
file_path = 'data/processed/diagnoses2021.csv'
df = pd.read_csv(file_path)

### 1. Understanding Diagnosis Code Distribution ###
# Get the top 10 most common principal diagnosis codes
top_10_diagnoses = df['principal_diagnosis_code'].value_counts().nlargest(10)

# Bar Chart
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_diagnoses.index, y=top_10_diagnoses.values, palette="viridis")
plt.xlabel("Principal Diagnosis Code")
plt.ylabel("Count")
plt.title("Top 10 Most Common Diagnosis Codes")
plt.xticks(rotation=45)
plt.show()

### 2. Diagnosis vs. Total Paid Amount ###
# Group by diagnosis code and calculate the mean total paid amount
diagnosis_paid_mean = df.groupby('principal_diagnosis_code')['total_paid_amt_sum'].mean().nlargest(5)

# Boxplot for top 5 diagnoses
top_5_diagnoses = diagnosis_paid_mean.index
df_top_5 = df[df['principal_diagnosis_code'].isin(top_5_diagnoses)]

plt.figure(figsize=(12, 6))
sns.boxplot(x="principal_diagnosis_code", y="total_paid_amt_sum", data=df_top_5, palette="coolwarm")
plt.xlabel("Principal Diagnosis Code")
plt.ylabel("Total Paid Amount")
plt.title("Distribution of Total Paid Amount for Top 5 Diagnoses")
plt.xticks(rotation=45)
plt.show()

### 3. Diagnoses by Age Group ###
# Create a contingency table
contingency_table = pd.crosstab(df['age_group_name'], df['principal_diagnosis_code'])

# Identify top 3 diagnoses for each age group
top_3_by_age = df.groupby('age_group_name')['principal_diagnosis_code'].value_counts().groupby(level=0).head(3)
print("Top 3 Diagnoses for Each Age Group:")
print(top_3_by_age)

# Chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"\nChi-square Test Result: χ²={chi2:.2f}, p-value={p:.4f}")
if p < 0.05:
    print("Significant difference in diagnosis distribution across age groups.")
else:
    print("No significant difference in diagnosis distribution across age groups.")

### 4. Insurer vs. Member Payment Differences ###
# Group by diagnosis code and calculate means
payment_means = df.groupby('principal_diagnosis_code')[['insurer_paid_amt_mean', 'member_paid_amt_mean']].mean()

# Top diagnoses with highest member out-of-pocket costs
top_member_paid = payment_means['member_paid_amt_mean'].nlargest(5)
print("\nTop 5 Diagnoses with Highest Member Out-of-Pocket Costs:")
print(top_member_paid)

# Scatter plot: Insurer Paid vs. Member Paid
plt.figure(figsize=(10, 6))
sns.scatterplot(x='insurer_paid_amt_mean', y='member_paid_amt_mean', data=payment_means, alpha=0.7)
plt.xlabel("Insurer Paid Mean")
plt.ylabel("Member Paid Mean")
plt.title("Insurer vs. Member Payment Differences")
plt.show()
