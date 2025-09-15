from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class MsGraphConfig(BaseSettings):
    model_config = SettingsConfigDict()
    tenant_id: str = Field(..., alias="MS_GRAPH_TENANT_ID")
    client_id: str = Field(..., alias="MS_GRAPH_CLIENT_ID")
    client_secret: str = Field(..., alias="MS_GRAPH_CLIENT_SECRET")
    scope: str = Field("https://graph.microsoft.com/.default", alias="MS_GRAPH_SCOPE")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict()
    python_env: str = "development"
    host: str | None = None
    port: int
    log_config: str | None = None
    mongo_uri: str | None = None
    mongo_database: str = "ai-chatbot-sp-data"
    mongo_truststore: str = "TRUSTSTORE_CDP_ROOT_CA"
    aws_endpoint_url: str | None = None
    http_proxy: HttpUrl | None = None
    enable_metrics: bool = False
    tracing_header: str = "x-cdp-request-id"
    ms_graph: MsGraphConfig = MsGraphConfig()


config = AppConfig()
