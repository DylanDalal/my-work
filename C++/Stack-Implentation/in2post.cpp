#include <iostream>
#include <string>
#include "stack.h"
#include <ctype.h>
#include <stdio.h>  // "goodbye"
#include <stdlib.h> //
#include <time.h>   // function

using namespace std;
using namespace cop4530;

bool isOperator(string str) {
  if (str == "+" || str == "-" || str == "*" || str == "/")
    return true;
  else
    return false;
}

bool isAlpha(string str) {
  if (str.find_first_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        != string::npos)
    return true;
  else
    return false;
}

bool isAlphaNum(string str) {
  if (str.find_first_of("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        != string::npos)
    return true;
  else
    return false;
}

bool legit(Stack<string> given) {     //error testing.
  Stack<string> stack2(given);
  int counter1 = 0, counter2 = 0;
  bool before = false;
  bool beforeVal = false;
  bool beforePar = false;

  for (int i = 0; i < given.size(); i++) {
    //Check for parentheses mismatch
    if (stack2.top() == "(") {
        counter1++;
        beforePar = true;
    } else if (stack2.top() == ")") { //brackets added so its easier to read
        counter2++;
        beforePar = false;
    //operator missing operands
    } else if ((stack2.top() == "+" || stack2.top() == "-" || stack2.top() == "*"
              || stack2.top() == "/") && (before == false && i != 0 && i !=
              given.size()-1)) {
        before = true;
    } else if ((stack2.top() == "+" || stack2.top() == "-" || stack2.top() == "*"
              || stack2.top() == "/") && before == true) {
      return false;
    } else if ((stack2.top() != "+" || stack2.top() != "-" || stack2.top() != "*"
              || stack2.top() != "/") && before == true) {
        before = false;
    } else if ((stack2.top() == "+" || stack2.top() == "-" || stack2.top() == "*"
              || stack2.top() == "/") && i == 0) {
        return false;
    } else if ((stack2.top() == "+" || stack2.top() == "-" || stack2.top() == "*"
              || stack2.top() == "/") && (i == given.size()-1)) {
        return false;
    //operands missing operator
    } else if (stack2.top().find_first_of("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
              != string::npos && beforeVal == false) {  //so since i needed this
        beforeVal = true;                             //later on i made function
    } else if (stack2.top().find_first_of("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
              != string::npos && beforeVal == true) {//isAlphaNum, but now since
        return false;                                   //ik this works here i'm
    } else if (stack2.top().find_first_of("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
              != string::npos && beforeVal == true)    //scared to change it lol
        beforeVal = false;
    else
      return false;
    stack2.pop();
  }
  if (counter1 != counter2)
    return false;
  if (beforePar)
    return false;
  else
    return true;
}

int priority(string str) {
  if (str == "-" || str == "+")
    return 1;
  else if (str == "*" || str == "/")
    return 2;
  return 0;
}

double evaluate(Stack<string> stack1) {
  double a, b, c, output = 0;
  int length = stack1.size();
  Stack<double> eval;
  string input;
  for (int i = 0; i < length; i++) {
    input = stack1.top();
    if ((isOperator(input))) {
      if (stack1.top() == "+") {
        a = eval.top();
        eval.pop();
        b = eval.top();
        eval.pop();
        c = a + b;
        eval.push(c);
      } else if (stack1.top() == "-") {
        a = eval.top();
        eval.pop();
        b = eval.top();
        eval.pop();
        c = b - a;
        eval.push(c);
      } else if (stack1.top() == "*") {
        a = eval.top();
        eval.pop();
        b = eval.top();
        eval.pop();
        c = a * b;
        eval.push(c);
      } else if (stack1.top() == "/") {
        a = eval.top();
        eval.pop();
        b = eval.top();
        eval.pop();
        c = b / a;
        eval.push(c);
      }
      stack1.pop();
    } else {
      eval.push(std::stod(input));
      stack1.pop();
    }
  }
  output = eval.top();
  return output;
}


Stack<string> converter(string given) {
  bool run = true;
  size_t pos = 0;
  Stack<string> stack1, output; // output a stack because i've already
  string delim = " ", piece, topp;    // set up the operator to display
  while ((pos = given.find(delim)) != string::npos) {  // it, so why not
    run = true;
    piece = given.substr(0, pos);
    if (piece.find_first_not_of(' ') != string::npos) {
      if (isOperator(piece)) {
        while (stack1.size() != 0 && run) {
          topp = stack1.top();
          if (priority(topp) >= priority(piece)){
            output.push(stack1.top());
            stack1.pop();
          } else
            run = false;
        } stack1.push(piece);
      } else if (isAlphaNum(piece)) {
          output.push(piece);
      } else if (piece == "(") {
          stack1.push("(");
      } else if (piece == ")") {
          if (stack1.size() != 0) {
            topp = stack1.top();
            while (priority(topp) != 0 && stack1.size() != 0) {
              output.push(stack1.top());
              stack1.pop();
              if (stack1.size() != 0)
                topp = stack1.top();
            }
          }
        stack1.pop();
      }
    }
    given.erase(0, pos + delim.length());
  }
  piece = given.substr(0, pos);
  if (piece.find_first_not_of(' ') != string::npos) {
    if (piece == ")") {
      if (stack1.size() != 0) {
        topp = stack1.top();
        while (priority(topp) != 0 && stack1.size() != 0) {
          output.push(stack1.top());
          stack1.pop();
          if (stack1.size() != 0)
            topp = stack1.top();
        }
      }
      stack1.pop();
    } else if (isAlphaNum(piece))
      output.push(piece);
  }
  int max = stack1.size();
  for (int i = 0; i < max; i++) {
    output.push(stack1.top());
    stack1.pop();
  }
  stack1.clear();
  output.reverse();
  return output;
}

Stack<string> splitter(string input) {
  size_t pos = 0;
  Stack<string> stack1;
  string delim = " ", piece;
  while ((pos = input.find(delim)) != string::npos) {
    piece = input.substr(0, pos);
    if (piece.find_first_not_of(' ') != string::npos)
      stack1.push(piece);
    input.erase(0, pos + delim.length());
  }
  piece = input.substr(0, pos);
  if (piece.find_first_not_of(' ') != string::npos)
    stack1.push(piece);
  return stack1;
}


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


/*----------------------------------------------------------------------------*/
int main () {
  bool running = true;
  string given, newer;
  Stack<string> stack1, stack2;


  while (running) {
    cout << "\nProvide an expression or type 'exit':\nInfix: ";
    getline(cin, given);
    if (given == "exit" || given == "Exit" || given == "EXIT") {
      goodbye();
      break;
    } stack1 = splitter(given);   //allows me to easily check for errors;
    stack1.reverse();             //i now recognize that it was not
    if (!(legit(stack1))) {       //entirely neccessary though lol
      cout << "Error: Invalid input." << endl;
      continue;
    } stack2 = converter(given);
    cout << "Postfix: " << stack2 << endl;
    if (isAlpha(given))
      continue;
    cout << "Total: " << evaluate(stack2) << endl;
  }
}
