using System;
using System.Threading.Tasks;

namespace TaskManager
{
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

        public Task Tsk
        {
            get { return tsk; }
            set { tsk = value; }
        }

        public string Name
        {
            get { return name; }
            set { name = value; }
        }

        public string Description
        {
            get { return desc; }
            set { desc = value; }
        }

        public string Deadline
        {
            get { return deadl; }
            set { deadl = value; }
        }

        public bool isCompleted
        {
            get { return tsk.IsCompleted; }
        }
    }
}
