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
    public partial class EditPage : ContentPage
    {
        public EditPage()
        {
            InitializeComponent();
        }
        async void OnPushedEditTask(object sender, EventArgs args)
        {
            
            if (String.IsNullOrWhiteSpace(EName.Text))
            {
                await DisplayAlert("Error!", "Please enter a name.", "OK");
            }
            else
            {
                bool found = false;
                string search = EName.Text.ToUpper();
                for (int i = 0; i < App.list.Count; i++)
                {
                    if (App.list[i].Name.ToUpper() == search)
                    {
                        if (App.list[i] is TaskObj)
                        {
                            await Navigation.PushAsync(new EditTPage(App.list[i] as TaskObj, i), true);
                            found = true;
                        }
                        else if (App.list[i] is Appointment)
                        {
                            await Navigation.PushAsync(new EditAPage(App.list[i] as Appointment, i), true);
                            found = true;
                        }
                    }
                }
                if (!found)
                {
                    await DisplayAlert("Error!", "Item " + EName.Text + " was not found.", "OK");
                }
            }
        }  
    }
}