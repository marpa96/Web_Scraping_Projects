import time
from bs4 import BeautifulSoup
import requests

print('Put in some skill you do not have')
unfamiliar_skills = input('>')
print('Filtering Out')

def Find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        job_published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in job_published_date:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skills not in skills:
                with open(f'Posts/{index}.txt', 'w') as f:
                    f.write(f'Company Name: {company_name.strip()} \n')
                    f.write(f'Required Skills: {skills.strip()} \n')
                    f.write(f'More Info: {more_info}')
                    f.write(' ')
                print(f'File Saved as {index}.txt')

if __name__ == '__main__':
    while True:
        Find_jobs()
        time_wait = .1
        print(f'Waiting {time_wait} minute(s)')
        time.sleep(time_wait * 60)
