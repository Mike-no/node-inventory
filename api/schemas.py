from pydantic import BaseModel, Field
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


class K8sClusterCluster(BaseModel):
    server: str
    certificateAuthorityData: str = Field(alias='certificate-authority-data')


class K8sCluster(BaseModel):
    name: str
    cluster: K8sClusterCluster


class K8sContextContext(BaseModel):
    cluster: str
    user: str


class K8sContext(BaseModel):
    name: str
    context: K8sContextContext


class K8sUserUser(BaseModel):
    clientCertificateData: str = Field(alias='client-certificate-data')
    clientKeyData: str = Field(alias='client-key-data')


class K8sUser(BaseModel):
    name: str
    user: K8sUserUser


class Kubeconfig(BaseModel):
    def __init__(self, **entries):
        super().__init__(**entries)
        self.__dict__.update(entries)
    apiVersion: str
    clusters: List[K8sCluster] = []
    contexts: List[K8sContext] = []
    currentContext: str = Field(alias='current-context')
    kind: str
    preferences: dict
    users: List[K8sUser] = []


class ClusterBase(BaseModel):
    name: str
    kubeconfig: Kubeconfig


class ClusterCreate(ClusterBase):
    pass


class Cluster(ClusterBase):
    id: int

    nodes: List[Node] = []

    class Config:
        orm_mode = True


class ResponseMessage400(BaseModel):
    detail: str


class ResponseMessage404(BaseModel):
    detail: str
