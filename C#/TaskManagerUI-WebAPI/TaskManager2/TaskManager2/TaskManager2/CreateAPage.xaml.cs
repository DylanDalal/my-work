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
    public partial class CreateAPage : ContentPage
    {
        public CreateAPage()
        {
            InitializeComponent();
            SliderVal.Text = "0";
        }
        async void OnPushedCreateAppointment(object sender, EventArgs args)
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
        void OnSliderValueChanged(object sender, ValueChangedEventArgs e)
        {
            var newStep = Math.Round(e.NewValue);
            SliderVal.Text = newStep.ToString();
            APriority.Value = newStep;
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