# deal
DEAL_IS_FOR_TAKEAWAY = '461'
DEAL_IS_FOR_DELIVERY = '459'
DEAL_IS_IN_1C_STAGE = 'C17:8'
DEAL_IS_EQUIPPED_STAGE = 'C17:NEW'
DEAL_IS_IN_DELIVERY_STAGE = 'C17:FINAL_INVOICE'
DEAL_IS_IN_APPROVED_STAGE = 'C17:10'
DEAL_IS_IN_UNAPPROVED_STAGE = 'C17:9'
DEAL_FLORIST_STAGE = 'C17:7'
DEAL_WAITING_FOR_SUPPLY_STAGE = 'C17:13'  # Ждет поставки
DEAL_RESERVED_STAGE = 'C17:6'  # Обработан \ Отложено

DEAL_INCOGNITO_MAPPING_CLIENT = {
   '0': False,
   '1': True
}

DEAL_INCOGNITO_MAPPING_OPERATOR = {
   '0': 'нет',
   '1': 'ВНИМАНИЕ \\- ДА\\!'
}

DEAL_SUPPLY_METHOD_MAPPING = {
   DEAL_IS_FOR_TAKEAWAY: 'Самовывоз',
   DEAL_IS_FOR_DELIVERY: 'Доставка'
}

# contact
CONTACT_HAS_PHONE = 'Y'

# user positions
FLORIST_POSITION_ID = '2343'  # Флорист

# has reserve
DEAL_HAS_RESERVE_YES = '2551'
DEAL_HAS_RESERVE_NO = '2553'
