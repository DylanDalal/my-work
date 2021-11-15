#include "hashtable.h"
#include "passserver.h"
#include <iostream>
#include <string>
#include <stdio.h>  // "goodbye"
#include <stdlib.h> //
#include <time.h>   // function

using std::cout;
using std::endl;
using namespace cop4530;

void goodbye() {
  srand (time(NULL));
  int random = rand() % 10;
  switch (random) {
    case 0:
      cout << "\tGoodbye!" << endl << endl;
      break;
    case 1:
      cout << "\tLater~~" << endl << endl;
      break;
    case 2:
      cout << "\t Hasta!" << endl << endl;
      break;
    case 3:
      cout << "\t Deuces." << endl << endl;
      break;
    case 4:
      cout << "\t Bye-bye!" << endl << endl;
      break;
    case 5:
      cout << "\t Leaving so soon?" << endl << endl;
      break;
    case 6:
      cout << "\t Take care!" << endl << endl;
      break;
    case 7:
      cout << "\t Thanks for your time!" << endl << endl;
      break;
    case 8:
      cout << "\t Take it easy." << endl << endl;
      break;
    case 9:
      cout << "\t Happy trails!" << endl << endl;
      break;
  }
}

void Menu()
{
  cout << "\n\n";
  cout << "l - Load From File" << endl;
  cout << "a - Add User" << endl;
  cout << "r - Remove User" << endl;
  cout << "c - Change User Password" << endl;
  cout << "f - Find User" << endl;
  cout << "d - Dump HashTable" << endl;
  cout << "s - HashTable Size" << endl;
  cout << "w - Write to Password File" << endl;
  cout << "x - Exit program" << endl;
  cout << "\nEnter choice : ";
}

int main()  {
  bool running = true;
  std::string input, username, password;
  int cap;
  cout << "Enter preferred hash table capacity: ";
    cin >> cap;
  PassServer table(cap);

  while (running) {
    Menu();
      std::cin >> input;
    if (!(input.compare("x"))) {
      goodbye();
      running = false;
      break;
    }

    else if (!(input.compare("w"))) { //Write to password
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {
        cout << "Enter filename to write to: ";
          cin >> username;
        if (table.write_to_file(username.c_str()))
          cout << "Hash written to file " << username << "." << endl;
    }}

    else if (!(input.compare("s"))) { //size
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {
        cout << table.size() << endl;
    }}

    else if (!(input.compare("d"))) { //Dump
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {
        table.dump();
    }}

    else if (!(input.compare("f"))) { //Find user
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {

    }}

    else if (!(input.compare("c"))) { //change pw
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {
    }}

    else if (!(input.compare("r"))) { //rm user
      if (table.size() == 0) { cout << "Hash is empty." << endl; }
      else {
        cout << "Enter username to remmove: ";
          std::cin >> username;
        if (table.removeUser(username))
          cout << "User " << username << " removed." << endl;
        else
          cout << "Failed to remove user " << username << "." << endl;
    }}

    else if (!(input.compare("a"))) { //add user
      cout << "Enter username: ";
        std::cin >> username;
      cout << "Enter password: ";
        std::cin >> password;
      std::pair<std::string,std::string> add(username,password);
      if (table.addUser(add))
        cout << "User " << username << " added." << endl;
    }

    else if (!(input.compare("l"))) { //load from file
      cout << "Enter filename: ";
        std::cin >> username;
      if (table.load(username.c_str()))
        cout << "Successfully loaded " << username << " into hashmap." << endl;
      else
        cout << "Unable to load " << username << "." << endl;
    }

    else
      cout << "Invalid input." << endl;
  }
}
