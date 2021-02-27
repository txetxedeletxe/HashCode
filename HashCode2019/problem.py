import sys
def read_instance(stream=sys.stdin):
    lines = int(stream.readline())
    instance = []
    ids = {}
    for _ in range(lines):
        line = stream.readline()
        tags = line.split()[2:]
        for tag in tags:
            if tag not in ids:
                ids[tag] = len(ids)
        tags=[ids[tag]for tag in tags]
        line = (line[0], tags)
        instance.append(line)
    return instance


print(read_instance())