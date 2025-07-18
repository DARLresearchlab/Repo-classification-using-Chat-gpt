import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your actual governance model CSV files
ground_truth = pd.read_csv('ground truth input file path')
ai_classified = pd.read_csv('ai classified input file path')

ground_truth.columns = ground_truth.columns.str.strip()
ai_classified.columns = ai_classified.columns.str.strip()

# Merge on GithubLink
merged = pd.merge(ground_truth, ai_classified, on='GithubLink')

# Detect AI governance label columns
ai_label_columns = ai_classified.columns[4:]

# Set confusion matrix labels
governance_labels = sorted(set(ground_truth['GovernanceModel'].unique()) | set(ai_label_columns))

# Initialize confusion matrix
confusion_matrix = pd.DataFrame(0.0, index=governance_labels, columns=governance_labels)

# Populate confusion matrix with fractional weights
for _, row in merged.iterrows():
    true_label = row['GovernanceModel']
    ai_labels = [label for label in ai_label_columns if row[label] == 1]
    if ai_labels:
        fractional_weight = 1 / len(ai_labels)
        for predicted_label in ai_labels:
            confusion_matrix.loc[true_label, predicted_label] += fractional_weight

# Containment Accuracy Calculation
correct_count = 0
total_count = 0
for _, row in merged.iterrows():
    true_label = row['GovernanceModel']
    ai_labels = [label for label in ai_label_columns if row[label] == 1]
    if true_label in ai_labels:
        correct_count += 1
    total_count += 1

containment_accuracy = correct_count / total_count

# Plot Confusion Matrix (Filtered for clarity)
fig, ax = plt.subplots(figsize=(16, 12))
im = ax.imshow(confusion_matrix.values, cmap='Blues')

ax.set_xticks(np.arange(len(confusion_matrix.columns)))
ax.set_yticks(np.arange(len(confusion_matrix.index)))
ax.set_xticklabels(confusion_matrix.columns, rotation=90, ha="center")
ax.set_yticklabels(confusion_matrix.index)

plt.colorbar(im, ax=ax)
ax.set_xlabel("AI Classified (Predicted Label)")
ax.set_ylabel("Ground Truth (True Label)")
ax.set_title("Governance Model Confusion Matrix")

for i in range(len(confusion_matrix.index)):
    for j in range(len(confusion_matrix.columns)):
        value = confusion_matrix.values[i, j]
        if value > 0:
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", color="black")

plt.tight_layout()
plt.show()

# Print Results
total_sum = confusion_matrix.values.sum()
correct_sum = np.trace(confusion_matrix.values)
accuracy = correct_sum / total_sum

print(f"Total sum: {total_sum:.4f}")
print(f"Correct (diagonal) sum: {correct_sum:.4f}")
print(f"Fractionally Weighted Accuracy: {accuracy:.4%}")
print(f"Containment Accuracy (True Label Appears in AI Labels): {containment_accuracy:.4%}")
print(f"Total projects evaluated: {total_count}")
