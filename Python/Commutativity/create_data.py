import numpy as np, pandas as pd
from numpy.core.defchararray import isdigit
import re  # for regular expressions
from collections import Counter, deque
import json
from tqdm import tqdm
from os.path import exists
import openpyxl


def add_resp_info_to_items():
    ''' Add the following info to each item in the items dict:
    'resp_lists', a list containing each participant's responses in list format
    'valid_resp_counts', a list of valid individual responses and their frequencies
    'valid_resps', a list of valid individual responses without frequencies '''

    def validate(r, item):
        ''' Check whether r is a valid response for item '''
        I = items[item]
        numbers = [int(n) for n in re.findall('(\d+)', r)]
        if len([n for n in numbers if n not in I['opts']]) > 0:
            return False
        else:
            try:
                return eval(r) == I['targ']
            except (SyntaxError, ZeroDivisionError):
                return False
    # Keep track of how many individual responses have been provided
    individuals = 0
    # Keep track of how many pairs of responses should be generated
    pairs = 0
    for item in raw_dat.columns:
        # Create list of every collection of responses in a column
        v = list(raw_dat.loc[:, item])
        # Separate each response into a list of strings with no brackets
        w = [([] if pd.isnull(resp) else re.findall("\[(.*?)\]", resp)) for resp in v]
        # Simplify response strings, removing occurences of '+-'
        w = [[simplify_response(r) for r in resp] for resp in w]
        items[item]['resp_lists'] = w

        # Put all of the individual responses in a list and then organize them into pairs (x, y)
        # where the second value (y) is the number of times that response (x) occurs
        x = [r for r in [r for resps in w for r in resps] if validate(r, item)]
        items[item]['valid_resp_counts'] = Counter(x).most_common()

        # Add to number of total responses
        individuals += len(items[item]['valid_resp_counts'])
        # Calculate number of response pairs
        pairs += len(items[item]['valid_resp_counts']) * (len(items[item]['valid_resp_counts']) - 1) / 2

        items[item]['valid_resps'] = [resp for (resp, count) in items[item]['valid_resp_counts']]

    print(str(int(individuals)), "individual responses created.")
    print(str(int(pairs)), "response pairs should be created.")

# This function returns a list of every single valid responses by combining all values from the
# “valid_resps" key from all tasks in items.


def create_resp_list():
    ''' R: a list of all valid responses with parentheses stripped '''
    R = []
    for item in items:
        R = R + items[item]['valid_resps']
    return R

# Takes the data from items and uses it to populate a pandas DataFrame object. Concurrently populates
# the DataFrame with numbers for successive and total cooccurrence. Pandas is a library abbreviated as
# pd and a DataFrame is a two-dimensional tabular data structure.


def create_resp_data():
    ''' Create a data frame with one row per pair of valid responses for the same item
    with columns showing frequencies of co-occurrence and successive co-occurrence of the responses in the pair '''
    R = create_resp_list()
    arith_dat = pd.read_excel(input_data_filename, sheet_name=arith_knowledge_sheet, index_col=0)
    # first create matrices for co-occurrence and successive co-occurrence
    # (one row and one column per response)
    cooc_dat = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    succ_dat = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    # below and above median math fluency value
    for item in tqdm(items.values(), desc="Building data tables..."):
        for row, resps in enumerate(item['resp_lists']):
            if len(resps) > 1:
                for i in range(0, len(resps) - 1):
                    for j in range(i + 1, len(resps)):
                        r1 = simplify_response(resps[i])
                        r2 = simplify_response(resps[j])
                        if r1 in item['valid_resps'] and r2 in item['valid_resps']:
                            cooc_dat.loc[r1, r2] += 1
                            cooc_dat.loc[r2, r1] += 1
                            if j == i + 1:
                                succ_dat.loc[r1, r2] += 1
                                succ_dat.loc[r2, r1] += 1
    # now create a df as described in the docstring
    idx = []
    dat = []
    it = ['A', 'B', 'C', 'D', 'E']
    for value, item in enumerate(tqdm(items.values(), desc="Populating main dataframe...")):
        v = item['valid_resps']
        for i in range(0, len(v) - 1):
            for j in range(i, len(v)):
                r1 = v[i]
                r2 = v[j]
                pair = str(r1) + "," + str(r2)
                revr = str(r2) + "," + str(r1)
                if r1 != r2 and pair not in idx and revr not in idx:
                    idx.append(pair)
                    dat.append([it[value], r1, r2, cooc_dat.loc[r1, r2], succ_dat.loc[r1, r2]])

    resp_dat = pd.DataFrame(dat, index=idx, columns=['item', 'resp1', 'resp2', 'cooc_tot', 'cooc_suc'])

    print("Built base .csv file resp_dat.csv\n\n")
    return resp_dat


