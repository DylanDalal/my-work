#include <iostream>
#include "List.h"

using namespace cop4530;


/*************************************/
/*       Const Iterator Class        */
/*************************************/
/* Constructors */
template <typename T>
List<T>::const_iterator::const_iterator() {
    current = nullptr;
}

template<typename T>
List<T>::const_iterator::const_iterator(List::Node *p) {
    current = p;
};

/* Getters (Retters? :D) */
template<typename T>
T &List<T>::const_iterator::retrieve() const {
    return current->data;
}

/* Operator Overloding */
template <typename T>
const T &List<T>::const_iterator::operator*() const {
    return retrieve();
}
template<typename T>
typename List<T>::const_iterator &List<T>::const_iterator::operator++() {
    current = current->next;
    return *this;
}
template<typename T>
typename List<T>::const_iterator List<T>::const_iterator::operator++(int) {
    const_iterator old = *this;
    ++(*this);
    return old;
}
template<typename T>
typename List<T>::const_iterator &List<T>::const_iterator::operator--() {
    this->current = this->current->prev;
    return *this;
}
template<typename T>
typename List<T>::const_iterator List<T>::const_iterator::operator--(int) {
    const_iterator old = *this;
    --(*this);
    return old;
}
template<typename T>
bool List<T>::const_iterator::operator==(const List::const_iterator &rhs) const {
    return {rhs.current == this->current};
}
template<typename T>
bool List<T>::const_iterator::operator!=(const List::const_iterator &rhs) const {
    return !(rhs == *this);
}

/********************************************/
/*               Iterator                   */
/********************************************/

/* -structors of Sorts */
template<typename T>
List<T>::iterator::iterator() {
    // :D
}

template<typename T>
List<T>::iterator::iterator(List::Node *p):const_iterator(p) {} //Review

/* Operator Overloading */
template<typename T>
const T &List<T>::iterator::operator*() const {
    return const_iterator::operator*();
}

template<typename T>
T &List<T>::iterator::operator*() {
    return const_iterator::retrieve();
}

template<typename T>
typename List<T>::iterator &List<T>::iterator::operator++() {
    this->current = this->current->next;
    return *this;
}

template<typename T>
typename List<T>::iterator List<T>::iterator::operator++(int) {
    iterator old = *this;
    ++(*this);
    return old;
}

template<typename T>
typename List<T>::iterator &List<T>::iterator::operator--() {
    this->current = this->current->prev;
    return *this;
}

template<typename T>
typename List<T>::iterator List<T>::iterator::operator--(int) {
    iterator old = *this;
    --(*this);
    return old;
}

/********************************************/
/*                  List                    */
/********************************************/
/* Constructors
 * Operators
 * Getters
 * Insertion/Removal
 * Methods
 *  Push and Pop
 *  Setters
 *  Other
 */

/* Constructors */
template<typename T>
List<T>::List() {
    init();
}

template<typename T>
List<T>::List(const List &rhs) {
    init();
    for (auto &x : rhs)
        push_back(x);
}

template<typename T>
List<T>::List(List &&rhs) {
    theSize = rhs.theSize;
    head = rhs.head;
    tail = rhs.tail;
    rhs.theSize=0;
    rhs.head = nullptr;
    rhs.tail = nullptr;
}

template<typename T>
List<T>::List(int num, const T &val) {
    init();
    for (int i = 0; i < num; i++)
        push_front(val);
}

template<typename T>
List<T>::List(List::const_iterator start, List::const_iterator end) {
    init();
    Node *temp = head;
    head->next = start.current;
    tail = end.current;
    while(start != end || start == this->end()) {
        temp->next = new Node(*(start++), temp);
        temp = temp->next;
        theSize++;
    }
    tail->next = nullptr;
}

template<typename T>
List<T>::List(std::initializer_list<T> iList) {
    init();
    for (const auto &t : iList)
        push_back(t);
}

template<typename T>
List<T>::~List() {
    clear();
    delete head;
    delete tail;
}

/* Operators */
template<typename T>
const List<T> & List<T>::operator=(const List &rhs) {
    theSize = rhs.theSize;
    head=rhs.head;
    tail=rhs.tail;
}

template<typename T>
List<T> &List<T>::operator=(List &&rhs) {
    std::swap(theSize, rhs.theSize);
    std::swap(head, rhs.head);
    std::swap(tail, rhs.tail);

    return *this;
}

template<typename T>
List<T> &List<T>::operator=(std::initializer_list<T> iList) {
    init();
    for (const auto &t : iList) {
        push_back(t);
    }
    return *this;
}


/* Getters */

template<typename T>
typename List<T>::iterator List<T>::begin() {
    return head->next;
}

template<typename T>
typename List<T>::const_iterator List<T>::begin() const {
    const_iterator itr(head);
    return ++itr;
}

template<typename T>
typename List<T>::iterator List<T>::end() {
    return tail;
}

