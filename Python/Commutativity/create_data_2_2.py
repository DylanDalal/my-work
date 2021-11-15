import numpy as np, pandas as pd
from numpy.core.defchararray import isdigit
import re  # for regular expressions
from collections import Counter, deque


class BET:  # binary expression tree
    def __init__(self, value, left=None,
                 right=None):  # value is expected to be a string representing either an arithmetic symbol or a number
        self.value = value
        self.left = left
        self.right = right

    # calling display on the root will display the BET in a nice format (root.display())
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def simplify_response(r):
    ''' Replace +- with just - and remove parentheses from a response if they don't affect the result
    The purpose of doing this is to avoid treating responses as different if they are basically the same '''
    # This has been extended to distributing negative signs into parentheses because of the fact
    # that -(3+3) breaks the program, lol
    if r[-1] == "+" or r[-1] == "-":
        r = r[:-1]

    if "+-" in r:
        new_r = r.replace("+-", "-")
        r = new_r
    r = r.replace("+*", "*")

    if "(" not in r and ")" not in r:
        return r
    else:   # So, there are parentheses in the expression.
        original_r = r

        # Determines if there are parentheses that can be removed from the expression.
        negative = False
        check_for_close = False
        open_par = 0
        changed = False
        # Algorithm for parentheses removal with negative sign distribution.
        index = 0

        while True:
            try:
                before = index - 1
                peek = index + 1
                # This ends the algorithm. It ensures that removing the parentheses doesn't change
                # the final output value of the expression.
                if changed:
                    r = re.sub(" ", "", r)
                    r = re.sub(" ", "", r)
                    r2 = re.sub("-", "+-", r)
                    r3 = re.sub("\+\+", "+", r2)
                    r4 = re.sub("\*\+-", "*-", r3)
                    r = re.sub("/\+-", "/-", r4)
                    if pd.eval(r) != pd.eval(original_r):
                        r = original_r
                    changed = False
                    check_for_close = False
                    open_par = False

                # Finding an open parentheses starts the algorithm, as long as the character before the
                # parentheses is an addition or subtraction symbol. There is no point removing the parentheses
                # surrounding a value that is being multiplied or dividing something else, as it will always
                # impact the final calculation, if not the final value.
                if r[index] == "(":
                    if r[before] == "+" or r[before] == "-":
                        check_for_close = True
                        open_par = index
                        if r[before] == "-":
                            r = r[:before] + "+ +" + r[peek:]
                            negative = True

                # If an open parentheses hasn't yet been found there is no point checking the rest of this.
                if check_for_close is True:
                    if negative is True:  # Flip the addition/subtraction values; add negatives where needed.
                        if r[index] == "-":
                            r = r[:index] + "+" + r[peek:]
                        elif r[index] == "+":
                            r = r[:index] + "-" + r[peek:]
                        elif r[index] == "*":
                            if r[peek] != "-":
                                r = r[:index] + "*-" + r[peek:]
                        elif r[index] == "/":
                            if r[peek] != "-":
                                r = r[:index] + "/-" + r[peek:]
                    if r[index] == ")":
                        if peek == len(r) or peek < len(r) and (r[peek] == "+" or r[peek] == "-"):
                            r = r[:open_par] + " " + r[open_par+1:]
                            r = r[:index] + " " + r[peek:]
                            negative = False
                            changed = True
                        else:
                            negative = False

                index = index + 1
            except IndexError:
                if changed:
                    r = re.sub(" ", "", r)
                    if pd.eval(r) != pd.eval(original_r):
                        r = original_r
                break

        r = re.sub(" ", "", r)
        r = re.sub("-", "+-", r)

        c1 = False
        c2 = False
        c3 = False
        c4 = False
        c5 = True
        while c5:
            if "++" in r:
                r = re.sub("\+\+", "+", r)
            else:
                c1 = True
            if "*+-" in r:
                r = re.sub("\*\+-", "*-", r)
            else:
                c2 = True
            if "/+-" in r:
                r = re.sub("/\+-", "/-", r)
            else:
                c3 = True
            if "*+" in r:
                r = re.sub("\*\+", "*", r)
            else:
                c4 = True
            if c1 and c2 and c3 and c4:
                c5 = False
        return r


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                   Additive Commutativity                              #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


