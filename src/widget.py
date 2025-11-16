from .masks import get_mask_card_number ,get_mask_account
def mask_account_card(card_info:str) -> str:
    """Принимает данные карты, возвращает строку с замаскированным номером"""

    card_info_part = card_info.split()
    number_part = card_info_part [-1]

    if card_info_part[0].lower() == "счет":
        number_part = card_info_part [-1]
        masked = get_mask_account(number_part)
        return f"Счет{masked}"
    else:
        card_number =  number_part
        card_name = " ".join(card_info_part[:-1])
        masked = get_mask_card_number(card_number)
        return f"{card_name} {masked}"


def get_date(date:str) -> str:
    """Принимает строку с датой в формате
"2024-03-11T02:26:18.671407" и возвращает строку с датой в формате
"ДД.ММ.ГГГГ" """
    split_date = date.split("T")
    date_part = split_date[0]

    year = date_part[0:4]
    month = date_part[5:7]
    day = date_part[8:10]

    return f"{day}.{month}.{year}"


