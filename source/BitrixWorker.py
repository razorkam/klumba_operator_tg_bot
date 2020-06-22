import requests
from . import creds
import logging

from .BitrixFieldsAliases import *
from .BitrixFieldMappings import *
from .MiscConstants import *
from .ClientDealDesc import ClientDealDesc

from . import Utils
from . import TextSnippets


class BitrixWorker:
    SESSION = requests.session()
    REQUESTS_TIMEOUT = 10
    REQUESTS_MAX_ATTEMPTS = 3

    TgWorker = None

    def __init__(self, TGWorker):
        self.TgWorker = TGWorker

    def _send_request(self, user, method, params=None, custom_error_text='', notify_user=True):
        if params is None:
            params = {}

        for a in range(self.REQUESTS_MAX_ATTEMPTS):
            try:
                response = self.SESSION.post(url=creds.BITRIX_API_URL + method,
                                             json=params, timeout=self.REQUESTS_TIMEOUT)

                if response and response.ok:
                    json = response.json()

                    if 'result' in json:
                        return json
                    else:
                        error = 'Bitrix bad response %s : Attempt: %s, Called: %s : Request params: %s' \
                                % (a, json, custom_error_text, params)
                        logging.error(error)
                else:
                    error = 'Bitrix response failed - %s : Attempt: %s,  Called: %s : Request params: %s' \
                            % (a, response.text, custom_error_text, params)
                    logging.error(error)

            except Exception as e:
                error = 'Sending Bitrix api request %s' % e
                logging.error(error)

        if notify_user:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.ERROR_BITRIX_REQUEST})

        return None

    def update_deal_image(self, user, deal_id, digest):
        photos_list = user.get_deal_encoded_photos()

        if not photos_list:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.NO_PHOTOS_TEXT + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        deal = self._send_request(user, 'crm.deal.get', {'id': deal_id}, notify_user=False)

        if not deal or not deal['result']:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.NO_SUCH_DEAL.format(deal_id) + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        if deal['result'][DEAL_STAGE_ALIAS] != DEAL_IS_IN_1C_STAGE:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.PHOTO_LOAD_WRONG_DEAL_STAGE + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        update_obj = {'id': deal_id, 'fields': {DEAL_SMALL_PHOTO_ALIAS: [], DEAL_BIG_PHOTO_ALIAS: [],
                                                DEAL_STAGE_ALIAS: DEAL_IS_EQUIPPED_STAGE,
                                                DEAL_CLIENT_URL_ALIAS: digest}}

        is_takeaway = deal['result'][DEAL_SUPPLY_METHOD_ALIAS] == DEAL_IS_FOR_TAKEAWAY

        for photo in photos_list:
            update_obj['fields'][DEAL_SMALL_PHOTO_ALIAS].append({'fileData': [photo.name_small,
                                                                              photo.data_small]})

            update_obj['fields'][DEAL_BIG_PHOTO_ALIAS].append({'fileData': [photo.name_big,
                                                                            photo.data_big]})

            logging.info('Chat id %s updating deal %s with photo ids %s:', user.get_chat_id(),
                         deal_id, photo.name_small)

        # load fake photo to checklist in case of takeaway deal
        if is_takeaway:
            fake_photo = photos_list[0]
            update_obj['fields'][DEAL_CHECKLIST_ALIAS] = {'fileData': [fake_photo.name_small,
                                                                       fake_photo.data_small]}

        result = self._send_request(user, 'crm.deal.update', update_obj)

        if result['result']:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.DEAL_UPDATED_TEXT})
        else:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.ERROR_BITRIX_REQUEST + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        user.clear_deal_photos()
        return True

    def process_checklist_deal_info(self, deal_id, user):
        deal = self._send_request(user, 'crm.deal.get', {'id': deal_id}, notify_user=False)

        if not deal or not deal['result']:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.NO_SUCH_DEAL.format(deal_id) + '\n'
                                                             + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        data = deal['result']

        if data[DEAL_STAGE_ALIAS] != DEAL_IS_EQUIPPED_STAGE:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.CHECKLIST_LOAD_WRONG_DEAL_STAGE + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        user.checklist.deal_id = deal_id
        user.checklist.order = Utils.prepare_external_field(data, DEAL_ORDER_ALIAS)

        contact_data = {}

        try:
            contact_id = data[DEAL_CONTACT_ALIAS]
            contact_data = self._send_request(user, 'crm.contact.get',
                                              {'id': contact_id}, notify_user=False)

            if 'result' in contact_data:
                contact_data = contact_data['result']
            else:
                contact_data = {}

        except Exception as e:
            logging.error("Exception getting contact data, %s", e)

        contact_name = Utils.prepare_external_field(contact_data, CONTACT_USER_NAME_ALIAS)
        contact_phone = ''

        if contact_data[CONTACT_HAS_PHONE_ALIAS] == CONTACT_HAS_PHONE:
            contact_phone = Utils.prepare_external_field(contact_data[CONTACT_PHONE_ALIAS][0], 'VALUE')

        user.checklist.contact = contact_name + ' ' + contact_phone
        user.checklist.florist = Utils.prepare_external_field(data, DEAL_FLORIST_ALIAS)
        user.checklist.order_received_by = Utils.prepare_external_field(data, DEAL_ORDER_RECEIVED_BY_ALIAS)
        user.checklist.total_sum = Utils.prepare_external_field(data, DEAL_TOTAL_SUM_ALIAS)

        payment_type_id = Utils.prepare_external_field(data, DEAL_PAYMENT_TYPE_ALIAS)
        payment_types_dict = {}

        try:
            payment_type_field = self._send_request(user, 'crm.deal.userfield.get', {'id': PAYMENT_TYPE_FIELD_ID})
            payment_types = payment_type_field['result']['LIST']
            payment_types_dict = {pt['ID']: pt['VALUE'] for pt in payment_types}
        except Exception as e:
            logging.error("Exception getting payment types data, %s", e)

        user.checklist.payment_type = Utils.prepare_external_field(payment_types_dict, payment_type_id)

        payment_method_id = Utils.prepare_external_field(data, DEAL_PAYMENT_METHOD_ALIAS)
        payment_methods_dict = {}

        try:
            payment_method_field = self._send_request(user, 'crm.deal.userfield.get', {'id': PAYMENT_METHOD_FIELD_ID})
            payment_methods = payment_method_field['result']['LIST']
            payment_methods_dict = {pt['ID']: pt['VALUE'] for pt in payment_methods}
        except Exception as e:
            logging.error("Exception getting payment methods data, %s", e)

        user.checklist.payment_method = Utils.prepare_external_field(payment_methods_dict, payment_method_id)

        user.checklist.payment_status = Utils.prepare_external_field(data, DEAL_PAYMENT_STATUS_ALIAS)
        user.checklist.prepaid = Utils.prepare_external_field(data, DEAL_PREPAID_ALIAS)
        user.checklist.to_pay = Utils.prepare_external_field(data, DEAL_TO_PAY_ALIAS)

        return True

    def get_couriers_list(self, user):
        couriers = []

        try:
            courier_field = self._send_request(user, 'crm.deal.userfield.get', {'id': COURIER_FIELD_ID})
            couriers = courier_field['result']['LIST']
        except Exception as e:
            logging.error("Exception getting couriers data, %s", e)

        return {c['ID']: (' ' + COURIER_FIELD_DELIMETER + ' ')
            .join(Utils.prepare_external_field(c, 'VALUE').split(COURIER_FIELD_DELIMETER)) for c in couriers}

    def update_deal_checklist(self, user):
        update_obj = {'id': user.checklist.deal_id,
                      'fields': {DEAL_CHECKLIST_ALIAS: {'fileData': [user.checklist.photo_name,
                                                                     user.checklist.photo_data]},
                                 DEAL_STAGE_ALIAS: DEAL_IS_IN_DELIVERY_STAGE,
                                 DEAL_COURIER_ALIAS: user.checklist.courier_id}}

        result = self._send_request(user, 'crm.deal.update', update_obj)

        if result['result']:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.DEAL_UPDATED_TEXT})
        else:
            self.TgWorker.send_message(user.get_chat_id(), {'text': TextSnippets.ERROR_BITRIX_REQUEST + '\n'
                                                                    + TextSnippets.SUGGEST_CANCEL_TEXT})
            return False

        user.clear_checklist()
        return True

    def get_deal_info_for_client(self, deal_id):
        try:
            deal = self._send_request(None, 'crm.deal.get', {'id': deal_id}, notify_user=False)

            if not deal or not deal['result']:
                logging.error('Cant get deal info for deal %s', deal_id)
                return False

            data = deal['result']
            deal_desc = ClientDealDesc()

            address, location = Utils.prepare_deal_address(data, DEAL_ADDRESS_ALIAS)
            deal_desc.address = address

            contact_data = {}

            try:
                contact_id = data[DEAL_CONTACT_ALIAS]
                contact_data = self._send_request(None, 'crm.contact.get',
                                                  {'id': contact_id}, notify_user=False)

                if 'result' in contact_data:
                    contact_data = contact_data['result']
                else:
                    contact_data = {}

            except Exception as e:
                logging.error("Exception getting contact data, %s", e)

            contact_phone = ''

            if contact_data[CONTACT_HAS_PHONE_ALIAS] == CONTACT_HAS_PHONE:
                contact_phone = Utils.prepare_external_field(contact_data[CONTACT_PHONE_ALIAS][0], 'VALUE')

            deal_desc.phone = contact_phone
            deal_desc.date = Utils.prepare_deal_date(data, DEAL_DATE_ALIAS)
            deal_desc.time = Utils.prepare_deal_time(data, DEAL_TIME_ALIAS)
            deal_desc.sum = Utils.prepare_external_field(data, DEAL_SUM_ALIAS)

        except Exception as e:
            logging.error('Error getting client deal info: %s', e)
            return None

        return deal_desc


