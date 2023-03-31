#!/usr/bin/python3

import sys
import getopt
import csv

'''
等额本息计算公式
每月还款额=贷款本金×[月利率×（1+月利率）^还款月数]÷[（1+月利率）^还款月数-1]

总支付利息：总利息=还款月数×每月月供额-贷款本金

每月应还利息=贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕

每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕

总利息=还款月数×每月月供额-贷款本金
'''

LPR = 0.043
BP_Plus = 55*0.0001


def commercial_loan(loan_principal, month_num):
    """ calculate multi num about a loan depend on args.

    Args:
        loan_principal: The principal of a loan.
        month_num: Num of months of the loan.

    Returns:
        A loan detail struct.
    """
    yearly_interest_rate = LPR + BP_Plus
    monthly_interest_rate = yearly_interest_rate / 12
    cur_month_fee = loan_principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** month_num) / \
                      ((1 + monthly_interest_rate) ** month_num - 1)
    cur_month_interest = loan_principal * monthly_interest_rate
    cur_month_principal = cur_month_fee - cur_month_interest
    print(month_num, cur_month_principal, cur_month_interest)
    return cur_month_principal, cur_month_interest


def format_money(num):
    return round(num, 2)

def public_savings_loan():
    return 1603


def get_loan_pay_plan(principal, month):
    cur_month_public_savings_loan = public_savings_loan()
    plan = []
    plan_header = ["month", "cur_month_total_fee", "cur_month_principal", "cur_month_interest",
                   "cur_month_commercial_loan", "cur_month_public_savings_loan",
                   "origin_principal", "left_loan_principal"]
    plan.append(plan_header)
    while month > 0:
        cur_month_principal, cur_month_interest = commercial_loan(principal, month)
        origin_principal = principal
        month -= 1
        principal -= cur_month_principal
        left_loan_principal = principal
        cur_total_debt = cur_month_interest + cur_month_principal+cur_month_public_savings_loan
        cur_total_commercial_debt = cur_month_interest + cur_month_principal
        plan.append([300-month,
                     format_money(cur_total_debt),
                     format_money(cur_month_principal),
                     format_money(cur_month_interest),
                     format_money(cur_total_commercial_debt),
                     format_money(cur_month_public_savings_loan),
                     format_money(origin_principal),
                     format_money(left_loan_principal)])
    return plan


def parse_params():
    principal_str, month_num_str = "", ""
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "p:m:",
                                   ["principal=", "month="])  # 长选项模式
    except:
        print("Error")
        return int(principal_str), int(month_num_str)
    for opt, arg in opts:
        if opt in ['-p', '--principal']:
            principal_str = arg
        elif opt in ['-m', '--month']:
            month_num_str = arg
    return int(principal_str), int(month_num_str)


def write_csv(data):
    # 打开 csv 文件并写入数据
    with open('loan_plan.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    principal, month = parse_params()
    cur_month_principal, cur_month_interest = commercial_loan(principal, month)
    cur_month_public_savings_loan = public_savings_loan()
    print("total_fee:{}, cur_month_principal:{}, cur_month_interest:{}, commercial_loan:{}, public_savings_loan:{}".
          format(cur_month_principal + cur_month_interest + cur_month_public_savings_loan,
                 cur_month_principal,
                 cur_month_interest,
                 cur_month_interest + cur_month_principal,
                 cur_month_public_savings_loan))
    plan = get_loan_pay_plan(principal, month)
    write_csv(plan)


if __name__ == '__main__':
    main()
