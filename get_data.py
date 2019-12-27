import bs4
from bs4 import BeautifulSoup
import xml
import requests

def get_price(soup):
    try:
        price = float( soup.find("div", {'class':"My(6px) Pos(r) smartphone_Mt(6px)"}).find('span').text.replace(',', '') )
    except:
        price = 'N/A'
    return price

def get_50_SMA(stats_soup):
    try:
        SMA = float( stats_soup.find_all("tr" , {"class":"Bxz(bb) H(36px) BdB Bdbc($seperatorColor)"})[4].find("td", {"class": "Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)"}).text.replace(",", '') )
    except:
        SMA ='N/A'
    return SMA

def get_200_SMA(stats_soup):
    try:
        SMA = float( stats_soup.find_all("tr" , {"class":"Bxz(bb) H(36px) BdB Bdbc($seperatorColor)"})[5].find("td", {"class": "Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)"}).text.replace(",", '') )
    except:
        SMA = 'N/A'
    return SMA

def get_open(soup):
    try:
        m_open = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[1].find('span').text.replace(',', '') )
    except:
        m_open = 'N/A'
    return m_open

def get_close(soup):
    try:
        m_close = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[0].find('span').text.replace(',', '') )
    except:
        m_close = 'N/A'
    return m_close

def get_vol(soup):
    try:
        vol = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[6].find('span').text.replace(',', '') )
    except:
        vol = 'N/A'
    return vol

