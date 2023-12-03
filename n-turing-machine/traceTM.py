import sys
import collections
def parse_input():
    nta = {
    'name': '',
    'states': '',
    'alphabet': '',
    'tape': '',
    'start': '',
    'accept': '',
    'reject': '',
    'transitions': []
    }
    sections, input_file =[], "contains.csv"
    opened_file = open(input_file, 'r')
    for line in opened_file:
        sections.append([x for x in line.strip().split(',') if x])
    nta['name']= sections[0]
    nta['states']= sections[1]
    nta['alphabet']= sections[2]
    nta['tape']= sections[3]
    nta['start']= sections[4][0]
    nta['accept']= sections[5]
    nta['reject']= sections[6]
    nta['transitions'] = sections[7:]
    return nta
def decompose_transition(nta):
    dictionary = collections.defaultdict(list)
    for i, state in enumerate(nta['transitions']):
        size = i
    if len(state[0])==2 and state[0] in nta['states']:
        dictionary[state[0]].append(state[1:])
    return dictionary
def make_tree(nta, string, states_map):
    #Initialize the tree by including the root node in level 0
    tree = [[[nta['start'],-1,-1, string, 0]]]
    depth = -1
    while depth < 15:
        # Keep track of tree height
        depth +=1
        current_level = []
        next_node = 'na'
        for track_pindex, state in enumerate(tree[-1]): #Reference all of nodes in last level
            node, pheight, pindex, string, strindex = state

            for child in states_map[node]:
                if strindex >= len(string):
                    string += '_'
                if child[0]== string[strindex]: #Match
#Format String: child[2] refers to the replacing character
                    temp= string
                    string = list(string)
                    string[strindex] = child[2] if len(child) >= 3 else string[strindex] #Case where there are no replacement variable
                    string = ''.join(string)
                    #Format Direction:
                    direction = 1 if len(child) >= 3 and child[3]=='R' else -1
                    #child[3] is either L or R
                    #Get Current Node:
                    next_node = child[1]
                    #Populating Level
                    current_level.append([next_node, len(tree)-1, track_pindex,string, strindex+direction])
                    #Fixing string back so it doesn't affect other cases
                    string = temp
                else:
                    current_level.append([nta['reject'][0], len(tree)-1, track_pindex, string, strindex])

    tree.append(current_level)
#Manage case were all of the inputs are rejected
    if tree[-1] == []: return nta['reject']
    if next_node == nta['accept'][0]:
        return tree, nta['accept'][0]
    elif next_node == 'na':
        return tree, nta['reject'][0]
    return tree

def path_len(tree, nta, size):
    path = []
    flag = False
    #Get the q_accept coordinate:
    height, index = tree[-1][-1][1], tree[-1][-1][2]
    for level in tree[::-1]:
        for state in level:
            #print(state)
            if state[0] == nta['accept'][0]:
                height, index = state[1],state[2]
                path.append(nta['accept'][0])
                flag = True
                break

        if flag: break
    while height!= -1 and index != -1:
        path.append(tree[height][index][0])
        height, index = tree[height][index][1], tree[height][index][2]
    return path[::-1]
def configure_output(tree, nta, size):
    path = []
    flag = False
    ans = []
    height, index = tree[-1][-1][1], tree[-1][-1][2]
    #Get the q_accept coordinate:
    for level in tree[::-1]:
        for state in level:
        #print(state)
            if state[0] == nta['accept'][0]:
                height, index = state[1],state[2]
                ans.append(state[3][:state[4]]+state[0]+state[3][state[4]:])
                path.append(nta['accept'][0])
                flag = True
                break
        if flag: break
    while height!= -1 and index != -1:
        head = tree[height][index][4]
        curstring = tree[height][index][3]
        curstate = tree[height][index][0]
        if head == 0:
            output = curstate+ curstring
        else:
            output = curstring[:head] + curstate + curstring[head:]
        ans.append(output)
        path.append(tree[height][index][0])
        height, index = tree[height][index][1], tree[height][index][2]
    return(ans)
def calc_trans(tree):
    size = 0
    for level in tree:
        for node in level:
            size +=1
    return size
def main():
    string = '1#1'
    nta = parse_input()
    states_map= decompose_transition(nta)
    tree, status = make_tree(nta, string, states_map)

    size = calc_trans(tree)
    print(nta['name'][0])
    print(string)
    print(f'{size-2} total transitions traced')
    path = path_len(tree, nta, len(string))
    print(f'String accepted in {len(path)-1}' if status== nta['accept'][0] else
    f'String rejected in {len(path)-1}')
    ans = configure_output(tree, nta, len(string))
    for s in ans[::-1]:
        print(s)
if __name__=='__main__':
    main()