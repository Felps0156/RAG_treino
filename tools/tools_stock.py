from langchain.tools import tool
from vectorstore import supabase

@tool
def check_inventary(item_name: str) -> str:
    """
    Útil para verificar a quantidade exata e a unidade de medida de um ingrediente no estoque.
    USE SEMPRE que o usuário fizer perguntas como: 'temos arroz?', 'quanto resta de feijão?' ou 
    'verifique se há óleo na dispensa'.
    Esta ferramenta retorna o saldo atual. Se o item não for encontrado, ela informará que 
    o ingrediente não está cadastrado.
    """
    try:
        response = supabase.table('inventory').select('*').ilike('item_name', f"%{item_name}%").execute()
            # supabase.table = buscar a tabela chamada inventory
            # .select: pega tas as colunas daquela tabela(nome, quantidade, unidade)
            # .ilike: recebe todos os tipos de busca, se buscar por arros ele não importa se é maiuscula ou minuscula
            # %: Ele busca todos os itens que contem a palavra. ex: se passar arroz ele busca por arroz branco, arroz integral...
        data = response.data
    
        if not data:
            return f"O item '{item_name}' não foi encontrado no estoque."
            
        item = data[0]
        return f"Estoque atual: {item['quantity']} {item['unit']} de {item['item_name']}."

    except Exception as e: #caso o agente crash aqui
        return f"Erro ao acessar o banco de dados: {str(e)}"
    

@tool
def update_inventary(item_name: str, quantity_stock: int) -> int:
    """
    Útil para cadastrar um ingrediente que NUNCA foi inserido no sistema anteriormente.
    USE APENAS quando o usuário disser algo como 'cadastre um novo item', 'chegou um produto novo' 
    ou quando a ferramenta 'check_inventory' confirmar que o item não existe.
    REQUER: 
    - item_name: Nome do produto.
    - quantity: Quantidade inicial.
    - unit: Unidade de medida (ex: 'kg', 'unidades', 'gramas').
    """
    
    response = supabase.table('inventory').select('*').ilike('item_name', f"%{item_name}%").execute()
    data = response.data
    
    current_quantity = response.data[0]['quantity']
    
    new_quantity = current_quantity + quantity_stock
    
    update_quantity = supabase.table('inventory').update({"quantity": new_quantity}).ilike('item_name', f"%{item_name}%").execute()
    
    return update_quantity


@tool
def add_item(item_name: str, quantity: int, unit: str) -> str:
    """
    USE ESTA FERRAMENTA APENAS para cadastrar um item que AINDA NÃO EXISTE no estoque.
    Você deve fornecer o nome do item, a quantidade inicial e a unidade de medida (ex: 'kg', 'litros', 'unidades').
    Se o usuário quiser apenas alterar a quantidade de algo que já tem, use a ferramenta 'update_inventory'.
    """
    
    try:
        check_existing = supabase.table('inventory').select('*').ilike("item_name", f"%{item_name}%")
            
        if check_existing:
            return(f"O item ja esta cadastrado no estoque.")

        new_item = {
            "item_name": item_name.lower(),
            "quantity": quantity,
            "unit": unit,
        }
        
        new_stock = supabase.table('inventory').insert(new_item).execute()
        return f"O item {item_name} foi adicionado ao estoque com {quantity} {unit}"
    
      
    except Exception as e:
        return f"Erro ao tentar cadastrar o {item_name} no estoque: {str(e)}"