using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TaskLibrary.Models
{
    partial class Appointment : Item
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
}
