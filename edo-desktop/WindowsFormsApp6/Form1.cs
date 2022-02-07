using CefSharp;
using CefSharp.WinForms;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using WindowsFormsApp6.Encrypto;

namespace WindowsFormsApp6
{
    public partial class Form1 : Form
    {
        private void chromiumWebBrowser1_ConsoleMessage(object sender, ConsoleMessageEventArgs e)
        {
            Console.WriteLine("////////////////////");
            Console.WriteLine(e.Message);
            Console.WriteLine("////////////////////");
            string[] command = e.Message.Split('|');
            if(command[0] == "command")
            {
                switch (command[1])
                {

                    //загрузка шаблона
                    //рузльтат:список полей
                    case "LOAD_TEMPLATE":


                        WebClient client = new WebClient();
                        //СКАЧИВАЕТСЯ ШАБЛОН
                        client.DownloadFile(new Uri(command[2]), "~template");

                        //ЧИТАЮТСЯ ПОЛЯ
                        string[] fields = template.ReadFields("~template");

                        //ПЕЧАТАЮТСЯ В ИНТЕРФЕЙС
                        chromiumWebBrowser1.ExecuteScriptAsync("  FileManagerBus.dispatchEvent(new CustomEvent('LoadFiles', {detail:{ type: 'DocumentChangeTemplateSuccess',fields:['" + String.Join("','", fields) + "']}}))");
                
                        break;
                    //ЗАПОЛНИТЬ ПОЛЯ ШАБЛОНА
                    case "CREATE_TEMPLATE":


                        Dictionary<string, string> form = new Dictionary<string, string>();
                        
                        //СПИСОК ЗАПОЛНЕНЫХ ПОЛЕЙ   
                        string[] fieldsForm = command[2].Split(':');


                        for (int i = 0; i < fieldsForm.Length / 2; i++)
                        {
                            form.Add(fieldsForm[i * 2], fieldsForm[i * 2 + 1]);
                        }
                        
                        //ПЕРЕДАЕМ ПОЛЯ В ШАБЛОН
                        template.WriteFields(form);
                        chromiumWebBrowser1.ExecuteScriptAsync("  FileManagerBus.dispatchEvent(new CustomEvent('LoadFiles', {detail:{ type: 'DOCUMENT_CREATE',fields:[]}}))");

                        break;
                    //ПОДПИСЬ ДОКУМЕНТА
                    case "SIGN":
                        WebClient document = new WebClient();

                        //СКАЧИВАЕМ ДОКУМЕНТ
                        document.DownloadFile(new Uri(command[2]), "~document");

                        //ЧИТАЕМ СЕРИЙНЫЙ НОМЕР СЕРТИФИКАТА
                        string number = File.ReadAllText("key.txt");
                        //ВЫЗЫВАЕМ МЕТОД ДЛЯ ПОДПИСИ
                        Sign.File(
                          new string[] {"~document", number}
                            );


                        //ЗАГРУЖАЕМ ФАЙЛ НА СЕРВЕР
                        WebClient fileUpload = new WebClient();
                        try
                        {
                            string fileName = command[2].Split('/').Last();
                            File.WriteAllBytes(fileName,File.ReadAllBytes("~document"));
                            byte[] responce = fileUpload.UploadFile("http://api.live-widget.ru/catalog/load/?type=file&reconciliation=" + command[4], fileName);
                            string signObj = Encoding.UTF8.GetString(responce);
                        }
                        catch (WebException ex)
                        {
                            String responseFromServer = ex.Message.ToString() + " ";
                            if (ex.Response != null)
                            {
                                using (WebResponse response = ex.Response)
                                {
                                    Stream dataRs = response.GetResponseStream();
                                    using (StreamReader reader = new StreamReader(dataRs))
                                    {
                                        responseFromServer += reader.ReadToEnd();
                                    }
                                }
                            }
                            Console.WriteLine(responseFromServer);
                        }
                        chromiumWebBrowser1.ExecuteScriptAsync("  FileManagerBus.dispatchEvent(new CustomEvent('LoadFiles', {detail:{ type: 'ReconciliationSignSuccess',id:["+ command[4] + "]}}))");

                        break;
                  


                    //ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
                    case "UPLOAD_FILE":
                       
                        OpenFileDialog fd = new OpenFileDialog();
                        //открыть диалог выбора файлов
                        if (fd.ShowDialog() == DialogResult.OK)
                        {
                            symmetric sEncode = new symmetric();
                            //ЗАЩИФРОВАЛИ ФАЙЛ
                            sEncode.encrypt(fd.FileName);
                            //ПОЛУЧИЛИ КЛЮЧ ШИФРОВАНИЯ 
                            string keysend = File.ReadAllText("key_tmp.key");
                            //ВЫПОЛНИЛИ ГЕНЕРАЦИЮ КЛЮЧЕЙ ПО Д/Х И ПОЛУЧИЛИ МАССИВ ОТКРЫТЫХ КЛЮЧЕЙ RSA

                            //в эту функцию мы передаем id хранилища
                            string[] keysDH = DH.getKeys(command[1]);
                            //ЗАЩИФРОВАЛИ  КЛЮЧ И ПОЛУЧИЛИ МАССИВ КЛЮЧЕЙ ПОД КАЖДОГО ПОЛЬЗОВАТЕЛЯ  
                            string[] keysRSA = asymmetric.encrypt(keysend, keysDH);
                            //ОТПРАВИЛИ ФАЙЛ И КЛЮЧИ
                            sendFile("file_tmp.data", keysRSA);

                        }


                        break;
                    //СКАЧИВАНИЕ ФАЙЛА
                    case "LOAD_FILE":
                        //скачивает файл
                        //id файла И id текущего пользователя
                        getFile(command[1], command[2]);

                        //сохраняем зашифрованный ключ
                        string key = File.ReadAllText("key_tmp.key");
                        //ключ по ДХ
                        string keyDH = File.ReadAllText("DH_KEYS.data");

                        //расшифровываем ключ aes
                        byte[] keyResult = asymmetric.decrypt(key, keyDH);
                        symmetric sDecode = new symmetric();
                        //расшифровываем файл
                        byte[] file = sDecode.decrypt("file_tmp.data", keyResult);

                        //и сохраняем его
                        SaveFileDialog sd = new SaveFileDialog();
                        if (sd.ShowDialog() == DialogResult.OK)
                        {
                            File.WriteAllBytes(sd.FileName, file);
                        }

                        break;

                    case "OPEN":
                        WebClient fileLoader = new WebClient();

                        //СКАЧИВАЕМ ДОКУМЕНТ
                        fileLoader.DownloadFile(new Uri(command[2]), "~document_tmp");
                        Process.Start("~document_tmp");


                        break;
                }

            }
        }
















