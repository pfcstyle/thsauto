########### Resource IDs
# base.py
RESOURCE_ID_SCROLLER = "com.hexin.plat.android:id/scroller"  # 滚动视图ID
RESOURCE_ID_SCROLLVIEW = "com.hexin.plat.android:id/chedan_listview"  # 撤单滚动根视图ID
RESOURCE_ID_MAIN_LAYOUT = "com.hexin.plat.android:id/main_layout"  # 主布局ID
RESOURCE_ID_RECYCLER_VIEW = "com.hexin.plat.android:id/recyclerview_id"  # 循环视图ID
RESOURCE_ID_CHEDAN_RECYCLER_VIEW = "com.hexin.plat.android:id/chedan_recycler_view"  # 撤单循环视图ID
RESOURCE_ID_DIALOG_LAYOUT = "com.hexin.plat.android:id/dialog_layout"  # 对话框布局ID
RESOURCE_ID_DIALOG_TITLE = "com.hexin.plat.android:id/dialog_title"  # 对话框标题ID
RESOURCE_ID_PROMPT_CONTENT = "com.hexin.plat.android:id/prompt_content"  # 对话框内容ID
RESOURCE_ID_BTN_TRANSACTION = "com.hexin.plat.android:id/btn_transaction"  # 交易按钮ID
RESOURCE_ID_AUTO_STOCKCODE = "com.hexin.plat.android:id/auto_stockcode"  # 自动股票代码输入框ID
RESOURCE_ID_STOCKCODE_TV = "com.hexin.plat.android:id/stockcode_tv"  # 股票代码显示框ID
RESOURCE_ID_STOCKVOLUME = "com.hexin.plat.android:id/stockvolume"  # 股票数量输入框ID
RESOURCE_ID_STOCKPRICE = "com.hexin.plat.android:id/stockprice"  # 股票价格输入框ID
RESOURCE_ID_CANCEL_BTN = "com.hexin.plat.android:id/cancel_btn"  # 取消按钮ID
RESOURCE_ID_OK_BTN = "com.hexin.plat.android:id/ok_btn"  # 确认按钮ID
RESOURCE_ID_CHE_ALL_BTN = "com.hexin.plat.android:id/quanche_tv"  # 全撤按钮ID
RESOURCE_ID_CHE_BUY_BTN = "com.hexin.plat.android:id/che_buy_tv"  # 撤买按钮ID
RESOURCE_ID_CHE_SELL_BTN = "com.hexin.plat.android:id/che_sell_tv"  # 撤卖按钮ID
RESOURCE_ID_OPTION_CANCEL = "com.hexin.plat.android:id/option_cancel"  # 撤卖按钮ID
RESOURCE_ID_DIALOG_CONTAINER = "com.hexin.plat.android:id/dialogplus_view_container" # 键盘精灵容器ID

# ths.py
RESOURCE_ID_BTN = "com.hexin.plat.android:id/btn"
RESOURCE_ID_REFRESH = "com.hexin.plat.android:id/refresh_img"
RESOURCE_ID_REFRESH_CHEDAN = "com.hexin.plat.android:id/title_bar_img"

########### XPath Constants
# base.py
XPATH_NAVIGATION_BAR = '//*[@resource-id="com.hexin.plat.android:id/btn"]/@bounds'  # 导航栏按钮边界XPath
XPATH_BALANCE_LAYOUT1 = '//*[@resource-id="com.hexin.plat.android:id/main_layout"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/descendant::android.widget.TextView/@text'  # 资产信息显示XPath
XPATH_BALANCE_LAYOUT2 = '//*[@resource-id="com.hexin.plat.android:id/main_layout"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[4]/descendant::android.widget.TextView/@text'  # 备用资产信息显示XPath
XPATH_POSITIONS_RECYCLER_VIEW = '//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout'  # 持仓信息的循环视图XPath
XPATH_POSITIONS_TEXT_VIEW = '//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout[{i}]/descendant::android.widget.TextView/@text'  # 持仓详细信息XPath
XPATH_ORDERS_RECYCLER_VIEW = '//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout'  # 撤单信息的循环视图XPath
XPATH_ORDERS_TEXT_VIEW = '//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i}]/descendant::android.widget.TextView/@text'  # 撤单详细信息XPath
XPATH_DIALOG_LAYOUT = '//*[@resource-id="com.hexin.plat.android:id/dialog_layout"]/descendant::android.widget.TextView/@text'  # 对话框内文本信息XPath
XPATH_DIALOG_TITLE = '//*[@resource-id="com.hexin.plat.android:id/dialog_title"]/@text'  # 对话框标题XPath
XPATH_DIALOG_CONTENT = '//*[@resource-id="com.hexin.plat.android:id/prompt_content"]/@text'  # 对话框内容XPath
XPATH_BTN_TRANSACTION = '//*[@resource-id="com.hexin.plat.android:id/btn_transaction"]/@bounds'  # 交易按钮边界XPath
XPATH_BOUND_ORDER = '//*[@resource-id="com.hexin.plat.android:id/auto_stockcode"]/@bounds'  # 下单边界XPath
XPATH_CANCEL_BTN = '//*[@resource-id="com.hexin.plat.android:id/cancel_btn"]'  # 取消按钮XPath
XPATH_CHE_DIALOG_TITLE = '//*[@resource-id="com.hexin.plat.android:id/title_view"]/@text' # 撤单确认标题
XPATH_CHE_DIALOG_CONTENT = '//*[@resource-id="com.hexin.plat.android:id/content_layout"]/descendant::android.widget.TextView/@text' # 撤单确认内容
XPATH_CHE_AREA = '//*[@resource-id="com.hexin.plat.android:id/option_chedan"]/@bounds' # 撤单区域边界XPath
XPATH_CHE_BUY_AREA = '//*[@resource-id="com.hexin.plat.android:id/option_chedan_and_buy"]/@bounds' # 撤单买区域
XPATH_CHE_CANCEL_AREA = '//*[@resource-id="com.hexin.plat.android:id/option_cancel"]/@bounds' # 取消区域
XPATH_OK_BTN = '//*[@resource-id="com.hexin.plat.android:id/ok_btn"]/@bounds' # 成功按钮区域
XPATH_CANCEL_BTN = '//*[@resource-id="com.hexin.plat.android:id/cancel_btn"]/@bounds' # 取消按钮区域