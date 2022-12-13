from . import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship


class Cluster(Base):
    __tablename__ = 'clusters'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True)
    kubeconfig = Column(JSON, index=True)

    nodes = relationship('Node', back_populates='cluster',
                         cascade='all, delete', passive_deletes=True)


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey('clusters.id', ondelete='CASCADE'))

    uid = Column(String, index=True)
    status = Column(String, index=True)
    internal_ip = Column(String, index=True)
    allocatable = Column(JSON, index=True)
    capacity = Column(JSON, index=True)
    labels = Column(JSON, index=True)

    cluster = relationship('Cluster', back_populates='nodes')
