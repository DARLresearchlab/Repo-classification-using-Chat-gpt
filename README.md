# README

We first attempted to filter out open-source software (OSS) projects that had not been active for a long time from a pool of 6,000 OSS projects. Using the GitHub API endpoint, we determined the duration distribution and plotted four types of graphs for these projects:
1. All projects without filters.
2. Projects with a 30-day filter.
3. Projects with a 60-day filter.
4. Projects with a 90-day filter.

However, we ultimately abandoned this approach due to survivorship bias and the surge in cryptocurrency activity in 2020.

---

Next, we analyzed **600 projects** using ChatGPT for two distinct AI scenarios:
1. One with a framework providing specific classification key terms for ChatGPT to select from.
2. Another without the framework, where ChatGPT generated classifications independently before sorting them into given categories.

We compared the classification results from both scenarios with manually collected classifications of over 600 OSS projects from the summer. The framework-based scenario resulted in a following accuracy rates:
- **Funding model accuracy rate**: 73%.
- **Governance model accuracy rate**: 95%.
- **Project type accuracy rate**: 69%.

---

## Accuracy and Verification

To ensure the accuracy of the manually collected classifications:
- We double-checked **60 projects**, 46 of which had clear classifications.
- A **confusion matrix** (Figure 1) was created, where:
  - The y-axis represents the actual classifications.
  - The x-axis represents the AI classifications.
  - Diagonal entries show correctly classified projects.

The AI correctly classified **50%** of the projects, with the highest number of accurate classifications in the "Product/Service Sales Income" category. Most classifications clustered around the diagonal.

---

## ChatGPT-4 Classification Process

We used **ChatGPT-4** to classify the funding models of **516 manually collected OSS projects**. These projects were submitted to ChatGPT in **batches of 12**, with project names and GitHub links provided for classification. Clear instructions were given, including a list of funding model categories for ChatGPT to choose from.

### Challenges and Improvements
- After processing 3–4 batches, ChatGPT often classified all projects under an "unspecified" category.
- We reiterated the instructions, which improved accuracy upon reclassification.
- Weighted dual classifications were used, allowing certain projects to have multiple classifications.

The AI classification accuracy was **47.4%** (Figure 2).

---

## Prompt Refinement

To address mismatches, particularly between **"Donations"** and **"Crowdfunding Without Token"**, we enhanced ChatGPT-4 prompts by including definitions for both categories. Each message included the following prompt:
First, review each project's GitHub repository, white paper, CoinMarketCap profile, and official website (if available). Based on this information and documentation, classify each project's funding model (choose from the options below and list all applicable primary funding models): Public Token Sale, Crowdfunding Without Token, Product/Service Sales Income, Donations, and Others. Definitions: Donations: A gift of money, goods, services, or time made to an organization by an individual or entity without expecting anything in return.
Crowdfunding Without Token: Funding a project or venture by raising money from a large number of people, typically via the internet.
Carefully distinguish between these two funding models. Please list all applicable funding models, as more than one may apply.


---

## Updated Results

After improving the prompt:
- A weighted confusion matrix improved the accuracy rate to **49%**.
- Another matrix (Figure 4) allowing overlapping models increased accuracy to **53.1%**.
- For **45 projects** analyzed individually, we achieved a similarity rate of **70.6%** using **Manhattan Distance**.

For larger batches:
- **200 projects**: Accuracy rate of **69.12%**.
- **1,000 projects**: Processing 5 projects per batch using ChatGPT-4 API manually.

---

## Automation 

To automate classification:
1. **API-Based Automation**: Used ChatGPT-3.5 Turbo.
2. **Selenium Automation**: Automated ChatGPT-4 using a Google Chrome driver.

### Reference Files
- `Funding_models_classifications`: API-based automation using GPT-3.5.
- `Funding_models_classifications_Selenium`: Automation using Selenium.

---
## Note 

- One of the challenges we encountered was related to sending multiple project prompts in the same ChatGPT session. This often resulted in inappropriate responses for the classification of funding models. For instance, batches of projects would sometimes not be classified under any of the predefined funding models, leading to inconsistencies. To address this, we ensured that each batch was submitted in a new, isolated chat session, which helped mitigate the issue and improve classification accuracy.
