from flask import Flask, json, request
import requests, markovify, re, random, time, threading
app = Flask(__name__)
lock = threading.Lock()

class NewlineText(markovify.Text):
    def sentence_split(self, text):
        return re.split(r"\s*\n\s*", text)

with open("isis_logs_with_names.csv") as f:
    lines = []
    people = {}
    for line in f:
        if ',' in line:
            info = line.split(',',1)
            name, text = info[0], info[1]
            if name not in people:
                people[name] = []
            for i in range(3):
                people[name].append(text)
            lines.append(text)

for p in people:
    people[p] += lines

models = {}
for p in people:
    models[p] = NewlineText('\n'.join(people[p]))
print len(models)
print "chains done building"
timer = time.time()

def send_message(name, text):
    requests.post('https://api.groupme.com/v3/bots/post', data = {"text" : name + ": " + text, "bot_id" : "5cbb24cded44209a3fc9b3b292"})

@app.route('/',methods=['POST'])
def recieved_message():
    message = json.loads(request.data)
    sender_type = message['sender_type']
    sender_name = message['name']
    message_text = message['text']
    if sender_type == 'bot':
        return "Success-bot"
    for p in people:
        people[p].append(message_text)
    for i in range(3):
        people[sender_name].append(message_text)
    # if time.time() - timer > 60 * 10:
    name = random.choice(models.keys())
    message = models[name].make_sentence()
    send_message(name, message)
    if lock.acquire(blocking=False):
        for p in people:
            models[p] = NewlineText('\n'.join(people[p]))
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
