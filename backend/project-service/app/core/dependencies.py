from functools import lru_cache
from sqlalchemy.orm import Session
from app.db.session import get_db


class Container:
    def __init__(self, db: Session):
        self.db = db
        self._repositories = {}
        self._services = {}

    def get_repository(self, repository_class):
        if repository_class not in self._repositories:
            self._repositories[repository_class] = repository_class(self.db)
        return self._repositories[repository_class]

    def get_service(self, service_class, *repository_classes):
        if service_class not in self._services:
            repositories = [self.get_repository(repo) for repo in repository_classes]
            self._services[service_class] = service_class(*repositories)
        return self._services[service_class]


def get_container(db: Session = next(get_db())):
    return Container(db)
