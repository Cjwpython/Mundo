# coding: utf-8
from urllib.parse import urlparse


def is_same_netloc(base_netloc, real_url):

    real_url_netloc = urlparse(real_url).netloc
    if base_netloc != real_url_netloc:
        # print("ignore  {}:{}".format(base_netloc,real_url_netloc))
        return False
    return True


if __name__ == '__main__':
    target = "http://bh4ars.riskivy.xyz/SSTI/"
    print(urlparse(target).netloc)