class Seq:
    def __init__(self, strbases = None):
        self.strbases = strbases
        if self.strbases == None:
            self.strbases = 'NULL'
            print('NULL Seq created')
        else:
            if self.is_valid():
                print('New sequence created!')
            else:
                print('INVALID Seq!')
                self.strbases = 'ERROR'
                # print('Wrong character detected:', e)
    # Esta función me devuelve las bases para trabajar con ellas,
    # pero si está vacía o no es válida me cambiará la base por error


    def __str__(self):
        return self.strbases
    # Esta función me saca lo que yo haya establecido como clase Seq
    # y me lo returnea como un string para poder trabajar con él.

    def is_valid(self):
        valid = True
        i = 0
        while i < len(self.strbases) and valid:
            for e in self.strbases:
                if e != 'A' and e != 'C' and e != 'G' and e != 'T':
                    valid = False
                i += 1
        return valid
    # Aquí sí se returnean cosas. Si encuentra algo que no es válido
    # me devuelve que es falso. Sólo hago un while porque quiero parar.

    def len(self):
        length = 0
        if self.strbases != 'ERROR' and self.strbases != 'NULL':
            length = len(self.strbases)
        return length
    # Sólo me devuelve la longitud si es válido.

    def count_base(self, base):
        counter = 0
        for e in self.strbases:
            if e == base:
                counter += 1
        return counter
    #

    def count_bases(self):
        base = ['T', 'C', 'G', 'A']
        count = [0, 0, 0, 0]
        for e in self.strbases:
            if e == base[0]:
                count[0] += 1
            elif e == base[1]:
                count[1] += 1
            elif e == base[2]:
                count[2] += 1
            elif e == base[3]:
                count[3] += 1
        dict_seq = dict(zip(base, count))
        return dict_seq

    def count(self):
        base = ['T', 'C', 'G', 'A']
        count = [0, 0, 0, 0]
        for e in self.strbases:
            if e == base[0]:
                count[0] += 1
            elif e == base[1]:
                count[1] += 1
            elif e == base[2]:
                count[2] += 1
            elif e == base[3]:
                count[3] += 1
        dict_seq = dict(zip(base, count))
        return dict_seq

    def percentage(self):
        number_bases = Seq.len(self)
        base = ['T', 'C', 'G', 'A']
        count_t = 0
        count_a = 0
        count_c = 0
        count_g = 0
        per_t = ''
        per_a = ''
        per_c = ''
        per_g = ''
        per_list = []
        for e in self.strbases:
            if e == base[0]:
                count_t += 1
                per_t = str(round(count_t * 100 / number_bases, 2))+'%'
            elif e == base[1]:
                count_c += 1
                per_c = str(round(count_c * 100 / number_bases, 2))+'%'
            elif e == base[2]:
                count_g += 1
                per_g = str(round(count_g * 100 / number_bases, 2))+'%'
            elif e == base[3]:
                count_a += 1
                per_a = str(round(count_a*100/number_bases, 2))+'%'
        per_list.append(per_t)
        per_list.append(per_c)
        per_list.append(per_g)
        per_list.append(per_a)
        dict_seq = dict(zip(base, per_list))
        return dict_seq

    def reverse(self):
        if self.is_valid():
            reversed = self.strbases[::-1]
        else:
            reversed = self.strbases
        return reversed

    def complement(self):
        complement = ''
        if self.is_valid():
            for e in self.strbases:
                if e == 'A':
                    complement += 'T'
                elif e == 'T':
                    complement += 'A'
                elif e == 'C':
                    complement += 'G'
                elif e == 'G':
                    complement += 'C'
        else:
            complement = self.strbases

        return complement

    def read_fasta(self, filename):
        from pathlib import Path

        filename1 = "./sequences/" + filename.upper().replace('.txt', '') + '.txt'
        # print('current directory: ', Path.cwd())

        file_contents = Path(filename1).read_text()
        list_contents = file_contents.split('\n')
        header = list_contents[0]
        sequence = ''
        for e in range(1, len(list_contents)):
            sequence += list_contents[e]
        first_20 = ''
        for e in range(0, 20):
            first_20 += sequence[e]
        self.strbases = sequence
        return sequence

    def most_frequent(self, dictionary):
        if self.is_valid():
            return max(dictionary, key=dictionary.get), min(dictionary, key=dictionary.get)
        else:
            return 'ERROR', 'ERROR'
