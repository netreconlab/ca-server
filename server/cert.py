# source: https://stackoverflow.com/questions/56285000/python-cryptography-create-a-certificate-signed-by-an-existing-ca-and-export
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

RSA_PRIVATE_KEY = "./server/ca/private/cakey.pem"
ROOT_CA_CERT = "./server/ca/private/cacert.der"

class CA:
    def __init__(self):
        self.root_key = self.load_private_key()
        self.ca_cert = self.load_root_cert()

    def generate_private_key(self):
        if self.root_key == None:
            return

        root_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Write our key to disk for safe keeping
        with open(RSA_PRIVATE_KEY, "wb") as f:
            f.write(root_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            ))

        self.root_key = root_key

    def generate_root_cert(self, root_key: rsa.RSAPrivateKey):
        if self.ca_cert == None:
            return
            # Various details about who we are. For a self-signed certificate the
        # subject and issuer are always the same.
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Kentucky"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Lexington"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"1 Degree Technologies LLC"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"AlleyOop"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"AlleyOop CA"),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"support@1degreetech.com"),
        ])

        root_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            root_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 365 days
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
            # Sign our certificate with our private key
        ).sign(root_key, hashes.SHA256())

        with open(ROOT_CA_CERT, "wb") as f:
            f.write(root_cert.public_bytes(serialization.Encoding.DER))

    def load_private_key(self) -> rsa.RSAPrivateKey:
        with open(RSA_PRIVATE_KEY, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    def load_root_cert(self) -> Certificate:
        with open(ROOT_CA_CERT, "rb") as f:
            return x509.load_der_x509_certificate(f.read())

    def load_cert(self, der_data):
        return x509.load_der_x509_certificate(der_data)

    def sign_certificate_request(self, csr_bytes: bytes, validityIndays: int) -> bytes:
        csr_cert = x509.load_pem_x509_csr(csr_bytes)
        cert = x509.CertificateBuilder().subject_name(
            csr_cert.subject
        ).issuer_name(
            self.ca_cert.subject
        ).public_key(
            csr_cert.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 60 days
            datetime.utcnow() + timedelta(days=validityIndays)
        # Sign our certificate with our private key
        ).sign(self.root_key, hashes.SHA256())

        # return DER certificate
        return cert.public_bytes(serialization.Encoding.PEM)

def get_test_csr():
    # Now we want to generate a cert from that root
    cert_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
         # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Texas"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Austin"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"New Org Name!"),
     ])).add_extension(
         x509.SubjectAlternativeName([
             # Describe what sites we want this certificate for.
             x509.DNSName(u"mysite.com"),
             x509.DNSName(u"www.mysite.com"),
             x509.DNSName(u"subdomain.mysite.com"),
         ]),
         critical=False,
     # Sign the CSR with our private key.
     ).sign(cert_key, hashes.SHA256())

    return  csr.public_bytes(serialization.Encoding.PEM)