def create_detailed_resp_data(data):
    ''' Create a data frame with one row per pair of valid responses for the same item
    with columns showing frequencies of co-occurrence and successive co-occurrence of the responses in the pair '''
    R = create_resp_list()
    arith_dat = pd.read_excel(input_data_filename, sheet_name=arith_knowledge_sheet, index_col=0)
    mf_median = arith_dat['Math Fluency'].median()
    # first create matrices for co-occurrence and successive co-occurrence
    # (one row and one column per response)
    cooc_dat = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    succ_dat = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    # below and above median math fluency value
    cooc_tot_hi = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    cooc_suc_hi = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    cooc_tot_lo = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    cooc_suc_lo = pd.DataFrame(data=np.zeros((len(R), len(R)), dtype=int), index=R, columns=R)
    total = 0
    total2 = 0
    for item in tqdm(items.values(), desc="Calculating math fluency totals..."):
        for row, resps in enumerate(item['resp_lists']):
            if len(resps) > 1:
                for i in range(0, len(resps) - 1):
                    for j in range(i + 1, len(resps)):
                        r1 = simplify_response(resps[i])
                        r2 = simplify_response(resps[j])
                        if r1 in item['valid_resps'] and r2 in item['valid_resps']:
                            cooc_dat.loc[r1, r2] += 1
                            cooc_dat.loc[r2, r1] += 1
                            try:
                                if arith_dat['Math Fluency'][row] == mf_median:
                                    total += 1
                                else:
                                    total2 += 1
                                if arith_dat['Math Fluency'][row] > mf_median:
                                    cooc_tot_hi.loc[r1, r2] += 1
                                    cooc_tot_hi.loc[r2, r1] += 1
                                elif arith_dat['Math Fluency'][row] <= mf_median:
                                    cooc_tot_lo.loc[r1, r2] += 1
                                    cooc_tot_lo.loc[r2, r1] += 1
                                else: # Not sure if empty data will generate exception
                                    continue
                            except:
                                continue
                            if j == i + 1:
                                succ_dat.loc[r1, r2] += 1
                                succ_dat.loc[r2, r1] += 1
                                try:
                                    if arith_dat['Math Fluency'][row] >= mf_median:
                                        cooc_suc_hi.loc[r1, r2] += 1
                                        cooc_suc_hi.loc[r2, r1] += 1
                                    elif arith_dat['Math Fluency'][row] < mf_median:
                                        cooc_suc_lo.loc[r1, r2] += 1
                                        cooc_suc_lo.loc[r2, r1] += 1
                                    else:  # Not sure if empty data will generate exception
                                        continue
                                except:
                                    continue
    print("\nParticipants that matched the median Math Fluency score: ", total)
    print("Participants that did not match the median Math Fluency score: ", total2)
    # now create a df as described in the docstring
    idx = []
    dat = []
    for value, item in enumerate(tqdm(items.values(), desc="Merging dataframes...")):
        v = item['valid_resps']
        for i in range(0, len(v) - 1):
            for j in range(i, len(v)):
                r1 = v[i]
                r2 = v[j]
                pair = str(r1) + "," + str(r2)
                revr = str(r2) + "," + str(r1)
                if r1 != r2 and pair not in idx and revr not in idx:
                    idx.append(pair)
                    dat.append([cooc_tot_hi.loc[r1, r2], cooc_tot_lo.loc[r1, r2], cooc_suc_hi.loc[r1, r2],
                                cooc_suc_lo.loc[r1, r2]])

    details = pd.DataFrame(dat, index=idx, columns=['cooc_tot_hi', 'cooc_tot_lo', 'cooc_suc_hi', 'cooc_suc_lo'])

    resp_dat = pd.concat([data, details], axis=1)
    return resp_dat


# Defines the expression tree used across multiple properties. It is a fairly simple and
# implementation, tree is primarily defined as a system of nodes, which each have a left
# and right property pointing to another node. The top node represents the “tree.” These
# children do not both have to exist in every scenario. Subtraction is a unary operator
# that has a single child.

class BET:
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

    if "+-" in r:
        new_r = r.replace("+-", "-")
        r = new_r
    return r


# Implementation of an infix to postfix algorithm. Infix is the usual way that
# humans express an equation. Postfix has a number of advantages over infix for
# expressing algebraic formula, namely, that any formula can be expressed without
# parentheses.


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


'''tokenizes an infix expression, explained in previous function comment'''


def token_infix(infix):
    # https://www.regex101.com/
    number_or_symbol = re.compile('([/]?[-]?\d+|[^ 0-9])')
    postfix_list = (re.findall(number_or_symbol, infix))

    # Convert division (x/y) to x * inverse(y).
    for entry_index in range(0, len(postfix_list)):
        if "/" in postfix_list[entry_index]:
            if postfix_list[entry_index] == "/":
                del postfix_list[entry_index]
                # This means that there is a parentheses in front of the "/"
                parentheses_count = 0  # Account for nested parentheses
                for end_par in range(entry_index, len(postfix_list)):
                    if postfix_list[end_par] == "(":
                        parentheses_count = parentheses_count + 1
                    elif postfix_list[end_par] == ")":
                        parentheses_count = parentheses_count - 1
                        if parentheses_count == 0:
                            postfix_list.insert(end_par + 1, "*")
                            postfix_list.insert(end_par + 1, "inv")
            else:
                postfix_list[entry_index] = postfix_list[entry_index][1:]
                postfix_list.insert(entry_index + 1, '*')
                postfix_list.insert(entry_index + 1, "inv")
    return postfix_list


'''func for checking if character is an operator to be used by add_tree'''


def is_binary_operator(c):
    return c == '+' or c == '*'


'''func for checking if character is an operator to be used by add_tree'''


def is_operator(c):
    return c == '+' or c == '*' or c == "inv"


'''Returns the priority assigned to different operators as established by
PEMDAS, where ‘*’ and ‘inv’ have higher priority than ‘+’ and ‘-‘. These
terms are explained in the is_binary_operator(c) and is_operator(c) section.'''

def priority(c):
    if c == '+' or c == '-':
        return 0
    if c == '*' or c == 'inv':
        return 1
    else:
        return 2


'''Constructs the BET from the given infix expression, first tokenizes infix
expression, converts it into tokenized postfix expression, then builds the BET'''


