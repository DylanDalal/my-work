using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TaskManager2
{
    public partial class Item
    {
        protected string name;
        protected string desc;
        protected string type;
        protected int priority;

        public string Description   // property
        {
            get { return desc; }   // get method
            set { desc = value; }  // set method
        }
        public string Name   // property
        {
            get { return name; }   // get method
            set { name = value; }  // set method
        }

        public string Type   // property
        {
            get
            {
                type = "Unknown";
                if (Convert.ToString(this.GetType()) == "TaskManager2.TaskObj")
                {
                    type = "Task";
                }
                else if (Convert.ToString(this.GetType()) == "TaskManager2.Appointment")
                {
                    type = "Appointment";
                }
                return type;
            }   // get method
            set { type = value; }  // set method
        }

        public int Priority
        {
            get { return priority; }
            set { priority = value; }
        }
    }
    public partial class Appointment : Item
    {
        protected TimeSpan start;
        protected TimeSpan stop;
        protected string deadl;
        protected string strAtt;
        protected List<String> attendees;

        public Appointment(string na, string dsc, string dat, TimeSpan sta, TimeSpan sto, string att, List<String> atte, int pr)
        {
            name = na;
            desc = dsc;
            start = sta;
            deadl = dat;
            stop = sto;
            strAtt = att;
            attendees = atte;
            priority = pr;
        }
        public TimeSpan Start   // property
        {
            get { return start; }   // get method
            set { start = value; }  // set method
        }

        public TimeSpan Stop // property
        {
            get { return stop; }   // get method
            set { stop = value; }  // set method
        }

        public string Deadline   // property
        {
            get { return deadl; }   // get method
            set { deadl = value; }  // set method
        }

        public string StrAtt
        {
            get { return strAtt; }
            set { strAtt = value; }
        }

        public List<String> Attendees
        {
            get { return attendees; }
            set { attendees = value; }
        }
    }
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
