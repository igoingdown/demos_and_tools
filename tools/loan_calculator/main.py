#!/usr/bin/python3

import csv
import argparse


'''
等额本息计算公式
每月还款额=贷款本金×[月利率×（1+月利率）^还款月数]÷[（1+月利率）^还款月数-1]

总支付利息：总利息=还款月数×每月月供额-贷款本金

每月应还利息=贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕

每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕

总利息=还款月数×每月月供额-贷款本金
'''


def commercial_loan(loan_principal, month_num, lpr, bp_plus):
    """ calculate multi num about a loan depend on args.

    Args:
        loan_principal: The principal of a loan.
        month_num: Num of months of the loan.
        lpr: lpr of a country.
        bp_plus: base point add to lpr.

    Returns:
        A loan detail struct.
    """
    yearly_interest_rate = lpr + bp_plus
    monthly_interest_rate = yearly_interest_rate / 12
    cur_month_fee = loan_principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** month_num) / \
                      ((1 + monthly_interest_rate) ** month_num - 1)
    cur_month_interest = loan_principal * monthly_interest_rate
    cur_month_principal = cur_month_fee - cur_month_interest
    # print(month_num, cur_month_principal, cur_month_interest)
    return cur_month_principal, cur_month_interest


def format_money(num):
    return round(num, 2)

def public_savings_loan(use_public_saving_loan):
    if use_public_saving_loan:
        return 1603
    else:
        return 0


def get_loan_pay_plan(principal, total_month,lpr, bp_plus, use_public_saving_loan):
    cur_month_public_savings_loan = public_savings_loan(use_public_saving_loan)
    plan = []
    plan_header = ["month", "cur_month_total_fee", "cur_month_principal", "cur_month_interest",
                   "cur_month_commercial_loan", "cur_month_public_savings_loan",
                   "origin_principal", "left_loan_principal"]
    plan.append(plan_header)
    cur_month = total_month
    while cur_month > 0:
        cur_month_principal, cur_month_interest = commercial_loan(principal, total_month, lpr, bp_plus)
        origin_principal = principal
        cur_month -= 1
        principal -= cur_month_principal
        left_loan_principal = principal
        cur_total_debt = cur_month_interest + cur_month_principal+cur_month_public_savings_loan
        cur_total_commercial_debt = cur_month_interest + cur_month_principal
        plan.append([total_month-cur_month,
                     format_money(cur_total_debt),
                     format_money(cur_month_principal),
                     format_money(cur_month_interest),
                     format_money(cur_total_commercial_debt),
                     format_money(cur_month_public_savings_loan),
                     format_money(origin_principal),
                     format_money(left_loan_principal)])
    return plan


def parse_params():
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-p", "--principal", help="贷款总金额", type=int, default=4000000)
    parser.add_argument("-m", "--month", help="还款月数", type=int, default=300)
    parser.add_argument("-r", "--rate", help="5 年期贷款LPR", type=float, default=0.043)
    parser.add_argument("-b", "--base_point", help="额外加息 BP", type=float, default=0.0055)
    parser.add_argument('-f', '--forced_savings_loan', action='store_true', help='是否使用公积金贷款')
    return parser.parse_args()


def write_csv(data):
    # 打开 csv 文件并写入数据
    with open('loan_plan.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    args = parse_params()
    loan_principal, month_num, lpr, bp_plus, use_public_saving_loan = args.principal, args.month, args.rate,args.base_point, args.forced_savings_loan
    cur_month_principal, cur_month_interest = commercial_loan(loan_principal, month_num, lpr, bp_plus)
    cur_month_public_savings_loan = public_savings_loan(use_public_saving_loan)
    print("total_fee:{}, cur_month_principal:{}, cur_month_interest:{}, commercial_loan:{}, public_savings_loan:{}".
          format(cur_month_principal + cur_month_interest + cur_month_public_savings_loan,
                 cur_month_principal,
                 cur_month_interest,
                 cur_month_interest + cur_month_principal,
                 cur_month_public_savings_loan))
    plan = get_loan_pay_plan(loan_principal, month_num, lpr, bp_plus, use_public_saving_loan)
    write_csv(plan)


if __name__ == '__main__':
    main()
