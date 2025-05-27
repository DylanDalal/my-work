using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using Xamarin.Forms;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace TaskManager2
{
    public partial class MainPage : ContentPage
    {
        public string ButtonVisibility { get; set; }

        public MainPage()
        {
            InitializeComponent();

            var existingPages = Navigation.NavigationStack;
            foreach (var page in existingPages)
            {
                Navigation.RemovePage(page);
            }

            try
            {
                int count = App.list.Count;
                if (count != 0)
                {
                    EditButton.IsEnabled = true;
                    CompleteButton.IsEnabled = true;
                    DeleteButton.IsEnabled = true;
                    ListButton.IsEnabled = true;
                    SaveButton.IsEnabled = true;
                }
            }
            catch (NullReferenceException)
            {
                EditButton.IsEnabled = false;
                CompleteButton.IsEnabled = false;
                DeleteButton.IsEnabled = false;
                ListButton.IsEnabled = false;
                SaveButton.IsEnabled = false;
            }
        }

        async void OnPushedGoToCreate(object sender, EventArgs args)
        {
            await Navigation.PushAsync(new CreatePage(), true);
        }

        async void OnPushedGoToDelete(object sender, EventArgs args)
        {
            await Navigation.PushAsync(new DeletePage(), true);
        }
        async void OnPushedGoToEdit(object sender, EventArgs args)
        {
            await Navigation.PushAsync(new EditPage(), true);
        }
        async void OnPushedGoToComplete(object sender, EventArgs args)
        {
            await Navigation.PushAsync(new CompletePage(), true);
        }
        async void OnPushedGoToList(object sender, EventArgs args)
        {
            await Navigation.PushAsync(new ListPage(), true);
        }
        async void OnPushedSaveList(object sender, EventArgs args)
        {
            bool custom = false;
            bool proceed = false;
            string selection = await DisplayActionSheet("Where would you like "
                + " to save your list?", "Cancel", null, "Default directory",
                "Custom directory");
            string filename = "";
            string filepath = "";

            if (selection == "Application directory")
            {
                try //This doesn't work. Needs to be fixed.
                {
                    filename = await DisplayPromptAsync("Filename",
                        "Please provide a filename for your list.");
                    proceed = true;
                }
                catch (NullReferenceException)
                {
                    proceed = false;
                }
            }
            else if (selection == "Custom directory")
            {
                await DisplayPromptAsync("Sorry!", "Custom Directory not yet supported.");
                //filename = await DisplayPromptAsync("Filename",
                //   "Please provide a filename for your list.");
                //filepath = await DisplayPromptAsync("File Path",
                //   "Please provide a path for where to save your list.");
                proceed = true;
                custom = true;
            }
            if (proceed)
            {
                string write = writeToFile();
                if (filename.Substring(Math.Max(0, filename.Length - 4)) != ".txt")
                {
                    filename += ".txt";
                }
                string check = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), filename);
                File.WriteAllText(check, write);
                await DisplayAlert("Success!", "File " + filename + " written to path " + check, "OK");
            }
        }

        public string writeToFile()
        {
            string writeToFile = "";
            for (int i = 0; i < App.list.Count; i++)
            {
                writeToFile += App.list[i].Type + "\t" + App.list[i].Name
                    + "\t" + App.list[i].Description + "\t" + App.list[i].Priority;
                if (App.list[i].Type == "Task")
                { //Type    Name    Desc    Prior   Deadl   IsCompleted
                    writeToFile += "\t" + (App.list[i] as TaskObj).Deadline +
                        "\t" + (App.list[i] as TaskObj).isCompleted;
                } //Type    Name    Desc    Prior   Deadl   Start
                  //Stop    AttList.Count   Each Attendee (separated by spaces)
                else if (App.list[i].Type == "Appointment")
                {
                    writeToFile += "\t" + (App.list[i] as Appointment).Deadline +
                        "\t" + (App.list[i] as Appointment).Start + "\t" + (App.list[i]
                        as Appointment).Stop + "\t" +
                        (App.list[i] as Appointment).Attendees.Count;
                    for (int o = 0; o < (App.list[i] as Appointment).Attendees.Count; o++)
                    {
                        writeToFile += "\t" + (App.list[i] as Appointment).Attendees[o];
                    }
                }
                writeToFile += "\n";
            }
            return writeToFile;
        }

        async void OnPushedLoadList(object sender, EventArgs args)
        {
            bool custom = false;
            bool MessageBox = true;
            bool proceed = false;
            bool proceed1 = false;
            int counter = 0;
            string filename = "";
            string filepath = "";
            List<JObject> JObjectList = new List<JObject>();

            if (App.list.Count != 0)
            {
                MessageBox = false;
                MessageBox = await DisplayAlert("Wait!", "This will replace your current list. " +
                    "Would you like to continue?", "Yes", "No");
            }
            if (MessageBox)
            {
                string selection = await DisplayActionSheet("From where would you like "
                                    + " to load your list?", "Cancel", null, "Default directory",
                                    "Custom directory", "Default JSON web list", "Custom JSON web list");

                if (selection == "Default directory")  //This doesn't work. Needs to be fixed.
                {
                    try
                    {
                        filename = await DisplayPromptAsync("Filename",
                            "Please provide a filename for your list.");
                        proceed = true;
                    }
                    catch (NullReferenceException)
                    {
                        proceed = false;
                    }
                }
                else if (selection == "Custom Directory")
                {
                    await DisplayPromptAsync("Sorry!", "Custom Directory not yet supported.");
                    //filename = await DisplayPromptAsync("Filename",
                           //"Please provide a filename for your list.");
                    //filepath = await DisplayPromptAsync("File Path",
                           //"Please provide a path for where to retrieve your list.");
                    //custom = true;
                    proceed = false;
                }
                else if (selection == "Custom JSON web list")
                {
                    await DisplayPromptAsync("Sorry!", "Custom JSON web list not yet supported.");
                    //filename = await DisplayPromptAsync("Filename",
                    //"Please provide a filename for your list.");
                    //filepath = await DisplayPromptAsync("File Path",
                    //"Please provide a path for where to retrieve your list.");
                    //custom = true;
                    proceed = false;
                }
                else if (selection == "Default JSON web list")
                {
                    var handler = new WebRequestHandler();
                    JObjectList = JsonConvert.DeserializeObject<List<JObject>>(handler.Get("http://localhost/TManagerAPI/ticket/test").Result);
                    Debug.WriteLine(JObjectList[0]);
                    proceed1 = true;
                }
                if (proceed1) // Web
                {
                    foreach (var obj in JObjectList)
                    {
                        char type = JObjectList[counter].First.ToString()[9];
                        if (type == 'A')
                        {
                            string strAtt = "";
                            List<String> attendees = new List<string>();
                            foreach (var attendee in JObjectList[counter]["Attendees"])
                            {   //might be able to be replaced by LINQ
                                string temp = attendee.ToString();
                                strAtt += temp + "\n";
                                attendees.Add(temp);
                            }
                            var appt1 = new Appointment((string)JObjectList[counter]["Name"],
                                (string)JObjectList[counter]["Description"],
                                (string)JObjectList[counter]["Deadline"],
                                (TimeSpan)JObjectList[counter]["Start"],
                                (TimeSpan)JObjectList[counter]["Stop"],
                                strAtt, attendees, (int)JObjectList[counter]["Priority"]);
                            App.list.Add(appt1);
                        }
                        else if (type == 'T')
                        {
                            var t = new Task(() => Console.WriteLine("Task {0} completed!", (string)JObjectList[counter]["Name"]));
                            if ((bool)JObjectList[counter]["isCompleted"])
                            {
                                t.Start();
                            }
                            var task1 = new TaskObj((string)JObjectList[counter]["Name"],
                                (string)JObjectList[counter]["Description"],
                                (string)JObjectList[counter]["Deadline"], t,
                                Convert.ToInt32(JObjectList[counter]["Priority"]));
                            App.list.Add(task1);
                        }
                        counter++;
                    }
                    await Navigation.PushAsync(new MainPage(), true);
                }
                if (proceed) // Local
                {
                    if (filename.Substring(Math.Max(0, filename.Length - 4)) != ".txt")
                    {
                        filename += ".txt";
                    }
                    string check = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), filename);
                    string read = File.ReadAllText(check);
                    List<Item> readList = readFromFile(read);
                    App.list = readList;
                    await Navigation.PushAsync(new MainPage(), true);
                }

            }
        }

        List<Item> readFromFile(string readFromFile)
        {
            List<Item> itemList = new List<Item>();

            string[] lines = readFromFile.Split('\n');

            foreach (string line in lines)
            {
                Debug.Write(line);
                string[] words = line.Split('\t');
                if (words.Length > 6)
                {   // Appointment

                    string tAtt = "";
                    string[] attende = new string[words.Length - 8];
                    Array.Copy(words, 8, attende, 0, words.Length - 8); //if there's an error it is here, words.length - 9
                    List<String> attendees = new List<String>(attende);
                    for (int i = 0; i < attendees.Count; i++)
                    {
                        tAtt += attende[i] + "\n";
                    }
                    var task1 = new Appointment(words[1], words[2], words[4], TimeSpan.Parse(words[5]), TimeSpan.Parse(words[6]),
                            tAtt, attendees, Convert.ToInt32(words[3]));
                    itemList.Add(task1);
                }
                else if (words.Length == 6)
                {   // Task
                    var t = new Task(() => Console.WriteLine("Task {0} completed!", words[1]));
                    if (words[5] == "True")
                    {
                        t.Start();
                    }
                    var task1 = new TaskObj(words[1], words[2], words[4], t, Convert.ToInt32(words[3]));
                    itemList.Add(task1);
                }
            }
            return itemList;
        }
    }
}
