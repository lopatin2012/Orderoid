# helpers/helper_character.py

from config import ATTR_BASE_COST, ATTR_COST_MULTIPLIER

# FIXME подумать над альтернативой. Слишком дорого.
def get_result_calculate_upgrade_cost(current_value: int) -> int:
    """
    Рассчитать стоимость улучшения характеристики.
    cost = base × multiplier^(current_value)
    """
    return int(ATTR_BASE_COST * (ATTR_COST_MULTIPLIER ** current_value))
