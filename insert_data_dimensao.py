from db_conncet import session
from create_table import Empresa, Relatorio, CentroCusto, MovimentoContabil
from sqlalchemy import Column, Integer, String


empresas_data = [
    {"nome_empresa": "Empresa A"},
    {"nome_empresa": "Empresa B"},
    {"nome_empresa": "Empresa C"},
    {"nome_empresa": "Empresa D"}
]
relatorio_data = [
    {"tipo_relatorio": "Financeiro", "StatusAtivo": "Sim"},
    {"tipo_relatorio": "Operacional", "StatusAtivo": "Não"},
    {"tipo_relatorio": "Vendas", "StatusAtivo": "Sim"}
]
centros_custo_data = [
    {"tipo_centCusto": "Administração", "StatusAtivo": "Sim"},
    {"tipo_centCusto": "RH", "StatusAtivo": "Não"},
    {"tipo_centCusto": "TI", "StatusAtivo": "Sim"}
]
if __name__ == "__main__":
        
    def insert_if_not_exists(model, data, unique_field):
        inserted_data = 0 
        for item in data:
            exists = session.query(model).filter_by(**{unique_field: item[unique_field]}).first()
            if not exists:
                session.add(model(**item))
                inserted_data += 1  
        if inserted_data > 0:
            print(f"{inserted_data} novos dados inseridos na tabela {model.__name__}!")
        else:
            print(f"Nenhum novo dado foi inserido na tabela {model.__name__}.")

    insert_if_not_exists(Empresa, empresas_data, "nome_empresa")
    insert_if_not_exists(Relatorio, relatorio_data, "tipo_relatorio")
    insert_if_not_exists(CentroCusto, centros_custo_data, "tipo_centCusto")

    session.commit()



    
