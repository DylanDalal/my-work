#include "passserver.h"
#include <stdio.h>
#include <unistd.h>
#include <crypt.h>
using namespace cop4530;
using namespace std;

/*-------- ~ Structors ~ --------*/
PassServer::PassServer(size_t size) : table(size) {
}

PassServer::~PassServer() {
  table.clear();
}

/*-------- ~ I/O ~ --------------*/
bool PassServer::load(const char *filename) {
  return table.load(filename);
}

void PassServer::dump() const {
  return table.dump();
}

bool PassServer::write_to_file(const char *filename) const {
  return table.write_to_file(filename);
}

/*-------- ~ Getters ~ -----------*/

size_t PassServer::size() const {
  return table.getSize();
}

/*-------- ~ Actions ~ -----------*/

bool PassServer::addUser(pair<string, string> &kv) {
  string encrypted = encrypt(kv.second);
  pair<string,string> user = make_pair(kv.first,encrypted);
  return table.insert(user);
}

bool PassServer::addUser(pair<string, string> &&kv) {
  string encrypted = encrypt(kv.second);
  pair<string,string> user = make_pair(kv.first,encrypted);
  return table.insert(user);
}

bool PassServer::removeUser(const string &k) {
  return table.remove(k);
}

bool PassServer::changePassword(const pair<string,string> &p, const string & newpassword) {
  if(!table.contains(p.first))
    return false;
  else {
    pair<string,string> change(p.first, newpassword);
    return table.insert(change);
  }
}

bool PassServer::find(const string &user) {
  return table.contains(user);
}

/* ------- ~ Helper Functions ~ ----*/

string PassServer::encrypt(const string &str){
  char salt[] = "$1$########";
  string temp = crypt(str.c_str(), salt);
  string encryption = temp.substr(12,34);
  return encryption;
}
