import time
import pytest
import allure

@allure.epic("订单管理")
@allure.feature("订单创建")
class TestOrder:
    
    @allure.story("创建市价买单")
    @allure.title("创建SOL-USDT市价买单")
    @pytest.mark.order
    def test_create_market_buy_order(self, api_client):
        """测试创建市价买单"""
        with allure.step("获取配置信息"):
            configs = api_client.configs_v3()
            
        with allure.step("获取账户信息"):
            account_data = api_client.get_account_v3()
            api_client.accountV3 = account_data
            
        with allure.step("创建市价买单"):
            current_time = time.time()
            create_order_res = api_client.create_order_v3(
                symbol="SOL-USDT",
                side="BUY",
                type="MARKET",
                size="1.2",
                timestampSeconds=current_time,
                price="126",
                brokerId=6443
            )
            
        with allure.step("验证订单创建结果"):
            assert create_order_res is not None, "订单创建失败"
            allure.attach(str(create_order_res), "订单响应", allure.attachment_type.TEXT)
            
    @allure.story("创建限价卖单")
    @allure.title("创建SOL-USDT限价卖单")
    @pytest.mark.order
    def test_create_limit_sell_order(self, api_client):
        """测试创建限价卖单"""
        with allure.step("获取配置信息"):
            configs = api_client.configs_v3()
            
        with allure.step("获取账户信息"):
            account_data = api_client.get_account_v3()
            api_client.accountV3 = account_data
            
        with allure.step("创建限价卖单"):
            current_time = time.time()
            create_order_res = api_client.create_order_v3(
                symbol="SOL-USDT",
                side="SELL",
                type="LIMIT",
                size="1.2",
                timestampSeconds=current_time,
                price="130",
                brokerId=6443
            )
            
        with allure.step("验证订单创建结果"):
            assert create_order_res is not None, "订单创建失败"
            allure.attach(str(create_order_res), "订单响应", allure.attachment_type.TEXT)