        public Form1()
        {

            CefSettings settings = new CefSettings();
            settings.CachePath = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\CEF";
            CefSharp.Cef.Initialize(settings);

            InitializeComponent();

            BrowserSettings setting = new BrowserSettings();
            setting.ApplicationCache = CefSharp.CefState.Enabled;
            chromiumWebBrowser1.BrowserSettings = setting;
            chromiumWebBrowser1.Load("https://api.live-widget.ru/?v=50");




        }


        private void getFile(string idFile, string token, string options = "")
        {
            WebClient fileUpload = new WebClient();
            try
            {
                string fileName = idFile.Split('/').Last();
                File.WriteAllBytes(fileName, File.ReadAllBytes("~document"));
                byte[] responce = fileUpload.UploadFile("http://api.live-widget.ru/catalog/load/?type=file&id=" + idFile, fileName);
                string signObj = Encoding.UTF8.GetString(responce);
            }
            catch (WebException ex)
            {
                String responseFromServer = ex.Message.ToString() + " ";
                if (ex.Response != null)
                {
                    using (WebResponse response = ex.Response)
                    {
                        Stream dataRs = response.GetResponseStream();
                        using (StreamReader reader = new StreamReader(dataRs))
                        {
                            responseFromServer += reader.ReadToEnd();
                        }
                    }
                }
                Console.WriteLine(responseFromServer);
            }
        }

        private string sendFile(string path, string[] keys, string options = "")
        {

            WebClient fileUpload = new WebClient();
            try
            {
                byte[] responce = fileUpload.UploadFile("http://api.live-widget.ru/catalog/load/?" + options, path);
                return Encoding.UTF8.GetString(responce);
            }
            catch (WebException ex)
            {
                String responseFromServer = ex.Message.ToString() + " ";
                if (ex.Response != null)
                {
                    using (WebResponse response = ex.Response)
                    {
                        Stream dataRs = response.GetResponseStream();
                        using (StreamReader reader = new StreamReader(dataRs))
                        {
                            responseFromServer += reader.ReadToEnd();
                        }
                    }
                }

                return "";

            }
        }
    }
}