def infix_to_postfix(precedence_order, infix_input: list) -> list:
    associativity = {'+': "LR", '-': "LR", '*': "LR", '/': "LR"}
    i = 0
    postfix = []

    operators = "+-/*^"
    stack = deque()
    while i < len(infix_input):
        char = infix_input[i]
        # check if char is operator
        if char in operators:
            # check if the stack is empty or the top element is '('
            if len(stack) == 0 or stack[0] == '(':
                # just push the operator into stack
                stack.appendleft(char)
                i += 1
            # otherwise compare the curr char with top of the element
            else:
                # peek the top element
                top_element = stack[0]
                # check for precedence
                # if they have equal precedence
                if precedence_order[char] == precedence_order[top_element]:
                    # check for associativity
                    if associativity[char] == "LR":
                        # pop the top of the stack and add to the postfix
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
                    # if associativity of char is Right to left
                    elif associativity[char] == "RL":
                        # push the new operator to the stack
                        stack.appendleft(char)
                        i += 1
                elif precedence_order[char] > precedence_order[top_element]:
                    # push the char into stack
                    stack.appendleft(char)
                    i += 1
                elif precedence_order[char] < precedence_order[top_element]:
                    # pop the top element
                    popped_element = stack.popleft()
                    postfix.append(popped_element)
        elif char == '(':
            # add it to the stack
            stack.appendleft(char)
            i += 1
        elif char == ')':
            top_element = stack[0]
            while top_element != '(':
                popped_element = stack.popleft()
                postfix.append(popped_element)
                # update the top element
                top_element = stack[0]
            # now we pop opening parenthases and discard it
            stack.popleft()
            i += 1
        # char is operand
        else:
            postfix.append(char)
            i += 1

    # empty the stack
    if len(stack) > 0:
        for i in range(len(stack)):
            postfix.append(stack.popleft())
    # while len(stack) > 0:
    #     postfix.append(stack.popleft())

    return postfix


# tokenizes an infix expression, explained in previous function comment
def token_infix(infix):
    # https://www.regex101.com/
    number_or_symbol = re.compile('([/]?[-]?\d+|[^ 0-9])')
    postfix_list = (re.findall(number_or_symbol, infix))

    # Convert division (x/y) to x * inverse(y).
    for entry_index in range(0, len(postfix_list)):
        if "/" in postfix_list[entry_index]:
            postfix_list[entry_index] = "(inv(" + postfix_list[entry_index][1:] + "))"
            postfix_list.insert(entry_index, '*')

    return postfix_list


# func for checking if character is an operator to be used by add_tree
def is_operator(c):
    return c == '+' or c == '*' or c == '/' or c == '-'


def priority(c):
    if c == '+' or c == '-':
        return 0
    if c == '*' or c == '/':
        return 1
    else:
        return 2


# Constructs the BET from the given infix expression, first tokenizes infix expression, converts it into
# tokenized postfix expression, then builds the BET
def construct_tree(infix):
    # Convert subtraction operator "-" to "+-" so that subtraction-rooted
    # expressions now count as addition-rooted expressions.
    try:
        back = infix[1:len(infix)]
        if "-" in back:
            new_back = back.replace("-", "+-")
            new_new_back = new_back.replace("++", "+")      # OK so this got a little
            new_back = new_new_back.replace("+-(", "-(")    # out of hand perhaps it
            new_new_back = new_back.replace("*+-", "*-")    # could use a streamline
            new_back = new_new_back.replace("/+-", "/-")    # in the future
            infix = infix[0] + new_back
    except:
        infix = infix

    postfix = infix_to_postfix({'+': 0, '-': 0, '*': 1, '/': 1}, token_infix(infix))
    stack = []
    # Traverse through every character of input expression
    for itr in range(0, len(postfix)):
        # If operand, simply push into stack
        if not is_operator(postfix[itr]):
            t = BET(postfix[itr])
            stack.append(t)
        # Operator
        else:
            # Pop two top nodes
            t = BET(postfix[itr])
            t1 = stack.pop()
            t2 = stack.pop()

            # make them children
            t.right = t1
            t.left = t2

            # Add this subexpression to stack
            stack.append(t)

    # Only element will be the root of expression tree
    t = stack.pop()

    return t


def is_numeric(in_string):
    if in_string[0] == "-":
        in_string = in_string[1:]
    return in_string.isnumeric()


def contains_numbers(in_string):
    return any(char.isdigit() for char in in_string)


def get_first(in_string):
    if in_string[0] == "-":
        return in_string[:2]
    else:
        return in_string[0]


def O(expr):
    if expr is not None:
        return expr
    else:
        return None


def L(expr):
    if expr.left is not None:
        return expr.left
    else:
        return None


def R(expr):
    if expr.right is not None:
        return expr.right
    else:
        return None


def comm_add(exprA, exprB):
    if O(exprA) is None or O(exprB) is None:
        return O(exprA) == O(exprB)
    elif O(exprA).value != O(exprB).value:
        return False
    elif sorted(add_children(exprA)) == sorted(add_children(exprB)):
        return True
    else:
        return comm_add(L(exprA), L(exprB)) and comm_add(R(exprA), R(exprB))


