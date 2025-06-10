using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace TaskManager
{
    class Program
    {
        static List<TaskObj> list = new List<TaskObj>();

        static void Main(string[] args)
        {
            int input = 0;
            while (input != 7)
            {
                Console.Clear();
                Menu();
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.Write("Select an option: ");
                Console.ResetColor();

                if (!int.TryParse(Console.ReadLine(), out input))
                {
                    ShowError("Invalid input.");
                    continue;
                }

                switch (input)
                {
                    case 1: CreateTask(); break;
                    case 2: DeleteTask(); break;
                    case 3: EditTask(); break;
                    case 4: CompleteTask(); break;
                    case 5: ListTasks(false); break;
                    case 6: ListTasks(true); break;
                    case 7: Goodbye(); break;
                    default: ShowError("Invalid option."); break;
                }

                if (input != 7)
                {
                    Pause();
                }
            }
        }

        static void Menu()
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("========== Task Manager ==========");
            Console.ResetColor();
            Console.WriteLine("1. Create a new task");
            Console.WriteLine("2. Delete a task");
            Console.WriteLine("3. Edit a task");
            Console.WriteLine("4. Complete a task");
            Console.WriteLine("5. List incomplete tasks");
            Console.WriteLine("6. List all tasks");
            Console.WriteLine("7. Quit");
            Console.WriteLine("==================================");
        }

        static void CreateTask()
        {
            Console.Write("Task name: ");
            string name = Console.ReadLine();
            Console.Write("Description: ");
            string desc = Console.ReadLine();

            DateTime deadline;
            while (true)
            {
                Console.Write("Deadline (MM/dd/yyyy): ");
                string input = Console.ReadLine();
                if (DateTime.TryParseExact(input, "MM/dd/yyyy", null, System.Globalization.DateTimeStyles.None, out deadline))
                    break;

                ShowError("Invalid date format. Please use MM/dd/yyyy.");
            }

            var t = new Task(() => {});
            list.Add(new TaskObj(name, desc, deadline, t));
            ShowSuccess("Task added.");
        }

        static void DeleteTask()
        {
            int index = GetTaskIndex("Enter the task number to delete:");
            if (index == -1) return;

            Console.Write($"Are you sure you want to delete '{list[index].Name}'? (Y/N): ");
            if (Console.ReadLine().Trim().ToUpper() == "Y")
            {
                list.RemoveAt(index);
                ShowSuccess("Task deleted.");
            }
        }

        static void EditTask()
        {
            int index = GetTaskIndex("Enter the task number to edit:");
            if (index == -1) return;

            var task = list[index];

            Console.WriteLine($"\nCurrent Task:");
            PrintTruncatedTask(task, index + 1);

            Console.WriteLine("\nWhat would you like to edit?");
            Console.WriteLine("1. Name\n2. Description\n3. Deadline\n4. All");

            if (!int.TryParse(Console.ReadLine(), out int choice))
            {
                ShowError("Invalid selection.");
                return;
            }

            switch (choice)
            {
                case 1: EditTaskName(task); break;
                case 2: EditTaskDescription(task); break;
                case 3: EditTaskDeadline(task); break;
                case 4: EditTaskName(task); EditTaskDescription(task); EditTaskDeadline(task); break;
                default: ShowError("Invalid option."); return;
            }

            task.Tsk = new Task(() => {});
            ShowSuccess("Task updated.");
        }

        static void EditTaskName(TaskObj task)
        {
            Console.Write("New name: ");
            task.Name = Console.ReadLine();
        }

        static void EditTaskDescription(TaskObj task)
        {
            Console.Write("New description: ");
            task.Description = Console.ReadLine();
        }

        static void EditTaskDeadline(TaskObj task)
        {
            task.Deadline = PromptForDate("New deadline (MM/dd/yyyy): ");
        }

        static void PrintTruncatedTask(TaskObj task, int number)
        {
            string name = Truncate(task.Name, 50);
            string desc = Truncate(task.Description, 50);
            string due = task.Deadline.ToString("MM/dd/yyyy");

            Console.Write($"[{number}] ");
            if (task.isCompleted)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write("[✔]");
            }
            else
            {
                Console.Write("[ ]");
            }
            Console.ResetColor();

            Console.WriteLine($" {name} (Due: {due})");
            Console.WriteLine($"    Description: {desc}");
        }

        static string Truncate(string input, int maxLength)
        {
            if (string.IsNullOrEmpty(input)) return input;
            return input.Length <= maxLength ? input : input.Substring(0, maxLength - 3) + "...";
        }

        static void CompleteTask()
        {
            int index = GetTaskIndex("Enter the task number to complete:");
            if (index == -1) return;

            var t = list[index];

            if (t.isCompleted)
            {
                ShowInfo($"Task '{t.Name}' is already completed.");
                return;
            }

            try
            {
                t.Tsk.Start();

                Console.Write("Completing");
                for (int i = 0; i < 3; i++) { Thread.Sleep(300); Console.Write("."); }
                Console.WriteLine();

                Thread.Sleep(100); // short pause before success message
                ShowSuccess($"Task '{t.Name}' marked as completed!");
            }
            catch (InvalidOperationException)
            {
                ShowError("This task has already been completed and cannot be started again.");
            }
        }

        static void ListTasks(bool showAll)
        {
            if (list.Count == 0)
            {
                ShowInfo("No tasks found.");
                return;
            }

            Console.WriteLine();
            for (int i = 0; i < list.Count; i++)
            {
                var task = list[i];
                if (!showAll && task.isCompleted) continue;

                Console.Write($"[{i + 1}] ");
                if (task.isCompleted)
                {
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.Write("[✔]");
                }
                else
                {
                    Console.Write("[ ]");
                }
                Console.ResetColor();
                Console.WriteLine($" {task.Name} (Due: {task.Deadline:MM/dd/yyyy})");

                Console.WriteLine($"    Description: {task.Description}");
            }
        }

        static DateTime PromptForDate(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                string input = Console.ReadLine();
                if (DateTime.TryParseExact(input, "MM/dd/yyyy", null, System.Globalization.DateTimeStyles.None, out DateTime date))
                    return date;

                ShowError("Invalid date format. Please use MM/dd/yyyy.");
            }
        }

        static int GetTaskIndex(string prompt)
        {
            if (list.Count == 0)
            {
                ShowInfo("No tasks available.");
                return -1;
            }

            ListTasks(true);
            Console.Write(prompt + " ");
            if (!int.TryParse(Console.ReadLine(), out int idx) || idx < 1 || idx > list.Count)
            {
                ShowError("Invalid task number.");
                return -1;
            }

            return idx - 1;
        }

        static void Pause()
        {
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write("Press Enter to continue...");
            Console.ResetColor();
            Console.ReadLine();
        }

        static void Goodbye()
        {
            var goodbyes = new[] {
                "Goodbye!", "Thank you for your time!", "Farewell!", "Godspeed.", 
                "Toodles!", "Hasta", "See ya!", "Later", "Leaving so soon?", 
                "What, are you bored?", "Don't go!!"
            };
            Console.WriteLine("\n" + goodbyes[new Random().Next(goodbyes.Length)]);
        }

        static void ShowError(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Error: " + msg);
            Console.ResetColor();
        }

        static void ShowSuccess(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine(msg);
            Console.ResetColor();
        }

        static void ShowInfo(string msg)
        {
            Console.ForegroundColor = ConsoleColor.DarkCyan;
            Console.WriteLine(msg);
            Console.ResetColor();
        }
    }
}
