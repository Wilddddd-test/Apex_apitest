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
                symbol="BTC-USDT",
                side="BUY",
                type="MARKET",
                size="0.001",
                timestampSeconds=current_time,
                price="100000",



            )
            
        with allure.step("验证订单创建结果"):
            assert create_order_res is not None, "订单创建失败"
            allure.attach(str(create_order_res), "订单响应", allure.attachment_type.TEXT)
            

            
