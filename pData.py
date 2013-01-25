def processData(data):
    result = []
    for d in data:
        a = d.split(',')
        result.append(int(a[1]))
    return result
