#!/usr/bin/python3


'''
等额本息计算公式
每月还款额=贷款本金×[月利率×（1+月利率）^还款月数]÷[（1+月利率）^还款月数-1]

总支付利息：总利息=还款月数×每月月供额-贷款本金

每月应还利息=贷款本金×月利率×〔(1+月利率)^还款月数-(1+月利率)^(还款月序号-1)〕÷〔(1+月利率)^还款月数-1〕

每月应还本金=贷款本金×月利率×(1+月利率)^(还款月序号-1)÷〔(1+月利率)^还款月数-1〕

总利息=还款月数×每月月供额-贷款本金
'''


import numpy as np


def loan(loan_principal, loan_term, yearly_interest_rate):
    """ calculate multi num about a loan depend on args.

    Args:
        loan_principal: The principal of a loan.
        loan_term: Num of months of the loan.
        yearly_interest_rate: Interest rate every year, if LPR is used, this method can not give a predict result.

    Returns:
        A loan detail struct.
    """
    monthly_interest_rate = np.exp(np.log(yearly_interest_rate + 1) / 12) - 1
    monthly_payment = loan_principal * (monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term)) / \
                      ((1 + monthly_interest_rate) ** (loan_term - 1))

    print(monthly_interest_rate)
    print(np.exp(np.log(1.05)/12))
    print(monthly_payment)


if __name__ == "__main__":
    loan(2430000, 25*12, 0.049)
