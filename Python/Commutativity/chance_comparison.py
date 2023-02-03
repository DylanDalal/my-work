import pandas as pd
import random
from tqdm import tqdm

# Notes from the programmer are expressed through comments; instructions on algorithm are given through docstrings

# Repeat the following N (e.g., N=500) times:

# i. Randomly permute the participant’s responses WITHIN EACH ITEM (in other words, the responses for item A are
# not mixed up with those for item B, for example)

# ii. For each relation, calculation the proportion of “number of relation-present successive pairs” to “total number
# of successive pairs” in the permuted data

# For each relation, average the proportions obtained from the N random iterations, yielding the proportions expected
# by chance

# Thus, for each participant, we should end up with 10 numbers:

# i. 5 proportions, one for each relation, indicating the true proportion of relation-present pairs to total pairs

# ii. 5 more proportions, one for each relation, indicating the expected-by-chance proportion of relation-present
# pairs to total pairs

# Save the output of the above in a .csv file with one row and 10 columns for each participant

# Import csvs for analysis
participant_dat = pd.read_excel("ANK_raw_data.xlsx", sheet_name="Sheet1")

processed_dat = pd.read_csv("resp_dat_with_features.csv")

vals = dict(enumerate(processed_dat.values))

val_list = processed_dat[processed_dat.columns[0]].values.tolist()
indices = {}
for index, num in enumerate(val_list):
    indices[num] = index

columns = {}
for index, num in enumerate(processed_dat.columns):
    columns[num] = index

relations = ['add_comm', 'mul_comm', 'add_decomp', 'mul_decomp', 'mul_rep_add']
items = ['A', 'B', 'C', 'D', 'E']

''' For each participant
    For each of the five relations (add_comm, mul_comm, …)
    i. Determine the proportion of “number of relation-present successive pairs” to “total number of successive
    pairs" '''

idx = []
dat = []


def related(resp1, resp2):
    # The first column doesn't have a title, so we have to get the location of the value equal to pair
    # located in the name (empty) of the first column (but I can't just write '' or something)
    pair_ = resp1 + ',' + resp2
    try:
        value = vals[indices[pair_]]
    except KeyError:
        try:
            pair_ = resp2 + ',' + resp1
            value = vals[indices[pair_]]
        except KeyError:
            return "False"
    # Since we have a single row, get first row value at column 'relation';
    # returns numpy.bool so convert to str to evaluate
    return str(value[columns[relation]])


if __name__ == '__main__':
    for index, row in tqdm(participant_dat.iterrows(), total=participant_dat.shape[0]):
        proportions = []
        for relation in relations:
            averages = []
            # Participant values:
            resp_total = 0
            resp_related = 0
            # Random values:
            r_resp_related = 0
            for item in items:
                try:
                    responses = row[item].strip('][').split('][')
                # Some participants did not answer all items so they throw an AttributeError when parsing item's response
                except AttributeError:
                    continue
                ''' A successive pair is defined as two valid responses that were generated in immediate succession
                    for the same item (e.g., for item A) '''
                for i in range(1, len(responses)):
                    ''' A relation-present successive pair is a successive pair that has the relation in question,
                    which can be determined by lookup '''
                    '''The two numbers mentioned in (i) are summed over all five items, but pairs can only be successive
                    if the two items in the pair were generated for the same item'''
                    resp_total += 1
                    if related(responses[i - 1], responses[i]) == "True":
                        resp_related += 1
                '''Repeat the following N (e.g., N=500) times'''
                N = 2000

                resp_set = []
                for o in range(0, N):
                    '''Randomly permute the participant’s responses WITHIN EACH ITEM'''
                    # shuffle() randomizes the original list, modifying it directly; create a copy
                    copy = responses.copy()
                    random.shuffle(copy)

                    '''For each relation, calculate the proportion of “number of relation-present successive pairs”
                    to “total number of successive pairs” in the permuted data'''
                    r_resp_rel = 0
                    for i in range(1, len(copy)):
                        pair = copy[i - 1] + ',' + copy[i]
                        if related(copy[i - 1], copy[i]) == "True":
                            r_resp_rel += 1
                    resp_set.append(r_resp_rel / len(copy))

                averages.append(sum(resp_set) / len(resp_set))

            participant_related = resp_related / resp_total
            randomly_related = sum(averages) / len(averages)
            proportions.extend([participant_related, randomly_related])

        # End of relation
        idx.append(index)
        dat.append(proportions)

    resp_dat = pd.DataFrame(dat, index=idx, columns=['add_comm', 'add_comm_b', 'mul_comm', 'mul_comm_b', 'add_decomp',
                                                     'add_decomp_b', 'mul_decomp', 'mul_decomp_b', 'mul_rep_add',
                                                     'mul_rep_add_b'])

    resp_dat.to_csv("chance_comparison.csv")
