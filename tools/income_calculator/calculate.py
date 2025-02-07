#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   计算新个税下的个人收入。
===============================================================================
"""

from tools.income_calculator.const import *
from tools.write_csv import write_csv
import argparse

result_header = [
    "month",
    "总税前收入",
    "养老保险个人部分总计",
    "失业保险个人部分总计",
    "医疗保险个人部分总计",
    "住房公积金个人部分总计",
    "专项附加扣除总计",
    "免税额度总计",
    "总应税收入",
    "税率",
    "总纳税额",
    "总税后收入",
]
result = []


def find_tax_range(before_tax_income_sum):
    for k, v in salary_tax_rate_dict.items():
        if before_tax_income_sum > k:
            continue
        return v


# 专项扣除: 三险一金
class SpecialDeduction(object):
    def __init__(self, rate, min_base, max_base, fee_base=BASE_FEE_DEFAULT):
        self.rate = rate
        self.max_base = max_base
        self.min_base = min_base
        self.fee_base = fee_base

    def get_fee(self, base):
        base = max(min(base, self.max_base), self.min_base)
        fee = base * self.rate
        fee += self.fee_base
        return fee


# 专项附加扣除: 子女教育, 大病医疗, 赡养老人, 继续教育, 住房贷款利息, 住房租金及其他扣除(捐赠)
class SpecialExpenseDeduction(object):
    def __init__(self, base_fee, is_salary, valid_months):
        self.base_fee = base_fee
        self.is_salary = is_salary
        self.valid_months = valid_months

    def get_fee(self, i):
        if i in self.valid_months:
            return self.base_fee
        else:
            return 0


# raw_salary: 当月税前月薪
# last_year_average_raw_salary: 去年平均月薪，每年7月更新
# housing_fund: 公积金
# pension: 养老保险
# unemployment_insurance: 失业保险
# housing_fund_fee(公积金总数) = last_year_average_raw_salary * housing_fund_rage
# taxed_salary = raw_salary - insurance_fee - housing_fund_fee - tax
# base_tax_free_salary: 每月免税金额,每月￥5000
# tax_free_salary(每月实际免税收入) = base_tax_free_salary + tax_free_allowance
# tax_free_allowance: 免税津贴,如租房个税减免
# tax_free_house_rent_allowance: 租房个税减免金额，￥1000
# donation_tax_free_salary: 捐赠个税减免
# tax: 个税
# taxed_salary: 每月税后收入
# 公积金基数上线:

class Calculator(object):
    def __init__(self,
                 raw_salary_list,
                 registered_insurance_base_list,
                 housing_fund_needed=True,
                 unemployment_insurance_needed=True,
                 pension_needed=True,
                 medical_insurance_needed=True,
                 special_expense_deduction_list=None
                 ):
        self.raw_salary_list = raw_salary_list
        self.registered_insurance_base_list = registered_insurance_base_list

        assert len(self.raw_salary_list) == len(self.registered_insurance_base_list)

        # 三险一金
        self.unemployment_insurance = SpecialDeduction(UNEMPLOYMENT_INSURANCE_RATE, MIN_BASE_UNEMPLOYMENT_INSURANCE,
                                                       MAX_BASE_UNEMPLOYMENT_INSURANCE)
        self.pension = SpecialDeduction(PENSION_RATE, MIN_BASE_PENSION_INSURANCE, MAX_BASE_PENSION_INSURANCE)
        self.medical_insurance = SpecialDeduction(MEDICAL_INSURANCE_RATE, MIN_BASE_MEDICAL_INSURANCE,
                                                  MAX_BASE_MEDICAL_INSURANCE, fee_base=BASE_FEE_MEDICAL)
        self.housing_fund = SpecialDeduction(HOUSING_FUND_RATE, MIN_BASE_HOUSING_FUND, MAX_BASE_HOUSING_FUND)

        self.housing_fund_needed = housing_fund_needed
        self.unemployment_insurance_needed = unemployment_insurance_needed
        self.pension_needed = pension_needed
        self.medical_insurance_needed = medical_insurance_needed

        # 专项附加扣除
        self.special_expense_deduction_list = []
        if special_expense_deduction_list is not None:
            for item in special_expense_deduction_list:
                self.special_expense_deduction_list.append(
                    SpecialExpenseDeduction(item["base_fee"], item["is_salary"], item["valid_months"]))

    '''
    calculate_tax_sum 计算税费总数
    '''

    def calculate_tax_sum(self, cur_month):
        result_item = [cur_month]
        before_tax_income_sum = sum(self.raw_salary_list[:cur_month])
        result_item.append(before_tax_income_sum)

        pension_fee = 0
        if self.pension_needed:
            pension_fee += sum([self.pension.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]])
            before_tax_income_sum -= pension_fee
        result_item.append(pension_fee)

        unemployment_insurance_fee = 0
        if self.unemployment_insurance_needed:
            unemployment_insurance_fee += sum([self.unemployment_insurance.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]])
            before_tax_income_sum -= unemployment_insurance_fee
        result_item.append(unemployment_insurance_fee)

        medical_insurance_fee = 0
        if self.medical_insurance_needed:
            medical_insurance_fee += sum(
                [self.medical_insurance.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]])
            before_tax_income_sum -= medical_insurance_fee
        result_item.append(medical_insurance_fee)

        housing_fund_fee = 0
        if self.housing_fund_needed:
            housing_fund_fee += sum(
                [self.housing_fund.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]])
            before_tax_income_sum -= housing_fund_fee
        result_item.append(housing_fund_fee)

        after_tax_income_sum = before_tax_income_sum

        special_deduction_sum = 0
        for special_expense_deduction in self.special_expense_deduction_list:
            deduction_value = sum([special_expense_deduction.get_fee(x + 1) for x in range(cur_month)])
            special_deduction_sum += deduction_value

            before_tax_income_sum -= deduction_value
            if not special_expense_deduction.is_salary:
                after_tax_income_sum -= deduction_value
        result_item.append(special_deduction_sum)

        tax_free_sum = base_tax_free_salary * cur_month
        before_tax_income_sum -= tax_free_sum
        result_item.append(tax_free_sum)

        result_item.append(before_tax_income_sum)
        # 查dict，找出税率和速算扣除数
        rate, reduce_num = find_tax_range(before_tax_income_sum)
        result_item.append(rate)
        tax_sum = before_tax_income_sum * rate - reduce_num
        result_item.append(tax_sum)

        # 计算税后总收入
        after_tax_income_sum -= tax_sum
        result_item.append(after_tax_income_sum)
        global result
        result.append(result_item)
        return int(tax_sum), int(after_tax_income_sum)

    '''
    calculate_every_month_salary: 给定税前收入列表，输出每月税后收入和个税
    '''

    def calculate_every_month_salary(self):
        cur_tax_sum = 0
        cur_after_tax_income_sum = 0
        for i in range(len(self.raw_salary_list)):
            tax_sum, after_tax_income_sum = self.calculate_tax_sum(i + 1)
            print("{0}月缴税{1}￥, 税后收入{2}￥, 累计收入{3}￥ ".format(i + 1, tax_sum - cur_tax_sum,
                                                           after_tax_income_sum - cur_after_tax_income_sum,
                                                           after_tax_income_sum))

            cur_tax_sum = tax_sum
            cur_after_tax_income_sum = after_tax_income_sum
        write_csv("income.csv", result_header, result)

    def print_tax_curve(self):
        # TODO: 把税收结果画成曲线图
        pass


def float_list(string):
    try:
        values = [float(x) for x in string.split(',')]
        return values
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid float value")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--my_list', type=float_list, nargs=12, default=[100.0] * 12, help='Input float list')
    args = parser.parse_args()
    return args

def parse_params():
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument('-r','--raw', type=float_list, default=[10000.0] * 12, help='raw income list')
    parser.add_argument("-b", "--base_num", type=float_list, default=[31884.0] * 12, help='base bum list')
    parser.add_argument("-f", "--base_fee", type=float_list, default=[1500.0] * 12, help='base fee list')
    parser.add_argument("-s", "--is_salary", type=float_list, default=[1500.0] * 12, help='base fee list')
    parser.add_argument("-r", "--rate", help="5 年期贷款LPR", type=float, default=0.043)
    parser.add_argument("-b", "--base_point", help="额外加息 BP", type=float, default=0.0055)
    return parser.parse_args()

if __name__ == "__main__":
    raw_salary_list = [52000] * 12
    registered_insurance_base_list = [35000] * 12
    special_expense_deduction_list = [{"base_fee": 1500, "is_salary": True, "valid_months": [i + 1 for i in range(12)]}]

    c = Calculator(raw_salary_list,
                   registered_insurance_base_list,
                   unemployment_insurance_needed=True,
                   medical_insurance_needed=True,
                   special_expense_deduction_list=special_expense_deduction_list)
    c.calculate_every_month_salary()
