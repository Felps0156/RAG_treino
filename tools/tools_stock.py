from langchain.tools import tool
from vectorstore import supabase

@tool
def check_inventary(item_name: str) -> str:
    """
    Útil para verificar a quantidade exata e a unidade de medida de um ingrediente no estoque.
    USE SEMPRE que o usuário fizer perguntas como: 'temos arroz?', 'quanto resta de feijão?' ou 
    'verifique se há óleo na dispensa'.
    """
    try:
        response = supabase.table('inventory').select('*').ilike('item_name', f"%{item_name}%").execute()
        data = response.data
    
        if not data:
            return f"O item '{item_name}' não foi encontrado no estoque."
            
        item = data[0]
        return f"Estoque atual: {item['quantity']} {item['unit']} de {item['item_name']}."

    except Exception as e:
        return f"Erro ao acessar o banco de dados: {str(e)}"
    

@tool
def update_inventary(item_name: str, quantity_stock: int) -> str:
    """
    Útil para registrar a ENTRADA ou SAÍDA de ingredientes que JÁ EXISTEM no estoque.
    """
    try:
        response = supabase.table('inventory').select('*').ilike('item_name', f"%{item_name}%").execute()
        
        if not response.data:
            return f"O item '{item_name}' não existe no estoque. Por favor, utilize a ferramenta add_item."
            
        current_quantity = response.data[0]['quantity']
        new_quantity = current_quantity + quantity_stock
        
        supabase.table('inventory').update({"quantity": new_quantity}).ilike('item_name', f"%{item_name}%").execute()
        
        return f"Sucesso! O estoque de {item_name} foi atualizado para {new_quantity}."
        
    except Exception as e:
        return f"Erro ao atualizar o item: {str(e)}"


@tool
def add_item(item_name: str, quantity: int, unit: str) -> str:
    """
    USE ESTA FERRAMENTA APENAS para cadastrar um item que AINDA NÃO EXISTE no estoque.
    """
    try:
        check_existing = supabase.table('inventory').select('*').ilike("item_name", f"%{item_name}%").execute()
            
        if check_existing.data:
            return f"O item ja esta cadastrado no estoque. Use update_inventary."

        new_item = {
            "item_name": item_name.lower(),
            "quantity": quantity,
            "unit": unit,
        }
        
        supabase.table('inventory').insert(new_item).execute()
        return f"O item {item_name} foi adicionado ao estoque com {quantity} {unit}."
    
    except Exception as e:
        return f"Erro ao tentar cadastrar o {item_name} no estoque: {str(e)}"