import grpc
from chirpstack_api import api
import json
import os

CHIRP_HOST = os.environ.get("CHIRP_HOST", "chirpstack")
CHIRP_PORT = int(os.environ.get("CHIRP_PORT", 8080))
CHIRP_USER = os.environ.get("CHIRP_USER", "admin")
CHIRP_PASSWORD = os.environ.get("CHIRP_PASSWORD", "")
DEV_EUI = os.environ.get("DEV_EUI").removeprefix(r"\x")


channel = grpc.insecure_channel("chirpstack:8080")
iss = api.InternalServiceStub(channel)

login_req = api.LoginRequest()
login_req.email = CHIRP_USER
login_req.password = CHIRP_PASSWORD

resp = iss.Login(login_req)

api_key_req = api.CreateApiKeyRequest()
api_key_req.api_key.name = "lorabridge_v2_key"
api_key_req.api_key.is_admin = True
auth_token = [("authorization", "Bearer %s" % resp.jwt)]
api_key_resp = iss.CreateApiKey(api_key_req, metadata=auth_token)

with open("/token/token.json", "w") as tfile:
    tfile.write(json.dumps({"id": api_key_resp.id, "token": api_key_resp.token}))

dss = api.DeviceServiceStub(channel)
dev_req = api.GetDeviceRequest()
dev_req.dev_eui = DEV_EUI
dev_resp = dss.Get(dev_req, metadata=auth_token)

with open(f"/device/{dev_resp.device.dev_eui}.json", "w") as dfile:
    dfile.write(
        json.dumps(
            {"dev_eui": dev_resp.device.dev_eui, "application_id": dev_resp.device.application_id}
        )
    )