template<typename T>
typename List<T>::const_iterator List<T>::end() const {
    return tail;
}

template<typename T>
bool List<T>::empty() const {
    return size() == 0;
}

template<typename T>
int List<T>::size() const {
    return theSize;
}

/* Insertion and Removal */
template<typename T>
typename List<T>::iterator List<T>::insert(List::iterator itr, const T &val) {
    Node *p = itr.current;
    theSize++;
    return {p->prev = p->prev->next = new Node(val, p->prev, p)};
}

template<typename T>
typename List<T>::iterator List<T>::insert(List::iterator itr, T &&val) {
    Node *p = itr.current;
    theSize++;
    return { p->prev = p->prev->next = new Node(std::move(val), p->prev, p)};
}

template<typename T>
typename List<T>::iterator List<T>::erase(List::iterator itr) {
    Node *p = itr.current;
    iterator retVal(p->next);
    p->prev->next = p->next;
    p->next->prev = p->prev;
    delete p;
    theSize--;
    return retVal;
}

template<typename T>
typename List<T>::iterator List<T>::erase(List::iterator start, List::iterator end) {
    for (iterator itr = start; itr != end;)
        itr = erase(itr);

    return end;
}

/*-------Methods--------*/
/* Push and Pop */
template<typename T>
void List<T>::push_front(const T &val) {
    insert(begin(), val);
}

template<typename T>
void List<T>::push_front(T &&val) {
    insert(begin(), std::move(val));
}

template<typename T>
void List<T>::push_back(const T &val) {
    insert(end(), val);
}

template<typename T>
void List<T>::push_back(T &&val) {
    insert(end(), std::move(val));
}

template<typename T>
void List<T>::pop_front() {
    erase(begin());
}

template<typename T>
void List<T>::pop_back() {
    erase(--end());
}

/* Setters */
template<typename T>
T &List<T>::front() {
    return *begin();
}

template<typename T>
const T &List<T>::front() const {
    return *begin();
}

template<typename T>
T &List<T>::back() {
    return *--end();
}

template<typename T>
const T &List<T>::back() const {
    return *--end();
}


/* Other */
template<typename T>
void List<T>::clear() {
    while(!empty())
        pop_front();
}

template<typename T>
void List<T>::init() {
    theSize = 0;
    head = new Node();
    tail = new Node;
    head->next = tail;
    tail->prev = tail;
}


template<typename T>
void List<T>::print(std::ostream &os, char ofc) const {
    if (empty())
        os << "(empty)";
    else {
        auto itr = begin();
        os << "[ " << *itr;
        while (itr != end())
            os << ofc << *itr++;
        os <<" ]" << std::endl;
    }
}

template<typename T>
void List<T>::remove(const T &val) {
    const_iterator *itr = new const_iterator(head->next);
    for (int i = 0; i < size(); i++)
        if (itr->current->data == val) {     //remove
            itr++;
            erase(itr->current->prev);
        } else
            itr++;
}

template<typename T>
template<typename PREDICATE>
void List<T>::remove_if(PREDICATE pred) {
    const_iterator *itr = new const_iterator(begin());
    for (int i = 0; i<size(); i++) {
        auto test = itr->current->data;
        if (pred(test)) {
            i++;
            erase(itr->current->prev);
        }
        else
            i++;
    }
}

template<typename T>
void List<T>::reverse() {
    iterator *itr = new iterator(tail);
    if (empty()) {
    } else {
        while(itr->current != nullptr) {
            std::swap(itr->current->next, itr->current->prev);
            itr->current = itr->current->prev;
        }
    }
    std::swap(head, tail);
}


/************************************/
/*             Other                */
/************************************/

template<typename T>
bool operator==(const List<T> &lhs, const List<T> &rhs) {
    typename List<T>::const_iterator *itr1 = new typename List<T>::const_iterator(lhs.begin());
    typename List<T>::const_iterator *itr2 = new typename List<T>::const_iterator(rhs.begin());
    if (lhs.size() == rhs.size()) {
        for (int i = 0; i < lhs.size(); i++) {
            if (itr1 == itr2) {
                itr1++;
                itr2++;
            } else
                return false;
        }
        return true;
    }
}

template<typename T>
bool operator!=(const List<T> &lhs, const List<T> &rhs) {
    typename List<T>::iterator *itr1 = new typename List<T>::iterator(lhs.begin());
    typename List<T>::iterator *itr2 = new typename List<T>::iterator(rhs.begin());
    if (lhs.size() == rhs.size()) {
        for (int i = 0; i < lhs.size(); i++) {
            if (itr1->data == itr2->data) {
                itr1++;
                itr2++;
            } else
                return true;
        }
        return false;
    }
}

template<typename T>
std::ostream &operator<<(std::ostream &os, const List<T> &l) {
    l.print(os);
    return os;
}



}