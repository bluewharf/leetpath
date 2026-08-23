import sys


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None


def main():
    q = int(sys.stdin.readline())
    trie = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        op = parts[0]
        if op == "Trie":
            trie = Trie()
            print("null")
        elif op == "insert":
            trie.insert(parts[1])
            print("null")
        elif op == "search":
            print("true" if trie.search(parts[1]) else "false")
        elif op == "startsWith":
            print("true" if trie.startsWith(parts[1]) else "false")


if __name__ == "__main__":
    main()
