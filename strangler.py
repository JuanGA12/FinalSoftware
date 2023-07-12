import random
import urllib.request,json
import time
from tqdm import tqdm

class StranglerAPI:
    def __init__(self):
        self.load_percentage = 0.2
        self.increase_rate = 0.1

    def process_request(self, request):
        port = 6100 
        if not self.use_middleware():
            port = 6105 
        url = "http://127.0.0.1:{}/report?country={}".format(port,request)
        start_time = time.time()
        response = urllib.request.urlopen(url)
        data = response.read()
        reporte = json.loads(data)
        elapsed_time = time.time() - start_time
        return port, round(elapsed_time,2), reporte

    def use_middleware(self):
        if self.load_percentage < 1.0:
            if random.random() < self.load_percentage:
                self.load_percentage += self.increase_rate
                return False
            else:
                return True
        else:
            return False


strangler = StranglerAPI()
countrys = ["PE","CO"]
requests = [countrys[i%2] for i in range(100)]
ports=[]
file = open("output2.txt", "w")
for request in tqdm(requests):
    port, elapsed_time, reporte = strangler.process_request(request)
    ports.append(port)
    service = "Middleware" if port == 6100 else "Gateway"
    file.write(service+", Port: " +str(port)+ ", Time: " + str(elapsed_time)+" \n")
count_0 = ports.count(6100)
count_1 = ports.count(6105)
file.write("Total Middleware: " + str(count_0) + " Total Gateway: " + str(count_1))
file.close()