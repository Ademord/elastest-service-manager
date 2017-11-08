from typing import List
from esm.models.last_operation import LastOperation
from esm.models.manifest import Manifest
from esm.models.service_instance import ServiceInstance
from esm.models.service_type import ServiceType

class Storage(object):
    def add_service(self, service: ServiceType) -> tuple:
        raise NotImplementedError

    def get_service(self, service_id: str=None) -> List[ServiceType]:
        raise NotImplementedError

    def delete_service(self, service_id: str=None) -> None:
        raise NotImplementedError

    def add_service_instance(self, service_instance: ServiceInstance) -> tuple:
        raise NotImplementedError

    def get_service_instance(self, instance_id: str=None) -> List[ServiceInstance]:
        raise NotImplementedError

    def delete_service_instance(self, service_instance_id: str=None) -> None:
        raise NotImplementedError

    def add_manifest(self, manifest: Manifest) -> tuple:
        raise NotImplementedError

    def get_manifest(self, manifest_id: str=None, plan_id: str=None) -> List[Manifest]:
        raise NotImplementedError

    def delete_manifest(self, manifest_id: str=None) -> None:
        raise NotImplementedError

    def add_last_operation(self, instance_id: str, last_operation: LastOperation) -> tuple:
        raise NotImplementedError

    def delete_last_operation(self, instance_id: str=None) -> None:
        raise NotImplementedError

    def get_last_operation(self, instance_id: str=None) -> List[LastOperation]:
        raise NotImplementedError
