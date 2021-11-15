using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TaskManager2
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class CreateTPage : ContentPage
    {
        public CreateTPage()
        {
            InitializeComponent();
            SliderVal.Text = "0";
        }
        void OnCompletedName(object sender, TextChangedEventArgs e)
        {
            string newText = e.NewTextValue;
        }
        void OnCompletedDesc(object sender, TextChangedEventArgs e)
        {
            string newText = e.NewTextValue;
        }
        void OnCompletedDeadl(object sender, TextChangedEventArgs e)
        {
            string newText = e.NewTextValue;
        }
        async void OnPushedCreateTask(object sender, EventArgs args)
        {
            await DisplayAlert("Success!", "Task " + TName.Text + " added to the list.", "OK");
            var t = new Task(() => Console.WriteLine("Task {0} completed!", TName.Text));
            var task1 = new TaskObj(TName.Text, TDesc.Text, TDeadl.Date.Date.ToShortDateString(), t, Convert.ToInt32(TPriority.Value));
            App.list.Add(task1);
            await Navigation.PushAsync(new MainPage(), true);
        }
        void OnSliderValueChanged(object sender, ValueChangedEventArgs e)
        {
            var newStep = Math.Round(e.NewValue);
            SliderVal.Text = newStep.ToString();
            TPriority.Value = newStep;
        }
    }
}