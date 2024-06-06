from typing import Dict, Tuple, Any, Optional, Union

import time
import pandas as pd
import uiautomator2 as u2

from .base import get_balance, get_positions, get_orders, buy, sell, cancel_single, cancel_multiple, init_navigation, \
    exists_tab
from .parse import parse_confirm_order, parse_orders, parse_positions, parse_balance, parse_confirm_cancel
from .utils import Timer
from .xpath import XPath
from .const import *


class THS:
    # uiautomator2中的设备
    d = None
    x = None
    # 导航栏几个按扭位置
    navigation = {}

    # 以下未处理的私有成员变量可以人工访问实现特别功能
    balance = {}
    orders = []
    positions = []
    confirm = {}
    prompt = {}

    def __init__(self, debug: bool = True, skip_popup: bool = False) -> None:
        """初始化

        Parameters
        ----------
        debug: bool
            调试模式下不改变柜台状态。即下单和撤单时最后一步会自动点击取消
            初次使用时，请在`debug=True`模拟账号下走一遍流程
        skip_popup: bool
            启用后，下单时的弹出框的确认将交由`李跳跳`等工具完成。好处是弹出框关闭快、下单更快
            1. 用户需自行设置好相应的工具软件
            2. 弹出框的内容不再读取返回
            3. 实测`无障碍服务`与`uiautomator2`冲突，等这个问题解决后，这个功能就能正常使用了


        """
        self.debug: bool = debug
        self.skip_popup: bool = skip_popup

    def connect(self, addr: str = "emulator-5554") -> Dict[str, Any]:
        """连接

        Parameters
        ----------
        addr: str
            可以本地连接，也可以远程。连接方法参考`uiautomator2`项目
        """
        with Timer():
            self.d = u2.connect(addr)
            self.d.implicitly_wait(10.0)
            # 这里会引导环境准备
            return self.d.info
        
    def open_app(self) -> None:
        """打开同花顺APP"""
        with Timer("打开同花顺APP"):
            assert self.d is not None, '请先执行`connect`'
            self.d.app_start("com.hexin.plat.android")
            self.d.app_wait("com.hexin.plat.android", front=True, timeout=10)

    def close_app(self) -> None:
        """关闭同花顺APP"""
        with Timer("关闭同花顺APP"):
            assert self.d is not None, '请先执行`connect`'
            self.d.app_stop("com.hexin.plat.android")
        
    def enter_trade_page(self, trader_index: int = 1, pwd: str = "", debug: bool = None):
        """进入交易页面
        trader_index: int 券商索引
        """
        with Timer('进入交易页面'):
            assert self.d is not None, '请先执行`connect`'
            self.close_app()
            self.open_app()
            time.sleep(5) # 等待一下  看看有没有广告之类的
            if self.d(resourceId="com.hexin.plat.android:id/feedBackView").exists(timeout=3):
                self.d(resourceId="com.hexin.plat.android:id/feedBackView").child(resourceId="com.hexin.plat.android:id/closeBt").click()
            time.sleep(5) # 等待一下  看看有没有广告之类的
            # 查找根节点下第一层的FrameLayout，如果有多个，说明有弹窗，需要关闭
            frame_layouts = self.d.xpath('//hierarchy/android.widget.FrameLayout').all()
            if len(frame_layouts) > 1:
                if self.d(resourceId="com.hexin.plat.android:id/closeBt").exists(timeout=3):
                    self.d(resourceId="com.hexin.plat.android:id/closeBt").click()
                if self.d(resourceId="com.hexin.plat.android:id/close_button").exists(timeout=3):
                    self.d(resourceId="com.hexin.plat.android:id/close_button").click()
            # if self.d(resourceId="com.hexin.plat.android:id/dialog_layout").exists(timeout=3):
            #     self.d(resourceId="com.hexin.plat.android:id/feedBackView").child(resourceId="com.hexin.plat.android:id/closeBt").click()
            # 点击交易按钮
            self.d.xpath('//*[@content-desc="交易"]/android.widget.ImageView[1]').click()
            time.sleep(3)
            # 自动弹出登录界面（有时候不弹，所以先关闭，统一为手动点击登录）
            if self.d(resourceId="com.hexin.plat.android:id/login_component_base_view").exists(timeout=3):
                # 关闭弹窗
                self.d(resourceId="com.hexin.plat.android:id/login_component_base_view").child(resourceId="com.hexin.plat.android:id/close_button").click()
            debug = self.debug if debug is None else debug
            if debug: 
                # 模拟账号
                self.d(resourceId="com.hexin.plat.android:id/moni_layout_view").click()
            else:
                self.d(resourceId="com.hexin.plat.android:id/tab_a").click()
                # 点击券商
                self.d.xpath(f'//*[@resource-id="com.hexin.plat.android:id/nobindlist"]/android.widget.LinearLayout[{trader_index}]').click()
                # 输入交易密码
                self.d(resourceId="com.hexin.plat.android:id/weituo_edit_trade_password").set_text(pwd)
                self.d(resourceId="com.hexin.plat.android:id/weituo_btn_login").click()
            # 点击持仓
            retry_times = 2
            success = False
            while retry_times > 0:
                retry_times -= 1
                time.sleep(10)
                self.d(resourceId="com.hexin.plat.android:id/menu_holdings").click()
                time.sleep(10)
                try:
                    self.home()
                    success = True
                    break
                except Exception as e:
                    print(e)
            if not success:
                self.enter_trade_page(trader_index, pwd, debug)


    def home(self):
        """页首。这里记录了几个导航按钮的位置"""
        with Timer('home'):
            assert self.d is not None, '请先执行`connect`'
            self.x = XPath(self.d)
            self.x.dump_hierarchy()
            self.navigation = init_navigation(self.x)
            if len(self.navigation) != 5:
                self.x = None
                raise Exception("请检查当前是否处于可交易界面!!!")
            # else:
            #     print(self.navigation)

    def goto(self, tab: str):
        # 卖出，然后撤单，可能没点过去，所以循环一下
        for i in range(3):
            if self.x is None:
                self.home()
            self.x.click(*self.navigation[tab])

            if exists_tab(self.d, tab):
                return
        # 最后补救一次
        self.d(resourceId=RESOURCE_ID_BTN, text=tab).click()

    def refresh(self) -> Dict[str, float]:
        """刷新"""
        with Timer():
            self.d(resourceId=RESOURCE_ID_REFRESH).click()
            return {}
        
    def refresh_chedan(self) -> Dict[str, float]:
        """刷新"""
        with Timer():
            self.d(resourceId=RESOURCE_ID_REFRESH).click()
            return {}

    def get_balance(self) -> Dict[str, float]:
        """查询资产

        Returns
        -------
        dict

        """
        with Timer('获取资产'):
            self.goto('持仓')
            self.balance = get_balance(self.d)
            return parse_balance(self.balance)

    def get_positions(self, need_scroll: bool = True) -> pd.DataFrame:
        """查询持仓

        Returns
        -------
        pd.DataFrame

        """
        with Timer():
            self.goto('持仓')
            self.positions = get_positions(self.d, need_scroll=need_scroll)
            return parse_positions(self.positions)

    def get_orders(self, break_after_done: bool = True) -> pd.DataFrame:
        """查询委托

        Parameters
        ----------
        break_after_done: bool
            遇到订单已是最终状态时跳出查询，此功能建立在列表已经排序，已经成交和已经撤单的订单排在最后的特点。
            没有此特点的列表不要启用此功能

        Returns
        -------
        pd.DataFrame

        """
        with Timer():
            self.goto('撤单')
            self.orders = get_orders(self.d, break_after_done)
            return parse_orders(self.orders)

    def order_at(self, idx: int) -> Tuple:
        """返回委托列表中指定位置的委托

        Parameters
        ----------
        idx:int
            列表位置

        Returns
        -------
        Tuple

        """
        assert 0 <= idx < len(self.orders), '请先执行`get_orders`，或不要超过有效范围'
        order = self.orders[idx]
        return order

    def cancel_single(self, order,
                      input_mask=(True, True, True, False, True, False, True, False),
                      inside_mask=(True, True, True, False, True, False, True, False),
                      debug: Optional[bool] = None) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """笔委托撤单

        Parameters
        ----------
        order: tuple
            输入委托
        input_mask: tuple
            输入中选择部分用来比较
        inside_mask: tuple
            列表中选择部分用来比较
        debug: bool or None
            可临时应用新`debug`参数

        Returns
        -------
        confirm: dict
            需要人工确认的信息
        prompt: dict
            无需人工确认的提示信息

        Notes
        -----
        底层使用字符串比较的方法查找指定位置。字符串要完全对应。
        例如: `100.0`与`100.00`不同, ` 万  科 A`与`万科A`也不同
        为方便，请与`order_at`配合使用

        """
        with Timer():
            self.goto('撤单')
            debug = self.debug if debug is None else debug
            self.confirm, self.prompt = cancel_single(self.d, order, input_mask, inside_mask, debug)
            return parse_confirm_cancel(self.confirm), self.prompt

    def cancel_multiple(self, opt: str = 'all',
                        debug: Optional[bool] = None) -> Tuple[Dict[str, str], Dict[str, str]]:
        """批量撤单, 实盘才能使用

        Parameters
        ----------
        opt: str
            `all` `buy` `sell`
        debug: bool or None
            可临时应用新`debug`参数

        Returns
        -------
        confirm: dict
            需要人工确认的信息
        prompt: dict
            无需人工确认的提示信息

        """
        with Timer():
            self.goto('撤单')
            debug = self.debug if debug is None else debug
            self.confirm, self.prompt = cancel_multiple(self.d, opt, debug)
            return self.confirm, self.prompt

    def buy(self, qty: Union[int, str], price: Union[float, str] = float('nan'), *,
            name: Optional[str] = None, code: Optional[str] = None,
            debug: Optional[bool] = None, skip_popup: Optional[bool] = None) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """买入委托

        Parameters
        ----------
        qty: int
            委托量
        price: float or str
            委托价。如果使用默认值`float('nan')`将利用界面自动填入的`卖一价`
        name: str
            证券代码、名称、拼音缩写都支持。只要在键盘精灵排第一，不做校验
        code: str
            证券代码。会对输入进行校验。推荐使用证券代码
        debug: bool or None
            可临时应用新`debug`参数
        skip_popup: bool or None
            可临时应用新`skip_popup`参数

        Returns
        -------
        confirm: dict
            需要人工确认的信息
        prompt: dict
            无需人工确认的提示信息

        """
        with Timer():
            self.goto('买入')
            debug = self.debug if debug is None else debug
            skip_popup = self.skip_popup if skip_popup is None else skip_popup
            self.confirm, self.prompt = buy(self.d, qty, price, name, code, debug, skip_popup)
            return parse_confirm_order(self.confirm), self.prompt

    def sell(self, qty: Union[int, str], price: Union[float, str] = float('nan'), *,
             name: Optional[str] = None, code: Optional[str] = None,
             debug: Optional[bool] = None, skip_popup: Optional[bool] = None) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """卖出委托

        Parameters
        ----------
        qty: int or str
            委托量
        price: float or str
            委托价。如果使用默认值`float('nan')`将利用界面自动填入的`买一价`
        name: str
            证券代码、名称、拼音缩写都支持。只要在键盘精灵排第一，不做校验
        code: str
            证券代码。会对输入进行校验。推荐使用证券代码
        debug: bool or None
            可临时应用新`debug`参数
        skip_popup: bool or None
            可临时应用新`skip_popup`参数

        Returns
        -------
        confirm: dict
            需要人工确认的信息
        prompt: dict
            无需人工确认的提示信息

        """
        with Timer():
            self.goto('卖出')
            debug = self.debug if debug is None else debug
            skip_popup = self.skip_popup if skip_popup is None else skip_popup
            self.confirm, self.prompt = sell(self.d, qty, price, name, code, debug, skip_popup)
            return parse_confirm_order(self.confirm), self.prompt
