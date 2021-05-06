from datetime import datetime
from os import name, stat
def cleanUp(word):
    return word.replace('"',"",word.count('"'))

def extract(sheet,fromline,impcols):
    ex = []
    try:
        for line in sheet[fromline:]:
            words = line.split(",")
            imp = []
            for colno in impcols:
                words[colno] = cleanUp(words[colno])
                imp.append(words[colno])
            ex.append(imp[:])
    except IndexError:
        return ex

def duration(start,lastseen):
    starth = start.split(":")[0]
    startm = start.split(":")[1]
    lastseenh = lastseen.split(":")[0]
    lastseenm = lastseen.split(":")[1]
    then = datetime(2021,5,5,int(starth),int(startm))
    now = datetime(2021,5,5,int(lastseenh),int(lastseenm))
    delta = now - then
    return int(divmod(delta.total_seconds(),60)[0])

def get_mapping_dict(mapsheet):
    map_dict = {}
    for row in mapsheet:
        row_data = row.split(",")
        map_dict[row_data[0]] = row_data[1:]
    return map_dict

def get_name(gmeetname):
    for key in map_dict:
        if gmeetname in map_dict[key]:
            return key
    return "Z-No Match"
data = open("data.csv","r")
sheet = data.read().splitlines()
needs = extract(sheet,4,[0,4,5])
mapping =open("mapping.csv","r")
mapsheet = mapping.read().splitlines();
map_dict = get_mapping_dict(mapsheet)

min_dur_req = 30
list_report_dict = []

report_file = open("report.csv","w")


for need in needs:
    report_dict = {}
    report_dict['name'] = get_name(need[0])
    report_dict['gmeetname'] = need[0]
    report_dict["joined"] = need[1]
    report_dict["left"] = need[2]
    report_dict["duration"] = str(duration(need[1],need[2]))+" min"
    list_report_dict.append(report_dict)

sorted_list_report_dict = []
names = []
for report in list_report_dict:
    names.append(report['name'])

names.sort()

for name in names:
    for rec in list_report_dict:
        if(name == rec['name']):
            sorted_list_report_dict.append(rec)

report_file.write(''.join(sheet[0])+"\n")
report_file.write(''.join(sheet[1])+"\n\n\n")
report_file.write("Student Name,Google Meetname,Joined,Left,Present Duration\n\n")

for reco in sorted_list_report_dict:
    line=','.join(list(reco.values()))+'\n'
    print(line)
    if(not line.startswith('Z')):
        report_file.write(line)

report_file.close()
mapping.close()
