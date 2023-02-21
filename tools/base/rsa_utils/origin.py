from typing import Tuple, Union, List, Dict, Any
import rsa
import base64
import logging
import rsa
import os
import sys

if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../../'))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")

def generate_rsa_keys(bits=2048)->Tuple:
    pubkey,prikey = rsa.newkeys(bits,poolsize=os.cpu_count())
    return pubkey.save_pkcs1(), prikey.save_pkcs1()

if __name__ == "__main__":
    logging.debug("[RSA][TEST] Generate RSA keys")
    try:
        pubkey,prikey = generate_rsa_keys(bits=2048)
    except:
        import traceback
        logging.error(traceback.format_exc())
        logging.error("[RSA][TEST] Generate RSA keys failed")
    else:
        logging.debug("[RSA][TEST] Generate RSA keys success")
        logging.debug("[RSA][TEST] Public key:")
        logging.debug(str(pubkey,encoding="utf-8"))
        logging.debug("[RSA][TEST] Private key:")
        logging.debug(str(prikey,encoding="utf-8"))

class rsa_utils:
    def __init__(self,pubkey:Union[bytes,str,None]=None,prikey:Union[bytes,str,None]=None):
        self.has_priv_key = False
        self.has_pub_key = False
        self.verify_ok = False
        try:
            if prikey:
                prikey = bytes(prikey)
            self.private_key = rsa.PrivateKey.load_pkcs1(prikey)
        except:
            self.private_key = None
        else:
            self.has_priv_key = True
        try:
            if pubkey:
                pubkey = bytes(pubkey)
            self.public_key = rsa.PublicKey.load_pkcs1(pubkey)
        except:
            self.public_key = None
        else:
            self.has_pub_key = True
        if self.has_priv_key and self.has_pub_key:
            try:
                assert rsa.verify(b"Hello",rsa.sign(b"Hello",self.private_key,"SHA-256"),self.public_key) == "SHA-256"
            except:
                # 打印失败消息
                raise Exception("The Key Pairs are not matched")
            else:
                # 验证通过，设置True
                self.verify_ok = True

    def sign(self,data:bytes)->bytes:
        if self.has_priv_key:
            return rsa.sign(data,self.private_key,"SHA-256")
        else:
            raise Exception("No private key")
    
    def verify(self,data:bytes,sign:bytes)->bool:
        if self.has_pub_key:
            try:
                assert rsa.verify(data,sign,self.public_key) == "SHA-256"
            except rsa.VerificationError:
                return False
            except AssertionError:
                return False
            else:
                return True
        else:
            raise Exception("No public key")

    def encrypt(self,data:bytes)->bytes:
        if self.has_pub_key:
            return rsa.encrypt(data,self.public_key)
        else:
            raise Exception("No public key")

    def decrypt(self,data:bytes)->bytes:
        if self.has_priv_key:
            return rsa.decrypt(data,self.private_key)
        else:
            raise Exception("No private key")

if __name__ == "__main__":
    logging.debug("[RSA][TEST] importing the private key to module.")
    new_rsa_priv = rsa_utils(prikey=prikey)
    logging.debug("[RSA][TEST] Signing data")
    test_sign_bytes = b"""echo "Checking for the latest version of Minecraft Bedrock server..."
curl -H "Accept-Encoding: identity" -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/90.0.$RandNum.212 Safari/537.33" -o downloads/version.html https://minecraft.net/en-us/download/server/bedrock/
DownloadURL=$(grep -o 'https://minecraft.azureedge.net/bin-linux/[^"]*' downloads/version.html)
DownloadFile=$(echo "$DownloadURL" | sed 's#.*/##')
echo "$DownloadURL"
echo "$DownloadFile"
# Download latest version of Minecraft Bedrock dedicated server
echo "Downloading the latest version of Minecraft Bedrock server..."
UserName=$(whoami)
curl -H "Accept-Encoding: identity" -H "Accept-Language: en" -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/90.0.$RandNum.212 Safari/537.33" -o "downloads/$DownloadFile" "$DownloadURL"
unzip -o "downloads/$DownloadFile" """
    signed = new_rsa_priv.sign(test_sign_bytes)
    logging.debug("[RSA][TEST] Sign data success!")
    logging.debug("[RSA][TEST] importing the public key to module.")
    new_rsa_pub = rsa_utils(pubkey=pubkey)
    logging.debug("[RSA][TEST] Verifying data")
    try:
        assert new_rsa_pub.verify(test_sign_bytes,signed) == True
    except:
        logging.error("[RSA][TEST] Verifying data failed")
    else:
        logging.debug("[RSA][TEST] Verify data success!")

    logging.debug("[RSA][TEST] Encrypting data")
    test_encrypt_bytes = b"Hello"
    encrypted = new_rsa_pub.encrypt(test_encrypt_bytes)
    logging.debug("[RSA][TEST] Encrypt data success!")
    logging.debug("[RSA][TEST] Decrypting data")
    decrypted = new_rsa_priv.decrypt(encrypted)
    try:
        assert decrypted == test_encrypt_bytes
    except:
        logging.error("[RSA][TEST] Decrypt data failed")
    else:
        logging.debug("[RSA][TEST] Decrypt data success!")
    