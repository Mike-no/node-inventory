from db import models, engine, SessionLocal
from fastapi import FastAPI, Depends
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


@app.post('/cluster/register', tags=['cluster'], status_code=201, response_model=schemas.Cluster,
          description='Register a new K8s cluster in order to be monitored')
def register_cluster(cluster: schemas.ClusterCreate, db: Session = Depends(get_db)):
    print(cluster)
    print(db)
    return {
        'name': 'NXW',
        'kubeconfig': {
            'apiVersion': 'v1',
            'current-context': 'kubernetes-admin@kubernetes',
            'kind': 'Config',
            'preferences': {}
        },
        'id': 1
    }


@app.get('/cluster/{cluster_id}', tags=['cluster'], status_code=200, response_model=schemas.Cluster,
         description='Get K8s cluster details')
def get_cluster(cluster_id: int, db: Session = Depends(get_db)):
    print(cluster_id)
    print(db)
    return {
        'name': 'NXW',
        'kubeconfig': {
            'apiVersion': 'v1',
            'current-context': 'kubernetes-admin@kubernetes',
            'kind': 'Config',
            'preferences': {}
        },
        'id': 1
    }


@app.get('/clusters', tags=['cluster'], status_code=200, response_model=List[schemas.Cluster],
         description='Get K8s clusters details')
def get_clusters(db: Session = Depends(get_db)):
    print(db)
    return []


@app.delete('/cluster/unregister/{cluster_id}', tags=['cluster'], status_code=204,
            description='Unregister a monitored K8s cluster')
def unregister_cluster(cluster_id: int, db: Session = Depends(get_db)):
    print(cluster_id)
    print(db)


@app.get('/nodes', tags=['nodes'], status_code=200, response_model=List[schemas.Node],
         description='Get nodes details for all K8s clusters')
def get_nodes(db: Session = Depends(get_db)):
    print(db)
    return []


@app.get('/nodes/{cluster_id}', tags=['nodes'], status_code=200, response_model=List[schemas.Node],
         description='Get nodes details for the given K8s cluster')
def get_nodes_by_cluster(cluster_id: int, db: Session = Depends(get_db)):
    print(cluster_id)
    print(db)
    return []
