from pdb import set_trace
import pandas as pd
import urllib3
import time
import random
import os
import numpy as np

def crawl(pidstr, topics):
    qref = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + ','.join(
        pidstr) + '&rettype=abstract&retmode=text'
    http = urllib3.PoolManager()
    req = http.request('GET', qref)
    texts = req.data.decode()
    for the_pid in pidstr:
        target = 'PMID: ' + the_pid
        ind = texts.find(target)
        text = texts[:ind]
        texts = texts[ind + len(target) + 26:]
        try:
            parts = text.split("\n\n")
        except:
            set_trace()
        title = parts[1].replace("\n", " ").replace("  ", " ")
        abs_pos = np.argmax([len(part) for part in parts])
        if abs_pos <= 1:
            abstract = ""
        else:
            abstract = parts[abs_pos].replace("\n", " ").replace("  ", " ")
        topics["Document Title"].append(title)
        topics["Abstract"].append(abstract)
    time.sleep(random.randint(5, 10))
    return topics

batchsize = 50
input = "../train_data/qrel_abs_train"
with open(input, "r") as f:
    content = f.readlines()

seen = set([file.split(".csv")[0] for file in os.listdir("../abs_data")])

topics = None
pidstr = []
pre_topic = None
for i, line in enumerate(content):
    items = line.split()
    topic = items[0]
    if topic in seen:
        continue
    pid = items[2]
    label = "yes" if items[3]=="1" else "no"
    if topic!= pre_topic:
        if type(topics) != type(None):
            topics = crawl(pidstr, topics)
            pidstr = []
            topics = pd.DataFrame(topics, columns=["Topic", "PID", "Document Title", "Abstract", "label"])
            topics.to_csv("../abs_data/"+pre_topic+".csv", index=False)
        topics = {"Topic": [], "PID": [], "Document Title": [], "Abstract": [], "label": []}
        pre_topic = topic
    pidstr.append(pid)
    topics["Topic"].append(topic)
    topics["PID"].append(pid)
    topics["label"].append(label)


    if i % batchsize == batchsize - 1:
        topics = crawl(pidstr, topics)
        pidstr = []
topics = crawl(pidstr, topics)
pidstr = []
topics = pd.DataFrame(topics, columns=["Topic", "PID", "Document Title", "Abstract", "label"])
topics.to_csv("../abs_data/" + pre_topic + ".csv", index=False)


