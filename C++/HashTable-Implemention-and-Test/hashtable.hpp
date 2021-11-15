#include "hashtable.h"
#include <vector>
#include <list>
#include <iostream>


/*--------- ~ Structors ~ ---------*/
template <typename K, typename V>
HashTable<K, V>::HashTable(size_t size){
  int cap = prime_below(size);
  cout << cap << endl;
  vec.resize(cap);
  size = 0;
}

template <typename K, typename V>
HashTable<K, V>::~HashTable() {
  clear();
  size = 0;
}

/*--------- ~ Checks ~ ------------*/
template <typename K, typename V>
bool HashTable<K,V>::contains(const K &k) const {
  auto & check = vec[myhash(k)];
  for (auto itr : check)
    if (itr.first == k)
      return true;
  return false;
}

template <typename K, typename V>
bool HashTable<K, V>::isEmpty() {
  if (size == 0)
    return true;
  else
    return false;
}

template <typename K, typename V>
bool HashTable<K,V>::match(const std::pair<K,V> &kv) {
  auto & check = vec[myhash(kv.first)];
  for (auto itr : check) {
    if (itr.first == kv.first) {
      if (itr.second == kv.second)
        return true;
    }
  }
  return false;
}

template <typename K, typename V>
size_t HashTable<K, V>::getSize() const {
  return size;
}

/*--------- ~ Actions ~ ----------*/
template <typename K, typename V>
bool HashTable<K,V>::insert(const std::pair<K,V> &kv){
  auto & current = vec[myhash(kv.first)];
  if (match(kv)) {
    return false;
  } else {
    for (auto & itr : current) {
      if (itr.first == kv.first) {
        itr.second = kv.second;
        return true;
      }
    }
    current.push_back(kv);
    size++;
    if (size > vec.size())
      rehash();
    return true;
  }
}

template <typename K, typename V>
bool HashTable<K,V>::insert(std::pair<K,V> &&kv) {
  auto & current = vec[myhash(kv.first)];
  if (match(kv)) {
    return false;
  } else {
    for (auto & itr : current) {
      if (itr.first == kv.first) {
        itr.second = std::move(kv.second);
        size++;
        return true;
      }
    }
    current.push_back(kv);
    size++;
    if (size > vec.size())
      rehash();
    return true;
  }
}

template <typename K, typename V>
bool HashTable<K,V>::remove(const K & k) {
  auto & current = vec[myhash(k)];
  auto itr = current.begin();   //dont change this
  int counter = 0;
  list<pair<string,string>>::iterator itrJr;
  for (itrJr = current.begin(); itrJr != current.end(); itrJr++) {
    if (itrJr->first == k) {
      current.erase(itr);       //dont change this
      size--;
      return true;
    }
    itr++;
  }
  return false;
}

template <typename K, typename V>
void HashTable<K,V>::clear(){
  vec.clear();
  size = 0;
}

template <typename K, typename V>
bool HashTable<K,V>::load(const char *filename){
  ifstream input;
  K key;
  V val;

  input.clear();
  input.open(filename);
  if (input.is_open()) {
    while (!input.eof()) {
      input >> key >> val;
      insert(make_pair(key,val));
    }
  } else
    return false;
  input.close();
  return true;
}

template <typename K, typename V>
void HashTable<K,V>::dump() const {
  int counter = 0;
  for (auto & itr : vec) {
    counter++;
    cout << " v[" << counter << "]: ";
    for (auto & itrJr : itr) {
      if (itrJr != *itr.end() && itrJr != *itr.begin())
        cout << " : ";
      cout << itrJr.first << " " << itrJr.second;
    }
    cout << endl;
  }
}

template <typename K, typename V>
bool HashTable<K,V>::write_to_file(const char *filename) const {
  ofstream output;
  output.open(filename);
  if (output.is_open()) {
    for (auto & itr : vec) {
      for (auto & itrJr : itr)
        output << itrJr.first << " " << itrJr.second << "\n";
    }
  } else
    return false;
  output.close();
  return true;
}

/*--------- ~ Helper Functions ~ --*/
template <typename K, typename V>
void HashTable<K,V>::makeEmpty(){
  for (auto & itr : vec) {
    itr.clear();
  }
}

template <typename K, typename V>
void HashTable<K,V>::rehash(){
  int newSize = vec.size() * 2;
  vec.resize(prime_below(newSize));
}

template <typename K, typename V>
unsigned long HashTable<K, V>::prime_below (unsigned long n) {
  if (n > max_prime) {
      std::cerr << "** input too large for prime_below()\n";
      return 0;
  }
  if (n == max_prime) {
      return max_prime;
  }
  if (n <= 1) {
		std::cerr << "** input too small \n";
      return 0;
  }
  std::vector <unsigned long> v (n+1);
  setPrimes(v);
  while (n > 2) {
      if (v[n] == 1)
	return n;
      --n;
  }

  return 2;
}


template <typename K, typename V>
void HashTable<K, V>::setPrimes(std::vector<unsigned long>& vprimes) {
  int i = 0;
  int j = 0;

  vprimes[0] = 0;
  vprimes[1] = 0;
  int n = vprimes.capacity();

  for (i = 2; i < n; ++i)
    vprimes[i] = 1;

  for( i = 2; i*i < n; ++i) {
      if (vprimes[i] == 1)
        for(j = i + i ; j < n; j += i)
          vprimes[j] = 0;
  }
}

template <typename K, typename V>
size_t HashTable<K,V>::myhash(const K &k) const {
    size_t val = 0;
    for(auto ch : k)
        val = 37 * val + ch;
    return val % vec.size();
}
