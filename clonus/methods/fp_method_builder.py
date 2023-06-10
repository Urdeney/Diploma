import pygments.token
import pygments.lexers
from .method_builder import MethodBuilder
from .fp_method import FpMethodResult


class FingerprintMethodBuilder(MethodBuilder):
    input_files: list                   # список из 2 имен файлов для проверки
    pre_proc_out: list                  # выходные данные pre_processing_step
    proc_out: list                      # выходные данные processing_step
    post_proc_out: FpMethodResult     # выходные данные processing_step
    output: list                        # результат выполнения метода
    gram_size: int                      # размер K-грамы
    hash_param: int                     # параметр хэш-фукнции
    window_size: int                    # размер окна (для алгоритма winnowing)

    def __init__(self, f_list: list, gram_size=8,window_size=3,hash_param=273) -> None:
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
        tokens_text = []        # список токенов в строковом представлении
        gh_list = []            # список К-грам и хэш-значений текстов
        finger_prints = []      # fingerprints текстов

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

    def post_processing_step(self) -> FpMethodResult:
        return FpMethodResult(self.proc_out[0], self.proc_out[1], self.proc_out[2])

    def _to_list(self, arr):
        """Возвращает сами токены в списке"""
        return [str(x[0]) for x in arr]

    def _to_text(self, arr):
        """Возвращает сами токены в строке"""
        cleanText = ''.join(str(x[0]) for x in arr)
        return cleanText

    def _tokenize(self, filename: str) -> None:
        """Алгоритм токенизации с запоминанием позиции"""
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
            elif tokens[i][0] in pygments.token.Literal.Number.Integer:
                res.append(('I', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Literal.Number.Float:
                res.append(('D', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Name.Function:
                res.append(('F', source_cnt, product_cnt))
                product_cnt += 1
            elif i!= 0 and tokens[i-1][0] == pygments.token.Text.Whitespace: 
                pass
            elif not (tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment):
                res.append((tokens[i][1], source_cnt, product_cnt))
                product_cnt += len(tokens[i][1])
            source_cnt += len(tokens[i][1])

        return res

    def _get_text_from_file(self, filename):
        """Возвращает текст из файла"""
        with open(filename, 'r') as f:
            text = f.read().lower()
        return text

    def _get_text_processing(self, text):
        """Возвращает текст без стоп-символов"""
        stop_symbols = [' ', ',']
        return ''.join(j for j in text if j not in stop_symbols)

    def _get_hash_from_gram(self, gram, q):
        """Полиномиальная хеш-функция от фрагмента текста"""
        h = 0

        mod = 10 ** 9 + 7
        m = 1
        for letter in gram:
            x = ord(letter) - ord('a') + 1
            h = (h + m * x) % mod
            m = (m * q) % mod
        return h

    def _get_k_grams_from_text(self, text, k=25, q=31):
        """Разделить текст на K-граммы"""
        grams = []
        for i in range(0, len(text)-k+1):
            hash_gram = self._get_hash_from_gram(text[i:i+k], q)
            gram = Gram(text[i:i+k], hash_gram, i, i+k)
            grams.append(gram)
        return grams

    def _get_hashes_from_grams(self, grams):
        """Взять хэши от списка граммов"""
        hashes = []
        for gram in grams:
            hashes.append(gram.hash)
        return hashes

    def _min_index(self, window):
        """Индекс минимального значения в окне"""
        min_ = window[0]
        min_i = 0
        for i in range(0, len(window)):
            if window[i] < min_:
                min_ = window[i]
                min_i = i
        return min_i

    def _winnow(self, hashes, w):
        """Метод просеивания отпечатков"""
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

    def _distance_simpson(self, A, B):
        """Мера Шимкевича_Симпсона"""
        a = set(A)
        b = set(B)
        return len(a.intersection(b)) / min(len(a), len(b))

    def _distance_simpson_lst(self, lst):
        """Мера Шимкевича_Симпсона из списка"""
        a = set(lst[0])
        b = set(lst[1])
        return len(a.intersection(b)) / min(len(a), len(b))

    def _get_points(self, fp1, fp2, token, hashes, grams):
        """Найти похожие fingerprints"""
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

    def _get_points_lst(self, lst, token, hashes, grams):
        """Найти похожие fingerprints из листа"""
        return (self._get_points(lst[0], lst[1], token, hashes, grams))

    def _get_merged_points(self, points):
        """Склеить похожие fingerprints"""
        try:
            merged_points = []
            merged_points.append(points[0])
            for i in range(1, len(points)):
                last = merged_points[-1]
                if points[i][0] >= last[0] and points[i][0] <= last[1]:
                    if points[i][1] > last[1]:
                        merged_points = merged_points[:-1]
                        merged_points.append([last[0], points[i][1]])
                else:
                    merged_points.append(points[i])
            return merged_points
        except IndexError: # если нет совпадающих отпечатков
            return None


class Gram:
    def __init__(self, text, hash_gram, start_pos, end_pos):
        self.text = text
        self.hash = hash_gram
        self.start_pos = start_pos
        self.end_pos = end_pos
