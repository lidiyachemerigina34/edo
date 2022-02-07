using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp6
{
    class template
    {
        //ВЫТАЩИТЬ ПОЛЯ ИЗ ДОКУМЕНТА
        public static string[] ReadFields(string path)
        {

            List<string> fields = new List<string>();
            if (Directory.Exists("~templateDocx"))
            {
                Directory.Delete("~templateDocx",true);
            }


            //ОТКРЫВАЕМ КАК ЗИП АРХИВ
               ZipFile.ExtractToDirectory("~template", "~templateDocx");
                string content = File.ReadAllText(@"~templateDocx\word\document.xml");

            //МАЯКИ КОТОРЫЕ МЫ ИЩЕМ
            string[] separatingStrings = { "[#", "#]" };
            string[] separatingStringsTag = { "<", ">" };
            string[] parts = content.Split(separatingStrings, System.StringSplitOptions.RemoveEmptyEntries);
       


            //СОБИРАЕМ НАЙДЕННЫЕ МАЯКИ В МАССИВ
            for(int i = 0; i< parts.Length; i++)
            {


                if(i%2 !=0)
                {

                    string tmp = parts[i];
                    string[] tmpParts = tmp.Split(separatingStringsTag, System.StringSplitOptions.RemoveEmptyEntries);
                    for(int j = 0; j< tmpParts.Length; j++)
                    {
                        if(tmpParts[j].IndexOf("w:") != -1)
                        {
                            tmpParts[j] = "";
                        }
                    }

                    tmp = String.Join("", tmpParts);
                    Console.WriteLine(tmp);
                    parts[i] = "[#"+tmp+"#]";

                    if(fields.IndexOf(tmp) == -1)
                    {
                        fields.Add(tmp);
                    }
                }
            }


            content = String.Join(" ",parts);





           // Console.WriteLine(content);
            File.WriteAllText(@"~templateDocx\word\document.xml", content);
            return fields.ToArray();
        }


        //ЗАПОЛНИТЬ ЭТИ ПОЛЯ
        public static void WriteFields(Dictionary<string, string> form)
        {


            //ОТКРЫВАЕМ ФОРМУ ДЛЯ СОХРАНЕНИЯ ДОКУМЕНТА
            SaveFileDialog fd = new SaveFileDialog();
     
            if (fd.ShowDialog() == DialogResult.OK)
            {
                string content = File.ReadAllText(@"~templateDocx\word\document.xml");

                //ПЕРЕБИРАЕМ ПЕРМЕННЫЕК И ЗАМЕНЯЕМ НА ТО ЧТО ВВЕЛИ В ФОРМУ
                foreach (KeyValuePair<string, string> p in form)
                {
                    content = content.Replace("[#" + p.Key + "#]", p.Value);
                }
                File.WriteAllText(@"~templateDocx\word\document.xml", content);


                ZipFile.CreateFromDirectory("~templateDocx", fd.FileName);
            }
        }
    }
}
