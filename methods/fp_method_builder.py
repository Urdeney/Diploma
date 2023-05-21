import hashlib
import pygments.token
import pygments.lexers
from method_builder import Method_Builder
from fp_method import Fp_Method_Result


class Fingerprint_Method_Builder(Method_Builder):
    input_files: list                   # list of 2 filenames to detect clones
    pre_proc_out: list                  # pre_processing_step output
    proc_out: list                      # processing_step output
    post_proc_out: Fp_Method_Result     # processing_step output
    output: list                        # method_result
    gram_size: int                      # size of K-gram
    hash_param: int                     # hash_function parameter
    window_size: int                    # size of window (for winnowing)

    def __init__(self, f_list: list, gram_size=8, hash_param=259, window_size=3) -> None:
        super().__init__()
        self.input_files = f_list
        self.pre_proc_out = []
        self.proc_out = []
        self.post_proc_out = []
        self.gram_size = gram_size
        self.hash_param = hash_param
        self.window_size = window_size

    def pre_processing_step(self):
        for file_name in self.input_files:
            token_lst = self._tokenize(file_name)
            self.pre_proc_out.append(token_lst)

    def processing_step(self):
        tokens_text = []    # tokens in string notation
        gh_list = []        # list of texts' grams and hashes
        finger_prints = []   # texts' fingerprints

        if len(self.input_files) != len(self.pre_proc_out):
            raise AttributeError("Fingerprint method prepocessing error")

        for elem in self.pre_proc_out:
            tokens_text.append(self._to_text(elem))

        for i in range(len(tokens_text)):
            i_grams = self._get_k_grams_from_text(
                tokens_text[i], self.gram_size, self.hash_param)
            i_hashes = self._get_hashes_from_grams(i_grams)
            i_finger_prints = self._winnow(i_hashes, self.window_size)

            gh_list.append([i_grams, i_hashes])
            finger_prints.append(i_finger_prints)

        for i in range(len(tokens_text)):
            i_points = self._get_points_lst(
                finger_prints, self.pre_proc_out[i], gh_list[i][1], gh_list[i][0])
            i_merged_points = self._get_merged_points(i_points)
            self.proc_out.append(i_merged_points)

        self.proc_out.append(self._distance_simpson_lst(finger_prints))

    def post_processing_step(self) -> Fp_Method_Result:
        return Fp_Method_Result(self.proc_out[0], self.proc_out[1], self.proc_out[2])

    # Возвращает сами токены в списке
    def _to_list(self, arr):
        return [str(x[0]) for x in arr]

    # Возвращает сами токены в строке
    def _to_text(self, arr):
        cleanText = ''.join(str(x[0]) for x in arr)
        return cleanText

    # Алгоритм токенизации с запоминанием позиции
    def _tokenize(self, filename: str) -> None:
        file = open(filename, "r")
        text = file.read()
        file.close()
        lexer = pygments.lexers.guess_lexer_for_filename(
            filename, text)  # для определения языка
        tokens = lexer.get_tokens(text)
        tokens = list(tokens)
        res = []
        tokens_len = len(tokens)
        source_cnt = 0  # позиция элемента в исходном коде
        product_cnt = 0  # позиция элемента в обработаном коде
        for i in range(tokens_len):
            if tokens[i][0] == pygments.token.Name and i != tokens_len - 1 and tokens[i + 1][1] != '(':
                res.append(('N', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Literal.String:
                res.append(('S', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Name.Function:
                res.append(('F', source_cnt, product_cnt))
                product_cnt += 1
            elif not (tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment):
                res.append((tokens[i][1], source_cnt, product_cnt))
                product_cnt += len(tokens[i][1])
            source_cnt += len(tokens[i][1])

        return res

    # Возвращает текст из файла
    def _get_text_from_file(self, filename):
        with open(filename, 'r') as f:
            text = f.read().lower()
        return text

    # возвращает текст без стоп-символов
    def _get_text_processing(self, text):
        stop_symbols = [' ', ',']
        return ''.join(j for j in text if j not in stop_symbols)

    # Хеш-функция от куска текста 1
    def _get_hash_from_gram(self, gram, q):
        h = 0
        k = 273

        mod = 10 ** 9 + 7
        m = 1
        for letter in gram:
            x = ord(letter) - ord('a') + 1
            h = (h + m * x) % mod
            m = (m * k) % mod
        return h

    # Хеш-функция от куска текста 2
    def _get_hash_from_gram1(self, gram, q):
        hashval = hashlib.sha1(gram.encode('utf-8'))
        hashval = hashval.hexdigest()[-4:]
        hashval = int(hashval, 16)
        return hashval

    # Разделить текст на K-граммы
    def _get_k_grams_from_text(self, text, k=25, q=31):
        grams = []
        for i in range(0, len(text)-k+1):
            hash_gram = self._get_hash_from_gram(text[i:i+k], q)
            gram = Gram(text[i:i+k], hash_gram, i, i+k)
            grams.append(gram)
        return grams

    # Взять хэши от списка граммов
    def _get_hashes_from_grams(self, grams):
        hashes = []
        for gram in grams:
            hashes.append(gram.hash)
        return hashes

    # Индекс минимального значения в окне
    def _min_index(self, window):
        min_ = window[0]
        min_i = 0
        for i in range(0, len(window)):
            if window[i] < min_:
                min_ = window[i]
                min_i = i
        return min_i

    # Метод просеивания отпечатков
    def _winnow(self, hashes, w):
        n = len(hashes)
        prints = []
        windows = []
        prev_min = 0
        current_min = 0
        for i in range(n - w):
            window = hashes[i:i+w]
            windows.append(window)
            current_min = i + self._min_index(window)
            if current_min != prev_min:
                prints.append(hashes[current_min])
                prev_min = current_min
        return prints

    # Мера Шимкевича_Симпсона
    def _distance_simpson(self, A, B):
        a = set(A)
        b = set(B)
        return len(a.intersection(b)) / min(len(a), len(b))

    # Мера Шимкевича_Симпсона (лист)
    def _distance_simpson_lst(self, lst):
        a = set(lst[0])
        b = set(lst[1])
        return len(a.intersection(b)) / min(len(a), len(b))

    # Найти похожие fingerprints
    def _get_points(self, fp1, fp2, token, hashes, grams):
        points = []
        for i in fp1:
            for j in fp2:
                if i == j:
                    flag = False
                    startx = endx = None
                    match = hashes.index(i)
                    newStart = grams[match].start_pos
                    newEnd = grams[match].end_pos

                    for k in token:
                        if k[2] == newStart:
                            startx = k[1]
                            flag = True
                        if k[2] == newEnd:
                            endx = k[1]
                    if flag and endx is not None:
                        if [startx, endx] not in points:
                            points.append([startx, endx])
        points.sort(key=lambda x: x[0])
        return points

    # Найти похожие fingerprints из листа
    def _get_points_lst(self, lst, token, hashes, grams):
        return (self._get_points(lst[0], lst[1], token, hashes, grams))

    # Склеить похожие fingerprints
    def _get_merged_points(self, points):
        mergedPoints = []
        mergedPoints.append(points[0])
        for i in range(1, len(points)):
            last = mergedPoints[-1]
            if points[i][0] >= last[0] and points[i][0] <= last[1]:
                if points[i][1] > last[1]:
                    mergedPoints = mergedPoints[:-1]
                    mergedPoints.append([last[0], points[i][1]])
            else:
                mergedPoints.append(points[i])
        return mergedPoints


class Gram:
    def __init__(self, text, hash_gram, start_pos, end_pos):
        self.text = text
        self.hash = hash_gram
        self.start_pos = start_pos
        self.end_pos = end_pos