def construct_tree(infix):
    # Convert subtraction operator "-" to "+-" so that subtraction-rooted
    # expressions now count as addition-rooted expressions.
    try:
        back = infix[1:len(infix)]
        new_back = back.replace("-", "+-1*")
        new_new_back = new_back.replace("++", "+")
        new_back = new_new_back.replace("*+-", "*-")
        new_new_back = new_back.replace("/+-", "/-")
        if infix[0] == "-":
            infix = "-1*" + new_new_back
        else:
            infix = infix[0] + new_new_back
    except:
        infix = infix
    postfix = infix_to_postfix({'+': 0, '-': 0, '*': 1, 'inv': 1}, token_infix(infix))
    stack = []
    # Traverse through every character of input expression
    for itr in range(0, len(postfix)):
        # If operand, simply push into stack
        if not is_operator(postfix[itr]):
            t = BET(postfix[itr])
            stack.append(t)
        # Operator
        else:
            if postfix[itr] != "inv":
                # Pop two top nodes
                t = BET(postfix[itr])
                t1 = stack.pop()
                t2 = stack.pop()

                # make them children
                t.right = t1
                t.left = t2

                # Add this subexpression to stack
                stack.append(t)
            else:
                # Pop one node
                t = BET(postfix[itr])
                t1 = stack.pop()

                # make them children
                t.left = t1

                # Add this to stack
                stack.append(t)

    # Only element will be the root of expression tree
    t = stack.pop()
    return t


'''Helper function that determines if a string contains a number.
Implemented using the isnumeric() built-in function but stripping
the possible negative sign first.'''


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


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                   Additive Commutativity                              #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

'''This feature analyzes pairs of responses (x, y) where both x and y contain
addition or subtraction operators. It returns true when the addends of one
operation in entry x can be rearranged in order to exactly re-create the
other entry y.'''


def comm_add(exprA, exprB):
    if O(exprA) is None or O(exprB) is None:
        return O(exprA) == O(exprB)
    elif O(exprA).value != O(exprB).value:
        return False
    elif sorted(add_children(exprA)) == sorted(add_children(exprB)):
        return True
    else:
        return comm_add(L(exprA), L(exprB)) and comm_add(R(exprA), R(exprB))


'''Determines the children of a given node, outputting these children in a list.
Must account for the fact that there may not always be two children, or that
there can be no children at all in the case of leaf analysis.'''


