# Written by Yi Xiao (Shawn) Lu
# (chees-e)
import sys
import copy


# Will prob work better with numpy
# Content can't be too long

# TODO: add comments

# parse_tree
#     Function that takes a string and gives an dictionary objected used to generate
#     the text tree
#     Input:
#         st (string): The tree string
#     Output:
#         parsed_tree (dict): Dictionary object representing the tree
def parse_tree(st):
    tree = {"content": "",
            "subtrees": []}

    if "(" in st:
        content = st.split("(")[1].split("/")[0]
    else:
        content = st.replace("/", "")

    tree = {"content": content,
            "subtrees": []}

    stack = []
    subtrees = []
    if "(" in st:
        idx = st.index("(") + 1

        while True:
            while idx < len(st) and (not st[idx] in ["(", "/"]):
                idx += 1

            if idx >= len(st):
                break

            start_idx = idx
            stack.append(st[idx])

            while len(stack) > 0:
                idx += 1
                if st[idx] == "/":
                    if stack[-1] == "/":
                        stack.pop()
                    else:
                        stack.append("/")
                elif st[idx] == "(":
                    stack.append("(")
                elif st[idx] == ")":
                    stack.pop()
            tree["subtrees"].append(parse_tree(st[start_idx:idx+1]))
            idx += 1

    return tree


# generate_array
#     Generates a 2D list with r rows c columns filled with spaces
#     Input:
#         r (int): number of rows
#         c (int): number of columns
#     Output:
#         rv (List(List())): the requested array
def generate_array(r, c):
    rv = []
    for i in range(r):
        rv.append([" "] * c)

    return rv


# paste_array
#     Transfers the content of a smaller array to a specific location in a larger
#     array
#     Input:
#         big (List(List())): The big array
#         small (List(List())): The small array
#         r (int): row index in the big array where the paste starts
#         c (int): column index ~
#     Output:
#         rv (List(List())): Big array with the new contents pasted
def paste_array(big, small, r, c):
    assert len(big[0]) >= len(small[0]) + c
    assert len(big) >= len(small) + r

    rv = copy.deepcopy(big)

    for i in range(len(small)):
        for j in range(len(small[i])):
            rv[i+r][j+c] = small[i][j]

    return rv


# generate_tree
#     A recursive function that generates a 2D array that contains individual letters of the text tree
#     Input:
#         tree (dict): the parsed tree
#     Output:
#         rv (List(List)): the 2D array that represents the parsed tree
#         r: the number of rows of the 2D array
#         c: the number of columns of the 2D array
def generate_tree(tree):
    if len(tree["subtrees"]) == 0:
        return [list(tree["content"]),], 1, len(tree["content"])
    else:
        rows = []
        cols = []
        subtrees = []
        num = len(tree["subtrees"])

        for i in range(num):
            t, r, c = generate_tree(tree["subtrees"][i])
            rows.append(r)
            cols.append(c)
            subtrees.append(t)

        # calculated_c = sum(cols) + num - 1
        maxc = max(cols)
        calculated_c = maxc * num + num - 1
        assert len(tree["content"]) <= calculated_c

        adjusted_cols = [maxc] * num

        calculated_r = max(rows) + 4

        rv = generate_array(calculated_r, calculated_c)

        # paste subtrees
        cur_c = 0
        midpoints = []
        for i in range(num):
            cur_c = i * maxc + maxc//2 - cols[i]//2 + i # comment to squeeze the tree
            rv = paste_array(rv, subtrees[i], 4, cur_c)
            cur_c += cols[i] + 1

            # mp = sum(cols[0:i]) + i + cols[i]//2
            mp = sum(adjusted_cols[0:i]) + i + adjusted_cols[i]//2
            midpoints.append(mp)
            rv[3][mp] = "|"

        for i in range(midpoints[0], midpoints[-1] + 1):
            rv[2][i] = "-"

        rv[1][calculated_c//2] = "|"

        title_start = calculated_c//2 - len(tree["content"])//2
        for i in range(len(tree["content"])):
            rv[0][title_start + i] = tree["content"][i]

        return rv, calculated_r, calculated_c



# Print tree
#     Removes empty columns and
#     prints the tree in a 2D array
def print_tree(tree):
    while True:
        empty = True
        for row in tree:
            empty = empty and row[0] == " "

        if empty:
            for row in tree:
                row.pop(0)
        else:
            break

    for row in tree:
        print("".join(row))


# main:
#     takes the command line input/console input and
#     calls all the required functions to print the text tree
def main(args=[]):
    # Example input:
    # (S (NP /John/) (VP (VP (V /plays/) (NP /soccer/)) (PP (P /at/) (NP /soccer/))))
    if len(args) == 0:
        tree_st = input("Enter a tree: ")
    else:
        tree_st = " ".join(args)

    parsed_tree = parse_tree(tree_st.replace(" ", ""))

    generated_tree, rows, cols = generate_tree(parsed_tree)

    print_tree(generated_tree)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args=args)
