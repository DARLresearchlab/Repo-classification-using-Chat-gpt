import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load both CSV files
ground_truth = pd.read_csv('ground truth file path')
ai_classified = pd.read_csv('chatgppt generated file path')

# Merge using GithubLink
ground_truth.columns = ground_truth.columns.str.strip()
ai_classified.columns = ai_classified.columns.str.strip()

# Merge using GithubLink
merged = pd.merge(ground_truth, ai_classified, on='GithubLink')

# Automatically detect AI label columns
ai_label_columns = ai_classified.columns[4:]

project_type_labels = sorted(set(ground_truth['ProjectType'].unique()) | set(ai_label_columns))

confusion_matrix = pd.DataFrame(0.0, index=project_type_labels, columns=project_type_labels)

# Populate confusion matrix
for _, row in merged.iterrows():
    true_label = row['ProjectType']
    ai_labels = [label for label in ai_label_columns if row[label] == 1]
    if ai_labels:
        fractional_weight = 1 / len(ai_labels)
        for predicted_label in ai_labels:
            confusion_matrix.loc[true_label, predicted_label] += fractional_weight

#  Filtering only frequent labels
row_threshold = 5
col_threshold = 5
filtered_confusion = confusion_matrix.loc[
    confusion_matrix.sum(axis=1) > row_threshold,
    confusion_matrix.sum(axis=0) > col_threshold
]

# Plotting with bigger figure and rotated labels
fig, ax = plt.subplots(figsize=(20, 16))
im = ax.imshow(filtered_confusion.values, cmap='Blues')

ax.set_xticks(np.arange(len(filtered_confusion.columns)))
ax.set_yticks(np.arange(len(filtered_confusion.index)))
ax.set_xticklabels(filtered_confusion.columns, rotation=90, ha="center")
ax.set_yticklabels(filtered_confusion.index)

plt.colorbar(im, ax=ax)
ax.set_xlabel("AI Classified (Predicted Label)")
ax.set_ylabel("Ground Truth (True Label)")
ax.set_title("Filtered Project Type Confusion Matrix (Fractionally Weighted)")

for i in range(len(filtered_confusion.index)):
    for j in range(len(filtered_confusion.columns)):
        value = filtered_confusion.values[i, j]
        if value > 0:
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", color="black")

plt.tight_layout()
plt.show()

# Accuracy summary
total_sum = confusion_matrix.values.sum()
correct_sum = np.trace(confusion_matrix.values)
accuracy = correct_sum / total_sum

print(f"Total sum: {total_sum:.4f}")
print(f"Correct (diagonal) sum: {correct_sum:.4f}")
print(f"Fractionally Weighted Accuracy: {accuracy:.4%}")
# Containment Accuracy Calculation
correct_count = 0
total_count = 0

for _, row in merged.iterrows():
    true_label = row['ProjectType']
    ai_labels = [label for label in ai_label_columns if row[label] == 1]

    if true_label in ai_labels:
        correct_count += 1
    total_count += 1

containment_accuracy = correct_count / total_count

print(f"Containment Accuracy (True Label Appears in AI Labels): {containment_accuracy:.4%}")
print(f"Total projects evaluated: {total_count}")
