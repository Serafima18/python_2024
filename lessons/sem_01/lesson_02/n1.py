from uuid import uuid4

# Вспомогательная функция
def is_floats_eq(lhs: float, rhs: float, eps: float = 1e-6) -> bool:
    return abs(lhs - rhs) < eps

# Функции начисления скидок

def get_loyalty_discount(order: Order) -> float:
    if order.customer.loyalty_points >= 1000:
        return 5.0
    return 0.0

def get_item_amount_discount(order: Order) -> float:
    discount = 0.0
    for item in order.items:
        if item.amount >= 20:
            discount += item.price * item.amount * 0.10  # 10% скидка
    return discount

def get_general_amount_discount(order: Order) -> float:
    if len(order.items) >= 10:
        return order.price * 0.07  # 7% скидка на всю стоимость
    return 0.0