import openai
import pandas as pd
import os
import time

# Load API key securely
openai.api_key = "YOUR API KEY HERE"

def query_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error interacting with ChatGPT: {e}")
        return "No response"

# Read CSV input with error handling
try:
    input_file = "YOUR CSV INPUT FILE PATH HERE"
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: Input file not found at {input_file}")
    exit()
except Exception as e:
    print(f"Error reading input file: {e}")
    exit()

# Output DataFrame
results = []

# Process each project
for _, row in df.iterrows():
    try:
        project_name = row.iloc[0]
        github_link = row.iloc[1]

        # ChatGPT prompt
        prompt = f"""First, review each project's GitHub repository, white paper, CoinMarketCap profile, and official website (if available). 
        Based on this information and documentation, classify each project's funding model (choose from the options below and list all applicable primary funding models):
        - Public Token Sale
        - Crowdfunding Without Token
        - Product/Service Sales Income
        - Donations
        - Others

        Definitions:
        - Donations: A gift of money, goods, services, or time made to an organization by an individual or entity without expecting anything in return.
        - Crowdfunding Without Token: Funding a project or venture by raising money from a large number of people, typically via the internet.
        Carefully distinguish between these two funding models.
        
        Please list all applicable funding models, as more than one may apply.
        
        Project: {project_name}
        Link: {github_link}
        """
        
        response = query_chatgpt(prompt)

        # Parse response
        funding_models = {
            "Public Token Sale": 0,
            "Crowdfunding Without Token": 0,
            "Product/Service Sales Income": 0,
            "Donations": 0,
            "Others": 0
        }

        for model in funding_models.keys():
            if f"{model}" in response:
                funding_models[model] = 1

        # Append to results
        results.append({
            "Project Name": project_name,
            "GitHub Link": github_link,
            "Public Token Sale": funding_models["Public Token Sale"],
            "Crowdfunding Without Token": funding_models["Crowdfunding Without Token"],
            "Product/Service Sales Income": funding_models["Product/Service Sales Income"],
            "Donations": funding_models["Donations"],
        })

        # Delay to handle rate limits
        time.sleep(1)

    except Exception as e:
        print(f"Error processing project {project_name}: {e}")
        results.append({
            "Project Name": project_name,
            "GitHub Link": github_link,
            "Public Token Sale": 0,
            "Crowdfunding Without Token": 0,
            "Product/Service Sales Income": 0,
            "Donations": 0,
        })

# Save results to CSV
try:
    output_file = "YOUR CSV OUTPUT FILE PATH HERE"
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")
except Exception as e:
    print(f"Error saving output file: {e}")
