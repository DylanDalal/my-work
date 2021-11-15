using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace TManagerAPI
{
    public class Program
    {
        public static string JsonData = File.ReadAllText(@"C:\Users\Dylan\AppData\Local\Packages\e6b2dd56-945f-4c69-97f8-5dd4d7862dc5_ahkfgx9hz8qjg\LocalState\JSONTest.txt");
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
