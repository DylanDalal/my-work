#ifndef HASHTABLE_H
#define HASHTABLE_H
#include <vector>
#include <list>
#include <iostream>
#include <fstream>

using namespace std;

namespace cop4530 {
  template <typename K, typename V>
  class HashTable{
  public:
    HashTable(size_t size = 101);
    ~HashTable();

    bool contains(const K &k) const;
    bool match(const std::pair<K,V> &kv) ;
    bool insert(const std::pair<K,V> &kv);
    bool insert(std::pair<K,V> && kv);
    bool isEmpty();
    bool remove(const K & k);

    bool load(const char *filename);
    bool write_to_file(const char *filename) const;
    void clear();
    void dump() const;

    size_t getSize() const; //renamed "size()"

    static const unsigned int max_prime = 1301081;
    static const unsigned int default_capacity = 11;

  private:
    void makeEmpty();
    size_t myhash(const K &k) const;
    unsigned long prime_below(unsigned long);
    void setPrimes(std::vector<unsigned long> &);
    void rehash();

    std::vector<std::list<std::pair<K,V>>> vec;
    size_t size;
  };

  #include "hashtable.hpp"

}

#endif
