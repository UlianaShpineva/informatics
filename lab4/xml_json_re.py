import time
import re

# <?xml version="1.0" encoding="UTF-8"?>


class XmlParser:
    out = ''

    def __init__(self, xml_str):
        self.xml = ''.join([i.strip() for i in xml_str.split('\n')])

    def to_json(self):
        self.out = ''
        self.__find_sub(self.xml)
        return self.out

    def __find_sub(self, line: str, tabs=0, start=True):
        tag, info, rest = self.__match_tag(line)
        tags_in_info, tags_in_rest = self.__has_tag(info), self.__has_tag(rest)

        self.out += '    ' * tabs

        if not tags_in_info and not tags_in_rest:
            self.out += '"' + tag + '": ' + '"' + info + '"' + '\n'

        if not tags_in_info and tags_in_rest:

            if self.__get_tag(rest) == tag:
                self.out += '"' + tag + '": [\n'
                cnt = 0
                len_info = len(self.__get_list(line))
                for i in self.__get_list(line):
                    cnt += 1
                    if cnt < len_info:
                        self.out += '    ' * (tabs + 1) + '"' + i + '"' + ',\n'
                    else:
                        self.out += '    ' * (tabs + 1) + '"' + i + '"' + '\n'
                self.out += '    ' * tabs + ']\n'
                return

            self.out += '"' + tag + '": ' + '"' + info + '"' + ',\n'
            self.__find_sub(rest, tabs, start=False)
            return

        if tags_in_info and not tags_in_rest and not start:
            self.out += '"' + tag + '": {\n'
            self.__find_sub(info, tabs + 1, start=False)
            self.out += '    ' * tabs + '}\n'

        if tags_in_info and not tags_in_rest and start:
            self.out += '{\n' + '    ' * (tabs + 1) + '"' + tag + '": {\n'
            self.__find_sub(info, tabs + 2, start=False)
            self.out += '    ' * (tabs + 1) + '}\n'
            self.out += '}\n'

        if tags_in_info and tags_in_rest:
            if self.__get_tag(rest) == tag:
                first_tag = True
                cnt2 = 0
                len_info2 = len(self.__get_list(line))
                for element in self.__get_list(line):
                    cnt2 += 1
                    if first_tag:
                        self.out += '"' + tag + '": [\n' + '    ' * (tabs + 1) + '{\n'
                        first_tag = False
                    else:
                        self.out += '    ' * (tabs + 1) + '{\n'
                    self.__find_sub(element, tabs + 2, start=False)
                    if cnt2 < len_info2:
                        self.out += '    ' * (tabs + 1) + '},\n'
                    else:
                        self.out += '    ' * (tabs + 1) + '}\n' + '    ' * tabs + ']\n'
                return
            self.out += '"' + tag + '": {\n'
            self.__find_sub(info, tabs + 1, start=False)
            self.out += '    ' * tabs + '},\n'
            self.__find_sub(rest, tabs, start=False)

    @staticmethod
    def __get_list(line):
        return [i[1] for i in re.findall(r'<(\b\w+\b[\w]*)>(.*?)</\1>', line, flags=re.S)]

    @staticmethod
    def __has_tag(line):
        return bool(re.search(r'<(?P<tag>\b\w+\b)[\w]*>\s?(?P<info>.*?)</\1>', line, flags=re.S))

    @staticmethod
    def __get_tag(line):
        return re.search(r'<(?P<tag>\b\w+\b)[\w]*>', line, flags=re.S).group("tag")

    @staticmethod
    def __match_tag(line):
        matched = re.search(r'<(?P<tag>\b\w+\b)[\w]*>\s?(?P<info>.*?)</\1>\s?(?P<rest>.*)', line, flags=re.S)
        tag = matched.group("tag")
        info = re.sub('^\s{0,4}\t?', '', matched.group("info"), flags=re.M)
        rest = matched.group("rest")
        return tag, info, rest


if __name__ == '__main__':
    start_time = time.time()
    for i in range(100):
        with open("myxml.xml", "r", encoding="utf8") as input_file:
            parser_xml = XmlParser(input_file.read())
            with open('myjson_re.json', 'w', encoding="utf16") as out_file:
                out_file.write(parser_xml.to_json())
    print(time.time() - start_time)
# 0.17173457145690918
