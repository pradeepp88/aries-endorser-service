import logging

from sqlalchemy.ext.asyncio import AsyncSession

import api.acapy_utils as au
from api.endpoints.models.configurations import (
    ConfigurationType,
)
from api.endpoints.models.endorse import (
    EndorseTransactionType,
)
from api.services.configurations import (
    get_config_records,
    get_config_record,
    update_config_record,
)


logger = logging.getLogger(__name__)


async def get_endorser_configs(db: AsyncSession) -> dict:
    acapy_config = await au.acapy_GET(
        "status/config",
    )

    endorser_public_did = await au.acapy_GET(
        "wallet/did/public",
    )

    endorser_config_list = await get_config_records(db)
    endorser_configs = {}
    for endorser_config in endorser_config_list:
        endorser_configs[endorser_config.config_name] = endorser_config.json()
    endorser_configs["public_did"] = endorser_public_did["result"]

    return {
        "acapy_config": acapy_config["config"],
        "endorser_config": endorser_configs
    }


async def get_endorser_config(db: AsyncSession, config_name: str) -> dict:
    return await get_config_record(db, config_name)


def validate_endorser_config(
    config_name: str,
    config_value: str,
):
    if config_name == ConfigurationType.ENDORSER_AUTO_ENDORSE_TXN_TYPES.value:
        config_vals = config_value.split(',')
        txn_type_vals = [e.value for e in EndorseTransactionType]
        for config_val in config_vals:
            if not config_val in txn_type_vals:
                raise Exception(f"Error {config_val} is nto a valid transaction type")
    elif config_name == ConfigurationType.ENDORSER_AUTO_ACCEPT_CONNECTIONS.value:
        # TODO
        pass
    elif config_name == ConfigurationType.ENDORSER_AUTO_ACCEPT_AUTHORS.value:
        # TODO
        pass
    elif config_name == ConfigurationType.ENDORSER_AUTO_ENDORSE_REQUESTS.value:
        # TODO
        pass


async def update_endorser_config(
    db: AsyncSession,
    config_name: str,
    config_value: str,
) -> dict:
    return await update_config_record(db, config_name, config_value)
