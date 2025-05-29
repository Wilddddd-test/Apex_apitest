import os
import pytest
from apexpro.http_private_sign import HttpPrivateSign
from apexpro.constants import NETWORKID_TEST, APEX_OMNI_HTTP_TEST, NETWORKID_MAIN, APEX_OMNI_HTTP_MAIN


def get_env_or_fail(key: str) -> str:
    """获取环境变量，如果不存在则抛出异常"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is not set")
    return value


@pytest.fixture(scope="session")
def api_client():
    """创建API客户端"""
    # 从环境变量获取敏感信息
    api_key = get_env_or_fail("APEX_API_KEY")
    api_secret = get_env_or_fail("APEX_API_SECRET")
    api_passphrase = get_env_or_fail("APEX_API_PASSPHRASE")
    seeds = get_env_or_fail("APEX_SEEDS")
    l2_key = get_env_or_fail("APEX_L2_KEY")

    # 创建客户端
    client = HttpPrivateSign(
        APEX_OMNI_HTTP_MAIN,
        network_id=NETWORKID_MAIN,
        zk_seeds=seeds,
        zk_l2Key=l2_key,
        api_key_credentials={
            "key": api_key,
            "secret": api_secret,
            "passphrase": api_passphrase
        }
    )
    return client
