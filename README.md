# practice_exercise

## Установка библиотеки отрисовки Graphviz

Для отрисовки деревьев использовался API работы с графами **Graphviz**

Вариант установки - при помощи файла ```requirements.txt``` и ```pip``` (либо при помощи [официального сайта](https://graphviz.org/download/) и прописывания всей папки ```bin``` в переменные ```PATH``` среды)

```
pip install -r ./requirements.txt
```

Также в случае проблем с **Graphviz** есть вариант модуля авл-дерева без визуализаций (файл ```avl_without_viz.py```)

Примеры отрисовки представлены в файлах ```viz[1-5].png```

![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz1.png)
+
![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz2.png)
=

![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz3.png)

Пример разделения 

![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz3.png)

->
![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz4.png)
+
![AAAAAA](https://github.com/t33nsy/practice_exercise/blob/main/viz/viz5.png)

## Немного слов про ассоциативный массив

Ассоциативный массив (класс *DoubleHashingMap* модуля *assoc.py*) реализован на методе двойного хэширования для защиты от коллизий.

Также реализован класс-обертка *MyDict* для работы с мапой при помощи переопределенных операторов (просто удобно)

### Объяснение выбора операций

- ***Вставка***: Используется двойное хэширование для разрешения коллизий. Это улучшает равномерность распределения данных.

- ***Поиск***: Эффективен благодаря тому, что двойное хэширование минимизирует кластеризацию записей.

- ***Удаление***: Реализуется с помощью специального флага типа *object* для удаленных записей.

- ***Перехеширование (ресайзинг)***: Увеличение размера таблицы в случае 50% заполнения предотвращает перегрузку и улучшает производительность.

Данные операции составляют достаточную основу для эффективной работы с таблицей, также временная сложность всех самых основных операций (вставка, удаление, поиск) составляет *O(1)* в лучшем и *O(N)* в худшем случаях 