#ifndef PASSSERVER_H
#define PASSSERVER_H
#include "hashtable.h"

using namespace cop4530;
using namespace std;

class PassServer {
    public:
        PassServer(size_t size = 101);
        ~PassServer();
        bool load(const char *filename);
        bool addUser(std::pair<std::string, std::string> &kv);
        bool addUser(std::pair<std::string, std::string> &&kv);
        bool removeUser(const std::string &k);
        bool changePassword(const std::pair<std::string, std::string> &p, const std::string & newpassword);
        bool find(const std::string &user);
        void dump() const;
        bool write_to_file(const char *filename) const;
        size_t size() const;
        HashTable<string, string> table;
    private:
      	string encrypt(const std::string & str);
};

#endif
