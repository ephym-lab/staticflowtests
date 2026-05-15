async def inject_lapfund_creds(data, **kwargs):
    return {
        "grant_type": "client_credentials",
        "client_id": "swagger-ui",       
        "client_secret": "swagger-secret-key"
    }