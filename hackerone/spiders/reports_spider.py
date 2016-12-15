import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from hackerone.items import HackeroneItem

class ReportSpider(scrapy.Spider):
  name = "reports"
  start_urls = [
      'https://h1.sintheticlabs.com/'
  ]

  def __init__(self):
    self.driver = webdriver.Firefox()
    self.report_selector = Selector(text = "")

  def parse(self, response):
    report_urls = response.xpath('//tbody/tr/td[3]/a/@href').extract()
    item = HackeroneItem()
    for report_url in report_urls[1:]:
      self.driver.get(report_url)
      #Sleep for few moments so that webpage gets loaded properly otherwise content won't come up
      time.sleep(2)
      self.report_selector = Selector(text = self.driver.page_source)
      item = self.parseReport()
      if item != None:
        yield item
    #Everything is over and browser whould be quit
    self.driver.quit()

  def parseReport(self):

    print("Report called")
    #Check whether report is duplicate
    if self.report_selector.xpath('//i[contains(@class, "duplicate")]').extract_first() != None:
      self.log("Found a duplicate report")
      return None

    hid = self.get_hid()
    reward = self.get_reward()
    submission_date = self.get_submission_date()
    ending_date = self.get_end_date()
    vuln_type = self.get_vuln_type()
    severity = self.get_severity()

    item = HackeroneItem()
    item['hid'] = hid
    item['reward'] = reward
    item['submission_date'] = submission_date
    item['resolved_date'] = ending_date
    item['vuln_type'] = vuln_type
    item['severity'] = severity
    return item

  def get_hid(self):
    hid = self.report_selector.xpath("//div[@class='report-status']/a/text()[2]").extract_first()
    return hid

  def get_reward(self):
    reward = self.report_selector.xpath("//tr[contains(@class, 'bounty-amount')]/td/text()").extract()
    if (len(reward) == 0):
      reward = 0
    else:
      reward = float(reward[0][1:].replace(',', ''))
      #Typecasting reward to float first so that it can handle decimal
      reward = int(reward)
    return reward

  def get_submission_date(self):
    submission_date = self.report_selector.xpath("//span[contains(@class,'spec-timestamp')]/span/@title").extract_first()
    return submission_date

  def get_end_date(self):
    ending_date = self.report_selector.xpath("//div[contains(@data-activity, 'BugResolved')]/div[4]/div/span/@title").extract_first()
    if ending_date == None:
      ending_date = self.report_selector.xpath("//div[contains(@data-activity, 'BugInformative')]/div[4]/div/span/@title").extract_first()
      #TODO Construct better way to find reasons for non-existant end_date
    return ending_date

  def get_vuln_type(self):
    vuln_type = self.report_selector.xpath("//tr[contains(@class, 'vuln-types')]/td[2]/text()").extract()
    vuln_type = ','.join(vuln_type)
    return vuln_type

  def get_severity(self):
    severity = self.report_selector.xpath("//span[contains(@class, 'severity')]/text()").extract_first()
    return severity