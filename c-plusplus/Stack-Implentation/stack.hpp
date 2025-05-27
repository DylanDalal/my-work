#include <iostream>
using namespace cop4530;

// Using the <forward_list> container
//  .front() returns reference to first element
//  .begin() returns iterator to first element
//  .assign() can copy elements
//  .empty()
//  .clear()
//  .push_front() & pop_front()
//  erase, erase_after and eraseif


/* Constructors */

template<typename T>
Stack<T>::Stack() {
  length = 0;
}

template<typename T>
Stack<T>::~Stack() {
  flist.clear();
}

template<typename T>
Stack<T>::Stack(const Stack<T>& rhs) {
  std::forward_list<T> flist2 = rhs.flist;
  for (auto itr = flist2.begin(); itr != flist2.end(); itr++)
    push(*itr);
  reverse();
  length = rhs.length;
}

template<typename T>
Stack<T>::Stack(Stack<T> &&rhs) {
  swap(rhs.flist, flist);
  length = rhs.length;
  rhs.length = 0;
}

/* Assignment */
template<typename T>
Stack<T> &Stack<T>::operator=(const Stack<T> &rhs) {
  if (&rhs == this)
    return *this;       //storage purposes
  std::forward_list<T> flist2 = rhs.flist;
  for (auto itr = flist2.begin(); itr != flist2.end(); itr++)
    push(*itr);
  reverse();
  length = rhs.length;
  return *this;
}

template<typename T>
Stack<T> &Stack<T>::operator=(Stack<T> &&rhs) {
  swap(rhs.flist, flist);
  length = rhs.length;
  rhs.length = 0;
  return *this;
}

/* Getters */

template<typename T>
bool Stack<T>::empty() const {
  return (flist.empty());
}

template<typename T>
T& Stack<T>::top() {
  return flist.front();
}

template<typename T>
const T& Stack<T>::top() const {
  return flist.front();
}

template<typename T>
int Stack<T>::size() const {
  return length;
}

/* Methods */

template<typename T>
void Stack<T>::clear() {
  flist.clear();
}

template<typename T>
void Stack<T>::push(const T &x) {
  flist.emplace_front(x); //emplace creates a new
  length++;               //element to place in front
}

template<typename T>
void Stack<T>::push(T &&x) {
  flist.push_front(x);    //push copies or moves the
  length++;               //element depending on pass method
}

template<typename T>
void Stack<T>::pop() {
  flist.pop_front();
  length--;
}

template<typename T>
void Stack<T>::reverse() {
  flist.reverse();
}

template<typename T>
void Stack<T>::print(std::ostream &os, char ofc) const {
  if (flist.empty())
    os << "The stack is empty.";
  for (auto x : flist)
    os << x << ofc;
}

/* Operators */

template<typename T>
std::ostream &operator<<(std::ostream &os, const Stack<T> &a) {
    a.print(os);
    return os;
}

template <typename T>
bool operator== (const Stack<T> & a, const Stack <T>& b) {
  Stack<T> copy1(a);
  Stack<T> copy2(b);
  bool truth = true;
  if (a.size() == b.size()) {
    for (int i = 0; i < copy1.size(); i++) {
      if (copy1.top() != copy2.top())
        truth = false;
      copy1.pop();
      copy2.pop();
    }
  } else
    truth = false;
  return truth;
}

template <typename T>
bool operator!= (const Stack<T>& a, const Stack<T>& b) {
  Stack<T> copy1(a);
  Stack<T> copy2(b);
  bool truth = true;
  int counter = 0;
  if (copy1.size() == copy2.size()) {
    for (int i = 0; i < copy1.size(); i++) {
      if (copy1.top() == copy2.top())
        counter++;
      copy1.pop();
      copy2.pop();
    }
  }
  if (counter == a.size() && counter == b.size())
    truth = false;
  return truth;
}

template <typename T>
bool operator<= (const Stack<T>& a, const Stack<T>& b) {
  Stack<T> copy1(a);
  Stack<T> copy2(b);
  bool truth = true;
  if (a.size() == b.size()) {
    for (int i = 0; i < a.size(); i++) {
      if (copy1.top() > copy2.top())
        truth = false;
      copy1.pop();
      copy2.pop();
    }
  } else
    truth = false;
  return truth;
}


};
