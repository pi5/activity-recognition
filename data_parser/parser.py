import sys
import json
import math

def getJSON (s):
    j = json.loads(s)
    return j
    
    
def parsefile (s):
    f = open(s,'r')
    lines = f.readlines()
    f.close()

    arr = {
        'Head':[],
        'RightHand':[],
        'Neck':[],
        'RightElbow':[],
        'RightHip':[],
        'LeftKnee':[],
        'LeftFoot':[],
        'LeftHip':[],
        'RightKnee':[],
        'LeftElbow':[],
        'LeftShoulder':[],
        'RightShoulder':[],
        'LeftHand':[],
        'RightFoot':[],
    }

    for idx,line in enumerate(lines):
        j = getJSON(line)
        #print json.dumps(j, sort_keys=True, indent=4, separators=(',', ': '))
        for joint in j['skeleton_data']['skeleton']:
            disp = 0
            for i in range(0,3):
                print "\t", joint, "\t", j['skeleton_data']['skeleton'][joint][i], "\t", j['skeleton_data']['maxCartesian'][joint][i] 
                disp = disp + math.pow(j['skeleton_data']['maxCartesian'][joint][i], 2)
                
            arr[joint].append([idx,disp])

    print arr
    with open('Visualization/max_displacement.json','w') as outfile:
        json.dump(arr, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

    print "File max_displacement.json written: Visualization/max_displacement.json"

def main():
    f = "log.txt"
    parsefile(f)


main()