def add_children(expr):
    # If the expression is an addition sign
    if O(expr).value == "+":
        left = add_children(L(expr))
        right = add_children(R(expr))
        # Return the sorted list of children
        if right is not None:
            output = (left + right)
        else:
            output = left
        return output
    else:
        # If the expression is not an addition sign
        # But it is an operator
        if is_binary_operator(O(expr).value):
            left = ""
            # Test if its left child is an operator.
            if is_binary_operator(L(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(L(expr).value) < priority(O(expr).value):
                    string = "("
                    l = add_children(L(expr))
                    if isinstance(l, list):
                        for entry in l:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            string = string + entry + "+"
                        string = string[:-1]
                    else:
                        string = string + l
                    string = string + ")"
                    left = string
                else:
                    left = add_children(L(expr))
            else:
                left = add_children(L(expr))

            # Account for the fact that right child might be none in the case of division
            # or the fact that a string (in the case of an integer) does not have the
            # .value attribute.

            if is_binary_operator(R(expr).value):
                # Test if the child operator has a greater priority than the parent.
                if priority(R(expr).value) < priority(O(expr).value):
                    value = "("
                    r = add_children(R(expr))
                    if isinstance(r, list):
                        for entry in r:
                            # Ensure that added list items are once again displayed
                            # with a plus sign.
                            value = value + entry + "+"
                        value = value[:-1]
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

        elif O(expr).value == "inv":
            l = add_children(L(expr))
            string = ""
            if isinstance(l, list):
                for entry in l:
                    # Ensure that added list items are once again displayed
                    # with a plus sign.
                    string = string + entry + "+"
                string = string[:-1]
            else:
                string = l
            string = "inv(" + string + "))"
            return [string]

        # If it is an integer...
        else:
            return [O(expr).value]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                             Multiplicative Commutativity                              #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

'''This feature analyzes pairs of responses (x, y) where both x and y contain
multiplication or division operators. It returns true when the addends in one
entry (x) can be rearranged in order to exactly re-create the other entry (y).'''


def comm_mul(exprA, exprB):
    if O(exprA) is None or O(exprB) is None:
        return exprA == exprB
    elif O(exprA).value != O(exprB).value:
        return False
    elif sorted(mul_children(exprA)) == sorted(mul_children(exprB)):
        return True
    else:
        return comm_mul(L(exprA), L(exprB)) and comm_mul(R(exprA), R(exprB))


'''Determines the children of a given node, outputting these children in a
list. Must account for the fact that there may not always be two children,
or that there can be no children at all in the case of leaf analysis.'''


def mul_children(expr):
    if O(expr) is None:
        return ""
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
        if is_binary_operator(O(expr).value):
            left = ""
            # Test if its left child is an operator.
            if is_binary_operator(L(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(L(expr).value) > priority(O(expr).value):
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
            if is_binary_operator(R(expr).value):
                # Test if the child operator has a lower priority than the parent.
                if priority(R(expr).value) > priority(O(expr).value):
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
        # If it is inversion...
        elif O(expr).value == "inv":
            l = mul_children(L(expr))
            string = ""
            if isinstance(l, list):
                for entry in l:
                    # Ensure that added list items are once again displayed
                    # with a plus sign.
                    string = string + entry + "+"
                string = string[:-1]
            else:
                string = l
            string = "inv(" + string + "))"
            return [string]
        # If it is an integer...
        else:
            return [O(expr).value]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                    Decomposition                                      #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


def string_to_list(str):
    out = []
    str = str[0] + str[1:].replace("-", "+-")
    value = ""
    parentheses = 0

    for i, char in enumerate(str):
        if char in "*/+" and parentheses == 0:
            prev = i - 1
            if str[prev] == "+":
                if value != "":
                    out.append(value)
            else:
                if value != "":
                    out.append(value)
                out.append(char)
            value = ""
        elif char == "(":
            if value != "":
                if value != "-":
                    out.append(value)
                else:
                    out[-1] = "-"
                    value = ""
            parentheses += 1
            start = i + 1
            for o, val in enumerate(str[start:]):
                nested_parentheses = 1
                if val == "(":
                    nested_parentheses += 1
                elif val == ")":
                    nested_parentheses -= 1
                if nested_parentheses == 0:
                    end = start + o
                    out.append(string_to_list(str[start:end]))
                    break
            value = ""
        elif char == ")":
            parentheses -= 1
            continue
        else:
            if parentheses == 0:
                value += char
    if value != "":
        out.append(value)
    return out


def list_to_string(lst):
    out = ""
    if lst == []:
        return "0"
    else:
        for entry in lst:
            if isinstance(entry, list):
                out += "("
                for nested in entry:
                    out += nested
                out += ")"
            else:
                out += entry
        return out


def list_length(string):
    # Find lengths
    size = 0
    for entry in string:
        if isinstance(entry, list):
            for nested in entry:
                size += 1
        else:
            size += 1
    return size


def deco_mul(str1, str2):
    # Split expressions into A1, A2, A3 and B1, B2, B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False # Manually split A3/B3 indicator
        skip = False
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list): # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False and skip is False:
            # Means that all of A is accounted for
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 < 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 < 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[:len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1)-len(B3))]

        A3.reverse()
        B3.reverse()

        if A2 == [] and B2 == ['1', '*']:
            return False
        elif A2 == [] and B2 == ['*', '1']:
            return False
        elif A2 == [] and B2 == ['/', '1']:
            return False
        elif A2 == [] and B2 == ['1', '/']:
            return False

        # The 'A' set has already been established as the result;
        # B is the decomposition of A. If A is not one value, False.
        if len(A2) > 1:
            return False

        # If the parse has allowed A2 to contain an operator, return
        # False.
        if '+' in A2 or '-' in A2 or '*' in A2 or '/' in A2:
            return False

        # If the parse has allowed B2 to be just a single operand,
        # return False.
        if '*' not in B2 and '/' not in B2:
            return False

        if B2 == ['*'] or B2 == ['/']:
            return False

        A2_str = list_to_string(A2)
        B2_str = list_to_string(B2)

        A2_str.replace("/+-", "/-")
        B2_str.replace("*+-", "*-")

        # No + allowed in multiplicative decomposition.
        if '+' in B2_str:
            return False

        # Not allowing both * and / in valid multiplicative decomposition.
        if '*' in B2_str and '/' in B2_str:
            return False

        # If B2 ends/begins with a / or * operator, complete the equation
        if B2_str[0] in "*/":
            B2_str = B1[-1] + B2_str
        if B2_str[-1] in "*/":
            B2_str = B2_str + B3[0]
        if A2_str == B2_str == "0":
            return False
        if pd.eval(A2_str) == pd.eval(B2_str) != 0:
            return True
        else:
            if A2_str == "0":
                if len(A1) == 1:
                    if pd.eval(A1[0]) == pd.eval(B2_str):
                        return True
                elif len(A3) == 1:
                    if pd.eval(A3[0]) == pd.eval(B2_str):
                        return True
            return False


def deco_add(str1, str2):
    # Split expressions into A1 + A2 + A3 and B1 + B2 + B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False # Manually split A3/B3 indicator
        skip = False
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list): # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False and skip is False:
            # This means that A ended, so whatever is left on B must equal 0
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 <= 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 <= 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[: len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1)-len(B3))]

        A3.reverse()
        B3.reverse()
        # The 'A' set has already been established as the result;
        # B is the decompositoin of A. If A is not one value, False.

        # If the parse has allowed A2 to be just a single operator,
        # return False.
        if '+' in A2 or '-' in A2 or '*' in A2 or '/' in A2:
            return False

        # If the parse has allowed B2 to be just a single operand,
        # return False.
        if '+' not in B2 and '-' not in B2:
            return False

        A2_str = list_to_string(A2)
        A2_str = A2_str.replace("+-", '-')
        B2_str = list_to_string(B2)
        B2_str = B2_str.replace("+-", '-')
        # No * or / allowed in additive decomposition.
        if '*' in B2_str or '/' in B2_str:
            return False

        if B2_str == '*' or B2_str == '/':
            return False

        # Not allowing both + and - in valid additive decomposition.
        if '+' in B2_str and '-' in B2_str:
            return False

        # If B2 ends with a hanging operator, the entire thing is wrong.
        # This could be wrong, but, it doesn't seem wrong.
        if B2_str[0] in "+-*/" or B2_str[-1] in "+-*/":
            return False

        if A2_str == B2_str == "0":
            return False
        if pd.eval(A2_str) == pd.eval(B2_str) != 0:
            return True
        else:
            if A2_str == "0":
                if len(A1) == 1:
                    if pd.eval(A1[-1]) == pd.eval(B2_str):
                        return True
                elif len(A3) == 1:
                    if pd.eval(A3[0]) == pd.eval(B2_str):
                        return True
            return False


