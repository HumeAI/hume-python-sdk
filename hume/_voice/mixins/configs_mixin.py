import logging
from typing import Iterator, Optional

from hume._common.client_base import ClientBase
from hume._common.utilities.paging_utilities import Paging
from hume._voice.models.configs_models import (
    ConfigResponse,
    ConfigsResponse,
    PostConfigRequest,
    PostPromptRequest,
    PromptMeta,
    PromptResponse,
    VoiceConfig,
)
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
class ConfigsMixin(ClientBase):
    def create_config(
        self,
        *,
        name: str,
        prompt: str,
        description: Optional[str] = None,
    ) -> VoiceConfig:
        post_prompt_request = PostPromptRequest(name=name, version_description=description, text=prompt)
        post_prompt_body = post_prompt_request.to_json_str()
        endpoint = self._build_endpoint("evi", "prompts")
        response = self._request(endpoint, method="POST", body_json_str=post_prompt_body)
        prompt_response = PromptResponse.model_validate_json(response.text)
        prompt_meta = PromptMeta(id=prompt_response.id, version=prompt_response.version_number)

        post_config_request = PostConfigRequest(name=name, version_description=description, prompt=prompt_meta)
        post_config_body = post_config_request.to_json_str()
        endpoint = self._build_endpoint("evi", "configs")
        response = self._request(endpoint, method="POST", body_json_str=post_config_body)
        config_response = ConfigResponse.model_validate_json(response.text)

        return VoiceConfig(
            id=config_response.id,
            name=name,
            description=config_response.version_description,
            created_on=config_response.created_on,
            modified_on=config_response.modified_on,
            prompt=prompt,
        )

    def get_config(self, id: str) -> VoiceConfig:
        endpoint = self._build_endpoint("evi", f"configs/{id}")
        response = self._request(endpoint, method="GET")
        configs_response = ConfigsResponse.model_validate_json(response.text)
        if len(configs_response.configs) == 0:
            raise HumeClientException(f"Config not found with ID: {id}")

        return self._config_from_response(configs_response.configs[0])

    def _config_from_response(self, config_response: ConfigResponse) -> VoiceConfig:
        prompt_response = config_response.prompt
        prompt = prompt_response.text if prompt_response is not None else None

        return VoiceConfig(
            id=config_response.id,
            name=config_response.name,
            description=config_response.version_description,
            created_on=config_response.created_on,
            modified_on=config_response.modified_on,
            prompt=prompt,
        )

    def iter_configs(self) -> Iterator[VoiceConfig]:
        endpoint = self._build_endpoint("evi", "configs")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            configs_response = ConfigsResponse.model_validate_json(response.text)
            if len(configs_response.configs) == 0:
                break
            for res in configs_response.configs:
                yield self._config_from_response(res)

    def delete_config(self, id: str) -> None:
        endpoint = self._build_endpoint("evi", f"configs/{id}")
        self._request(endpoint, method="DELETE")
