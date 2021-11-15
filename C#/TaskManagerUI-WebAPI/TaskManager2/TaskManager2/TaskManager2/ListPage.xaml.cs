using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Collections.ObjectModel;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace TaskManager2
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class ListPage : ContentPage
    {


        public ListPage()
        {
            InitializeComponent();
            MainListView.ItemsSource = App.list;
        }

        void SearchTextChanged(object sender, EventArgs args)
        {
            string search = SB.Text;
            search = search.ToUpper();
            var results = from entry2 in App.list
                          where entry2.Name.ToUpper().Contains(search) || entry2.Description.ToUpper().Contains(search)
                          || ((entry2 as Appointment)?.StrAtt?.ToUpper().Contains(search) ?? false)
                          select entry2;
            List<Item> res = new List<Item>(results);
            if (res.Any())
            {
                MainListView.ItemsSource = res;
            }
            else
            {
                DisplayAlert("Error!", "No items found.", "OK");
                MainListView.ItemsSource = App.list;
                SB.Text = "";
            }
        }

        void OnClearButtonClicked(object sender, EventArgs args)
        {
            SB.Text = "";
        }

        void OnClickedSortDefault(object send, EventArgs args)
        {
            MainListView.ItemsSource = App.list;
        }

        void OnClickedSortPriority(object send, EventArgs args)
        {
            List<Item> SortedList = App.list.OrderByDescending(x => x.Priority).ToList();
            MainListView.ItemsSource = SortedList;
        }
        void OnClickedSortComplete(object send, EventArgs args)
        {   // sloppy, redo with LINQ
            List<Item> SortedList = new List<Item>();
            for (int i = 0; i < App.list.Count; i++)
            {
                if (App.list[i].Type == "Task")
                {
                    if ((App.list[i] as TaskObj).isCompleted)
                    {
                        SortedList.Add(App.list[i]);
                    }
                }
            }
            MainListView.ItemsSource = SortedList;
        }
    }
}