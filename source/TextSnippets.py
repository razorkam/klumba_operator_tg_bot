from . import Commands

FIELD_IS_EMPTY_PLACEHOLDER = 'нет'

REQUEST_PASS_MESSAGE = 'Добро пожаловать в *интерфейс оператора Клумба*!\n' \
                               'Введите пароль для дальнейшей работы.\n' \

AUTHORIZATION_SUCCESSFUL = 'Авторизация по паролю пройдена!\n' \
                           'Теперь вы можете использовать возможности бота.'

AUTHORIZATION_UNSUCCESSFUL = 'Авторизация не пройдена. Попробуйте снова.'


UNKNOWN_COMMAND = 'Неизвестная команда. Попробуйте снова.'
SUGGEST_CANCEL_TEXT = 'Вы можете использовать {} для возврата в меню'.format(Commands.CANCEL)


FILE_LOADING_FAILED = 'Произошла ошибка при загрузке файла. Попробуйте снова.'

BOT_HELP_TEXT = 'Меню: \n' \
                '1. Загрузка фото букета и перевод в стадию *Заказ укомплектован*: \n {} \n\n' \
                '2. Загрузка фото чек-листа, назначение курьера и перевод в стадию *В доставке*: \n {}\n\n'\
                '3. Назначение курьера на любой стадии заказа \n {}'\
    .format(Commands.PHOTO_LOAD, Commands.CHECKLIST_LOAD, Commands.COURIER_SET)

ERROR_BITRIX_REQUEST = 'Произошла ошибка при обращении к серверу. \n' \
                       'Попробуйте снова или подождите некоторое время.'

UNKNOWN_ERROR = 'Произошла непредвиденная ошибка при обработке команды. \n' \
                'Попробуйте снова, или подождите некоторое время'

ASK_FOR_PHOTO_TEXT = 'Загрузите одно или несколько фото заказа.' + '\n' + SUGGEST_CANCEL_TEXT
ASK_FOR_DEAL_NUMBER_TEXT = 'Введите номер заказа.' + '\n' + SUGGEST_CANCEL_TEXT

PHOTO_LOADED_TEXT = 'Фото успешно загружено. \n' \
                    'Введите номер заказа для прикрепления, загрузите другие фото, или отмените загрузку, используя {}'\
    .format(Commands.CANCEL)

DEAL_UPDATED_TEXT = 'Заказ успешно обновлен!'

NO_PHOTOS_TEXT = 'Загрузите фото перед указанием номера заказа.'

NO_SUCH_DEAL = 'Заказ #{} не существует. Попробуйте снова.' + ''

PHOTOS_GETTING_CANCELLED = 'Загруженные фотографии очищены.'

PHOTO_LOAD_WRONG_DEAL_STAGE = 'Заказ должен находиться в стадии \'Выбит в 1С\' или \'Несогласовано\' ' \
                              'для перевода в стадию \'Заказ укомплектован\' '
CHECKLIST_LOAD_WRONG_DEAL_STAGE = 'Заказ должен находиться в стадии \'Согласовано\' для перевода в стадию \'В ' \
                                  'доставке\' '

COURIER_TEMPLATE = '*{}\n{}\n\n*'
COURIER_UNKNOWN_ID_TEXT = 'Неизвестный курьер. Попробуйте снова'
COURIER_EXISTS_TEXT = 'Курьер *{}* уже назначен для этого заказа.\n' \
                      'Используйте {}, чтобы продолжить без изменения, или назначьте нового курьера.\n' \
                      + SUGGEST_CANCEL_TEXT + '\n\n'
COURIER_SUGGESTION_TEXT = 'Назначьте курьера. \n' + SUGGEST_CANCEL_TEXT + '\n\n'

CHECKLIST_PHOTO_REQUIRE_TEMPLATE = 'Загрузите фото чек-листа.\n' + SUGGEST_CANCEL_TEXT + '\n\n' \
                                   '*Заказ №*: {}\n' \
                                   '*Что заказано*: {}\n' \
                                   '*Контакт*: {}\n' \
                                   '*Флорист*: {}\n' \
                                   '*Кто принял заказ*: {}\n' \
                                   '*Инкогнито*: {}\n' \
                                   '*Комментарий к товару*: {}\n' \
                                   '*Комментарий по доставке*: {}\n' \
                                   '*Сумма заказа общая(итоговая):* {}\n\n' \
                                   '*Тип оплаты*: {}\n' \
                                   '*Способ оплаты*: {}\n' \
                                   '*Статус оплаты*: {}\n' \
                                   '*Предоплата*: {}\n' \
                                   '*К оплате*: {}'


SETTING_COURIER_DEAL_INFO_TEMPLATE = '*Заказ №*: {}\n' \
                                   '*Что заказано*: {}\n' \
                                   '*Контакт*: {}\n' \
                                   '*Флорист*: {}\n' \
                                   '*Кто принял заказ*: {}\n' \
                                   '*Инкогнито*: {}\n' \
                                   '*Комментарий к товару*: {}\n' \
                                   '*Комментарий по доставке*: {}\n' \
                                   '*Сумма заказа общая(итоговая):* {}\n\n' \
                                   '*Тип оплаты*: {}\n' \
                                   '*Способ оплаты*: {}\n' \
                                   '*Статус оплаты*: {}\n' \
                                   '*Предоплата*: {}\n' \
                                   '*К оплате*: {}\n' \
                                   '*Курьер*: {}\n'

DEAL_COMMENT_APPROVED_STUB = 'ОК: Успешное согласование клиентом'
