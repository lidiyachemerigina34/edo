﻿using System;
using System.Security.Cryptography.X509Certificates;
using System.IO.Packaging;
using System.Collections.Generic;
using System.Security.Cryptography;
using CryptoPro.Sharpei.Xml;
using System.Security.Cryptography.Xml;
using System.Xml;

namespace WindowsFormsApp6
{
    /// <summary>
    /// По мотивам http://blogs.msdn.com/b/vsod/archive/2009/06/19/how-to-sign-the-signatureline-using-office-open-xml.aspx
    /// </summary>
    public class Sign
    {
        static readonly string RT_OfficeDocument = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument";
        static readonly string OfficeObjectID = "idOfficeObject";
        static readonly string SignatureID = "idPackageSignature";
        static readonly string ManifestHashAlgorithm = CPSignedXml.XmlDsigGost3411Url;

 
        public static int File(string[] args)
        {
          
            if (args.Length < 2)
            {
                Console.WriteLine("Office.Sign <document> <certificate-dn>");
                return 1;
            }
            string document = args[0];
            string certificate_dn = args[1];

            //ОТКРЫВАЕМ ВСЕ СЕРТИФИКАТЫ 
            X509Store store = new X509Store("My", StoreLocation.CurrentUser);

            //ПЕРЕБИРАЕМ ИХ  И ИЩЕМ НАШ
            store.Open(OpenFlags.OpenExistingOnly | OpenFlags.ReadOnly);
            X509Certificate2Collection found = store.Certificates.Find(
                X509FindType.FindBySerialNumber, certificate_dn, false);


            //ЕСТЬ ЛИ ТАМ СЕКРЕТНЫЙ КЛЮЧ
            if (found.Count == 0)
            {
                Console.WriteLine("Секретный ключ не найден.");
                return 1;
            }
            if (found.Count > 1)
            {
                Console.WriteLine("Найдено более одного секретного ключа.");
                return 1;
            }


            X509Certificate2 certificate = found[0];
            //ОТКРЫВАЕТ ДОКУМЕНТ 
            using (Package package = Package.Open(document))
            {

                //ВЫПОЛНЯЕМ ПОДПИСЬ 
                SignAllParts(package, certificate);
            }

            Console.WriteLine("Документ {0} успешно подписан на ключе {1}.",
                document, certificate.Subject);
            return 0;
        }

        private static void SignAllParts(Package package, X509Certificate certificate)
        {
            List<Uri> PartstobeSigned = new List<Uri>();
            List<PackageRelationshipSelector> SignableReleationships = new List<PackageRelationshipSelector>();



            foreach (PackageRelationship relationship in package.GetRelationshipsByType(RT_OfficeDocument))
            {
                CreateListOfSignableItems(relationship, PartstobeSigned, SignableReleationships);
            }
            //БЫЛО В ДОКУМЕНТАЦИИ 
            PackageDigitalSignatureManager dsm = new PackageDigitalSignatureManager(package);
            dsm.CertificateOption = CertificateEmbeddingOption.InSignaturePart;
            dsm.HashAlgorithm = ManifestHashAlgorithm;


            try
            {

                //СОЗДАЕМ ПОДПИСЬ ПОДПИСЬ 
                System.Security.Cryptography.Xml.DataObject officeObject = CreateOfficeObject(SignatureID, dsm.HashAlgorithm);
                Reference officeObjectReference = new Reference("#" + OfficeObjectID);

                //ВЫЧИСЛЯЕМ ПОДПИСЬ 
                var sgn = dsm.Sign(PartstobeSigned, certificate, SignableReleationships, SignatureID, new System.Security.Cryptography.Xml.DataObject[] { officeObject }, new Reference[] { officeObjectReference });
            }
            catch (CryptographicException ex)
            {
                Console.WriteLine(ex.InnerException.ToString());
            }

        }

        //НЕВИДИМАЯ ПЕЧАТЬ 
        static System.Security.Cryptography.Xml.DataObject CreateOfficeObject(
           string signatureID, string manifestHashAlgorithm)
        {
            XmlDocument document = new XmlDocument();
            document.LoadXml(String.Format(
            "<OfficeObject>" +
                "<SignatureProperties xmlns=\"http://www.w3.org/2000/09/xmldsig#\">" +
                    "<SignatureProperty Id=\"idOfficeV1Details\" Target=\"{0}\">" +
                        "<SignatureInfoV1 xmlns=\"http://schemas.microsoft.com/office/2006/digsig\">" +
                          "<SetupID></SetupID>" +
                          "<ManifestHashAlgorithm>{1}</ManifestHashAlgorithm>" +
                          "<SignatureProviderId>{2}</SignatureProviderId>" +
                        "</SignatureInfoV1>" +
                    "</SignatureProperty>" +
                "</SignatureProperties>" +
            "</OfficeObject>", signatureID, manifestHashAlgorithm, "{F5AC7D23-DA04-45F5-ABCB-38CE7A982553}"));
            System.Security.Cryptography.Xml.DataObject officeObject = new System.Security.Cryptography.Xml.DataObject();
            // do not change the order of the following two lines
            officeObject.LoadXml(document.DocumentElement); // resets ID
            officeObject.Id = OfficeObjectID; // required ID, do not change
            return officeObject;
        }

        static void CreateListOfSignableItems(PackageRelationship relationship, List<Uri> PartstobeSigned, List<PackageRelationshipSelector> SignableReleationships)
        {
            // This function adds the releation to SignableReleationships. And then it gets the part based on the releationship. Parts URI gets added to the PartstobeSigned list.
            PackageRelationshipSelector selector = new PackageRelationshipSelector(relationship.SourceUri, PackageRelationshipSelectorType.Id, relationship.Id);
            SignableReleationships.Add(selector);
            if (relationship.TargetMode == TargetMode.Internal)
            {
                PackagePart part = relationship.Package.GetPart(PackUriHelper.ResolvePartUri(relationship.SourceUri, relationship.TargetUri));
                if (PartstobeSigned.Contains(part.Uri) == false)
                {
                    PartstobeSigned.Add(part.Uri);
                    // GetRelationships Function: Returns a Collection Of all the releationships that are owned by the part.
                    foreach (PackageRelationship childRelationship in part.GetRelationships())
                    {
                        CreateListOfSignableItems(childRelationship, PartstobeSigned, SignableReleationships);
                    }
                }
            }
        }
    }
}
