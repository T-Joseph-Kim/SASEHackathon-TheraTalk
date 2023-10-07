import os

os.environ["OPEN_API_KEY"] = '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'

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
documents =SimpleDirectoryReader('/Users/manasadepu/Documents/GitHub/SASEHACK-Mental-Health-/datasets/Mental_Health_FAQ.csv').load_data()
print(documents)
print('hello')