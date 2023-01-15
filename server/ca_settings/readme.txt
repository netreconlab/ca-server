#Followed steps in this link to create CA http://stackoverflow.com/questions/21297139/how-do-you-sign-certificate-signing-request-with-your-certification-authority

#Create CA Certificate (Do this and convert cert to DEM below)
##For EC
###Generate key
openssl ecparam -out cakey.pem -name prime256v1 -genkey

###Generate certificate
openssl req -config openssl-ca.cnf -new -key cakey.pem -x509 -nodes -days 365 -sha256  -out ca/cert.pem -outform PEM

##For RSA Key + Certificate
openssl req -x509 -config openssl-ca.cnf -newkey rsa:4096 -sha256 -days 365 -nodes -out ./cacert.pem -outform PEM
openssl req -x509 -config openssl-ca.cnf -newkey rsa:1024 -sha1 -nodes -out alleyoopCA/cacert.pem -outform PEM
openssl req -x509 -config openssl-ca.cnf -newkey rsa:1024 -sha1 -nodes -out cacert.der -outform DER

#Convert PEM to DER (Need to do every time you create a new certificate
openssl x509 -in ./cacert.pem -outform DER -out ./cacert.der

#Check CA certificate
openssl x509 -in ./cacert.der -inform DER -text -noout

#Check purpose of certificate
openssl x509 -purpose -in ./cacert.der -inform DER

#Create server CSR
openssl req -config openssl-server.cnf -newkey rsa:2048 -sha256 -nodes -out ./csrs/server.csr -outform PEM

#Sign a certificate with CA private key
openssl x509 -req -sha256 -days 60 -in ./csrs/test.csr -CA ./cert.pem -CAkey ca/cakey.pem -CAserial ./cacert.srl -out ./certs/testUserCert.der -outform DER

openssl x509 -req -in alleyoopCA/csrs/server.csr -CA alleyoopCA/cacert.pem -CAkey alleyoopCA/private/cakey.pem -CAserial cacert.srl -out alleyoopCA/certs/server.der -outform DER
openssl x509 -req -in Certificates/server.csr -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out server.der -outform DER

#Check certificate chain
openssl s_client -connect wamresearch.ece.ufl.edu:3000 -showcerts | grep "^ "
