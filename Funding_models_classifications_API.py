import openai
import pandas as pd
import os
import time

# Load API key securely
openai.api_key = "your_api_key_here"

def query_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error interacting with ChatGPT: {e}")
        return "No response"

# Read Excel input with error handling
try:
    input_file = "your excel file path link here"
    df = pd.read_excel(input_file)
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
        prompt = f"""Please classify the project's funding model based on its GitHub repository, white paper, CoinMarketCap, and official website (if available). 
        Respond in the following format (include only applicable funding models):
        - Public Token Sale: [Yes/No]
        - Product/Service Sales Income: [Yes/No]
        - Donations: [Yes/No]
        - Crowdfunding Without Token: [Yes/No]

        Project: {project_name}
        Link: {github_link}
        """
        
        response = query_chatgpt(prompt)

        # Parse response
        funding_models = {
            "Public Token Sale": 0,
            "Crowdfunding Without Token": 0,
            "Product/Service Sales Income": 0,
            "Donations": 0
        }

        for model in funding_models.keys():
            if f"{model}: Yes" in response:
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

# Save results to Excel
try:
    output_file = "your output file path here"
    output_df = pd.DataFrame(results)
    output_df.to_excel(output_file, index=False)
    print(f"Output saved to {output_file}")
except Exception as e:
    print(f"Error saving output file: {e}")
