import argparse
import sys
import csv

#procces csv
parent_dict = {}
entry_dict = {}
child_dict = {}

def process_csv(file, tool, info):
    if tool == 1:
        delimiter = ','
        ParentIdCol = 4
        ParentSeqCol = 5
        MFTIdCol = 2
        MFTSeqCol = 3
        NameCol = 0
        AttributeCol =10
        USNCol = 7
        ReasonCol = 9
    elif tool == 2:
        delimiter = '|'
        ParentIdCol = 7
        ParentSeqCol = 8
        MFTIdCol = 5
        MFTSeqCol = 6
        NameCol = 1
        AttributeCol = 9
        USNCol = 2
        ReasonCol = 4
    elif tool == 3:
        delimiter = ','
        ParentIdCol = 14
        ParentSeqCol = 15
        MFTIdCol = 12
        MFTSeqCol = 13
        NameCol = 11
        AttributeCol = 8
        USNCol = 3
        ReasonCol = 5

    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        next(reader)
        data = list(reader)

    for row in data:
        if not row or not row[USNCol]: #skip empty row
            continue

        parent_ref = row[ParentIdCol], row[ParentSeqCol]
        entry_ref = row[MFTIdCol], row[MFTSeqCol]
        name = row[NameCol]
        attribute = row[AttributeCol]
        usn = int(row[USNCol])
        reason = row[ReasonCol]

        #assign parent-child to parent_dict
        if entry_ref != parent_ref:
            if parent_ref in parent_dict:
                if entry_ref not in parent_dict[parent_ref]:
                    parent_dict[parent_ref].add(entry_ref)
            else:
                parent_dict[parent_ref] = {entry_ref}
        
        #assign child-details to entry_dict
        if info:
            if (entry_ref, parent_ref) in entry_dict:
                current_usn = entry_dict[entry_ref, parent_ref][1]
                if usn > current_usn: #get last USN
                    entry_dict[entry_ref, parent_ref] = [name, usn, reason, attribute]
                    child_dict[entry_ref] = parent_ref
            else:
                entry_dict[entry_ref, parent_ref] = [name, usn, reason, attribute]
                child_dict[entry_ref] = parent_ref
        else:
            if (entry_ref, parent_ref) in entry_dict:
                current_usn = entry_dict[entry_ref, parent_ref][1]
                if usn > current_usn: #get last USN
                    entry_dict[entry_ref, parent_ref] = [name, usn]
                    child_dict[entry_ref] = parent_ref
            else:
                entry_dict[entry_ref, parent_ref] = [name, usn]
                child_dict[entry_ref] = parent_ref

#search root node from child node
root_node = []
visited_node = []

def find_root(parent):
    if parent != ('5','5') and parent in child_dict:
        current_parent = child_dict[parent]
        if current_parent not in visited_node:
            visited_node.append(current_parent)
            find_root(current_parent)
    else:
        if parent not in root_node:
            root_node.append(parent)
        
#print tree one level depth
def print_tree(parent, info):
    if info:
        if parent not in entry_dict:
            print(f'(id: {parent[0]}, seq: {parent[1]})')
            children = sorted(parent_dict[parent])
            for child in children:
                print(f'   {entry_dict[child, parent][0]} (id: {child[0]}, seq: {child[1]}) {entry_dict[child, parent][3]}, {entry_dict[child, parent][1]}, {entry_dict[child, parent][2]}')
        else:
            print(f'{entry_dict[parent][0]} (id: {parent[0][0]}, seq: {parent[0][1]}) {entry_dict[parent][3]}, {entry_dict[parent][1]}, {entry_dict[parent][2]}')
            children = sorted(parent_dict[parent[0]])
            for child in children:
                print(f'   {entry_dict[child, parent[0]][0]} (id: {child[0]}, seq: {child[1]}) {entry_dict[child, parent[0]][3]}, {entry_dict[child, parent[0]][1]}, {entry_dict[child, parent[0]][2]}')
    else:
        if parent not in entry_dict:
            print(f'(id: {parent[0]}, seq: {parent[1]})')
            children = sorted(parent_dict[parent])
            for child in children:
                print(f'   {entry_dict[child, parent][0]} (id: {child[0]}, seq: {child[1]})')
        else:
            print(f'{entry_dict[parent][0]} (id: {parent[0][0]}, seq: {parent[0][1]})')
            children = sorted(parent_dict[parent[0]])
            for child in children:
                print(f'   {entry_dict[child, parent[0]][0]} (id: {child[0]}, seq: {child[1]})')

