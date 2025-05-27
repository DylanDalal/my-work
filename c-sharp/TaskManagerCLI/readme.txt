### DESCRIPTION

"C#"
CIS4930
Jun 1, 2021

Introductory assignment for C# class. TaskManager command-line interface menu 
program allows user to create objects of custom TaskObj class, each instance of
which stores the task name, description, deadline, and an asynchronous Task.
There are also menu items to list all TaskObjs, list all incomplete tasks, to 
edit or delete an existing TaskObj, and to complete a TaskObj's Task.

### INSTALLATION

I am running on a Mac, you might not have to install these dependencies on Windows.

Run by installing .NET SDK:
https://dotnet.microsoft.com/en-us/download
and .NET 8.0 Runtime:
https://dotnet.microsoft.com/en-us/download/dotnet/8.0/runtime?cid=getdotnetcore&os=macos&arch=arm64

verify installation:
dotnet --version

navigate to root folder TaskManagerCLI/ and run these commands:

dotnet clean
dotnet restore
dotnet build
dotnet run
