import speedtest


class Speed:
    def __init__(self):
        self.resultspeed = {}

    def test(self):
        print("Start SpeedTest...")
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        self.res = s.results.dict()
        # Print all information - Test
        # print(res)
        return self.res["download"], self.res["upload"], self.res["ping"], self.res["server"], self.res["client"]
        # return res

    def main(self):
        for i in range(1):
            self.d, self.u, self.p, self.s, self.c = self.test()
            #self.resultspeed = self.test()
            # print('\nResult Test #{}\n'.format(i+1))
            #print('Download: {} Mbps'.format(str(d)[:2]))
            #print('Upload: {} Mbps'.format(str(u)[:2]))
            #print('Latency: {:.0f} ms\n'.format(p))
            #print('Server Information:')
            #print('Local: {}'.format(s["name"]))
            #print('Country: {}'.format(s["country"]))
            #print('Sponsor: {}'.format(s["sponsor"]))
            #print('Host: {}\n'.format(s["host"]))
            #print("Client Information:")
            #print('IP: {}'.format(c["ip"]))
            #print('ISP: {}'.format(c["isp"]))
            #print('ISP Rating: {}\n'.format(c["isprating"]))
            # return self.resultspeed
            return self.d, self.u, self.p, self.s, self.c

# if __name__ == '__main__':
#    main()
