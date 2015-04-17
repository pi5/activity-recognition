import sys
import json

arr = [
    'Head',
    'RightHand',
    'Neck',
    'RightElbow',
    'RightHip',
    'LeftKnee',
    'LeftFoot',
    'LeftHip',
    'RightKnee',
    'LeftElbow',
    'LeftShoulder',
    'RightShoulder',
    'LeftHand',
    'RightFoot'
]
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

radar_vals = get_radar_vals("radar_log.txt")


def getJSON (s):
    j = json.loads(s)
    return j

def get_vals_in_range(start, end):
    s = ""
    count = 0
    for x in range(start, end):
        index = str(x)
        if index in radar_vals:
            s = s + "," + radar_vals[index]
            count = count + 1
    print "Found ", count, "values in range ", start, end
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
            if len(s) > 0:
                j['radar_data'] = s

                #Calculate and store magnitudes
                for joint in arr:
                    disp = 0
                    for coord in j['skeleton_data']['maxCartesian'][joint]:
                        print coord
                

                prev = curr
                t = json.dumps(j) + "\n"
                f.write(t)
    f.close()

main()

