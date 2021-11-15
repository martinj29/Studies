import os, sys


class InpTranslator:
    def __init__(self, path_to_file, model_names, verbose=1):
        assert os.path.isfile(path_to_file), f'Unable to access {path_to_file}'

        self._path = path_to_file
        self._verbose = verbose
        self._model_name = model_names

    def _read_file(self):
        with open(self._path, 'r') as inp_file:
            lines = inp_file.readlines()

        if self._verbose:
            print(f"File {self._path} : ")
            print("".join(lines))
        return lines

    def _parse(self, lines):
        lines = [line for line in lines if line[:2] != '**']
        return lines

    def _lines_to_dict(self, lines):
        d = {}
        n = len(lines)

        i = 0
        while i < n:
            if lines[i][0] == '*':
                prop_buffer = []
                j = i + 1
                while j < n and lines[j][0] != '*' :
                    prop_buffer.append(lines[j])
                    j += 1
                d[lines[i][1:]] = prop_buffer
                i = j
        return d

    def _clean_dict(self, dic):
        cleaned_dict = {}

        for head in dic:
            cleaned_head = head[0:-2]
            cleaned_values = []

            if "," in cleaned_head:
                l = cleaned_head.split(',')

                dic[l[0]] = dic[head]
                for param in l[1:]:
                    dic[l[0]].insert(0, param)
                dic.pop(head)
        a=1 #TODO Fix


    def main(self):
        lines = self._read_file()
        lines = self._parse(lines)
        mat_dict = self._lines_to_dict(lines)
        dic = self._clean_dict(mat_dict)




if __name__ == '__main__':
    inp = InpTranslator("Nitrile.inp", "Model-1")
    inp.main()
