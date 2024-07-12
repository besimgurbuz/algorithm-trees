class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.left: Node = None
        self.right: Node = None

    def __str__(self) -> str:
        return str(self.data)

    def traversePreorder(self):
        print(self.data)
        if self.left:
            self.left.traversePreorder()
        if self.right:
            self.right.traversePreorder()

    def traverseInorder(self):
        if self.left:
            self.left.traverseInorder()
        print(self.data)
        if self.right:
            self.right.traverseInorder()

    def traversePostorder(self):
        if self.left:
            self.left.traversePostorder()
        if self.right:
            self.right.traversePostorder()
        print(self.data)

    def search(self, target):
        if self.data == target:
            return self
        if self.left and self.data > target:
            return self.left.search(target)
        if self.right and self.data < target:
            return self.right.search(target)
        print("Value is not in the tree")

    def add(self, data):
        if self.data == data:
            return
        if data < self.data:
            if self.left is None:
                self.left = Node(data)
            else:
                self.left.add(data)
        if data > self.data:
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.add(data)

    def delete(self, target):
        if self.data == target:
            if self.left and self.right:
                min_value = self.right.find_min()
                self.data = min_value
                self.right = self.right.delete(min_value)
                return self
            return self.left or self.right
        if self.right and target > self.data:
            self.right = self.right.delete(target)
        if self.left and target < self.data:
            self.left = self.left.delete(target)
        return self

    def find_min(self):
        if self.left:
            return self.left.find_min()
        return self.data

    def find_max(self):
        if self.right:
            return self.right.find_max()
        return self.data

    def get_nodes_at_depth(self, depth, nodes=None):
        if nodes is None:
            nodes = []
        if depth == 0:
            nodes.append(self)
            return nodes
        if self.left:
            self.left.get_nodes_at_depth(depth - 1, nodes)

        if self.right:
            self.right.get_nodes_at_depth(depth - 1, nodes)

        return nodes

    def height(self, h=0):
        left_height = self.left.height(h + 1) if self.left else h
        right_height = self.right.height(h + 1) if self.right else h
        return max(left_height, right_height)

    def is_balanced(self):
        left_height = self.left.height() + 1 if self.left else 0
        right_height = self.right.height() + 1 if self.right else 0

        return abs(left_height - right_height) < 2

    def get_left_right_height_difference(self):
        left_height = self.left.height() + 1 if self.left else 0
        right_height = self.right.height() + 1 if self.right else 0

        return left_height - right_height

    def fix_imbalance_if_exists(self):
        if self.get_left_right_height_difference() > 1:
            # left imbalance
            if self.left.get_left_right_height_difference() > 0:
                # left left imbalance
                return rotate_right(self)

            # left right imbalance
            self.left = rotate_left(self.left)
            return rotate_right(self)
        elif self.get_left_right_height_difference() < -1:
            # right imbalance
            if self.right.get_left_right_height_difference() < 0:
                # right right imbalance
                return rotate_left(self)
            # right left imbalance
            self.right = rotate_right(self.right)
            return rotate_left(self)
        return self

    def to_str(self):
        if not self.is_balanced():
            return f"{str(self.data)}*"
        return str(self.data)


def rotate_right(root: Node):
    pivot = root.left
    reattach_node = pivot.right
    root.left = reattach_node
    pivot.right = root
    return pivot


def rotate_left(root: Node):
    pivot = root.right
    reattach_node = pivot.left
    root.right = reattach_node
    pivot.left = root
    return pivot


def node_to_char(node: Node, spacing):
    if node is None:
        return "_" + (" " * spacing)
    spacing = spacing - len(node.to_str()) + 1
    return node.to_str() + (" " * spacing)


def print_tree(root: Node):
    height = root.height()
    spacing = 3
    width = int((2**height - 1) * (spacing + 1) + 1)
    offset = int((width - 1) / 2)
    for depth in range(0, height + 1):
        if depth > 0:
            print(
                " " * (offset + 1)
                + (" " * (spacing + 2)).join(
                    ["/" + (" " * (spacing - 2)) + "\\"] * (2 ** (depth - 1))
                )
            )
        row = root.get_nodes_at_depth(depth, [])
        print((" " * offset) + "".join([node_to_char(n, spacing) for n in row]))
        spacing = offset + 1
        offset = int(offset / 2) - 1
    print("")


root = Node(50)
root.left = Node(25)
root.right = Node(75)
root.left.left = Node(10)
root.left.right = Node(35)
root.left.left.left = Node(5)
root.left.left.right = Node(13)
root.left.right.left = Node(30)
root.left.right.right = Node(42)
root.left.left.left.left = Node(4)
root.left.left.left.right = Node(6)
root.left.left.left.left.left = Node(3)

print("*" * 10, " PREORDER ", "*" * 10)
root.traversePreorder()
print("*" * 30)

print("*" * 10, " INORDER ", "*" * 10)
root.traverseInorder()
print("*" * 30)

print("*" * 10, " POSTORDER ", "*" * 10)
root.traversePostorder()
print("*" * 30)

# print(root.search(30))

print(root.get_nodes_at_depth(3))
print(root.height())
print(root.left.height())
print(root.right.height())
print(root.is_balanced())

print_tree(root)
# root.left = rotate_left(root.left)
root = rotate_right(root)
print_tree(root)
root = rotate_right(root)
print_tree(root)
