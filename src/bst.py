"""basic red black bst implementation with APIs

Author:
    Toshi
"""
import random

class BST:
    """BST class
    Attributes:
        root (Node) : the root of the tree
        num_items (int) : the number of items
    """
    class Node:
        """The class for node of the tree
        Attributes:
            key (int) : the key
            val (*) : the value
            rank (int) : the rank
            size (int) : the size of the subtree
            color (str) : the color for RB tree
            left (Node) : the left subtree
            right (Node) : the right subtree
        """
        def __init__(self, key, val=None, left=None, right=None, color='R'):
            self.key = key
            self.val = val
            self.color = color
            self.left = left
            self.right = right

        def __repr__(self):
            return "%s:%s{%s, left: %s, right: %s}"\
                % (self.color, self.key, self.val, self.left, self.right)

        def __eq__(self, other):
            return isinstance(other, type(self)) and self.key == other.key

    def __init__(self):
        self.root = None
        self.num_items = 0

    def size(self):
        return self.num_items

    def insert(self, key, val=None):
        self.root = BST._insert(self.root, key, val)
        self.root.color = 'B'
        self.num_items += 1

    @staticmethod
    def _size(tree):
        if tree is None:
            return 0
        return 1 + BST._size(tree.left) + BST._size(tree.right)

    @staticmethod
    def _rank(tree, key):
        """get the rank of a key.
        The rank is the number of keys smaller that the key.
        Args:
            tree (BST): the bst
            key (int): the key in the bst
        Returns:
            int : the rank of the key
        """
        if tree is None:
            return 0
        if tree.key < key:
            return 1 + BST._size(tree.left) + BST._rank(tree.right, key)
        elif tree.key == key:
            return BST._size(tree.left)
        return BST._rank(tree.left, key)

    @staticmethod
    def _insert(tree, key, val):
        if tree is None:
            return BST.Node(key, val)
        if tree.key == key:
            tree.val = val
        elif tree.key > key:
            tree.left = BST._insert(tree.left, key, val)
        else:
            tree.right = BST._insert(tree.right, key, val)
        return BST._rebalance(tree)

    def range_count(self, lo, hi):
        """get the number of key in the range.
        lower bound is inclusive, but the upper bound is non-inclusive.
        Args:
            lo (int): the key on the lower end.
            hi (int): the key on the higher end.
        Returns:
            int : the number of keys
        """
        return BST._rank(self.root, hi) - BST._rank(self.root, lo)
   
    def range(self, lo, hi):
        """get the keys in the range.
        lower bound is inclusive, but the upper bound is non-inclusive.
        Args:
            lo (int): the key on the lower end.
            hi (int): the key on the higher end.
        Returns:
            list : a list of keys
        """
        accum = []
        BST._range(self.root, lo, hi, accum)
        return accum

    @staticmethod
    def _range(tree, lo, hi, accum):
        if tree is None:
            return
        if tree.key >= hi:
            BST._range(tree.left, lo, hi, accum)
            return
        if tree.key < lo:
            return BST._range(tree.right, lo, hi, accum)
        BST._range(tree.left, lo, hi, accum)
        accum.append(tree.key)
        BST._range(tree.right, lo, hi, accum)
        return

    def find_min(self):
        node = BST._find_min(self.root)
        return node.key

    @staticmethod
    def _find_min(tree):
        if tree is None:
            raise IndexError('The tree is empty!')
        if tree.left is None:
            return tree
        return BST._find_min(tree.left)

    def find_max(self):
        node = BST._find_max(self.root)
        return node.key

    @staticmethod
    def _find_max(tree):
        if tree is None:
            raise IndexError('The tree is empty!')
        if tree.right is None:
            return tree
        return BST._find_max(tree.right)

    def delete(self, key):
        self.root = BST._delete(self.root, key)
        self.root.color = 'B'
        self.num_items -= 1 

    @staticmethod
    def _delete(tree, key):
        if tree is None:
            raise IndexError('The key: %s does not exists!' % (key))
        if tree.key == key:
            if tree.left is None:
                return tree.right
            if tree.right is None:
                return tree.left
            replacement = BST._find_min(tree.right)
            node = tree
            tree = BST._delete(tree, replacement.key)
            node.key = replacement.key
            node.val = replacement.val
        elif tree.key > key:
            tree = BST._lean_left(tree)
            tree.left = BST._delete(tree.left, key)
        else:
            tree = BST._lean_right(tree)
            tree.right = BST._delete(tree.right, key)
        return BST._rebalance(tree)

    @staticmethod
    def _rebalance(tree):
        if tree is None:
            return tree
        if tree.color == 'B' and tree.left and tree.left.color == 'R'\
            and tree.left.left and tree.left.left.color == 'R':
            tree = BST.Node(
                    tree.left.key,
                    tree.left.val,
                    BST.Node(
                        tree.left.left.key,
                        tree.left.left.val,
                        tree.left.left.left,
                        tree.left.left.right, 'B'), 
                    BST.Node(
                        tree.key,
                        tree.val,
                        tree.left.right,
                        tree.right, 'B'),
                    'R')
        elif tree.color == 'B' and tree.left and tree.left.color == 'R'\
            and tree.left.right and tree.left.right.color == 'R':
            tree = BST.Node(
                    tree.left.right.key,
                    tree.left.right.val,
                    BST.Node(
                        tree.left.key,
                        tree.left.val,
                        tree.left.left,
                        tree.left.right.left, 'B'), 
                    BST.Node(
                        tree.key,
                        tree.val,
                        tree.left.right.right,
                        tree.right, 'B'),
                    'R')
        elif tree.color == 'B' and tree.right and tree.right.color == 'R'\
            and tree.right.right and tree.right.right.color == 'R':
            tree = BST.Node(
                    tree.right.key,
                    tree.right.val,
                    BST.Node(
                        tree.key,
                        tree.val,
                        tree.left,
                        tree.right.left, 'B'), 
                    BST.Node(
                        tree.right.right.key,
                        tree.right.right.val,
                        tree.right.right.left,
                        tree.right.right.right, 'B'),
                    'R')
        elif tree.color == 'B' and tree.right and tree.right.color == 'R'\
            and tree.right.left and tree.right.left.color == 'R':
            tree = BST.Node(
                    tree.right.left.key,
                    tree.right.left.val,
                    BST.Node(
                        tree.key,
                        tree.val,
                        tree.left,
                        tree.right.left.left, 'B'), 
                    BST.Node(
                        tree.right.key,
                        tree.right.val,
                        tree.right.left.right,
                        tree.right.right, 'B'),
                    'R')
        return tree

    @staticmethod
    def _lean_left(tree):
        """lean the tree to the left
        Args:
            tree (Node) : a red black tree
        Returns:
            Node : a red black tree
        """
        if tree and tree.left and tree.left.color == 'B'\
            and tree.right:
            return BST.Node(
                tree.right.key,
                tree.right.val,
                BST.Node(
                    tree.key,
                    tree.val,
                    BST.Node(
                        tree.left.key,
                        tree.left.val,
                        tree.left.left,
                        tree.left.right,
                        'R'),
                    tree.right.left,
                    'R'),
                tree.right.right,
                'B')
        return tree

    @staticmethod
    def _lean_right(tree):
        """lean the tree to the right 
        Args:
            tree (Node) : a red black tree
        Returns:
            Node : a red black tree
        """
        if tree and tree.left\
            and tree.right and tree.right.color == 'B':
            return BST.Node(
                tree.left.key,
                tree.left.val,
                tree.left.left,
                BST.Node(
                    tree.key,
                    tree.val,
                    tree.left.right,
                    BST.Node(
                        tree.right.key,
                        tree.right.val,
                        tree.right.left,
                        tree.right.right,
                        'R'),
                    'R'),
                'B')
        return tree

def shuffle(items):
    length = len(items)
    for i in range(1, length):
        r = random.randint(0, i)
        items[i], items[r] = items[r], items[i]

def main():
    items = [i for i in range(10)]
    #random.seed(1)
    #shuffle(items)
    bst = BST()
    for item in items:
        bst.insert(item)
    print(bst.root)
    print(bst.size())
    print(bst.find_min())
    print(bst.find_max())
    print(bst.range_count(0,2))
    print(bst.range(0,2))
    print(bst.range_count(2,5))
    print(bst.range(2,5))
    print(bst.range_count(7,7))
    print(bst.range(7,7))
    
    bst.delete(5)
    print(bst.root)
    print(bst.size())
    print(bst.find_min())
    print(bst.find_max())
    print(bst.range_count(0,2))
    print(bst.range(0,2))
    print(bst.range_count(2,5))
    print(bst.range(2,5))
    print(bst.range_count(7,7))
    print(bst.range(7,7))

    bst.delete(8)
    print(bst.root)
    print(bst.size())

    bst.delete(9)
    print(bst.root)
    print(bst.size())

if __name__ == '__main__':
    main()