# 'Pure' multiplicative decomposition examines cases that only contain
# the multiplication symbol. From an implementation standpoint, it
# takes the code for multiplicative decomposition and excludes cases
# that contain a division symbol.
def deco_pure_mul(str1, str2):

    # Split expressions into A1, A2, A3 and B1, B2, B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False # Manually split A3/B3 indicator
        skip = False
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list): # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False and skip is False:
            # Means that all of A is accounted for
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 < 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 < 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[:len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1)-len(B3))]

        A3.reverse()
        B3.reverse()

        if A2 == [] and B2 == ['1', '*']:
            return False
        elif A2 == [] and B2 == ['*', '1']:
            return False
        elif A2 == [] and B2 == ['/', '1']:
            return False
        elif A2 == [] and B2 == ['1', '/']:
            return False

        # The 'A' set has already been established as the result;
        # B is the decomposition of A. If A is not one value, False.
        if len(A2) > 1:
            return False

        # If the parse has allowed A2 to contain an operator, return
        # False.
        if '+' in A2 or '-' in A2 or '*' in A2 or '/' in A2:
            return False

        # If the parse has allowed B2 to be just a single operand,
        # return False.
        if '*' not in B2 and '/' not in B2:
            return False

        if B2 == ['*'] or B2 == ['/']:
            return False

        A2_str = list_to_string(A2)
        B2_str = list_to_string(B2)

        A2_str.replace("/+-", "/-")
        B2_str.replace("*+-", "*-")

        # No + or / allowed in pure multiplicative decomposition.
        if '+' in B2_str or '/' in B2_str:
            return False

        # If B2 ends/begins with a * operator, complete the equation
        if B2_str[0] == '*':
            B2_str = B1[-1] + B2_str
        if B2_str[-1] == '*':
            B2_str = B2_str + B3[0]
        if A2_str == B2_str == "0":
            return False
        if pd.eval(A2_str) == pd.eval(B2_str) != 0:
            return True
        else:
            if A2_str == "0":
                if len(A1) == 1:
                    if pd.eval(A1[0]) == pd.eval(B2_str):
                        return True
                elif len(A3) == 1:
                    if pd.eval(A3[0]) == pd.eval(B2_str):
                        return True
            return False


# 'Pure' additive decomposition examines cases that only contain
# the additive symbol. From an implementation standpoint, it
# takes the code for additive decomposition and excludes cases
# that contain a subtraction symbol.
def deco_pure_add(str1, str2):
    # Split expressions into A1 + A2 + A3 and B1 + B2 + B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False # Manually split A3/B3 indicator
        skip = False
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list): # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False and skip is False:
            # This means that A ended, so whatever is left on B must equal 0
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 <= 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 <= 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[: len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1)-len(B3))]

        A3.reverse()
        B3.reverse()
        # The 'A' set has already been established as the result;
        # B is the decompositoin of A. If A is not one value, False.

        # If the parse has allowed A2 to be just a single operator,
        # return False.
        if '+' in A2 or '-' in A2 or '*' in A2 or '/' in A2:
            return False

        # If the parse has allowed B2 to be just a single operand,
        # return False.
        if '+' not in B2 and '-' not in B2:
            return False

        A2_str = list_to_string(A2)
        A2_str = A2_str.replace("+-", '-')
        B2_str = list_to_string(B2)
        B2_str = B2_str.replace("+-", '-')
        # No * or / or - allowed in pure additive decomposition.
        if '*' in B2_str or '/' in B2_str or '-' in B2_str:
            return False

        if B2_str == '+':
            return False

        # If B2 ends/begins with a + operator, complete the equation
        if B2_str[0] == '+':
            B2_str = B1[-1] + B2_str
        if B2_str[-1] == '+':
            B2_str = B2_str + B3[0]
        if A2_str == B2_str == "0":
            return False
        if pd.eval(A2_str) == pd.eval(B2_str) != 0:
            return True
        else:
            if A2_str == "0":
                if len(A1) == 1:
                    if pd.eval(A1[-1]) == pd.eval(B2_str):
                        return True
                elif len(A3) == 1:
                    if pd.eval(A3[0]) == pd.eval(B2_str):
                        return True
            return False


