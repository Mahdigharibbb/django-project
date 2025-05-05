from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, token, template='verifycode', is_link=False):
    """
        sending sms that needs template
    """
    try:
        api = KavenegarAPI(
            '562B55396938776D47356C65354F443643336946486F4F6D367353584B435572306732556C576C62717A343D'
        )
        params = {
            'receptor': receptor,
            'template': template,
            # 'token': token,
        }
        if is_link:
            params['token'] = token
        else:
            params['token'] = token
        # for key, value in tokens.items():
        #     params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI(
            '562B55396938776D47356C65354F443643336946486F4F6D367353584B435572306732556C576C62717A343D')
        params_buyer = {
            'receptor': receptor,
            'message': message,
            # 'sender': '2000660110'
        }
        response = api.sms_send(params_buyer)
        print(response)
    except APIException as e:
        print(e)
    except HTTPError as e:
        print(e)
