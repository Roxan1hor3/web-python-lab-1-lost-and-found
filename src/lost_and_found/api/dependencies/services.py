from fastapi import Depends

from src.lost_and_found.adapters.services.lost_and_found_service import (
    LostAndFoundService,
)
from src.lost_and_found.config import Settings, get_settings


class ServiceManager:
    _lost_and_found_service: LostAndFoundService = None

    def create(
        self,
        settings: Settings,
    ) -> None:
        self._lost_and_found_service = self.create_lost_and_found_service(
            settings=settings
        )

    def create_lost_and_found_service(self, settings):
        if self._lost_and_found_service is None:
            self._lost_and_found_service = LostAndFoundService()
        return self._lost_and_found_service


service_manager = ServiceManager()


def init_service_manager(
    settings: Settings,
):
    return service_manager.create(settings=settings)


def get_lost_and_found_service(
    settings: Settings = Depends(get_settings),
) -> LostAndFoundService:
    return service_manager.create_lost_and_found_service(settings=settings)
