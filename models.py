from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QueryTemplate(Base):
    __tablename__ = 'query_templates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    query = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

class QueryResult(Base):
    __tablename__ = 'query_results'
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey('query_templates.id'))
    result = Column(Text, nullable=False)
    executed_at = Column(TIMESTAMP, nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    telefono = Column(String(15))
    fecha_registro = Column(TIMESTAMP, nullable=False, default=None)
