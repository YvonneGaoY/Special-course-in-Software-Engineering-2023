from datetime import datetime, timedelta

# 模拟一些位置信息
LOCATIONS = [
    "Haidian District",
    "Minhang District",
    "Xuhui District"
]

# Simulated restaurant and menu information
RESTANRANTS = {
    "Pizza Hut": {
        "location": "Haidian District",
        "menu": ["Pizza", "Salad", "Steak"]
    },
    "McDonald's": {
        "location": "Minhang District",
        "menu": ["Burger", "Fried chicken", "Milkshake"]
    },
    "Hidden aquatic products": {
        "location": "Xuhui District",
        "menu": ["Sushi", "Salmon Sashimi", " Eel"]
    },
    "Yuanjia": {
        "location": "Xuhui District",
        "menu": ["Bibimbap", "Cold noodles", "Beef platter"]
    },
}


class OrderManager:
    def __init__(self):
        self.orders = {}
        self.orders_prefix = "orderid"
        self.orders_num = 1

    # def create_order(self, order_id, items, create_time):
    def create_order(self, items, create_time):
        order_id = f"{self.orders_prefix}{self.orders_num}"
        self.orders_num += 1
        if order_id not in self.orders:
            self.orders[order_id] = {
                "Meal": items, "Status": "Preparing", "Creation time": create_time}
        else:
            return None
        return order_id

    def get_order_status(self, order_id, current_time_str):
        oid_string = ', '.join(self.orders.keys())
        print(f"[OrderManager] get_order_status||{oid_string}")
        if order_id in self.orders:
            # 将字符串解析为 datetime 对象
            create_time = datetime.strptime(
                self.orders[order_id]["Creation time"], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.strptime(
                current_time_str, "%Y-%m-%d %H:%M:%S")
            # 计算两个 datetime 对象之间的时间差
            time_difference = current_time - create_time

            if time_difference > timedelta(minutes=1):
                self.orders[order_id]["Status"] = "Finished"
            return self.orders[order_id]["Status"]
        else:
            return None

    def delete_order(self, order_id):
        oid_string = ', '.join(self.orders.keys())
        print(f"[OrderManager] delete_order||{oid_string}")
        if order_id in self.orders:
            del self.orders[order_id]
        else:
            return None
        return "success"


# 创建订单管理器实例
ORDER_MANAGER = OrderManager()
