import urllib.parse

from server import models, schemas
from server.cert import CA
from cryptography.hazmat.primitives import serialization
import os

CA_DIRECTORY = os.getenv('CA_SERVER_CA_DIRECTORY', "./server/ca")
ROUNDS = os.getenv('CA_SERVER_ROUNDS', 5)

ca = CA()

def create_app_user(req: schemas.AppUserCreate):
    app_user = models.AppUser(id=req.user)
    app_user.save(force_insert=True)
    return app_user


def get_app_users():
    try:
        return list(models.AppUser.select())
    except Exception as e:
        print(e, "An exception occurred when getting app users")
        return []


def get_app_user(user: str):
    return models.AppUser.filter(models.AppUser.id == user).first()


def delete_app_user(user:str):
    n = models.AppUser.delete().where(models.AppUser.user == user).execute()
    return n


def sanitize_cert(cert: bytes) -> str:
    # remove pem headers
    signed_cert_arr = cert.decode("ascii").splitlines()[1:-1]
    cleaned_signed_cert = "".join(signed_cert_arr)
    # make string url safe for restful travel
    print("cleaned_signed_cert", cleaned_signed_cert)
    return urllib.parse.quote_plus(cleaned_signed_cert, safe='*')


def generate_cert(installationId: str, csr: str, validityIndays: int):
    # De-url the string
    csr_url_dec = urllib.parse.unquote_plus(csr)
    # put in pem format
    csr_url_dec = "-----BEGIN CERTIFICATE REQUEST-----\n" + csr_url_dec + "\n-----END CERTIFICATE REQUEST-----"
    # switch to bytes
    csr_b64bytes = csr_url_dec.encode('ascii')

    signed_cert = ca.sign_certificate_request(csr_bytes=csr_b64bytes, validityIndays=validityIndays)
    # maybe create csr from string
    # convert signed_cert to string
    csr_dir = f"{CA_DIRECTORY}/csrs/{installationId}.csr"
    with open(csr_dir, "w") as text_file:
        text_file.write(csr)

    return sanitize_cert(signed_cert)


def create_certificate(req: schemas.CertificateCreate):
    certificate =  models.Certificate(
        installation_id=req.installationId,
        user=req.user,
        csr = req.csr,
        certificate = generate_cert(req.installationId, req.csr, validityIndays=365)
    )
    certificate.save()
    return certificate


def update_certificate(req:schemas.CertificateUpdate):
    certificate = get_certificate(req.installationId)
    if certificate is None:
        return

    certificate.csr = req.csr
    certificate.certificate=generate_cert(req.installationId, req.csr, validityIndays=365)
    certificate.save()

    return certificate


def get_certificates():
    return list(models.Certificate.select())


def get_certificate(installation_id: str):
    return models.Certificate.filter(models.Certificate.installation_id == installation_id).first()


def delete_certificate(installation_id: str):
    n = models.Certificate.delete().where(models.Certificate.installation_id == installation_id).execute()
    return n


def get_ca_certificate():
    cert = ca.ca_cert.public_bytes(serialization.Encoding.PEM)
    print("ca_cert", cert)
    return sanitize_cert(cert)
