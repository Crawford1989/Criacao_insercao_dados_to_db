from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db_conncet import engine

Base = declarative_base()

#Tabela Empresa
class Empresa(Base):
    __tablename__ = 'empresa'
    empresa_id = Column(Integer, primary_key=True)
    nome_empresa = Column(String(255))
    
#Tabela Relatorio
class Relatorio(Base):
    __tablename__ = 'relatorio'
    relatorio_id = Column(Integer, primary_key=True)
    tipo_relatorio = Column(String(255))
    StatusAtivo = Column(String(3))
    
#Tabela Centro Custo
class CentroCusto(Base):
    __tablename__ = 'centro_custo'
    centCusto_id = Column(Integer, primary_key=True)
    tipo_centCusto = Column(String(255))
    StatusAtivo = Column(String(3))
    
#Tabela Movimento Contabil
class MovimentoContabil(Base):
    __tablename__ = 'movimento_contabil'
    id_mc = Column(Integer, primary_key=True)
    data = Column(Date)
    conta_contabil = Column(String(20))
    status_conta = Column(String(50))
    valor = Column(DECIMAL(10,2))
    id_relatorio = Column(Integer, ForeignKey('relatorio.relatorio_id'))
    id_empresa = Column(Integer, ForeignKey('empresa.empresa_id'))
    id_centCusto = Column(Integer, ForeignKey('centro_custo.centCusto_id'))
    relatorio = relationship('Relatorio')
    empresa = relationship('Empresa')
    centro_custo = relationship('CentroCusto')
    



if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print('Tabelas criadas com sucesso!')