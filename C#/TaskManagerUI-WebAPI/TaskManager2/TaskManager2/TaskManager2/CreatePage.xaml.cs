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
    public partial class CreatePage : ContentPage
    {
        public CreatePage()
        {
            InitializeComponent();
        }

        void GoToTPage(object sender, EventArgs args)
        {
            TBox.IsChecked = false;
            Navigation.PushAsync(new CreateTPage(), true);
        }

         void GoToAPage(object sender, EventArgs args)
        {
            ABox.IsChecked = false;
            Navigation.PushAsync(new CreateAPage(), true);
        }

      private void CheckBox_CheckedChanged(object sender, CheckedChangedEventArgs e)
        {

        }
    }
}