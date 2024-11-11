from collections import defaultdict

# Глобальные счетчики
discount_counters = {
    'loyalty_discount': 0,
    'item_amount_discount': 0,
    'general_amount_discount': 0
}

def calculate_best_discount(order: Order):
    # Расчёт всех доступных скидок
    discounts = {
        'loyalty_discount': get_loyalty_discount(order),
        'item_amount_discount': get_item_amount_discount(order),
        'general_amount_discount': get_general_amount_discount(order)
    }

    # Находим максимальную скидку
    max_discount = max(discounts.values())

    # Увеличиваем счётчики всех стратегий с максимальной скидкой
    for key, value in discounts.items():
        if is_floats_eq(value, max_discount):
            discount_counters[key] += 1

    return order.price - max_discount
