using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TaskLibrary.Models
{
    public partial class TaskObj : Item
    {
        protected Task tsk;
        protected string deadl;

        public TaskObj() { }
        public TaskObj(string nam, string de, string dea, Task t, int pr)
        {
            name = nam;
            desc = de;
            deadl = dea;
            tsk = t;
            priority = pr;
        }

        public Task Tsk   // property
        {
            get { return tsk; }   // get method
            set { tsk = value; }  // set method
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