def deco_and_iden_mul(str1, str2):
    # Split expressions into A1, A2, A3 and B1, B2, B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False # Manually split A3/B3 indicator
        skip = False
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list): # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i+1:]
                A3 = A[i+1:]
                skip = True
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False and skip is False:
            # Means that all of A is accounted for
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 < 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 < 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[:len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1)-len(B3))]

        A3.reverse()
        B3.reverse()

        if A2 == [] and B2 == ['1', '*']:
            return True
        elif A2 == [] and B2 == ['*', '1']:
            return True
        elif A2 == [] and B2 == ['/', '1']:
            return True
        elif A2 == [] and B2 == ['1', '/']:
            return True

        # The 'A' set has already been established as the result;
        # B is the decomposition of A. If A is not one value, False.
        if len(A2) > 1:
            return False

        # If the parse has allowed A2 to be just a single operator,
        # return False.
        if '+' in A2 or '-' in A2 or '*' in A2 or '/' in A2:
            return False

        # If the parse has allowed B2 to be just a single operand,
        # return False.
        if '*' not in B2 and '/' not in B2:
            return False

        if B2 == ['*'] or B2 == ['/']:
            return False

        A2_str = list_to_string(A2)
        B2_str = list_to_string(B2)

        A2_str.replace("/+-", "/-")
        B2_str.replace("*+-", "*-")

        # No + allowed in additive decomposition.
        if '+' in B2_str:
            return False

        # Not allowing both * and / in valid additive decomposition.
        if '*' in B2_str and '/' in B2_str:
            return False

        # If it ends/begins with a / or * operator, complete the equation
        if B2_str[0] in "*/":
            B2_str = B1[-1] + B2_str
        if B2_str[-1] in "*/":
            B2_str = B2_str + B3[0]
        if A2_str == B2_str == "0":
            return False
        if pd.eval(A2_str) == pd.eval(B2_str) != 0:
            return True
        else:
            if A2_str == "0":
                if len(A1) == 1:
                    if pd.eval(A1[0]) == pd.eval(B2_str):
                        return True
                elif len(A3) == 1:
                    if pd.eval(A3[0]) == pd.eval(B2_str):
                        return True
            return False


def identity_mul(str1, str2):
    # Split expressions into A1, A2, A3 and B1, B2, B3.
    # A1 must match B1.
    # B2 must evaluate to equal A2.
    # A3 must match B3.
    # String B is always the decomposition of string A.

    first = string_to_list(str1)
    second = string_to_list(str2)

    A1, A2, A2_1, A3, B1, B2, B2_1, B3 = [], [], [], [], [], [], [], []
    A, B, rev_A, rev_B = [], [], [], []

    # Evaluate A and B. If they are not equal, return false
    if pd.eval(str1) != pd.eval(str2):
        return False
    else:
        if len(str1) >= len(str2):
            B = first
            A = second
            rev_B = list(reversed(first))
            rev_A = list(reversed(second))
        else:
            B = second
            A = first
            rev_B = list(reversed(second))
            rev_A = list(reversed(first))

        # Determine A1, B1, the longest sub-lists at the beginning
        # of first, second such that A1==B1 (A1/B1 can be empty).
        find3 = False  # Manually split A3/B3 indicator
        for i, val in enumerate(A):
            if type(B[i]) == type(val):
                if val == B[i]:
                    A1.append(val)
                    B1.append(val)
                else:
                    A2_1 = A[i:]
                    B2_1 = B[i:]
                    find3 = True
                    break
            elif isinstance(B[i], list):
                B2 = B[i]
                A2 = val
                B3 = B[i + 1:]
                A3 = A[i + 1:]
                if A3 != B3:
                    return False
                break
            elif isinstance(val, list):  # Should never happen
                B2 = B[i]
                A2 = A[i]
                B3 = B[i + 1:]
                A3 = A[i + 1:]
                if A3 != B3:
                    return False
                break

        if B2_1 == [] and find3 is False:
            B2 = B[len(B1):]

        # Determine A3, B3, the longest sub-lists at the end of
        # first, second such that A3==B3 (A3/B3 can be empty).
        # Subtract their lengths from the length of A2_1/B2_1,
        # which will give the length of A2 and B2.
        if find3:
            for i, val in enumerate(rev_A):
                if val == rev_B[i]:
                    A3.append(val)
                    B3.append(val)
                else:
                    len_A2 = len(A2_1) - i
                    len_B2 = len(B2_1) - i
                    if len_A2 < 0:
                        A2 = ['0']
                    else:
                        A2 = A2_1[: len_A2]
                    if len_B2 < 0:
                        B2 = ['0']
                    else:
                        B2 = B2_1[:len_B2]
                    break
            if B2 == []:
                B2 = B2_1[:(len(B2_1) - len(B3))]

        if A2 == [] and B2 == ['1', '*']:
            return True
        elif A2 == [] and B2 == ['*', '1']:
            return True
        elif A2 == [] and B2 == ['/', '1']:
            return True
        elif A2 == [] and B2 == ['1', '/']:
            return True
        else:
            return False


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                        Related                                        #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


