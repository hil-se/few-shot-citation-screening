from pdb import set_trace
import pandas as pd
import urllib3
import time
import random


batchsize = 50
input = "../train_data/qrel_abs_train"
with open(input, "r") as f:
    content = f.readlines()

topics = {"Topic": [], "PID": [], "Document Title": [], "Abstract": [], "label": []}
pidstr = []
for i, line in enumerate(content):
    items = line.split()
    topic = items[0]
    pid = items[2]
    label = "yes" if items[3] else "no"
    topics["Topic"].append(topic)
    topics["PID"].append(pid)
    topics["label"].append(label)

    pidstr.append(pid)
    if i % batchsize == batchsize - 1 or i == len(content) - 1:
        qref = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + ','.join(
            pidstr) + '&rettype=abstract&retmode=text'
        http = urllib3.PoolManager()
        req = http.request('GET', qref)
        texts = req.data.decode()
        for the_pid in pidstr:
            target = 'PMID: ' + the_pid
            ind = texts.find(target)
            text = texts[:ind]
            texts = texts[ind+len(target)+26:]
            try:
                title = text.split("\n\n")[1].replace("\n"," ").replace("  "," ")
            except:
                set_trace()
            abstract = text.split("\n\n")[3].replace("\n"," ").replace("  "," ")
            topics["Document Title"].append(title)
            topics["Abstract"].append(abstract)
        pidstr = []
        time.sleep(random.randint(5,10))
topics = pd.DataFrame(topics, columns = ["Topic", "PID", "Document Title", "Abstract", "label"])
topics.to_csv("../abs_data/qrel_abs_train.csv",index=False)
