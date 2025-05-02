from graphRAGQuerier import GraphRagQuerier
query="Who were the normans and why were they so famous?"
graphRag=GraphRagQuerier()
response=graphRag.query(query)
print(response)