def mul_rep_add(exprA, exprB):
    if exprA is None or exprB is None:
        return exprA == exprB
    elif '+' not in exprA and '+' not in exprB:
        return False
    elif '*' not in exprA and '*' not in exprB:
        return False
    elif exprA == exprB:
        return False
    else:
        num_mul_A = re.findall('\\*', exprA)
        num_mul_B = re.findall('\\*', exprB)
        # Set A to always be the expression with more multiplication symbols
        if len(num_mul_A) < len(num_mul_B):
            A_BET = construct_tree(simplify_response(exprB))
            exprC = exprA
            exprA = simplify_response(exprB)
            exprB = simplify_response(exprC)
        elif len(num_mul_A) > len(num_mul_B):
            A_BET = construct_tree(simplify_response(exprA))
        else:
            # If they have the same number of multiplication symbols...
            return False
        A_parsed = add_children(A_BET)
        integers = []
        possibilities = {}
        for entry in A_parsed:
            try:
                values = entry.split('*')
                if len(values) == 2 and is_numeric(values[0]) and is_numeric(values[1]):
                    # There was only one multiplication symbol in the subexpression
                    if int(values[0]) > 0:
                        try:
                            if values[1] not in possibilities[values[0]]:
                                possibilities[values[0]].append(values[1])
                        except:
                            possibilities[values[0]] = [values[1]]
                            integers.append(values[0])
                    if int(values[1]) > 0:
                        try:
                            if values[0] not in possibilities[values[1]]:
                                possibilities[values[1]].append(values[0])
                        except:
                            possibilities[values[1]] = [values[0]]
                            integers.append(values[1])
            except:
                # Looking at an added value; not important
                continue

        for integer in integers:
            for o in possibilities[integer]:
                # Create the substring that could exist in B
                substr = ""
                if integer[0] != '-':
                    # if its not a negative number
                    for i in range(0, int(o)):
                        substr += integer
                        substr += '+'
                    substr = substr[:-1]
                else:
                    for i in range(0, int(o)):
                        substr += integer

                positions = find_occurrences(exprB, substr)
                for pos in positions:
                    # Create test string to compare to original string A
                    exprC = exprB[:pos] + integer + '*' + o + exprB[pos+len(substr):]
                    if exprA == exprC:
                        return True
                    exprC = exprB[:pos] + o + '*' + integer + exprB[pos + len(substr):]
                    if exprA == exprC:
                        return True
                    # Parentheses check
                    if '(' in exprB:
                        exprC = exprB[:pos] + '(' + o + '*' + integer + ')' + exprB[pos + len(substr):]
                        if exprA == exprC:
                            return True
                        if exprB[pos-1] == '(' and exprB[pos + len(substr)] == ')':
                            exprC = exprB[:pos-1] + o + '*' + integer + exprB[1+ pos + len(substr):]
                            if exprA == exprC:
                                return True
                        exprC = exprB[:pos] + '(' + integer + '*' + o + ')' + exprB[pos + len(substr):]
                        if exprA == exprC:
                            return True
                        if exprB[pos - 1] == '(' and exprB[pos + len(substr)] == ')':
                            exprC = exprB[:pos - 1] + integer + '*' + o + exprB[1 + pos + len(substr):]
                            if exprA == exprC:
                                return True

    return False


def mul_rep_add_with_id(exprA, exprB):
    if exprA is None or exprB is None:
        return exprA == exprB
    elif '+' not in exprA and '+' not in exprB:
        return False
    elif '*' not in exprA and '*' not in exprB:
        return False
    elif exprA == exprB:
        return False
    else:
        num_mul_A = re.findall('\\*', exprA)
        num_mul_B = re.findall('\\*', exprB)
        # Set A to always be the expression with more multiplication symbols
        if len(num_mul_A) < len(num_mul_B):
            A_BET = construct_tree(simplify_response(exprB))
            exprC = exprA
            exprA = simplify_response(exprB)
            exprB = simplify_response(exprC)
        elif len(num_mul_A) > len(num_mul_B):
            A_BET = construct_tree(simplify_response(exprA))
        else:
            # If they have the same number of multiplication symbols...
            return False
        A_parsed = add_children(A_BET)
        integers = []
        possibilities = {}
        for entry in A_parsed:
            try:
                values = entry.split('*')
                if len(values) == 2 and is_numeric(values[0]) and is_numeric(values[1]) and values[0] != '1' and values[1] != '1':
                    # There was only one multiplication symbol in the subexpression
                    if int(values[0]) > 0:
                        try:
                            if values[1] not in possibilities[values[0]]:
                                possibilities[values[0]].append(values[1])
                        except:
                            possibilities[values[0]] = [values[1]]
                            integers.append(values[0])
                    if int(values[1]) > 0:
                        try:
                            if values[0] not in possibilities[values[1]]:
                                possibilities[values[1]].append(values[0])
                        except:
                            possibilities[values[1]] = [values[0]]
                            integers.append(values[1])
            except:
                # Looking at an added value; not important
                continue

        for integer in integers:
            for o in possibilities[integer]:
                # Create the substring that could exist in B
                substr = ""
                if integer[0] != '-':
                    # if its not a negative number
                    for i in range(0, int(o)):
                        substr += integer
                        substr += '+'
                    substr = substr[:-1]
                else:
                    for i in range(0, int(o)):
                        substr += integer

                positions = find_occurrences(exprB, substr)
                for pos in positions:
                    # Create test string to compare to original string A
                    exprC = exprB[:pos] + integer + '*' + o + exprB[pos+len(substr):]
                    if exprA == exprC:
                        return True
                    exprC = exprB[:pos] + o + '*' + integer + exprB[pos + len(substr):]
                    if exprA == exprC:
                        return True
                    # Parentheses check
                    if '(' in exprB:
                        exprC = exprB[:pos] + '(' + o + '*' + integer + ')' + exprB[pos + len(substr):]
                        if exprA == exprC:
                            return True
                        if exprB[pos-1] == '(' and exprB[pos + len(substr)] == ')':
                            exprC = exprB[:pos-1] + o + '*' + integer + exprB[1+ pos + len(substr):]
                            if exprA == exprC:
                                return True
                        exprC = exprB[:pos] + '(' + integer + '*' + o + ')' + exprB[pos + len(substr):]
                        if exprA == exprC:
                            return True
                        if exprB[pos - 1] == '(' and exprB[pos + len(substr)] == ')':
                            exprC = exprB[:pos - 1] + integer + '*' + o + exprB[1 + pos + len(substr):]
                            if exprA == exprC:
                                return True

    return False


def find_occurrences(string, substring):
    lst = []
    start = 0

    while start < len(string):
        pos = string.find(substring, start)

        if pos != -1:
            # If a substring is present, move 'start' to
            # the next position from start of the substring
            start = pos + 1

            # add to list
            lst.append(pos)
        else:
            # If no further substring is present
            break

    return lst


