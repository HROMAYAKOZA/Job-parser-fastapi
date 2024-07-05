from bs4 import BeautifulSoup
from src.parse_core import get_page, get_selenium_page
import re

def hhru_parse_job(url):
    # soup = get_page(url)
    soup = get_selenium_page(url)
    jobs = soup.findAll('div',class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS vacancy-card_clickme--Ti9glrpeP1wwAE3hAklj") + soup.findAll('div',class_="vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS")
    # i=1
    lst = []
    for job in jobs:
        title = job.find('span',class_="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link").text
        if job.find('span',class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh") is None:
            continue
        price = job.find('span',class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
        if price.find("₽")==-1:
            continue
        price = int("".join(re.findall("\\d+", price.split("–")[0])))
        expirince = job.find('span',class_="label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM").text
        match expirince:
            case "Без опыта":
                expirince=0
            case "Опыт 1-3 года":
                expirince=1
            case "Опыт 3-6 лет":
                expirince=3
            case "Опыт более 6 лет":
                expirince=6
            case "Опыт более 6\xa0лет":
                expirince=6
        company = job.find('span',class_="company-info-text--vgvZouLtf8jwBmaD1xgp")
        if company is None:
            company="Частное лицо"
        else:
            company=company.text
        addres = job.find('span',attrs={'data-qa' : "vacancy-serp__vacancy-address"}).text
        resume=False
        if job.find('span',attrs={'data-qa' : "vacancy-label-no-resume"}) is None:
            resume = True
        remote=True
        if job.find('span',attrs={'data-qa' : "vacancy-label-remote-work-schedule"}) is None:
            remote = False
        link = job.find('a',class_="bloko-link").get("href").split("?hhtmFrom")[0]
        # print(i, title,price,expirince,company,addres,resume, remote, link)
        # i+=1
        lst.append([title,price,expirince,company,addres,resume, remote, link])
    # print(*lst)
    return lst

def hhru_parse_resum(url):
    # soup = get_page(url)
    soup = get_selenium_page(url)
    resums = soup.findAll('div',attrs={"data-qa":"resume-serp__resume"})
    lst=[]
    for resum in resums:
        title = resum.find('a',attrs={"data-qa":re.compile("^serp-item__title")}).text
        # title = resum.find('a',attrs={"data-qa":"serp-item__title"}).text
        # link = resum.find('a',attrs={"data-qa":"serp-item__title"}).get("href").split("?searchRid")[0]
        link = "https://hh.ru" + resum.find('a',attrs={"data-qa":re.compile("^serp-item__title")}).get("href").split("?searchRid")[0]
        # if title is None:
        #     title = resum.find('a',attrs={"data-qa":"serp-item__title serp-item__title_marked"}).text
        #     link = resum.find('a',attrs={"data-qa":"serp-item__title serp-item__title_marked"}).get("href").split("?searchRid")[0]
        if resum.find('span',attrs={"data-qa":"resume-serp__resume-age"}) is None:
            age = None
        else:
            age = int(resum.find('span',attrs={"data-qa":"resume-serp__resume-age"}).text.split()[0])
        salary = resum.find('div',class_="bloko-text bloko-text_strong")
        # if salary is None:
        #     continue
        if not (salary is None):
            salary=int("".join(re.findall("\\d+", salary.text)))
        status = resum.find('div',class_='tags--KXWWw64qnbyyonQqClH2')
        match status:
            case None:
                pass
            case _:
                status=next(status.children).text
        experience = resum.find('div',attrs={'data-qa':'resume-serp__resume-excpirience-sum'})
        if experience is None:
            experience=0
        else:
            experience=int("".join(re.findall("\\d+", experience.text.split("лет")[0].split("год")[0])))
        last_company = resum.find('div',attrs={'data-qa':'resume-serp_resume-item-content'})
        if not (last_company is None):
            last_company = next(next(last_company.children).children).text
        # print(title, age, salary, status, experience, last_company, link)
        lst.append([title, age, salary, experience, status, last_company, link])
    # print(len(lst),"elements parsed")
    return lst


# print(hhru_parse_job("https://hh.ru/search/vacancy?text=&excluded_text=&professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=100&hhtmFrom=vacancy_search_filter"))
# print(hhru_parse_job("https://hh.ru/search/vacancy?text=&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"))

# with open("file.txt", "w", encoding="utf-8") as output:
#     output.write(str(hhru_parse_job("https://hh.ru/search/vacancy?text=&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line")))