def add_children(expr):
    # If the expression is an addition sign
    if O(expr).value == "+":
        left = add_children(L(expr))
        right = add_children(R(expr))
        # Return the sorted list of children
        output = (left + right)
        return output
    else:
        # If the expression is not an addition sign
        # But it is an operator
        if is_operator(O(expr).value):
            left = ""
            # Test if its left child is an operator.
            if is_operator(L(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(L(expr).value) < priority(O(expr).value):
                    value = "("
                    l = add_children(L(expr))
                    if isinstance(l, list):
                        for entry in l:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            value = value + entry + "+"
                        value = value[:-1]
                    else:
                        value = value + l
                    value = value + ")"
                    left = value
                else:
                    left = add_children(L(expr))
            else:
                left = add_children(L(expr))

            # Test if its right child is an operator.
            if is_operator(R(expr).value):
                # Test if the child operator has a greater priority than the parent.
                if priority(R(expr).value) < priority(O(expr).value):
                    value = "("
                    r = add_children(R(expr))
                    if isinstance(r, list):
                        for entry in r:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            value = value + entry + "+"
                    else:
                        value = value + r
                    value = value + ")"
                    right = value
                else:
                    right = add_children(R(expr))
            else:
                right = add_children(R(expr))

            # Bonus error checking (might be unnecessary)
            if isinstance(left, str):
                left = [left]
            if isinstance(right, str):
                right = [right]

            left[-1] = left[-1] + O(expr).value + right[0]
            del right[0]
            if right != []:
                left.extend(right)
            return sorted(left)

        # If it is an integer...
        else:
            return [O(expr).value]


def comm_mul(exprA, exprB):
    if O(exprA) is None or O(exprB) is None:
        return exprA == exprB
    elif O(exprA).value != O(exprB).value:
        return False
    elif sorted(mul_children(exprA)) == sorted(mul_children(exprB)):
        return True
    else:
        return comm_mul(L(exprA), L(exprB)) and comm_mul(R(exprA), R(exprB))


def mul_children(expr):
    # If the expression is an addition sign
    if O(expr).value == "*":
        left = mul_children(L(expr))
        right = mul_children(R(expr))
        # Return the sorted list of children
        output = (left + right)
        return output
    else:
        # If the expression is not an addition sign
        # But it is an operator
        if is_operator(O(expr).value):
            left = ""
            # Test if its left child is an operator.
            if is_operator(L(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(L(expr).value) < priority(O(expr).value):
                    value = "("
                    l = mul_children(L(expr))
                    if isinstance(l, list):
                        for entry in l:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            value = value + entry + "*"
                        value = value[:-1]
                    else:
                        value = value + l
                    value = value + ")"
                    left = value
                else:
                    left = mul_children(L(expr))
            else:
                left = mul_children(L(expr))

            # Test if its right child is an operator.
            if is_operator(R(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(R(expr).value) < priority(O(expr).value):
                    value = "("
                    r = mul_children(R(expr))
                    if isinstance(r, list):
                        for entry in r:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            value = value + entry + "*"
                        value = value[:-1]
                    else:
                        value = value + r
                    value = value + ")"
                    right = value
                else:
                    right = mul_children(R(expr))
            else:
                right = mul_children(R(expr))

            # Bonus error checking (might be unneccesary)
            if isinstance(left, str):
                left = [left]
            if isinstance(right, str):
                right = [right]

            left[-1] = left[-1] + O(expr).value + right[0]
            del right[0]
            if right:
                left.extend(right)
            return sorted(left)

        # If it is an integer...
        else:
            return [O(expr).value]


if __name__ == '__main__':
    print("\n")
    a_ = "1*2+4"
    b_ = "2+4*1"
    print("a_:", a_)
    print("b_:", b_)

    a_a = construct_tree(simplify_response(a_))
    b_a = construct_tree(simplify_response(b_))
    a_m = construct_tree(simplify_response(a_))
    b_m = construct_tree(simplify_response(b_))
    print(a_a.display())
    print(b_a.display())

    print("Add_children (a): ", add_children(a_a))
    print("Add_children (b): ", add_children(b_a))
    print("These equations demonstrate the commutative \nproperty of addition:\t\t", comm_add(a_a, b_a), "\n")

    print("a_:", a_)
    print("b_:", b_)
    print("Mul_children (a): ", mul_children(a_m))
    print("Mul_children (b): ", mul_children(b_m))
    print("These equations demonstrate the commutative \nproperty of multiplication:\t\t", comm_mul(a_m, b_m), "\n")