def find_sub_list(sl,l):
    results = []
    sll = len(sl)
    for ind in (i for i, e in enumerate(l) if e == sl[0]):
        if l[ind : ind + sll] == sl:
            results.append((ind, ind+sll-1))

    return results


def generate_resp_dat():
    if exists("resp_dat.csv"):
        print("\n\nFound file resp_dat.csv.")
        resp_dat = pd.read_csv("resp_dat.csv", index_col=0)
    else:
        print("\n\nUnable to find base file resp_dat.csv. Building a new file (this could take a second):")
        resp_dat = create_resp_data()
        resp_dat.to_csv("resp_dat.csv")


def add_properties(resp_dat):
    resp_data = resp_dat
    # adding features for additive commutativity and multiplicative commutativity
    resp_data = add_feature(resp_data, "add_comm", comm_add)
    resp_data = add_feature(resp_data, "mul_comm", comm_mul)

    # adding features for additive decomposition and multiplicative decomposition
    resp_data = add_feature(resp_data, "add_decomp", deco_add)
    resp_data = add_feature(resp_data, "mul_decomp", deco_mul)
    resp_data = add_feature(resp_data, "add_decomp_non_neg", deco_pure_add)
    resp_data = add_feature(resp_data, "mul_decomp_no_div", deco_pure_mul)
    resp_data = add_feature(resp_data, "identity", identity_mul)

    # adding feature for multiplication as repeated addition
    resp_data = add_feature(resp_data, "mul_rep_add", mul_rep_add)
    resp_data = add_feature(resp_data, "mul_rep_add_with_id", mul_rep_add_with_id)

    return resp_data


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                     Add Feature                                       #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


def add_feature(resp_dat, feature_name, feature_func):
    ''' Add a column to resp_dat to indicate presence or absence of a given feature for each pair of responses '''
    vec = [None for i in resp_dat.index]
    if feature_name == "add_comm" or feature_name == "mul_comm":
        for i in tqdm(range(0, len(resp_dat.index)), desc = feature_name + "\t"):
            idx = resp_dat.index[i]
            # Run the function with the two given responses
            try:
                vec[i] = feature_func(construct_tree(simplify_response(resp_dat.loc[idx, 'resp1'])),
                                      construct_tree(simplify_response(resp_dat.loc[idx, 'resp2'])))
            except:
                print("Error in add_feature: " + feature_name + "; " + idx)
                break
    else:
        for i in tqdm(range(0, len(resp_dat.index)), desc = feature_name + "\t"):
            idx = resp_dat.index[i]
            try:
                vec[i] = feature_func((resp_dat.loc[idx, 'resp1']), (resp_dat.loc[idx, 'resp2']))
            except:
                print("Error in add_feature: " + feature_name + "; " + idx)
                break

    resp_dat[feature_name] = vec
    return resp_dat


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
#                                                                                       #
#                                         Main                                          #
#                                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


if __name__ == '__main__':
    ''' Variables to load data (used throughout) '''
    # The name of the excel file (must be .xlsx) that contains the response data
    # (required) and the participants' math fluency scores:
    input_data_filename = "ANK_raw_data.xlsx"

    # The name of the sheet that contains participants' response data
    raw_data_sheet = "Sheet1"

    # The name of the sheet that contains participants' math fluency scores
    arith_knowledge_sheet = "Arith knowledge"

    # The individual tests participants responded to
    items = {
        'A': {'opts': [1, 2, 3, 4], 'targ': 6, 'type': 'dense'},
        'B': {'opts': [2, 4, 8, 12, 32], 'targ': 16, 'type': 'dense'},
        'C': {'opts': [1, 2, 3, 5, 30], 'targ': 59, 'type': 'sparse'},
        'D': {'opts': [2, 4, 6, 16, 24], 'targ': 12, 'type': 'dense'},
        'E': {'opts': [3, 5, 30, 120, 180], 'targ': 12, 'type': 'sparse'}
    }

    # Load raw data
    raw_dat = pd.read_excel(input_data_filename, sheet_name=raw_data_sheet, index_col=0)

    add_resp_info_to_items()
    R2 = create_resp_list()

    '''1.	Takes raw data as input; outputs a Pandas dataframe containing 
    all valid response pairs for the same item; this dataframe would include 
    the “item”, “resp1”, and “resp2” columns only.'''

    if exists("resp_dat.csv"):
        print("\n\nFound file resp_dat.csv.")
        data = pd.read_csv("resp_dat.csv", index_col=0)
    else:
        print("\n\nUnable to find base file resp_dat.csv. Building a new file (this could take a second):")
        data = create_resp_data()

    '''2.	Take the dataframe from #1 or #3 as input; adds columns for the
    various mathematical relations (e.g., “add_comm”, “mul_comm”, etc.) and
    returns the resulting datafram.'''

    data = add_properties(data)

    '''3.	Takes the dataframe from #1 or #2 as input; adds columns for the
    co-occurrence frequencies (i.e., cooc_tot, cooc_suc, cooc_tot_hi,
    cooc_tot_lo, cooc_suc_hi, cooc_suc_lo) and returns the resulting dataframe'''

    data = create_detailed_resp_data(data)

    '''4.	Takes the dataframe resulting from 1, 2 , or 3 as input and saves
    it as a .csv file '''

    data.to_csv("resp_dat_with_features.csv")

    '''5.	Loads a .csv file resulting from 1, 2, or 3 and converts it to a
    Pandas dataframe'''

    data = pd.read_csv("resp_dat_with_features.csv", index_col=0)

