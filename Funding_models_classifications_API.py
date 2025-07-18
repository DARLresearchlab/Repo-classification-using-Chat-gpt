import openai
import pandas as pd
import os
import time

# Load API key securely
openai.api_key = "your api key" 

def query_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error interacting with ChatGPT: {e}")
        return "No response"

# Read CSV input with error handling
input_path = "your csv input file path"

try:
    df = pd.read_csv(input_path)
except Exception as exc:
    raise SystemExit(f"  Failed to load {input_path}: {exc}")

blank_model_flags = {
    "Public Token Sale": 0,
    "Crowdfunding Without Token": 0,
    "Product/Service Sales Income": 0,
    "Donations": 0,
    "Others": 0, 
}

results = []
start_time = time.time()

for idx, row in df.iterrows():
    ProjectName = row["ProjectName"]
    GithubLink = row["GithubLink"]

    print(f"\n Processing ({idx + 1}/{len(df)}): {GithubLink}")

    # ETA estimate
    elapsed = time.time() - start_time
    avg_time = elapsed / (idx + 1)
    remaining = avg_time * (len(df) - (idx + 1))
    print(f" Estimated time remaining: {int(remaining)}s")

    try:
        prompt = f"""
First, review the project's GitHub repository (and any linked docs) at:
{GithubLink}

Based on all publicly available material, classify **every** relevant funding model category that fits the project.  
Use ONLY the labels below and mark every one that applies (0/1 is fine):

        - Public Token Sale
        - Crowdfunding Without Token
        - Product/Service Sales Income
        - Donations
        - Others

        Definitions:
        - Donations: A gift of money, goods, services, or time made to an organization by an individual or entity without expecting anything in return.
        - Crowdfunding Without Token: Funding a project or venture by raising money from a large number of people, typically via the internet.
        Carefully distinguish between these two funding models.
        
Return your answer as a simple bullet list or CSV line of the labels that apply.
"""

        reply = query_chatgpt(prompt)

        model_flags = blank_model_flags.copy()
        for label in model_flags:
            if label.lower() in reply.lower():
                model_flags[label] = 1

        results.append({
            "GithubLink": GithubLink,
            "ProjectName": ProjectName,
            **model_flags
        })

        # Autosave progress every 10 rows
        if (idx + 1) % 10 == 0:
            pd.DataFrame(results).to_csv("intermediate_output.csv", index=False)
            print("💾 Progress saved to intermediate_output.csv")

        time.sleep(1)

    except Exception as exc:
        print(f" Error on {GithubLink}: {exc}")
        results.append({
            "GithubLink": GithubLink,
            "ProjectName": ProjectName,
            **{k: 0 for k in blank_model_flags}
        })

# Save final results
output_path = "your output file path" 
try:
    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"\n Final output saved to {output_path}")
except Exception as exc:
    print(f" Could not save final CSV: {exc}")

