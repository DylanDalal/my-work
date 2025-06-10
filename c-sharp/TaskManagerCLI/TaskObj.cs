using System;
using System.Threading.Tasks;

namespace TaskManager
{
    public class TaskObj
    {
        public TaskObj(string name, string description, DateTime deadline, Task task)
        {
            Name = name;
            Description = description;
            Deadline = deadline;
            Tsk = task;
        }

        public Task Tsk { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }

        public DateTime Deadline { get; set; }

        public bool isCompleted => Tsk.IsCompleted;
    }
}
