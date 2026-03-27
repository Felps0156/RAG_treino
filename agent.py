import uuid

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tools import knowledge_base_search


model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")


tools = [
    knowledge_base_search,
]

system_prompt = """
Você é um agente pessoal chamado Pedro
Seja educado.
Se não sabe a resposta diz que não sabe, mas nunca invente
"""

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
)


# thread_id = str(uuid.uuid4())
# config = {'configurable': {'thread_id': '1'}}

# while True:
#     try:
#         user_input = input('\nFelipe, digite sua dúvida (ou "sair"): ')
        
#         if user_input.lower() in ['sair', 'exit', 'quit']:
#             print("Até logo!")
#             break   

#         # 2. O input_message deve ser passado como uma lista de mensagens ou dicionário de estado
#         input_data = {"messages": [("user", user_input)]}

#         # 3. Loop de Streaming
#         for step in agent.stream(
#             input_data, 
#             config, 
#             stream_mode="values"
#         ):
#             # Pegamos a última mensagem gerada no passo atual
#             if "messages" in step:
#                 last_message = step["messages"][-1]
                
#                 # Só imprimimos se for uma mensagem do Assistente (AI)
#                 # Isso evita imprimir a sua própria pergunta de novo
#                 if last_message.type == "ai" and last_message.content:
#                     last_message.pretty_print()
               
#     except KeyboardInterrupt:
#         print("\nEncerrando...")
#         break
#     except Exception as e:
#         print(f"\nOcorreu um erro: {e}")
#         break