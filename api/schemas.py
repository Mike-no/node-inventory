from pydantic import BaseModel
from typing import List


class Node(BaseModel):
    id: int
    cluster_id: int

    name: str
    status: str
    internal_ip: str
    allocatable: dict
    capacity: dict
    labels: dict

    class Config:
        orm_mode = True


class ClusterBase(BaseModel):
    name: str


class ClusterCreate(ClusterBase):
    pass


class Cluster(ClusterBase):
    id: int

    kubeconfig: dict
    nodes: List[Node] = []

    class Config:
        orm_mode = True
