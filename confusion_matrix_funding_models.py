import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load both CSV files
ground_truth = pd.read_csv('ground truth input file path')
ai_classified = pd.read_csv('ai classified input file path')

funding_labels = [
    'Public Token Sale',
    'Crowdfunding Without Token',
    'Product/Service Sales Income',
    'Donations',
    # 'Others' intentionally excluded now
]

# Remove "Others" rows from ground truth BEFORE merging
ground_truth = ground_truth[ground_truth['FundingModel'].str.strip() != 'Others']

# Merge on GithubLink
merged = pd.merge(ground_truth, ai_classified, on='GithubLink')

# Keep only rows with valid ground truth labels
filtered = merged[merged['FundingModel'].isin(funding_labels)].copy()

# Initialize weighted confusion matrix
weighted_cm = pd.DataFrame(0.0, index=funding_labels, columns=funding_labels)

for _, row in filtered.iterrows():
    true_label = row['FundingModel']
    ai_labels = [label for label in funding_labels if row[label] == 1]

    if ai_labels:
        fractional_weight = 1 / len(ai_labels)
        for predicted_label in ai_labels:
            weighted_cm.loc[true_label, predicted_label] += fractional_weight

# Visualizations and reporting same as before
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(weighted_cm.values, cmap='Blues')

ax.set_xticks(np.arange(len(funding_labels)))
ax.set_yticks(np.arange(len(funding_labels)))
ax.set_xticklabels(funding_labels, rotation=45, ha="right")
ax.set_yticklabels(funding_labels)

plt.colorbar(im, ax=ax)
ax.set_xlabel("AI Classified (Predicted Label)")
ax.set_ylabel("Ground Truth (True Label)")
ax.set_title("Fractionally Weighted Confusion Matrix (Excluding 'Others')")

for i in range(len(funding_labels)):
    for j in range(len(funding_labels)):
        value = weighted_cm.values[i, j]
        ax.text(j, i, f"{value:.2f}", ha="center", va="center", color="black")

plt.tight_layout()
plt.show()

print("Ground truth value counts (excluding 'Others'):")
print(filtered['FundingModel'].value_counts())

print("\nAI-classified label counts (excluding 'Others'):")
print(pd.DataFrame({label: (filtered[label] == 1).sum() for label in funding_labels}, index=['Count']).T)

total_sum = weighted_cm.values.sum()
correct_sum = weighted_cm.values.diagonal().sum()
accuracy = correct_sum / total_sum

print(f"Total sum: {total_sum:.4f}")
print(f"Correct (diagonal) sum: {correct_sum:.4f}")
print(f"Fractionally Weighted Accuracy: {accuracy:.4%}")

merged['AI_Label_Count'] = merged[funding_labels].sum(axis=1)
print(merged['AI_Label_Count'].value_counts())

correct_count = 0
total_count = 0

for _, row in filtered.iterrows():
    true_label = row['FundingModel']
    ai_labels = [label for label in funding_labels if row[label] == 1]
    
    if true_label in ai_labels:
        correct_count += 1
    total_count += 1

containment_accuracy = correct_count / total_count

print(f"Containment Accuracy (True Label Appears in AI Labels): {containment_accuracy:.4%}")
print(f"Total projects evaluated: {total_count}")
print(f"Rows skipped (AI labels empty): {(filtered[funding_labels].sum(axis=1) == 0).sum()}")
empty_ai_label_rows = filtered[filtered[funding_labels].sum(axis=1) == 0]

# Print project names and GitHub links where AI labels are empty
print(empty_ai_label_rows[['GithubLink']])
print(f"Total projects with empty AI labels: {empty_ai_label_rows.shape[0]}")
