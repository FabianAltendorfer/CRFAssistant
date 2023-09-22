# CRFAssistant
CRFAssistant is a RAG Application that uses a finetuned GPT3-Model to answer user questions regarding investment decisions. To give advice, the finetuned model gives Stock tickers as output which are sent to the Yahoo Finance API to retrieve detailed financial information about the stocks in question.

To use it, you need to finetune an LLM to give a standard output in the form of (Example in German):

„Soll ich in den Bereich der kuenstlichen Intelligenz 
investieren?\n“, „completion“: „GOOGL\nAAPL\
nIBM\nMSFT\nINTC“}


Those stock tickers will be sent to Yahoo Finance to retrieve financial information.

The final result can be seen in this Youtube-Video: https://www.youtube.com/watch?v=-ENA95SvR7I&t=55s

This project was published under an MIT-License.
