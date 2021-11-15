using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TaskManager
{
    class Program
    {
        static void Main(string[] args)
        {
            int input = 0;
            var list = new List<TaskObj>();
            while (input != 7)
            {
                Menu();
                input = Convert.ToInt32(Console.ReadLine());
                switch (input)
                {
                    case 1: // Create ----------------------------------------------------------------------------------------------------
                        Console.WriteLine("Please provide a name for the task: ");
                        string name = Console.ReadLine();
                        Console.WriteLine("Please provide a description for the task: ");
                        string desc = Console.ReadLine();
                        Console.WriteLine("Please provide a deadline for the task: ");
                        string deadline = Console.ReadLine();
                        var t = new Task(() => Console.WriteLine("Task {0} completed!", name));
                        var task1 = new TaskObj(name, desc, deadline, t);
                        list.Add(task1);
                        Console.WriteLine("Added");
                        break;
                        
                    case 2: // Delete ----------------------------------------------------------------------------------------------------
                        Console.WriteLine("Please give the name of the task you would like to complete: ");
                        name = Console.ReadLine();
                        for (int i = 0; i < list.Count; i++)
                        {
                            if (list[i].Name == name)
                            {
                                list.RemoveAt(i);
                                break;
                            }
                        }
                        break;

                    case 3: // Edit ------------------------------------------------------------------------------------------------------
                        Console.WriteLine("Please give the name of the task you would like to edit: ");
                        name = Console.ReadLine();
                        int counter = 0;
                        bool found = false;
                        for (int i = 0; i < list.Count; i++)
                        {
                            if (list[i].Name == name)
                            {
                                found = true;
                                counter = i;
                                bool loop = true;
                                bool loop2 = true;
                                while (loop)
                                {
                                    Console.WriteLine("Would you like to edit all aspects of the task? [Enter T/F]");
                                    string edit = Console.ReadLine();
                                    if (edit == "T")
                                    {
                                        Console.WriteLine("Give the task a new name:");
                                        list[counter].Name = Console.ReadLine();
                                        Console.WriteLine("Give the task a new description:");
                                        list[counter].Description = Console.ReadLine();
                                        Console.WriteLine("Give the task a deadline:");
                                        list[counter].Deadline = Console.ReadLine();
                                        list[counter].Tsk = new Task(() => Console.WriteLine("Task {0} completed!", list[counter].Name));
                                        loop = false;
                                    }
                                    else if (edit == "F")
                                    {
                                        while (loop2)
                                        {
                                            Console.WriteLine("Would you like to edit the task name? [Enter T/F]");
                                            string inp = Console.ReadLine();
                                            if (inp == "T")
                                            {
                                                Console.WriteLine("Give the task a new name:");
                                                list[counter].Name = Console.ReadLine();
                                                loop2 = false;
                                            }
                                            else if (inp == "F")
                                                loop2 = false;
                                            else
                                                Console.WriteLine("Invalid input.");
                                        }
                                        loop2 = true;
                                        while (loop2)
                                        {
                                            Console.WriteLine("Would you like to edit the task description? [Enter T/F]");
                                            string inp = Console.ReadLine();
                                            if (inp == "T")
                                            {
                                                Console.WriteLine("Give the task a new description:");
                                                list[counter].Description = Console.ReadLine();
                                                loop2 = false;
                                            }
                                            else if (inp == "F")
                                                loop2 = false;
                                            else
                                                Console.WriteLine("Invalid input.");
                                        }
                                        loop2 = true;
                                        while (loop2)
                                        {
                                            Console.WriteLine("Would you like to edit the task deadline? [Enter T/F]");
                                            string inp = Console.ReadLine();
                                            if (inp == "T")
                                            {
                                                Console.WriteLine("Give the task a new deadline:");
                                                list[counter].Deadline = Console.ReadLine();
                                                loop2 = false;
                                            }
                                            else if (inp == "F")
                                                loop2 = false;
                                            else
                                                Console.WriteLine("Invalid input.");
                                        }
                                        list[counter].Tsk = new Task(() => Console.WriteLine("Task {0} completed!", list[counter].Name));
                                        loop = false;
                                    }
                                    else
                                        Console.WriteLine("Invalid input.");
                                }
                                break;
                            }
                        }
                        if (found == false)
                            Console.WriteLine("Task {0} not found.", name);
                        break;

                    case 4: // Complete --------------------------------------------------------------------------------------------------
                        Console.WriteLine("Enter the name of the task you would like to complete.");
                        name = Console.ReadLine();
                        for (int i = 0; i < list.Count; i++)
                        {
                            if (list[i].Name == name)
                            {
                                list[i].Tsk.Start();
                                break;
                            }
                        }
                        System.Threading.Thread.Sleep(700);
                        break;

                    case 5: // List ------------------------------------------------------------------------------------------------------
                        if (list.Count == 0)
                            Console.WriteLine("This list is empty!");
                        for (int i = 0; i < list.Count; i++)
                        {
                            if (list[i].isCompleted == false)
                            {
                                Console.WriteLine("Task #{0}:", i + 1);
                                Console.WriteLine("Name:\t\t{0}", list[i].Name);
                                Console.WriteLine("Description:\t{0}", list[i].Description);
                                Console.WriteLine("Deadline:\t{0}", list[i].Deadline);
                                Console.WriteLine("Status:\t\tIncomplete");
                            }
                        }
                        break;

                    case 6: // List ------------------------------------------------------------------------------------------------------
                        if (list.Count == 0)
                            Console.WriteLine("This list is empty!");
                        for (int i = 0; i < list.Count; i++)
                        {
                            Console.WriteLine("Task #{0}:", i + 1);
                            Console.WriteLine("Name:\t\t{0}", list[i].Name);
                            Console.WriteLine("Description:\t{0}", list[i].Description);
                            Console.WriteLine("Deadline:\t{0}", list[i].Deadline);
                            if (list[i].isCompleted)
                                Console.WriteLine("Status:\t\tCompleted");
                            else
                                Console.WriteLine("Status:\t\tIncomplete");
                        }
                        break;

                    case 7: // End -------------------------------------------------------------------------------------------------------
                        Goodbye();
                        break;

                }

            }
        }

        public static void Menu()
        {
            Console.WriteLine("\nType the number to perform an action: ");
            Console.WriteLine("1. Create a new task");
            Console.WriteLine("2. Delete an existing task");
            Console.WriteLine("3. Edit an existing task");
            Console.WriteLine("4. Complete a task");
            Console.WriteLine("5. List all outstanding (incomplete) tasks");
            Console.WriteLine("6. List all tasks");
            Console.WriteLine("7. Quit");
        }
        public static void Goodbye()
        {
            Random rnd = new Random();
            string[] goodbyes = { "Goodbye!", "Thank you for your time!", "Farewell!",
                                  "Godspeed.", "Toodles~", "Hasta", "See ya!", "~Later",
                                  "Leaving so soon?", "What, are you bored?", "Don't go!!"};
            int mIndex = rnd.Next(goodbyes.Length);
            Console.WriteLine("{0}", goodbyes[mIndex]);
            System.Threading.Thread.Sleep(700);
        }
    }

    public class TaskObj 
    {
        private Task tsk;
        private string name;
        private string desc;
        private string deadl;
       
        public TaskObj(string na, string des, string dea, Task t)
        {
            name = na;
            desc = des;
            deadl = dea;
            tsk = t;
        }
        public Task Tsk   // property
        {
            get { return tsk; }   // get method
            set { tsk = value; }  // set method
        }

        public string Name   // property
        {
            get { return name; }   // get method
            set { name = value; }  // set method
        }

        public string Description   // property
        {
            get { return desc; }   // get method
            set { desc = value; }  // set method
        }

        public string Deadline   // property
        {
            get { return deadl; }   // get method
            set { deadl = value; }  // set method
        }

        public bool isCompleted   // property
        {
            get { return tsk.IsCompleted; }   // get method
        }
    }
}
