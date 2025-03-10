from db_conncet import session
from create_table import Empresa, Relatorio, CentroCusto, MovimentoContabil

def get_id(model, field, value):
    """Busca o ID de uma dimensão pelo campo e valor fornecidos."""
    obj = session.query(model).filter(getattr(model, field) == value).first()
    
    if obj:
        # Obtém o nome correto da chave primária dinamicamente
        primary_key_column = next(
            (column.name for column in model.__table__.columns if column.primary_key), None
        )
        return getattr(obj, primary_key_column)
    
    return None


def insert_fato_if_not_exists(session, fato_model, dimensao_models, dimensao_data, fato_data):
    """
    Função para inserir dados na tabela de fato automaticamente, associando com as tabelas de dimensão,
    caso os dados não existam.
    """
    dimensao_ids = {}  # Dicionário para armazenar os IDs das dimensões

    # Mapeamento de nomes de tabela para os nomes reais das colunas na fato
    tabela_para_campo = {
        "empresa": "empresa_id",
        "relatorio": "relatorio_id",
        "centro_custo": "centCusto_id",
    }

    # Verifica se o dado já existe na tabela de fato, considerando as chaves estrangeiras
    exists_fato = session.query(fato_model).filter_by(
        data=fato_data["data"],
        conta_contabil=fato_data["conta_contabil"],
        valor=fato_data["valor"],
        relatorio_id=fato_data["relatorio_id"],
        empresa_id=fato_data["empresa_id"],
        centCusto_id=fato_data["centCusto_id"]
    ).first()

    if exists_fato:
        print(f"{fato_model.__tablename__} já existe: {fato_data}")
        return  # Impede a inserção se já existir

    for model, item_data in zip(dimensao_models, dimensao_data):
        exists = session.query(model).filter_by(**item_data).first()

        if not exists:
            new_entry = model(**item_data)
            session.add(new_entry)
            session.commit()  # Commit para garantir que os IDs são gerados
            exists = new_entry  # Agora ele existe!

            print(f"{model.__tablename__} inserido: {item_data}")

        # Buscar o ID da dimensão corretamente
        primary_key_column = next(
            (column.name for column in model.__table__.columns if column.primary_key), None
        )
        id_dado = getattr(exists, primary_key_column)

        # Garante que a chave estrangeira correta é atribuída
        dimensao_ids[tabela_para_campo[model.__tablename__]] = id_dado

    # Atualiza os dados da tabela de fato com os IDs das dimensões
    fato_data.update(dimensao_ids)

    # Insere o dado na tabela de fato
    session.add(fato_model(**fato_data))
    session.commit()  # Commit único após todas as inserções
    print(f"{fato_model.__tablename__} inserido: {fato_data}")


# Exemplo de uso

# Dados das dimensões
dimensao_data = [
    {"nome_empresa": "Empresa A"},
    {"tipo_relatorio": "Financeiro", "StatusAtivo": "Sim"},
    {"tipo_centCusto": "Administração", "StatusAtivo": "Sim"}
]

# Dados da tabela de fato (MovimentoContabil)
# Dados da tabela de fato (MovimentoContabil)
fato_data = {
    "data": "2020-10-10",
    "conta_contabil": "899645",
    "status_conta": "Ativa",
    "valor": 2500.00,
    "relatorio_id": 2,  # 'relatorio_id' está correto
    "empresa_id": 3,    # 'empresa_id' está correto
    "centCusto_id": 2   # Alterado para 'centCusto_id'
}



# Chama a função para inserir tudo automaticamente
insert_fato_if_not_exists(session, MovimentoContabil, [Empresa, Relatorio, CentroCusto], dimensao_data, fato_data)
