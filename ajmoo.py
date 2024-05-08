import os

num_of_logs = 0
num_of_entries = 0
num_of_error_entries = 0
directory_path = input() #Path to dataset
suffix = '.logtxt'
time_warnings =[]
is_warning = False

all_words=[]
all_words_qty=[]

def sub_time(t1, t2):
    day1 = int(t1[:2])
    day2 = int(t2[:2])
    month1 = int(t1[3:5])
    month2 = int(t2[3:5])
    year1 = int(t1[6:10])
    year2 = int(t2[6:10])
    hours1 = int(t1[11:13])
    hours2 = int(t2[11:13])
    mins1 = int(t1[15:17])
    mins2 = int(t2[15:17])
    if len(t1) == 21:
        sec1 = int(t1[19])
    else:
        sec1 = int(t1[19:21])
    if len(t2) == 21:
        sec2 = int(t2[19])
    else:
        sec2 = int(t2[19:21])
    s = (day2-day1)*24*3600 + (month2-month1)*30*24*3600 + (hours2-hours1)*3600 + (mins2 - mins1)*60 + (sec2-sec1)

    return s

def add_to_words(words):
    k = 0
    if len(words) == 0:
        return
    while words[k] != '---':
        k +=1
        if k == len(words):
            return

    for i in range(k + 1, len(words)):
        if words[i][-1] == ',':
            words[i] = words[i][:(len(words[i])-1)]
        if words[i] not in all_words:
            all_words.append(words[i])
            all_words_qty.append(1)
        else:

            all_words_qty[all_words.index(words[i])] += 1

def calc_time(time_warnings):
    times=[]
    times.append(0)
    time=0
    for i in range(1, len(time_warnings)):
        times.append(sub_time(time_warnings[0],time_warnings[i]))
    if len(time_warnings) < 6:
        return 0
    else:
        for i in range(len(time_warnings)-5):
            curr_time = times[i+5] - times[i]
            if(curr_time>time):
                time = curr_time
    return time



with os.scandir(directory_path) as main_dir:
    for a in main_dir:
        if a.is_file():
            if a.name.endswith(suffix):
                num_of_logs +=1

                file_path = os.path.join(directory_path, a.name)

                # Opening file
                with open(file_path, 'r') as file:
                    # Reading content of file as one string
                    file_content = file.read()
                    # Spliting lines of file
                    entries = file_content.split('\n')

                    # Removing empty lines of file, and picking up other info from single entry(time and if it is warning)
                    i = 0
                    while i < len(entries):
                        if not '---' in entries[i]:
                            entries.remove(entries[i])
                        else:
                            i += 1

                    for entry in entries:
                        words = entry.split(' ')
                        add_to_words(words)
                        if words[1] == 'the-warning':
                            is_warning = True
                            time_warnings.append(words[0])

                        # Adding number of entries to total num of entries
                    num_of_entries += len(entries)

                if is_warning == True:
                    num_of_error_entries += 1
                    is_warning = False
            else:
                file_path = os.path.join(directory_path, a.name)

                # Opening file
                with open(file_path, 'r') as file:
                    # Reading content of file as one string
                    file_content = file.read()
                    # Spliting lines of file
                    entries = file_content.split('\n')

                    # Removing empty lines of file, and picking up other info from single entry(time and if it is warning)
                    i=0
                    while i < len(entries):
                        if not '---' in entries[i]:
                            entries.remove(entries[i])
                        else:
                            i+=1

                    for entry in entries:
                        words = entry.split(' ')
                        add_to_words(words)
                        if words[1] == 'the-warning':
                            time_warnings.append(words[0])


        elif a.is_dir():
            with os.scandir(os.path.join(directory_path,a.name)) as sub_dir:
                for b in sub_dir:
                    if b.is_file():
                        if b.name.endswith(suffix):
                            num_of_logs += 1

                            file_path = os.path.join(directory_path, a.name, b.name)

                            # Opening file
                            with open(file_path, 'r') as file:
                                # Reading content of file as one string
                                file_content = file.read()
                                # Spliting lines of file
                                entries = file_content.split('\n')

                                # Removing empty lines of file, and picking up other info from single entry(time and if it is warning)
                                i = 0
                                while i < len(entries):
                                    if not '---' in entries[i]:
                                        entries.remove(entries[i])
                                    else:
                                        i += 1

                                for entry in entries:
                                    words = entry.split(' ')
                                    add_to_words(words)
                                    if words[1] == 'the-warning':
                                        is_warning = True
                                        time_warnings.append(words[0])

                                    # Adding number of entries to total num of entries
                                num_of_entries += len(entries)

                            if is_warning == True:
                                num_of_error_entries += 1
                                is_warning = False
                        else:
                            file_path = os.path.join(directory_path, a.name, b.name)

                            # Opening file
                            with open(file_path, 'r') as file:
                                # Reading content of file as one string
                                file_content = file.read()
                                # Spliting lines of file
                                entries = file_content.split('\n')

                                # Removing empty lines of file, and picking up other info from single entry(time and if it is warning)
                                i = 0
                                while i < len(entries):
                                    if not '---' in entries[i]:
                                        entries.remove(entries[i])
                                    else:
                                        i += 1

                                for entry in entries:
                                    words = entry.split(' ')
                                    add_to_words(words)
                                    if words[1] == 'the-warning':
                                        time_warnings.append(words[0])



#Calculating time
t = calc_time(time_warnings)

#Creating answer list with sorted the most frequent words
answer_list = []
dict_words = dict(zip(all_words,all_words_qty))
dict_view = dict_words.items()
list_words = list(dict_view)
sorted_list_words = sorted(list_words, key= lambda x : x[1], reverse=True)

ind=0
k = sorted_list_words[0][1]
for i in range(1, len(sorted_list_words)):
    if sorted_list_words[i][1] == k:
        continue
    else:
        sorted_list_words[ind:i] = sorted(sorted_list_words[ind:i], key=lambda x: x[0])
        ind = i
        k=sorted_list_words[i][1]
sorted_list_words[ind:len(sorted_list_words)] = sorted(sorted_list_words[ind:len(sorted_list_words)], key=lambda x: x[0])

if len(sorted_list_words)>5:
    for i in range(5):
        answer_list.append(sorted_list_words[i][0])
else:
    for i in range(len(sorted_list_words)):
        answer_list.append((sorted_list_words[i][0]))


print(num_of_logs)
print(num_of_entries)
print(num_of_error_entries)
for i in range(len(answer_list)):
    print(answer_list[i], end='')
    if i!=len(answer_list)-1:
        print(', ', end='')

print('\n', end='')
print(t)