from sqlalchemy.orm import Session, joinedload
from . import models
from api import schemas
import json

def create_cluster(db: Session, cluster: schemas.ClusterCreate):
    db_cluster = models.Cluster(
        name=cluster.name,
        kubeconfig=json.loads(json.dumps(cluster.kubeconfig, default=lambda o: o.__dict__))
    )

    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)

    return db_cluster


def create_node(db: Session, cluster_id:int, node: schemas.NodeCreate):
    db_node = models.Node(**node.dict(), cluster_id=cluster_id)

    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def get_cluster_by_id(db: Session, cluster_id: int):
    return db.query(models.Cluster).filter(models.Cluster.id == cluster_id).options(joinedload('*')).first()


def get_node_by_id(db: Session, node_id: int):
    return db.query(models.Node).filter(models.Node.id == node_id).options(joinedload('*')).first()


def get_cluster_by_name(db: Session, name: str):
    return db.query(models.Cluster).filter(models.Cluster.name == name).first()


def get_clusters(db: Session):
    return db.query(models.Cluster).all()


def get_nodes(db: Session):
    return db.query(models.Node).all()


def delete_cluster(db:Session, cluster: models.Cluster):
    db.delete(cluster)
    db.commit()


def delete_node(db:Session, node: models.Node):
    db.delete(node)
    db.commit()
