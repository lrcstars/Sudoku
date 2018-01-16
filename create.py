import re
import random
import time
import copy


class Create(object):
    MOULD = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
        ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
        ['2', '3', '1', '5', '6', '4', '8', '9', '7'],
        ['5', '6', '4', '8', '9', '7', '2', '3', '1'],
        ['8', '9', '7', '2', '3', '1', '5', '6', '4'],
        ['3', '1', '2', '6', '4', '5', '9', '7', '8'],
        ['6', '4', '5', '9', '7', '8', '3', '1', '2'],
        ['9', '7', '8', '3', '1', '2', '6', '4', '5']
    ]

    def __init__(self):
        self.object = copy.deepcopy(Create.MOULD)
        self.target = []
        self.data_generate = []
        self.data_solve = []
        self.select = None

    def __rand(self, h, l, n):
        source = self.object[h][l]
        if source == n:
            return
        self.object[h][l] = n
        # print(h,l,'--->',n)
        for i in range(9):
            if (i != h) and (self.object[i][l] == n):
                self.__rand(i, l, source)
            if (i != l) and (self.object[h][i] == n):
                self.__rand(h, i, source)
            if (i != (h % 3)*3+(l % 3)) and (self.object[(h//3)*3+(i//3)][(l//3)*3+(i % 3)] == n):
                self.__rand((h//3)*3+(i//3), (l//3)*3+(i % 3), source)

    def generate(self, level_difficult=40, level_random=1.0):
        self.object = copy.deepcopy(Create.MOULD)
        for h in range(9):
            for l in range(9):
                if random.randint(1, int(1 / level_random)) == 1:
                    self.__rand(h, l, str(random.randint(1, 9)))
        remove_list = random.sample(range(81), level_difficult)
        for remove in remove_list:
            self.object[remove // 9][remove % 9] = '?'
        self.data_generate = self.object
        return self.data_generate

    def solve(self, data_file=None, data_list=None):
        if data_file is not None:
            self.target = self.__read_file(data_file)
        elif data_list is not None:
            self.target = data_list
        else:
            self.target = self.data_generate
        self.object = copy.deepcopy(Create.MOULD)

        count = 0
        mark = False
        while True:
            for h in range(9):
                for l in range(9):
                    if self.target[h][l] != '?' and self.target[h][l] != self.object[h][l]:
                        mark = True
                        if random.randint(1, 2) == 1:
                            continue
                        # print(h,l,'-->',create_target[h][l])
                        self.__rand(h, l, self.target[h][l])
            if not mark:
                break
            mark = False
            count += 1
            # 程序中，更新采用随机机制，如果进入死胡同，就从来吧
            if count > 50:
                self.object = copy.deepcopy(Create.MOULD)
                count = 0
        self.data_solve = self.object
        return self.data_solve

    @staticmethod
    def __read_file(path):
        create = []
        with open(path) as f:
            # 按行读取
            for line in f:
                # +号开头的行内无数据，抛弃
                if line.startswith('+'):
                    continue
                # re的分割更好用
                tmp_line = re.split('[ |]', line)
                # 分割后，头尾元素无用
                # print(tmp_line)
                del tmp_line[0]
                del tmp_line[9]  # 第二次元素少了１个
                create.append(tmp_line)
        return create

    @staticmethod
    def __make_str(data_list):
        if not data_list:
            return '请先调用方法生成数据'

        s = '+-----+-----+-----+'
        data = s + '\r\n'
        for i, line in enumerate(data_list):
            for j, x in enumerate(line):
                if j % 3 == 0:
                    data += '|'
                else:
                    data += ' '
                data += str(x)
            data += '|'
            data += '\r\n'
            if i % 3 == 2:
                data += s + '\r\n'
        return data

    @property
    def str_generate(self):
        return self.__make_str(self.data_generate)

    @property
    def str_solve(self):
        return self.__make_str(self.data_solve)

if __name__ == '__main__':
    a = Create()
    for iii in range(9):
        # print(a.str_generate)
        print(time.time())
        a.solve(data_list=a.generate())
        print(time.time())
        print(a.str_generate)
        print(a.str_solve)
        # print(a)
