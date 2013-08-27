
def create_ip_range(range_start, range_end):
    ip_range = []
    start = int(range_start[range_start.rfind('.')+1:])
    end = int(range_end[range_end.rfind('.')+1:])
    for i in range(start, end+1):
        ip = range_start[:range_start.rfind('.')+1] + str(i)
        ip_range.append(ip)
        print ip