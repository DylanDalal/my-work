using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TaskManager2
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class CompletePage : ContentPage
    {
        public CompletePage()
        {
            InitializeComponent();
        }

        async void OnPushedCompleteTask(object sender, EventArgs args)
        {
            bool found = false;
            for (int i = 0; i < App.list.Count; i++)
            {
                if (App.list[i] is TaskObj)
                {
                    if (App.list[i].Name == CName.Text)
                    {
                        if ((App.list[i] as TaskObj).isCompleted == false)
                        {
                            (App.list[i] as TaskObj).Tsk.Start();
                            await DisplayAlert("Success!", "Task " + CName.Text + " completed.", "OK");
                            found = true;
                        }
                        else
                        {
                            await DisplayAlert("Error", "Task " + CName.Text + " already completed.", "OK");
                        }
                    }
                }
            }
            if (found)
            {
                await Navigation.PushAsync(new MainPage(), true);
            }
            else
            {
                await DisplayAlert("Error", "Task " + CName.Text + " not found. Only Tasks can be completed.", "OK");
            }
        }

        async void Proceed()
        {
            await Navigation.PushAsync(new MainPage(), true);
        }
    }
}