import sys
import json

def get_radar_vals(f):
    fp = open(f, 'r')
    lines = fp.readlines()
    fp.close()

    d = {}
    for line in lines:
        ts = line.split(',')[0].strip()
        d[ts] = line[15:].rstrip('\n').rstrip('\r')

    return d

radar_vals = get_radar_vals("radar_log.txt")


def getJSON (s):
    j = json.loads(s)
    return j

def get_vals_in_range(start, end):
    s = ""
    count = 0
    for x in range(start, end):
        try:
            s = s + "," + radar_vals[x]
            count = count + 1
        except:
            pass
    print "Copied ", count, "values in range ", start, end
    return s

def main():
    f = open("log.txt", 'r')
    lines = f.readlines();
    f.close()

    f = open("merged_log.txt",'w')
    prev = 0
    curr = 0
    for line in lines:
        j = getJSON(line);
        if prev == 0:
            prev = j['timestamp']
        
        else:
            curr = j['timestamp']
            s = get_vals_in_range(prev, curr)
            j['radar_data'] = s
            vals = get_vals_in_range (prev, curr)
            prev = curr
            #print j
            #with open('data.txt', 'a') as outfile:
            t = json.dumps(j) + "\n"
            f.write(t)
    f.close()




#print radar_vals
main()

