#!/usr/bin/python
import urllib2
import re
import datetime
import csv
import getopt
import sys
import os

re_tag = re.compile('</?\w+[^>]*>')
options = {"path": ""}


class Spider(object):
    def __init__(self):
        self.url = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=dividends&begindate=%(date)s"

    def td_date(self, td):
        date_data = re_tag.sub("", td).replace("&#x2F;", " ").split()
        date_data = date_data[-1:] + date_data[:-1]
        return "-".join(date_data)

    def deal_tr(self, tr):
        item_data = {}
        tds_data = re.findall('<td.*?</td>', tr, re.S)
        company_data = re.findall('<strong.*?</strong>', tr, re.S)[0].replace("&#x20;", " ")
        item_data["company"] = re_tag.sub("", company_data)
        website_data = re.findall('<span.*?</span>', tr, re.S)
        if len(website_data) == 0:
            website_data = ""
            symbol_data = re_tag.sub("", tds_data[0])
            symbol_data = re.sub(r'\n|\t', '', symbol_data)
        else:
            website_data = website_data[0]
            website_data = re.findall("\(.*?\)", website_data, re.S)[0].split(',')[1]. \
                replace('\'', '').replace(')', '')
            symbol_data = re.findall('<a.*?</a>', tds_data[0], re.S)[0]

        item_data["website"] = re_tag.sub("", website_data)
        item_data["symbol"] = re_tag.sub("", symbol_data)
        item_data["dividend"] = re_tag.sub("", tds_data[1])
        item_data["anouncement_date"] = self.td_date(tds_data[2])
        item_data["record_date"] = self.td_date(tds_data[3])
        item_data["ex_date"] = self.td_date(tds_data[4])
        item_data["pay_date"] = self.td_date(tds_data[5])
        return item_data

    def deal_tbody(self, tr_arr_content):
        data_list = []
        for tr_date in tr_arr_content:
            data_list.append(self.deal_tr(tr_date))
        return data_list

    def generate_date(self):
        date_list = []
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        day_range = 30
        for i in range(day_range):
            cur_date = datetime.datetime(year, month, day) + datetime.timedelta(days=i)
            cur_date = cur_date.strftime('%m/%d/%Y')
            date_list.append(cur_date)
        return date_list

    def get_day_data(self, date):
        response = urllib2.urlopen(self.url % ({"date": date})).read()
        if "No Dividends for this date" in response:
            return []
        table_content = \
        re.findall('<table class="datatable-component events-calender-table-three".*?</table>',
                   response, re.S)[0]
        body_content = re.findall('<tbody.*?</tbody>', table_content, re.S)[0]
        tr_arr_content = re.findall('<tr.*?</tr>', body_content, re.S)
        return self.deal_tbody(tr_arr_content)

    def create_csv_file(self):
        date_list = self.generate_date()
        file_name = os.path.join(options["path"], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.csv"))
        with open(file_name, "wb") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["company", "website", "symbol", "dividend", "anouncement_date", "record_date",
                 "ex_date", "pay_date"])
            for date in date_list:
                print("Crawling date: %s" % date)
                day_data = self.get_day_data(date)
                for line in day_data:
                    writer.writerows([[line["company"], line["website"], line["symbol"],
                                       line["dividend"], line["anouncement_date"],
                                       line["record_date"], line["ex_date"], line["pay_date"]]])
        print("Save csv file in %s" % file_name)


def printUsage():
    print ('''usage: spider -o <path>''')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:",["path="])
    except getopt.GetoptError:
        print('usage: spider -o <path>')
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            exit(0)
        elif opt in ("-o", "--output"):
            options["path"] = arg
            if not os.path.exists(options["path"]):
                print("The path: %s is not exist" % options["path"])
                exit(-1)
    if options["path"] == "":
        print("Please specify the output path")
        printUsage()
        exit(-1)
    spider = Spider()
    spider.create_csv_file()


if __name__ == '__main__':
    main()