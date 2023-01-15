import bcrypt
import base64
import urllib.parse

from server import models, schemas
from server.cert import CA
from cryptography.hazmat.primitives import serialization

ROUNDS = 5

ca = CA()

# def create_user(req: schemas.UserCreate):
#     user = models.User(
#         username=req.username,
#         password=bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(ROUNDS))
#     )
#     user.save(force_insert=True)
#     print(user)
#     return user
#
# # Use conditions to compare the authenticating password with the stored one:
# # if bcrypt.checkpw(login.password('utc-8'), User.password):
# #     print("login success")
# # else:
# #     print("incorrect password")

# def get_users():
#     return list(models.User.select())
#
# def get_user(username: str):
#     return models.User.filter(models.User.username == username).first()


def create_app_user(req: schemas.AppUserCreate):
    print("got here", req.user)
    app_user = models.AppUser(id=req.user)
    print("got here2", app_user)
    app_user.save(force_insert=True)
    # print("shina", type(app_user.creator))
    return app_user

def get_app_users():
    try:
        return list(models.AppUser.select())
        # return []
    except Exception as e:
        print(e, "An exception occurred when getting app users")
        return []

    # return [app_user for app_user in models.AppUser.select().dicts()]

def get_app_user(user: str):
    return models.AppUser.filter(models.AppUser.id == user).first()

def delete_app_user(user:str):
    n = models.AppUser.delete().where(models.AppUser.user == user).execute()
    return n


# CA_KEY_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.key')
# CA_CERT_FILE = os.path.join(settings.ROOT_CRT_PATH, 'rootCA.crt')


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
    ca_dir = "server/ca"
    csr_dir = f"{ca_dir}/csrs/{installationId}.csr"
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


# //Create certificate from string
# function createCSRFromString(csrString){
#   var head = '-----BEGIN CERTIFICATE REQUEST-----\n';
#   var foot = '-----END CERTIFICATE REQUEST-----\n';
#   var isMultiple = false;
#   var newCSRString = head;
#
#   //Check if string size is a multiple of 64
#   if (csrString.length%64 == 0){
#     isMultiple = true;
#   }
#
#   for (i=1; i <= csrString.length; i++){
#     newCSRString += csrString[i-1];
#
#     if ((i != 1) && (i%64 == 0)){
#       newCSRString += '\n';
#     }
#
#     if ((i == csrString.length) && !isMultiple){
#       newCSRString += '\n';
#     }
#   }
#
#   newCSRString += foot;
#
#   return newCSRString;
# }