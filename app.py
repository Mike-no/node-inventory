from db import models, engine, SessionLocal, query
from fastapi import FastAPI, Depends, HTTPException,Request
from api import schemas
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='k8s-node-inventory')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cluster/register',
          tags=['cluster'],
          responses={
              201: {'model': schemas.Cluster},
              400: {'model': schemas.ResponseMessage400}
          },
          status_code=201,
          description='Register a new K8s cluster in order to be monitored')
def register_cluster(cluster: schemas.ClusterCreate, db: Session = Depends(get_db)):
    db_cluster = query.get_cluster_by_name(db=db, name=cluster.name)
    if db_cluster:
        raise HTTPException(status_code=400, detail='Cluster with name ' + cluster.name + ' already registered.')

    db_cluster = query.create_cluster(db=db, cluster=cluster)

    query.create_node(db=db, cluster_id=db_cluster.id, node=schemas.NodeCreate(
        uid='9fffd7e0-2e93-488c-8917-ba9787c36588',
        status='Ready',
        internal_ip='192.168.1.9',
        allocatable={
            'cpu': '8',
            'ephemeral-storage': '211520996Ki',
            'memory': '16145760Ki',
        },
        capacity={
            'cpu': '8',
            'ephemeral-storage': '212569572Ki',
            'memory': '16248160Ki',
        },
        labels={
            'beta.kubernetes.io/arch': 'amd64',
            'beta.kubernetes.io/os': 'linux',
            'kubernetes.io/arch': 'amd64',
            'kubernetes.io/hostname': 'michael',
            'kubernetes.io/os': 'linux',
            'microk8s.io/cluster': 'true',
            'node.kubernetes.io/microk8s-controlplane': 'microk8s-controlplane'
        }
    ))

    db.refresh(db_cluster)

    return db_cluster


@app.get('/cluster/{cluster_id}',
         tags=['cluster'],
         responses={
             200: {'model': schemas.Cluster},
             404: {'model': schemas.ResponseMessage404}
         },
         description='Get K8s cluster details by ID')
def get_cluster_by_id(cluster_id: int, db: Session = Depends(get_db)):
    db_cluster = query.get_cluster_by_id(db=db, cluster_id=cluster_id)

    if db_cluster is None:
        raise HTTPException(status_code=404, detail='Cluster ' + str(cluster_id) + ' not found.')

    return db_cluster


@app.get('/clusters', tags=['cluster'], status_code=200, response_model=List[schemas.Cluster],
         description='Get K8s clusters details')
def get_clusters(db: Session = Depends(get_db)):
    return query.get_clusters(db=db)


@app.delete('/cluster/unregister/{cluster_id}',
            tags=['cluster'],
            responses={
                204: {'model': None},
                404: {'model': schemas.ResponseMessage404}
            },
            status_code=204,
            description='Unregister a monitored K8s cluster')
def unregister_cluster(cluster_id: int, db: Session = Depends(get_db)):
    db_cluster = query.get_cluster_by_id(db=db, cluster_id=cluster_id)

    if db_cluster is None:
        raise HTTPException(status_code=404, detail='Cluster ' + str(cluster_id) + ' not found.')

    query.delete_cluster(db=db, cluster=db_cluster)


@app.get('/cluster/{cluster_id}/nodes',
         tags=['cluster'],
         responses={
             200: {'model': List[schemas.Node]},
             404: {'model': schemas.ResponseMessage404}
         },
         description='Get nodes details for the given K8s cluster')
def get_nodes_by_cluster(cluster_id: int, request: Request, db: Session = Depends(get_db)):
    db_cluster = query.get_cluster_by_id(db=db, cluster_id=cluster_id)

    if db_cluster is None:
        raise HTTPException(status_code=404, detail='Cluster ' + str(cluster_id) + ' not found.')

    if not request.query_params:
        return db_cluster.nodes

    nodes = []
    for node in db_cluster.nodes:
        ins = True
        for key in request.query_params.keys():
            if key not in node.labels:
                ins = False
            elif request.query_params.get(key) != node.labels.get(key):
                ins = False

            if not ins:
                break

        if ins:
            nodes.append(node)

    return nodes