#print tree recursively
def print_tree_recursive(parent, info, indent=''):
    if info:
        if parent not in entry_dict:
            print(f'{indent}(id: {parent[0]}, seq: {parent[1]})')
            if parent in parent_dict:
                children = sorted(parent_dict[parent])
                for child in children:
                    child = child, parent
                    print_tree_recursive(child, True, indent + '   ')
        else:
            print(f'{indent}{entry_dict[parent][0]} (id: {parent[0][0]}, seq: {parent[0][1]}) {entry_dict[parent][3]}, {entry_dict[parent][1]}, {entry_dict[parent][2]}')
            if parent[0] in parent_dict:
                children = sorted(parent_dict[parent[0]])
                for child in children:
                    child = child, parent[0]
                    print_tree_recursive(child, True, indent + '   ')
    else:
        if parent not in entry_dict:
            print(f'{indent}(id: {parent[0]}, seq: {parent[1]})')
            if parent in parent_dict:
                children = sorted(parent_dict[parent])
                for child in children:
                    child = child, parent
                    print_tree_recursive(child, False, indent + '   ')
        else:
            print(f'{indent}{entry_dict[parent][0]} (id: {parent[0][0]}, seq: {parent[0][1]})')
            if parent[0] in parent_dict:
                children = sorted(parent_dict[parent[0]])
                for child in children:
                    child = child, parent[0]
                    print_tree_recursive(child, False, indent + '   ')

#print all root parent
def print_parent_all(recursive, info):
    for parent in parent_dict:
        find_root(parent)
    for parent in root_node:
        if parent in child_dict:
            parent = parent, child_dict[parent]
        if recursive:
            print_tree_recursive(parent, info)
        else:
            print_tree(parent, info)

#print one parent
def print_parent(parent, recursive, info):
    if parent in parent_dict:
        print_path(parent)
        if parent in child_dict:
            parent = parent, child_dict[parent]
        if recursive:
            print_tree_recursive(parent, info)
        else:
            print_tree(parent, info)
    else:
        print(f'{parent} is invalid') #not in record, empty folder, and file mark as 'invalid'

#print path
def print_path(parent):
    find_root(parent)
    path = []
    if len(visited_node) > 0:
        visited_node.reverse()
        for i in range(len(visited_node)):
            if visited_node[i] not in child_dict:
                name = visited_node[i]
            elif visited_node[i] == ('5','5'):
                name = entry_dict[('5','5'), ('5','5')][0]
            else:
                name = entry_dict[visited_node[i], visited_node[i-1]][0]
            path.append(str(name))
        print('PATH: ' + '\\'.join(path) + '\\' + entry_dict[parent, visited_node[len(visited_node)-1]][0] + '\n')
    else:
        print('PATH: ' + str(parent) + '\n')

#argparse
def parse_args(argument_string):
    parser = argparse.ArgumentParser()

    parser.add_argument('-t',
        help='tool used for parsing (1 = MFTECmd, 2 = UsnJrnl2Csv(dump everything), 3 = ntfs_parse)',
        dest='tool',
        type=int,
        choices=range(1, 4),
        required=True)

    parser.add_argument('-f',
        help='parsed file (CSV)',
        dest='file',
        required=True)
    
    parser.add_argument('-p',
        help='parent refrence (-p [ParentId] [ParentSeq])',
        dest='num',
        nargs=2)

    parser.add_argument('-r',
        help='recursive',
        action='store_true')

    parser.add_argument('-i',
        help='info',
        action='store_true')

    return parser.parse_args(argument_string)

if __name__ == '__main__':

    args = parse_args(sys.argv[1:])

    file = args.file
    tool = args.tool
    recursive = args.r
    info = args.i

    process_csv(file, tool, info)

    if args.num:
        parent = tuple(args.num)
        print_parent(parent, recursive, info)
    else:
        print_parent_all(recursive, info)
