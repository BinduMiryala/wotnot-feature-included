from pydantic import BaseModel

class wocommerceConfig(BaseModel):
    template_data:str


class WooCommerceCredentials(BaseModel):
    base_url: str  # WooCommerce store URL, e.g., https://example.com
    consumer_key: str  # API key from WooCommerce
    consumer_secret: str  # API secret from WooCommerce
    store_name: str