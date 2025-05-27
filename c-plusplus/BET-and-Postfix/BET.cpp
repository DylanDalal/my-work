#include <iostream>

using namespace std;

/*-------------------------BET---------------------*/
BET::BET() {
  root = nullptr;
}

BET::BET(const string& postfix) {
  buildFromPostfix(postfix);
}

BET::BET(const BET& copy) {
  root = clone(copy.root);
  stacko.push(root);
}

BET::~BET() {
  if (!stacko.empty())
    makeEmpty(root);
}

bool BET::buildFromPostfix(const std::string& postfix1) {
  std::string postfix = postfix1;
  bool status = true;
  size_t pos = 0;
  string delim = " ";
  string piece, current;
  if(!empty()) {
    makeEmpty(root);
    emptyStack();
  }

  while ((pos = postfix.find(" ")) != string::npos) {
    piece = postfix.substr(0, pos++);
    if (piece.find_first_not_of(' ') != string::npos) {
      if (isOperator(piece)) {
        BinaryNode *right, *left;
        if (!stacko.empty()) {
          right = stacko.top();
          stacko.pop();
        } else {
          status = false;
          break;
        } if (!stacko.empty()) {
          left = stacko.top();
          stacko.pop();
        } else {
          status = false;
          break;
        } BinaryNode *operate = new BinaryNode(piece, left, right);
        stacko.push(operate);
      } else if (isAlphaNum(piece)) {
        BinaryNode *operand = new BinaryNode(piece,nullptr,nullptr);
        stacko.push(operand);
      }
    }
    postfix.erase(0, pos);
  }
  if (postfix.find_first_not_of(' ') != string::npos) {
    if (isOperator(postfix)) {
      BinaryNode *right, *left;
      if (!stacko.empty()) {
        right = stacko.top();
        stacko.pop();
      } else {
        status = false;
      } if (!stacko.empty()) {
        left = stacko.top();
        stacko.pop();
      } else {
        status = false;
      } BinaryNode *operate = new BinaryNode(postfix, left, right);
      stacko.push(operate);
    } else if (isAlphaNum(postfix)) {
      BinaryNode *operand = new BinaryNode(postfix,nullptr,nullptr);
      stacko.push(operand);
    }
    //stacko.pop();
  }
  if (!stacko.empty()) {
    root = stacko.top();
    if (stacko.size() > 1 && isAlphaNum(root->element))
      status = false;
  } else
    status = false;
  if(!status){
    std::cout << "Invalid postfix input." << std::endl;
    if(!empty()){
      makeEmpty(root);
      emptyStack();
    }
  }
  return status;
}

bool BET::isOperator(string str) {
  if (str == "+" || str == "-" || str == "*" || str == "/")
    return true;
  else
    return false;
}

bool BET::isAlphaNum(string str) {
  if (str.find_first_of("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        != string::npos)
    return true;
  else
    return false;
}

int BET::priority(string str) {
  if (str == "-" || str == "+")
    return 1;
  else if (str == "*" || str == "/")
    return 2;
  return 0;
}

const BET & BET::operator= (const BET & right) {
  root = right.root;
  emptyStack();
  stacko.push(root);
  return *this;
}

void BET::printInfixExpression() {
  printInfixExpression(root);
  cout << endl;
}

void BET::printPostfixExpression() {
  printPostfixExpression(root);
  cout << endl;
}

size_t BET::size() {
  return size(root);
}

size_t BET::leaf_nodes() {
  return leaf_nodes(root);
}

bool BET::empty() {
  return (root == nullptr);
}


/* Helper functions */
void BET::printInfixExpression(BinaryNode *n) {
  bool before = false;
  int prev = 0;
  if (n != nullptr) {
    if(isAlphaNum(n->element)) {
      before = false;
    }
    if (isOperator(n->element) && (prev == 0)) {
      prev = (priority(n->element));
      before = true;
    }
    if (isOperator(n->element) && (n != root) && (priority(n->element) > prev)) {
      std::cout << "( ";
      prev = (priority(n->element));
      before = true;
    } else if (isOperator(n->element) && (n != root) && before) {
      std::cout << "( ";
      prev = (priority(n->element));
      before = true;
    }
    printInfixExpression(n->left);
    std::cout << n->element << " ";
    printInfixExpression(n->right);
    if(isOperator(n->element) && n != root)
      std::cout << ") ";
  }
}

void BET::makeEmpty(BinaryNode* &t) {
  if (t != nullptr) {
    if (t->left != nullptr)
      makeEmpty(t->left);
    if (t->right != nullptr)
      makeEmpty(t->right);
  }
  t = nullptr;
}

BET::BinaryNode * BET::clone(BinaryNode* t) const{
  if (t==nullptr)
    return nullptr;
  else
    return new BinaryNode{t->element,clone(t->left),clone(t->right)};                //recursion! wow
}

void BET::printPostfixExpression(BinaryNode *n) {
  if (n != nullptr){
    printPostfixExpression(n->left);
    printPostfixExpression(n->right);
    std::cout << n->element << " ";
  }
}

void BET::emptyStack() {
  int max = stacko.size();
  for (int i = 0; i < max; i++) {
    stacko.pop();
  }
}


size_t BET::size(BinaryNode *t) {
  if (t == nullptr)
    return 0;
  else {
    int i = size(t->left);
    int o = size(t->right);   //review
    int p = 1 + i + o;
    return p;
  }
}

size_t BET::leaf_nodes(BinaryNode *t) {
  if (t == nullptr)
    return 0;
  if (t->left == nullptr & t->right == nullptr) //root = leaf
    return 1;
  else return 0 + leaf_nodes(t->left) + leaf_nodes(t->right);
}
