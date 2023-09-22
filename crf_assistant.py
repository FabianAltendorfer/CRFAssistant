import io
import os
import openai
import tempfile
import json
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk


'''
CREATOR: FABIAN ALTENDORFER
PUBLISHED UNDER MIT-LICENSE
'''

# PART 1 - GET INFORMATION FROM THE INTERNET

def financial_assistant(question):

    print("\n")
    print("### STARTED - ANALYZE QUESTION ###")
    print("\n")
    
    openai.api_key = [API KEY]

    question_file = question
    file_path = os.path.join(os.getcwd(), question_file)

   #with open(file_path, "r") as f: #Question File auslesen nicht mehr notwendig.
   #    question = f.read()
   #print(question)



    response = openai.Completion.create(
      model="davinci:ft-university-of-applied-sciences-upper-austria:financial-assistant-get-symbols-2023-03-13-06-08-36",
      prompt=question,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["END"]
    )

    json_obj = json.loads(str(response))
    text = json_obj['choices'][0]['text']
    values_list = text.split('\n')
    values_list = set(value for value in values_list if value != '')  # remove empty strings and use set to keep only unique values

    print(list(values_list))

    informations = []
    
    print("\n")
    print("### PART 1 - GATHERING INFORMATION ###")
    print("\n")

    for value in values_list:
        # Get Profit Margins and longBusinessSummary

        url_getsummary = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
        url_getfinancials = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"
        url_getquotes = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
        url_getrecommendations = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-recommendation-trend"


        querystring = {"symbol": value}
        querystring_getquotes = {"symbols": value}

        headers = {
            "X-RapidAPI-Key": [API KEY],
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
        

        
        # Get Summary Block
        try:
            response_getsummary = requests.request("GET", url_getsummary, headers=headers, params=querystring)
            response_json_getsummary = json.loads(response_getsummary.text)
            longBusinessSummary = {"longBusinessSummary": response_json_getsummary["summaryProfile"]["longBusinessSummary"]}
            profitMargins = {"profitMargins": response_json_getsummary["defaultKeyStatistics"]["profitMargins"]["fmt"]}
            summary = json.dumps(longBusinessSummary, indent=4)
            profitMargins = json.dumps(profitMargins, indent=4)
        except:
            summary = 0
        
        # Get Financials Block
        try:
            response_getfinancials = requests.request("GET", url_getfinancials, headers=headers, params=querystring)
            response_json_getfinancials = json.loads(response_getfinancials.text)
            try:
                last_cashflow_statement = response_json_getfinancials["cashflowStatementHistory"]["cashflowStatements"][0]
                cashflowStatement = {
                        k: v.get("longFmt") or v.get("fmt") if isinstance(v, dict) else v for k, v in last_cashflow_statement.items() if k in ["investments", "changeToLiabilities", "totalCashflowsFromInvestingActivities", "totalCashFromFinancingActivities", "netIncome", "changeInCash", "endDate", "effectOfExchangeRate", "totalCashFromOperatingActivities", "depreciation", "otherCashflowsFromInvestingActivities", "dividendsPaid", "changeToInventory", "changeToAccountReceivables", "otherCashflowsFromFinancingActivities"]
                    }
                cashflow_statement = json.dumps(cashflowStatement, indent=4) 
            except: 
                cashflow_statement = f"{value} No Cashflow Statement available"
            try:
                last_balance_sheet = response_json_getfinancials["balanceSheetHistory"]["balanceSheetStatements"][0]
                balanceSheet = {
                        k: v.get("longFmt") or v.get("fmt") if isinstance(v, dict) else v for k, v in last_balance_sheet.items() if k in ["totalAssets", "totalCurrentAssets", "totalLiab", "totalStockholderEquity", "totalCurrentLiabilities", "longTermDebt", "shortLongTermDebt", "totalLiabilitiesAndStockholderEquity", "totalCurrentLiabilities", "totalNonCurrentLiabilities", "totalStockholdersEquity"]
                    }
                balance_sheet = json.dumps(balanceSheet, indent=4)
            except:
                balance_sheet = f"{value} No Balance Sheet available"
        except:
            print(f"{value} No Financials available")
               
        # Get Quotes Block
        try:
            response_getquotes = requests.request("GET", url_getquotes, headers=headers, params=querystring_getquotes)
            response_json_getquotes = json.loads(response_getquotes.text)
            regular_market_price = "Regular Market Price: " + str(response_json_getquotes["quoteResponse"]["result"][0]["regularMarketPrice"])
        except:
            regular_market_price = f"{value} No Regular Market Price"
            
            
        # Get Recommendations
        try:
            response_getrecommendations = requests.request("GET", url_getrecommendations, headers=headers, params=querystring)
            response_json_getrecommendations = json.loads(response_getrecommendations.text)
            trend_data = "Recommendations: " + str(response_json_getrecommendations["quoteSummary"]["result"][0]["recommendationTrend"]["trend"])
        except:
            trend_data = f"{value} No Recommendations"
            
        if summary != 0:
            symbol_data = f"{summary}\n\n{profitMargins}\n\n{cashflow_statement}\n\n{balance_sheet}\n\n{regular_market_price}\n\n{trend_data}"
            if len(informations) <= 3:
                print("HEY THERE " + str(len(informations)))
                print("\n")
                print(symbol_data)
                informations.append(symbol_data)

    file_name = "Information.txt"
    file_path = os.path.join(os.getcwd(), file_name)
                
                
    results = ""
    for item in informations:
        results += item + "\n"
    print(results)

    with open(file_path, "w") as f:
        f.write(results)




    # PART 2 - USE INFORMATION
    
    print("\n")
    print("### PART 2 - ANALYZE SITUATION ###")
    print("\n")
    
    
    # Read Question
    file_path = os.path.join(os.getcwd(), question_file)

  #with open(file_path, "r") as f: #Question File auslesen nicht mehr notwendig
  # print(question)
  # print("\n")

    # Read Information
    informations_file = "Information.txt"
    file_path = os.path.join(os.getcwd(), informations_file)

    with open(file_path, "r") as f:
        informations = f.read()
    print(informations)
    print("\n")

    # Read Prompt
    prompt_file = "Prompt.txt"
    file_path = os.path.join(os.getcwd(), prompt_file)

    with open(file_path, "r") as f:
        prompt = f.read()
    print(prompt)


    # Replace placeholders
    prompt = prompt.replace("<<QUESTION>>", question)
    prompt_ready = prompt.replace("<<INFORMATION>>", informations)
    print(prompt_ready)


    openai.api_key = [API KEY]

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_ready,
      temperature=0.7,
      max_tokens=400,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["END"]
    )

    json_obj = json.loads(str(response))
    text = json_obj['choices'][0]['text']

    text ="Hello Fabian, \n" + text + "\n" + "I have sent you all the details in an email."

    answer_file = "Answer.txt"
    file_path = os.path.join(os.getcwd(), answer_file)
    with open(file_path, "w") as f:
        f.write(text)
        
        
        
        
    # PART 3 - AUSGABE via ELEVEN LABS API
    
    print("\n")
    print("### PART 3 - CREATING OUTPUT ###")
    print("\n")

    # ELEVEN LABS API KEY
    api_key = [API KEY]
    voice_id = "21m00Tcm4TlvDq8ikWAM"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }


    filename = "Answer.txt"

    with open(filename, "r") as file:
        content = file.read()
        
    print("\n")
    print(content)
    print("\n")

    data = {
        "text": content,
        "voice_id": voice_id,
        "voice_settings": {
            "stability": 0.25,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Request successful")

        # Load the audio data into an AudioSegment object
        audio_data = io.BytesIO(response.content)
        #pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
        print(audio_data)
        audio = AudioSegment.from_file(audio_data, format="mp3")

        # Play the audio
        play(audio)
    else:
        print(f"Error: Request failed (status code: {response.status_code})")
   
   
# GUI

def show_message():
    messagebox.showinfo("Working", "I will analyze the situation for you")

def on_ask():
    question = entry.get()
    entry.delete(0, tk.END)  # Clear the entry field
    # run_my_script(question)
    show_message()
    financial_assistant(question)

def on_voice_command():
    print("Voice command button clicked")
    # Add code to handle voice command functionality
    show_message()

# Create the main window
root = tk.Tk()
root.title("CRF Assistant")
root.geometry("500x300")
root.configure(bg="#FABB00")

# Load the logos
logo1 = PhotoImage(file="fincom_logo.png")
logo2 = PhotoImage(file="oberoesterreich_logo.png")
# Create the logo labels
logo1_label = ttk.Label(root, image=logo1, background="#FABB00")
logo2_label = ttk.Label(root, image=logo2, background="#FABB00")

# Place the logos at the bottom left and bottom right
logo1_label.place(x=30, y=260-logo1.height())
logo2_label.place(x=455-logo2.width(), y=280-logo2.height())

# Create a label with the name "CRF Assistant"
app_name_label = ttk.Label(root, text="CRF Assistant", font=("Arial", 24), background="#FABB00", foreground="black")
app_name_label.pack(pady=10)

# Create the entry field for the question
entry = ttk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)
entry.focus_set()

# Create the "Ask" button
ask_button = ttk.Button(root, text="Ask", command=on_ask)
ask_button.pack(pady=5)

# Create the "Voice Command" button
voice_command_button = ttk.Button(root, text="Voice Command", command=on_voice_command)
voice_command_button.pack(pady=5)

# Bind the Enter key to the on_ask function
root.bind("<Return>", lambda event: on_ask())

# Start the main loop
root.mainloop()