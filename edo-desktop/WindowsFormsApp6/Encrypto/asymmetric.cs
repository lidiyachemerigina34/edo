using Org.BouncyCastle.Crypto;
using Org.BouncyCastle.Crypto.Parameters;
using Org.BouncyCastle.OpenSsl;
using Org.BouncyCastle.Security;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp6.Encrypto
{
    class asymmetric
    {
        public static string[] encrypt(string key, string[] keysDH)
        {
            List<string> keys = new List<string>();
      

  

            UnicodeEncoding byteConverter = new UnicodeEncoding();

            //ПЕРЕДБИРАЕМ КЛЮЧИ
            foreach(string keyRSA in keysDH)
            {
                //ЗАГРУЖАЕМ КАЖДЫЙ КЛЮЧ
                RSACryptoServiceProvider RSA = ImportPublicKey(keyRSA);
                RSAParameters publicKey = RSA.ExportParameters(false);
                //ШИФРУЕМ
                keys.Add(byteConverter.GetString(RSAEncrypt(byteConverter.GetBytes(key), publicKey, false)));
            }

            return keys.ToArray();
      
        }

        public static byte[] decrypt(string key, string keyRSA)
        {
            UnicodeEncoding byteConverter = new UnicodeEncoding();
           //ЗАГРУЖАЕМ КЛЮЧ В БИБЛИОТЕКУ
            RSACryptoServiceProvider RSA = ImportPrivateKey(keyRSA);
            RSAParameters privateKey = RSA.ExportParameters(true);

            return RSADecrypt(byteConverter.GetBytes(key), privateKey, false);
        }

        public static RSACryptoServiceProvider RSA;
        public static RSAParameters privateKey;



        //ЧТЕНИЕ ЗАКРЫТОГОК КЛЮЧА

        public static RSACryptoServiceProvider ImportPrivateKey(string pem)
        {
            PemReader pr = new PemReader(new StringReader(pem));
            AsymmetricCipherKeyPair KeyPair = (AsymmetricCipherKeyPair)pr.ReadObject();
            RSAParameters rsaParams = DotNetUtilities.ToRSAParameters((RsaPrivateCrtKeyParameters)KeyPair.Private);

            RSACryptoServiceProvider csp = new RSACryptoServiceProvider();// cspParams);
            csp.ImportParameters(rsaParams);
            return csp;
        }

        //ЧТЕНИЕ ОТКРЫТОГО КЛЮЧА
        public static RSACryptoServiceProvider ImportPublicKey(string pem)
        {
            PemReader pr = new PemReader(new StringReader(pem));
            AsymmetricKeyParameter publicKey = (AsymmetricKeyParameter)pr.ReadObject();
            RSAParameters rsaParams = DotNetUtilities.ToRSAParameters((RsaKeyParameters)publicKey);

            RSACryptoServiceProvider csp = new RSACryptoServiceProvider();// cspParams);
            csp.ImportParameters(rsaParams);
            return csp;
        }



        static public byte[] RSAEncrypt(byte[] DataToEncrypt, RSAParameters RSAKeyInfo, bool DoOAEPPadding)
        {
            RSACryptoServiceProvider RSA = new RSACryptoServiceProvider();
            RSA.ImportParameters(RSAKeyInfo);
            return RSA.Encrypt(DataToEncrypt, DoOAEPPadding);
        }

        static public byte[] RSADecrypt(byte[] DataToDecrypt, RSAParameters RSAKeyInfo, bool DoOAEPPadding)
        {
            RSACryptoServiceProvider RSA = new RSACryptoServiceProvider();
            RSA.ImportParameters(RSAKeyInfo);
            return RSA.Decrypt(DataToDecrypt, DoOAEPPadding);
        }





    }
}
