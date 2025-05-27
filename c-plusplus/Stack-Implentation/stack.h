#include <iostream>
#include <forward_list>

namespace cop4530 {
  template <typename T>
  class Stack {
  private:
    std::forward_list<T> flist;
    int length;
  public:
    Stack();
    ~Stack();
    Stack(const Stack<T>& rhs);
    Stack(Stack<T> &&rhs);
    Stack<T>& operator=(const Stack <T>&rhs);
    Stack<T> & operator=(Stack<T> &&rhs);
    bool empty() const;
    void clear();
    void push(const T& x);
    void push(T && x);
    void pop();
    void reverse();
    T& top();
    const T& top() const;
    int size() const;
    void print(std::ostream& os, char ofc = ' ') const;
  };

  template <typename T>
  std::ostream& operator<< (std::ostream& os, const Stack<T>& a);
  template <typename T>
  bool operator== (const Stack<T> & a, const Stack <T>& b);
  template <typename T>
  bool operator!= (const Stack<T>& a, const Stack<T>& b);
  template <typename T>
  bool operator<= (const Stack<T>& a, const Stack<T>& b);

#include "stack.hpp"
