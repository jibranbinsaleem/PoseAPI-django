from safepay_python.safepay import *

env = Safepay(
    {
        "environment": "sandbox",
        "apiKey": "sec_85fcb230-c641-4cbf-98a5-4db00b3c6ae7",
        "v1Secret": "bddbd8e8ea346e9b26f6191e7d63dbccbd4d9a7824838c32eea64a9c79a3547b",
        "webhookSecret": "bddbd8e8ea346e9b26f6191e7d63dbccbd4d9a7824838c32eea64a9c79a3547b",
    }
)


payment_response = env.set_payment_details({"amount": 10000, "currency": "PKR"})

token = (payment_response['data'])['token']

checkout_url = env.get_checkout_url(
    {
        "beacon": token,
        "cancelUrl": "http://example.com/cancel",
        "orderId": "T800",
        "redirectUrl": "http://example.com/success",
        "source": "custom",
        "webhooks": False,
    }
)

signature_verification = env.is_signature_valid({"sig": "bddbd8e8ea346e9b26f6191e7d63dbccbd4d9a7824838c32eea64a9c79a3547b", "tracker": token})
print(signature_verification)
if signature_verification:
    print("Signature is valid")
else:
    print("Signature is invalid")
