using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TaskManager2
{
    public partial class App : Application
    {
        public static List<Item> list;

        public static int attendees;

        public static Item transfer;

        public App()
        {
            InitializeComponent();
            MainPage = new NavigationPage(new MainPage());
            list = new List<Item>();
            transfer = new Item();
        }

        protected override void OnStart()
        {
        }

        protected override void OnSleep()
        {
        }

        protected override void OnResume()
        {
        }

        public string SaveList()
        {
            string writeToFile = "";
            for (int i = 0; i < list.Count; i++)
            {
                writeToFile += list[i].Type + "\t" + list[i].Name
                    + "\t" + list[i].Description + "\t" + list[i].Priority;
                if (list[i].Type == "Task")
                { //Type    Name    Desc    Prior   Deadl   IsCompleted
                    writeToFile += "\t" + (list[i] as TaskObj).Deadline +
                        "\t" + (list[i] as TaskObj).isCompleted;
                } //Type    Name    Desc    Prior   Deadl   Start
                  //Stop    AttList.Count   Each Attendee (separated by spaces)
                else if (list[i].Type == "Appointment")
                {
                    writeToFile += "\t" + (list[i] as Appointment).Deadline +
                        "\t" + (list[i] as Appointment).Start + "\t" + (list[i]
                        as Appointment).Stop + "\t" +
                        (list[i] as Appointment).Attendees.Count;
                    for (int o = 0; o < (list[i] as Appointment).Attendees.Count; i++)
                    {
                        writeToFile += "\t" + (list[i] as Appointment).Attendees[o];
                    }
                }
                writeToFile += "\n";
            }
            return writeToFile;
        }
    }
}
