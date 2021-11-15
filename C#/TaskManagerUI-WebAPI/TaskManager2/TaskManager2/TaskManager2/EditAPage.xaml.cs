using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TaskManager2
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class EditAPage : ContentPage
    {
        protected string oName;
        protected string oDesc;
        protected string oDead;
        protected TimeSpan oStart;
        protected TimeSpan oEnd;
        protected int oNum;
        protected int oPrior;
        protected List<String> oAttendees;

        public string OName
        {
            get { return oName; }
            set { oName = value; }
        }

        public string ODesc
        {
            get { return oDesc; }
            set { oDesc = value; }
        }

        public string ODead
        {
            get { return oDead; }
            set { oDead = value; }
        }
        public TimeSpan OStart
        {
            get { return oStart; }
            set { oStart = value; }
        }
        public TimeSpan OEnd
        {
            get { return oEnd; }
            set { oEnd = value; }
        }
        public int ONum
        {
            get { return oNum; }
            set { oNum = value; }
        }
        public int OPrior
        {
            get { return oPrior; }
            set { oPrior = value; }
        }

        public List<String> OAttendees
        {
            get { return oAttendees; }
            set { oAttendees = value; }
        }

        public int itr;
        public EditAPage(Appointment appt, int i)
        {
            InitializeComponent();
            oName = appt.Name;
            oDesc = appt.Description;
            oDead = appt.Deadline;
            oStart = appt.Start;
            oEnd = appt.Stop;
            oNum = appt.Attendees.Count;
            oPrior = appt.Priority;
            oAttendees = new List<String>(appt.Attendees);

            AName.Text = oName;
            ADesc.Text = oDesc;
            ADeadl.Date = Convert.ToDateTime(oDead);
            AStart.Time = oStart;
            AEnd.Time = oEnd;
            numAtt.Text = Convert.ToString(oNum);
            parent.Children.Clear();
            for (int o = 0; o < oNum; o++)
            {
                Entry nameEntry = new Entry { Text=appt.Attendees[o], 
                    Placeholder="Attendee name...", PlaceholderColor = Color.LightGray };
                parent.Children.Add(nameEntry);
            }
            APriority.Value = appt.Priority;
            SliderVal.Text = appt.Priority.ToString();
            itr = i;
        }

        public void OnClickedRestoreName(object sender, EventArgs args)
        {
            AName.Text = oName;
        }
        public void OnClickedRestoreDesc(object sender, EventArgs args)
        {
            ADesc.Text = oDesc;
        }
        public void OnClickedRestoreDeadl(object sender, EventArgs args)
        {
            ADeadl.Date = Convert.ToDateTime(oDead);
        }

        public void OnClickedRestoreStart(object sender, EventArgs args)
        {
            AStart.Time = oStart;
        }

        public void OnClickedRestoreEnd(object sender, EventArgs args)
        {
            AEnd.Time = oEnd;
        }

        public void OnClickedRestoreNum(object sender, EventArgs args)
        {
            numAtt.Text = oNum.ToString();
            parent.Children.Clear();
            for (int o = 0; o < oNum; o++)
            {
                Entry nameEntry = new Entry
                {
                    Text = oAttendees[o],
                    Placeholder = "Attendee name...",
                    PlaceholderColor = Color.LightGray
                };
                parent.Children.Add(nameEntry);
            }
        }
        public void OnClickedRestorePriority(object sender, EventArgs args)
        {
            APriority.Value = oPrior;
        }
        void OnSliderValueChanged(object sender, ValueChangedEventArgs e)
        {
            var newStep = Math.Round(e.NewValue);
            SliderVal.Text = newStep.ToString();
            APriority.Value = newStep;
        }
        async void OnClickedEditAppt(object sender, EventArgs args)
        {
            if (String.IsNullOrWhiteSpace(AName.Text))
            {
                await DisplayAlert("Error!", "Appointment must have a name.", "OK");
            }
            else if (String.IsNullOrWhiteSpace(ADesc.Text))
            {
                await DisplayAlert("Error!", "Appointment must have a description.", "OK");
            }
            else if (AStart.Time == AEnd.Time)
            {
                await DisplayAlert("Error!", "Appointment start and stop times must be different.", "OK");
            }
            else
            {
                List<string> attendees = new List<string>();
                string tAtt = "";
                for (int i = 0; i < parent.Children.Count; i++)
                {
                    string temp = ((Entry)parent.Children[i]).Text.ToString();
                    tAtt = tAtt + temp + "\n";
                    attendees.Add(temp);
                }
                tAtt = tAtt.Substring(0, tAtt.Length - 1);
                await DisplayAlert("Success!", "Appointment " + AName.Text + " added to the list.", "OK");
                var task1 = new Appointment(AName.Text, ADesc.Text, ADeadl.Date.Date.ToShortDateString(), AStart.Time, AEnd.Time, tAtt, attendees, Convert.ToInt32(APriority.Value));
                App.list.Add(task1);
                await Navigation.PushAsync(new MainPage(), true);
            }
        }
        void Attendees_Entered(object sender, EventArgs args)
        {
            parent.Children.Clear();
            int length = 0;
            int errorCounter = Regex.Matches(numAtt.Text, @"[a-zA-Z]").Count;
            try
            {
                if (String.IsNullOrWhiteSpace(numAtt.Text) || errorCounter > 0)
                {
                    length = 0;
                }
                else
                {
                    length = Int32.Parse(numAtt.Text);
                }
            }
            catch (FormatException)
            {
                DisplayAlert("Error!", "The number of attendees cannot be empty or a character.", "OK");
            }
            for (int i = 0; i < length; i++)
            {
                Entry nameEntry = new Entry { Placeholder = "Attendee name...", PlaceholderColor = Color.LightGray };
                parent.Children.Add(nameEntry);
            }
        }
    }
}