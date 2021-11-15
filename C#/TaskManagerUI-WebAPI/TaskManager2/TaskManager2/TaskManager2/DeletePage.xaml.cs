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
    public partial class DeletePage : ContentPage
    {
        public DeletePage()
        {
            InitializeComponent();
        }

        async void OnPushedDeleteTask(object sender, EventArgs args)
        {
            bool proceed = false;
            for (int i = 0; i < App.list.Count; i++)
            {
                if (App.list[i].Name == IName.Text)
                {
                    App.list.RemoveAt(i);
                    await DisplayAlert("Success!", "Task " + IName.Text + " removed from the list.", "OK");
                    await Navigation.PopToRootAsync();
                    proceed = true;
                }
            }
            if (!proceed)
            {
                await DisplayAlert("Error", "Task " + IName.Text + " not found.", "OK");
            }
        }

        async void Proceed()
        {
            await Navigation.PopToRootAsync();
        }
    }
}