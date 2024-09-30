import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def detect_delimiter(line):
    possible_delimiters = [',', ';', '\t', '|']
    delimiter_counts = {delimiter: line.count(delimiter) for delimiter in possible_delimiters}
    return max(delimiter_counts, key=delimiter_counts.get)


def read_file(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        first_line = file.readline()
        delimiter = detect_delimiter(first_line)

        data = []
        file.seek(0)

        for line in file:
            # Разделяем строку и очищаем от лишних пробелов и кавычек
            row = [item.strip().replace('"', '') for item in line.split(delimiter)]

            # Если разделитель - запятая, преобразуем первый элемент в int
            if delimiter == ',':
                if row[0].isdigit():
                    row[0] = int(row[0])  # Преобразуем в int
                # Перемещаем int на первое место
                row = [row[0]] + row[1:]  # row[0] уже int

            # Если разделитель - точка с запятой, преобразуем все числовые значения в int
            elif delimiter == ';':
                # Преобразуем все числовые значения в int
                row = [int(item) if item.isdigit() else item for item in row]
                # Перемещаем int на первое место
                row = [row[1], row[0]]

            data.append(row)

    return data
