from kavenegar import *


def send_otp_code(phone_number,code):
    try:
        api = KavenegarAPI('Your APIKey')
        params = {
            'sender': '',  # optional
            'receptor': '',  # multiple mobile number, split by comma
            'message': '',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
