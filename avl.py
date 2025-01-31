from graphviz import Digraph  # для отрисовки


class AVLNode:
    def __init__(self, key):
        self.key = key  # Значение ключа узла (натуральное число)
        self.height = 1  # Высота узла
        self.left = None  # Левый потомок
        self.right = None  # Правый потомок


class AVLTree:
    def __init__(self):
        self.root = None  # корень дерева

    def _get_height(self, node: AVLNode) -> int:
        """Возвращает высоту узла

        Args:
            node (AVLNode): узел для поиска высоты

        Returns:
            int: высота узла
        """
        return node.height if node else 0

    def _update_height(self, node: AVLNode) -> None:
        """Обновляет высоту узла

        Args:
            node (AVLNode): узел для обновления высоты
        """
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _get_balance(self, node: AVLNode) -> int:
        """Возвращает баланс узла (разницу высот поддеревьев)

        Args:
            node (AVLNode): узел для поиска баланса

        Returns:
            int: баланс узла
        """
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Правый поворот вокруг узла y

        Args:
            y (AVLNode): узел для поворота

        Returns:
            AVLNode: узел после поворота
        """
        x = y.left
        T2 = x.right
        # Выполняем поворот
        x.right = y
        y.left = T2
        # Обновляем высоты
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Левый поворот вокруг узла x

        Args:
            x (AVLNode): узел для поворота

        Returns:
            AVLNode: узел после поворота
        """
        y = x.right
        T2 = y.left
        # Выполняем поворот
        y.left = x
        x.right = T2
        # Обновляем высоты
        self._update_height(x)
        self._update_height(y)
        return y

    def _balance_node(self, node: AVLNode) -> AVLNode:
        """Балансировка узла после вставки или удаления

        Args:
            node (AVLNode): узел для балансировки

        Returns:
            AVLNode: узел после балансировки
        """
        balance = self._get_balance(node)
        # Левый перевес
        if balance > 1:
            if self._get_balance(node.left) < 0:  # большой левый
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)  # малый левый
        # Правый перевес
        if balance < -1:
            if self._get_balance(node.right) > 0:  # большой правый
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)  # малый правый
        return node

    def insert(self, key: int) -> None:
        """Вставка нового узла с заданным ключом (внутренняя приватная часть)

        Args:
            key (int): ключ для вставки
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node: AVLNode, key: int) -> AVLNode:
        """Вставка нового узла с заданным ключом (внутренняя приватная часть)

        Args:
            node (AVLNode): текущий узел просмотра
            key (int): ключ для вставки

        Returns:
            AVLNode: узел после вставки
        """
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        # Обновляем высоту текущего узла
        self._update_height(node)
        # Балансировка узла
        return self._balance_node(node)

    def _find_min(self, node: AVLNode) -> AVLNode:
        """Находит узел с минимальным значением ключа

        Args:
            node (AVLNode): узел для поиска минимума в поддереве

        Returns:
            AVLNode: найденный минимум
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key: int) -> None:
        """Удаление узла с заданным ключом

        Args:
            key (int): ключ для удаления
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node: AVLNode, key: int) -> AVLNode:
        """Удаление узла с заданным ключом (внутренняя приватная часть)

        Args:
            node (AVLNode): текущий узел просмотра
            key (int): ключ для удаления

        Returns:
            AVLNode: узел после удаления
        """
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Узел с одним или нулем потомков
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Узел с двумя потомками ищем минимум в правом поддереве
            temp = self._find_min(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        # Обновляем высоту текущего узла
        self._update_height(node)
        # Балансировка узла
        return self._balance_node(node)

    def search(self, key: int) -> AVLNode:
        """Поиск узла с заданным ключом

        Args:
            key (int): ключ для поиска

        Returns:
            AVLNode: найденный узел или None
        """
        return self._search(self.root, key)

    def _search(self, node: AVLNode, key: int) -> AVLNode:
        """Поиск узла с заданным ключом (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала поиска и последующей рекурсии
            key (int): ключ для поиска

        Returns:
            AVLNode: найденный узел или None
        """
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder_traversal(self) -> list:
        """Обход дерева в порядке (inorder)

        Returns:
            list: список узлов
        """
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, node: AVLNode) -> list:
        """Обход дерева в порядке (inorder) (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала обхода и последующей рекурсии

        Returns:
            list: список узлов
        """
        result = []
        if node:
            result.extend(self._inorder_traversal(node.left))
            result.append(node.key)
            result.extend(self._inorder_traversal(node.right))
        return result

    def preorder_traversal(self) -> list:
        """Обход дерева в порядке (preorder)

        Returns:
            list: список узлов
        """
        return self._preorder_traversal(self.root)

    def _preorder_traversal(self, node: AVLNode) -> list:
        """Обход дерева в порядке (preorder) (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала обхода и последующей рекурсии

        Returns:
            list: список узлов
        """
        result = []
        if node:
            result.append(node.key)
            result.extend(self._preorder_traversal(node.left))
            result.extend(self._preorder_traversal(node.right))
        return result

    def postorder_traversal(self) -> list:
        """Обход дерева в порядке (postorder)

        Returns:
            list: список узлов
        """
        return self._postorder_traversal(self.root)

    def _postorder_traversal(self, node: AVLNode) -> list:
        """Обход дерева в порядке (postorder) (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала обхода и последующей рекурсии

        Returns:
            list: список узлов
        """
        result = []
        if node:
            result.extend(self._postorder_traversal(node.left))
            result.extend(self._postorder_traversal(node.right))
            result.append(node.key)
        return result

    def count_nodes(self) -> int:
        """Подсчет количества узлов в дереве

        Returns:
            int: число узлов
        """
        return self._count_nodes(self.root)

    def _count_nodes(self, node: AVLNode) -> int:
        """Подсчет количества узлов в дереве (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала обхода и последующей рекурсии

        Returns:
            int: число узлов
        """
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def validate_avl_tree(self) -> bool:
        """Валидация корректности структуры АВЛ-дерева

        Returns:
            bool: True, если корректно, иначе False
        """
        return self._validate_avl_tree(self.root)

    def _validate_avl_tree(self, node: AVLNode) -> bool:
        """Валидация корректности структуры АВЛ-дерева (внутренняя приватная часть)

        Args:
            node (AVLNode): узел для начала обхода

        Returns:
            bool: True, если корректно, иначе False
        """
        if not node:
            return True
        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False
        return self._validate_avl_tree(node.left) and self._validate_avl_tree(
            node.right
        )

    def visualize(self, filename: str = "viz") -> None:
        """Визуализация дерева с помощью Graphviz

        Args:
            filename (str): название файла
        """
        img = Digraph(format="png")
        if self.root:
            self._visualize(img, self.root, filename)
        img.render(filename)
        print(f"Отрисовка дерева сохранена в файл: {filename}.png")

    def _visualize(self, img: Digraph, node: AVLNode, filename: str) -> None:
        """Визуализация дерева с помощью Graphviz (внутренняя приватная часть)

        Args:
            img (Digraph): обьект графа отрисовки
            node (AVLNode): текущий узел
            filename (str): название файла
        """
        if node:
            img.node(str(node.key))
            if node.left:
                img.edge(str(node.key), str(node.left.key))
                self._visualize(img, node.left, filename)
            if node.right:
                img.edge(str(node.key), str(node.right.key))
                self._visualize(img, node.right, filename)

    def merge_trees(self, other) -> None:
        """Слияние двух деревьев за O(Mlog(N+M))

        Args:
            other (AVLTree): другое дерево
        """
        if not other.root:
            return
        # Рекурсивно начинаем добавлять вершины
        self._merge_nodes(other.root)

    def _merge_nodes(self, node: AVLNode) -> None:
        """Рекурсивная часть добавления узлов из другого дерева

        Args:
            node (AVLNode): текущий узел
        """
        if not node:
            return
        self.insert(node.key)
        self._merge_nodes(node.left)
        self._merge_nodes(node.right)

    def split_tree(self, key: int) -> tuple:
        """Разделение авл дерева по ключу

        Args:
            key (int): ключ с которой вершины будет происходить разделение

        Returns:
            tuple: полученные новые деревья
        """
        left, right = AVLTree(), AVLTree()
        self.root, left_root, right_root = self._split_tree(self.root, key)
        left.root, right.root = left_root, right_root
        return left, right

    def _split_tree(self, node: AVLNode, key: int) -> tuple:
        """Разделение авл дерева по ключу (внутренняя часть)

        Args:
            node (AVLNode): текущий узел
            key (int): ключ для деления

        Returns:
            tuple: новые вершины
        """
        if not node:
            return None, None, None
        if key < node.key:
            node.left, left_root, right_root = self._split_tree(node.left, key)
            return node, left_root, self._balance_node(right_root)
        elif key > node.key:
            node.right, left_root, right_root = self._split_tree(node.right, key)
            return self._balance_node(left_root), node, right_root
        else:
            # Нашли узел по которому делим
            left_root, right_root = node.left, node.right
            node.left, node.right = None, None
            return node, left_root, right_root

    def __len__(self) -> int:
        """Магический метод определения количества нод в дереве

        Returns:
            int: количество нод в дереве
        """
        return self._count_nodes(self.root) if self.root else 0

    def __getitem__(self, key: int) -> AVLNode:
        """Магический метод получения узла по ключу

        Args:
            key (int): ключ

        Returns:
            AVLNode: найденный по ключу узел
        """
        return self._search(self.root, key)

    def __delitem__(self, key: int) -> None:
        """Магический метод удаления узла по ключу

        Args:
            key (int): ключ для удаления
        """
        self._delete(self.root, key)

    def __str__(self) -> str:
        """Магический метод вывода дерева в виде строки
        
        Используется inorder обход

        Returns:
            str: дерево в виде строки
        """
        return str(self.inorder_traversal()) if self.root else "Empty tree"


# Пример использования
if __name__ == "__main__":
    avl_tree = AVLTree()

    # Вставка элементов
    for key in [10, 20, 30, 40, 50, 25, 60]:
        avl_tree.insert(key)

    print("Inorder traversal after inserts:", avl_tree.inorder_traversal())
    print(avl_tree)
    print("Total nodes:", avl_tree.count_nodes())
    print("Search (20): ", avl_tree[20], avl_tree[20].key)

    # Визуализация в случае правильно установленного Graphviz
    avl_tree.visualize("./viz/viz1")

    # Удаление узла
    avl_tree.delete(30)
    print("Inorder traversal after deletion (30):", avl_tree.inorder_traversal())
    print("AVL validation:", avl_tree.validate_avl_tree())

    # Визуализация после удаления в случае правильно установленного Graphviz
    avl_tree.visualize("./viz/viz2")

    avl_tree1 = AVLTree()
    for key in [1, 2, 3, 23, 11, 124, 12, 5]:
        avl_tree1.insert(key)

    # Слияние деревьев
    avl_tree.merge_trees(avl_tree1)
    print("Inorder traversal after merge:", avl_tree.inorder_traversal())
    print("AVL validation:", avl_tree.validate_avl_tree())
    avl_tree.visualize("./viz/viz3")

    # Разделение деревьев
    left, right = avl_tree.split_tree(10)
    print("Inorder traversal left:", left.inorder_traversal())
    print("Inorder traversal right:", right.inorder_traversal())
    print("AVL validation:", avl_tree.validate_avl_tree())
    print("Left validation:", left.validate_avl_tree())
    print("Right validation:", right.validate_avl_tree())
    left.visualize("./viz/viz4")
    right.visualize("./viz/viz5")
