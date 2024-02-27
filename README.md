# CRFAssistant
CRFAssistant is a RAG (Retrieval-Augmented Generation) application that utilizes a fine-tuned GPT-3 model to assist users with investment decision-making. The fine-tuned model outputs stock tickers in response to user queries, which are then used to fetch detailed financial information from the Yahoo Finance API regarding the stocks of interest. With CRFAssistant, I have analyzed the hallucination behavior of large language models (LLMs) when processing structured financial data. All components (except the APIs) were written by me in Python.

![image](https://github.com/FabianAltendorfer/CRFAssistant/assets/98153318/2381c824-a6b7-4451-a3bc-302104323968)

To utilize this application, you need to fine-tune a Large Language Model (LLM) to produce a standardized output format. For example, in German:

"Soll ich in den Bereich der künstlichen Intelligenz investieren?\n", "completion": "GOOGL\nAAPL\nIBM\nMSFT\nINTC"

These stock tickers are subsequently sent to Yahoo Finance to retrieve financial information. The process is as follows (please note that in this uploaded Version, I didn't use an open-source model but GPT3 from OpenAI)
![image](https://github.com/FabianAltendorfer/CRFAssistant/assets/98153318/c898f070-913d-4b0a-95ca-f28ad72d21d6)

You can view the final result in this YouTube video: https://www.youtube.com/watch?v=-ENA95SvR7I&t=55s

This project is published under the MIT License.
