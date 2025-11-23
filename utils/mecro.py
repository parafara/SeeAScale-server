from decimal import Decimal, ROUND_DOWN

def unit_standardization(quantity, prefix) -> Decimal:
    while prefix > 3 and quantity < 1:
        prefix -= 1
        quantity *= 1000

        print(prefix, quantity)
        
    while 3 >= prefix > -3 and quantity < 1:
        prefix -= 1
        quantity *= 10

        print(prefix, quantity)

    while -3 >= prefix > -10 and quantity < 1:
        prefix -= 1
        quantity *= 1000

        print(prefix, quantity)

    while prefix < -3 and quantity >= 1000:
        prefix += 1
        quantity /= 1000
        
    while -3 <= prefix < 3 and quantity >= 10:
        prefix += 1
        quantity /= 10

    while 3 <= prefix < 10 and quantity >= 1000:
        prefix += 1
        quantity /= 1000

    quantity = quantity.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    return quantity, prefix