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
    public partial class EditTPage : ContentPage
    {
        protected string oName;
        protected string oDesc;
        protected string oDead;
        protected int oPrior;

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
        public int OPrior
        {
            get { return oPrior; }
            set { oPrior = value; }
        }

        public int itr;
        public EditTPage(TaskObj task, int i)
        {
            InitializeComponent();
            oName = task.Name;
            oDesc = task.Description;
            oDead = task.Deadline;
            oPrior = task.Priority;
            itr = i;
            TName.Text = task.Name;
            TDesc.Text = task.Description;
            TDeadl.Date = Convert.ToDateTime(task.Deadline);
            TPriority.Value = task.Priority;
            SliderVal.Text = task.Priority.ToString();
        }

        public void OnClickedRestoreName(object sender, EventArgs args)
        {
            TName.Text = oName;
        }
        public void OnClickedRestoreDesc(object sender, EventArgs args)
        {
            TDesc.Text = oDesc;
        }
        public void OnClickedRestoreDeadl(object sender, EventArgs args)
        {
            TDeadl.Date = Convert.ToDateTime(oDead);
        }

        public void OnClickedRestorePriority(object sender, EventArgs args)
        {
            TPriority.Value = oPrior;
        }

        async void OnClickedEditTask(object sender, EventArgs args)
        {
            var t = new Task(() => Console.WriteLine("Task {0} completed!", TName.Text));
            var task1 = new TaskObj(TName.Text, TDesc.Text, TDeadl.Date.Date.ToShortDateString(), t, Convert.ToInt32(TPriority.Value));
            App.list[itr] = task1;
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