from method_builder import Method_Builder
import pygments.token,pygments.lexers
import hashlib

class Fingerprint_Method_Builder(Method_Builder):
    input : list    # list of filenames of texts (new preposesing?)
    pre_p : list    # pre_processing_step result = token1
    p: list       # processing_step result
    post_p : object # processing_step result
    output : list   # method_result

    def __init__(self,input : str) -> None:
        super().__init__()
        self.input = input # add other fields ?
        self.pre_p = []
        self.p = []
        self.post_p = []


    def pre_processing_step(self) -> None:
        for st in self.input:
            token_lst=self._tokenize(st) # ((token), sorcepos, proccespos)
            self.pre_p.append(token_lst)


    def processing_step(self):
        if len(self.input) != len(self.pre_p):
            raise AttributeError("Fingerprint method prepocessing error")

        k=8 #вынести в редактор
        q=259
        w=3
        text_tokens = [] # token1 and token2 (text1proc and textproc2)

        for elem in self.pre_p:
            text_tokens.append(self._to_text(elem))

        grams1 = self._get_k_grams_from_text(text_tokens[0], k, q)
        grams2 = self._get_k_grams_from_text(text_tokens[1], k, q)

        hashes1 = self._get_hashes_from_grams(grams1)
        hashes2 = self._get_hashes_from_grams(grams2)


        fp1 = self._winnow(hashes1, w)
        fp2 = self._winnow(hashes2, w)

        points1 = self._get_points(fp1, fp2, self.pre_p[0], hashes1, grams1)
        points2 = self._get_points(fp2, fp1, self.pre_p[1], hashes2, grams2)

        merged_points1 = self._get_merged_points(points1)
        merged_points2 = self._get_merged_points(points2)
        self.p.append([merged_points1, merged_points2, self._distance_simpson(fp1, fp2)])

        # for i in range(0,len(tokens)):
        #     grams = self._get_k_grams_from_text(tokens[i], k, q)
        #     hashes = self._get_hashes_from_grams(grams)    
        #     fp = self._winnow(hashes, w)

        #     points1 = self._get_points(fp1, fp2, token1, hashes1, grams1)
        #     points2 = self._get_points(fp1, fp2, token2, hashes2, grams2)
    
        #     merged_points1 =self._get_merged_points_extended(points1)
        #     merged_points2 = self._get_merged_points_extended(points2)
    
    def post_processing_step(self): #TO_DO
        print(self.p)

    #Возвращает только токены в списке
    def _to_list(self,arr):
        return [str(x[0]) for x in arr]

    #Возвращает только токены в строке
    def _to_text(self,arr):
        cleanText = ''.join(str(x[0]) for x in arr)
        return cleanText

    #алгоритм токенизации
    def _tokenize(self,st : str) -> None:
        file = open(st, "r")
        text = file.read()
        file.close()
        lexer = pygments.lexers.guess_lexer_for_filename(st, text) # для определения языка
        tokens = lexer.get_tokens(text)
        tokens = list(tokens)
        result = []
        lenT = len(tokens)
        source_cnt = 0  #позиция элемента в исходном коде
        product_cnt = 0  #позиция элемента в обработаном коде
        for i in range(lenT):
            if tokens[i][0] == pygments.token.Name and not i == lenT - 1 and not tokens[i + 1][1] == '(':
                result.append(('N', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Literal.String:
                result.append(('S', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] in pygments.token.Name.Function:
                result.append(('F', source_cnt, product_cnt))
                product_cnt += 1
            elif tokens[i][0] == pygments.token.Text or tokens[i][0] in pygments.token.Comment:
                pass
            else:
                result.append((tokens[i][1], source_cnt, product_cnt))  
                product_cnt += len(tokens[i][1])
            source_cnt += len(tokens[i][1])

        return result

    #возращает_текст_из_файла_(не_используется)
    def _get_text_from_file(self,filename):
        with open(filename, 'r') as f:
            text = f.read().lower()
        return text

    #возвращает_текст_без_стоп-символов(не_используется)
    def _get_text_processing(self,text):
        stop_symbols = [' ', ',']
        return ''.join(j for j in text if not j in stop_symbols)

    #хеш_функция_от_куска_текста (сделать разыне хэш-функции??)
    def _get_hash_from_gram(self,gram, q):
        h = 0
        k = 273

        mod = 10 ** 9 + 7  # 2**64
        m = 1
        for letter in gram:
            x = ord(letter) - ord('a') + 1
            h = (h + m * x) % mod
            m = (m * k) % mod
        return h

    #хеш_функция_от_куска_текста (сделать разыне хэш-функции??)
    def _get_hash_from_gram1(self,gram, q):
        hashval = hashlib.sha1(gram.encode('utf-8'))
        hashval = hashval.hexdigest()[-4:]
        hashval = int(hashval, 16)
        return hashval

    #разделить_текст_на_K-граммы
    def _get_k_grams_from_text(self,text, k=25, q=31):
        grams = []
        for i in range(0, len(text)-k+1):
            hash_gram = self._get_hash_from_gram(text[i:i+k], q)
            gram = Gram(text[i:i+k], hash_gram, i, i+k)
            grams.append(gram)
        return grams

    #взять_хэши_от_списка_граммов
    def _get_hashes_from_grams(self,grams):
        hashes = []
        for gram in grams:
            hashes.append(gram.hash)
        return hashes

    #индекс_миниамльного_значения_в_окне(для_winnowing)
    def _min_index(self,window):
        min_ = window[0]
        min_i = 0
        for i in range(0,len(window)):
            if window[i] < min_:
                min_ = window[i]
                min_i = i
        return min_i

    #метод_проссеивания_отпечатков(шаг_2)
    def _winnow(self,hashes, w):
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

    #Мера Шимкевича_Симпсона
    def _distance_simpson(self,A, B):
        a = set(A)
        b = set(B)
        return len(a.intersection(b)) / min(len(a), len(b))
    
    #найти похожие fingerprints
    def _get_points(self,fp1, fp2, token, hashes, grams):
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
        points.sort(key = lambda x: x[0])
        return points

    #склеить похожие fingerprints
    def _get_merged_points(self,points):
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