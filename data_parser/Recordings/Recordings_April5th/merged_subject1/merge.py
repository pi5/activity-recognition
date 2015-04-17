import sys
import json
import glob

infile = sys.argv[1]
radar_vals = {}
#radarfile = sys.argv[2]
#outfile = sys.argv[3]


def get_radar_vals(f):
    fp = open(f, 'r')
    lines = fp.readlines()
    fp.close()

    d = {}
    for line in lines:
        if len(line) > 0:
            ts = line.split(',')[0].strip()
            if len(ts) > 0:
                d[ts] = line[14:].rstrip('\n').rstrip('\r')

    return d


def getJSON (s):
    j = json.loads(s)
    return j

def get_vals_in_range(start, end):
    s = ""
    count = 0
    for x in range(start, end):
        index = str(x)
        #print radar_vals
        if index in radar_vals:
            s = s + "," + radar_vals[index]
            count = count + 1
    if count > 0:
        print "Found ", count, "values in range ", start, end
    return s


def main():
    global radar_vals
    f = open(infile, 'r')
    lines = f.readlines();
    f.close()

    for filename in glob.glob("*.txt"):
        print filename
        radar_vals = get_radar_vals(filename)
        #print radar_vals

        f = open("merged/" + filename + ".merged",'w')
        prev = 0
        curr = 0
        for line in lines:
            j = getJSON(line);
            if prev == 0:
                prev = j['timestamp']
            
            else:
                curr = j['timestamp']
                #print prev, curr
                s = get_vals_in_range(prev, curr)
                if len(s) > 0:
                    #print s
                    j['radar_data'] = s
                    t = json.dumps(j) + "\n"
                    f.write(t)
                prev = curr

        f.close()

main()

