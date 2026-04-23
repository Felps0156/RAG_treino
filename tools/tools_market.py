from langchain.tools import tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from vectorstore import supabase

@tool
def market_search(item: str):
    """
    Use esta ferramenta para pesquisar na internet o preço atual de um produto. Passe o nome do produto como argumento. Ela retornará trechos de sites com preços e nomes de lojas.
    """
    search = DuckDuckGoSearchRun()
    return search.run(item)


    
@tool
def market_save_item(item_name: str, estimated_price: float, store_name: str):
    """
    Adiciona um item com preço e loja à lista de compras no banco de dados.
    """
    try:
        item = {
            'item_name': item_name.lower(),
            'estimated_price': estimated_price,
            'store_name': store_name.lower(),
        }
        
        supabase.table('shopping_list').insert(item).execute()
        
        return f"Sucesso: {item_name} adicionado à lista por R$ {estimated_price}."
    except Exception as e:
        return f"Erro ao salvar na lista: {str(e)}"
    
    
@tool
def market_report():
    """
    Retorna todos os itens atuais na lista de compras e o valor total calculado.
    """
    
    try:
        response = supabase.table('shopping_list').select('*').execute()
        data = response.data
        
        if not data:
            return "A lista de compra esta vazia"
        
        total = 0
        report= ["=== Sua Lista de Compras ==="]
        
        for item in data:
            name = item.get('item_name')
            price = item.get('estimated_price', 'valora do proaduto não definido')
            total += price
            store = item.get('store_name', 'loja não definida')
            
            report.append(f"- {name.capitalize()} (Loja: {store}) -> R$ {price:.2f}")
            
        report.append(f"\nValor Total Estimado: R$ {total:.2f}")
        return "\n".join(report)
        
    except Exception as e:
        return f"Erro ao retornar a tabela: {str(e)}"
    
    
@tool
def market_clear_list():
    """
    Use esta ferramenta APENAS quando o usuário pedir para montar uma NOVA lista de compras
    ou para limpar/apagar a lista atual.
    """
    try:
        supabase.rpc('shopping_list').execute()
        return "Lista de compra limpada com sucesso"
    except Exception as e:
        return f"Erro ao limpar a lista de compra: {str(e)}"