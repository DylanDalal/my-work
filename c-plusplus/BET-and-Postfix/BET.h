#include <iostream>
#include <stack>
#include <string>


  class BET {
    private:
      struct BinaryNode {
        std::string element;
        BinaryNode *left;
        BinaryNode *right;

        BinaryNode() {
          left = nullptr;
          right = nullptr;
        } BinaryNode(const std::string &data, BinaryNode *l, BinaryNode *r) {
          element = data;
          left = l;
          right = r;
        }
      };
      BinaryNode * clone(BinaryNode *t) const;
      bool isOperator(std::string str);
      bool isAlphaNum(std::string str);
      int priority(std::string str);
      BinaryNode *root;
      std::stack<BinaryNode*> stacko;
      size_t size(BinaryNode *t);
      size_t leaf_nodes(BinaryNode *t);

      void makeEmpty(BinaryNode* &t);

      void printPostfixExpression(BinaryNode *n);
      void printInfixExpression(BinaryNode *n);
      void emptyStack();

  public:
    BET();
    BET(const std::string& postfix);
    BET(const BET&);
    ~BET();

    size_t size();
    size_t leaf_nodes();
    bool empty();

    bool buildFromPostfix(const std::string& postfix1);

    const BET & operator= (const BET & right);

    void printPostfixExpression();
    void printInfixExpression();
  };

#include "BET.cpp"
