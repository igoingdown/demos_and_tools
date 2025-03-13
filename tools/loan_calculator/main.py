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


def commercial_loan(
    loan_principal: float,
    total_months: int,
    lpr: float,
    bp_points: float,
    current_month: int
) -> tuple[float, float]:
    """计算等额本息贷款每月应还本金和利息
    
    Args:
        loan_principal: 贷款本金
        total_months: 总还款月数
        lpr: 贷款基准利率（年利率）
        bp_points: 加点基数（1BP=0.01%）
        current_month: 当前还款月份（1-based）
    
    Returns:
        tuple[float, float]: (当月应还本金, 当月应还利息)
    """
    # 计算实际年利率（考虑基点调整）
    annual_rate = lpr + bp_points / 10000  # 修复基点转换问题
    monthly_rate = annual_rate / 12
    
    # 公共分母提取避免重复计算
    denominator = (1 + monthly_rate) ** total_months - 1
    
    # 当月应还利息
    interest = (loan_principal * monthly_rate * 
               ((1 + monthly_rate) ** total_months - 
                (1 + monthly_rate) ** (current_month - 1)) / 
               denominator)
    
    # 当月应还本金
    principal = (loan_principal * monthly_rate * 
                (1 + monthly_rate) ** (current_month - 1) / 
                denominator)
    
    return principal, interest


def format_money(num):
    return round(num, 2)

def public_savings_loan(use_public_savings: bool) -> int:
    """获取公积金贷款额度"""
    return 1603 if use_public_savings else 0


def get_loan_pay_plan(principal, total_month, lpr, bp_plus, use_public_saving_loan):
    cur_month_public_savings_loan = public_savings_loan(use_public_saving_loan)
    plan = []
    plan_header = ["month", "cur_month_total_fee", "cur_month_principal", "cur_month_interest",
                   "cur_month_commercial_loan", "cur_month_public_savings_loan",
                   "origin_principal", "left_loan_principal"]
    plan.append(plan_header)
    cur_month = total_month
    left_loan_principal = principal 
    while cur_month > 0:
        # 传入当前还款月数
        cur_month_principal, cur_month_interest = commercial_loan(principal, 
            total_month, lpr, bp_plus, total_month - cur_month + 1)
        cur_month -= 1
        left_loan_principal -= cur_month_principal
        cur_total_debt = cur_month_interest + cur_month_principal + cur_month_public_savings_loan
        cur_total_commercial_debt = cur_month_interest + cur_month_principal
        plan.append([total_month - cur_month,
                     format_money(cur_total_debt),
                     format_money(cur_month_principal),
                     format_money(cur_month_interest),
                     format_money(cur_total_commercial_debt),
                     format_money(cur_month_public_savings_loan),
                     format_money(principal),
                     format_money(left_loan_principal)])
    return plan


def parse_params():
    parser = argparse.ArgumentParser(description="脚本描述信息")
    # 添加参数
    parser.add_argument("-p", "--principal", help="贷款总金额", type=int, default=1910000)
    parser.add_argument("-m", "--month", help="还款月数", type=int, default=134)
    parser.add_argument("-r", "--rate", help="5 年期贷款LPR", type=float, default=0.0360)
    parser.add_argument("-b", "--base_point", help="额外加息 BP", type=float, default=-30)
    parser.add_argument('-f', '--forced_savings_loan', 
                        action='store_false',  # 反转存储逻辑
                        default=True,          # 设置默认值为True
                        help='是否使用公积金贷款（默认启用）')  # 更新帮助说明
    
    return parser.parse_args()


def write_csv(data):
    # 打开 csv 文件并写入数据
    with open('loan_plan.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    args = parse_params()
    loan_principal, month_num, lpr, bp_plus, use_public_saving_loan = args.principal, args.month, \
        args.rate,args.base_point, args.forced_savings_loan
    cur_month_principal, cur_month_interest = commercial_loan(loan_principal, month_num, lpr, bp_plus, 1)
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
