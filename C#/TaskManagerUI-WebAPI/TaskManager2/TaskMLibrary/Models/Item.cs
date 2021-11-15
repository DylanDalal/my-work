using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TaskLibrary.Models
{
    public partial  class Item
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
                if (Convert.ToString(this.GetType()) == "TaskManagerLibrary.TaskObj")
                {
                    type = "Task";
                }
                else if (Convert.ToString(this.GetType()) == "TaskManagerLibrary.Appointment")
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
}
