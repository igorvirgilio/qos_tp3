import speedtest


def test():
    print("Start SpeedTest...")
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    # Print all information - Test
    #print(res)
    return res["download"], res["upload"], res["ping"], res["server"], res["client"]


def main():
    for i in range(1):
        d, u, p, s, c = test()
        print('\nResult Test #{}\n'.format(i+1))
        print('Download: {} Mbps'.format(str(d)[:2]))
        print('Upload: {} Mbps'.format(str(u)[:2]))
        print('Latency: {:.0f} ms\n'.format(p))
        print('Server Information:')
        print('Local: {}'.format(s["name"]))
        print('Country: {}'.format(s["country"]))
        print('Sponsor: {}'.format(s["sponsor"]))
        print('Host: {}\n'.format(s["host"]))
        print("Client Information:")
        print('IP: {}'.format(c["ip"]))
        print('ISP: {}'.format(c["isp"]))
        print('ISP Rating: {}\n'.format(c["isprating"]))



if __name__ == '__main__':
    main()
