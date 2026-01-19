#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   计算新个税下的个人收入所需的常量列表。
WARNING: 此文件已弃用 (Deprecated)。新的配置系统使用 default_config.json 和 config_loader.py。
请勿在新代码中引用此文件。
===============================================================================
"""

# DEPRECATED: Use config_loader.py instead


# MIN_BASE_PENSION_INSURANCE 养老保险的缴纳基数下限
MIN_BASE_PENSION_INSURANCE = 3613
# MAX_BASE_PENSION_INSURANCE 养老保险的缴纳基数上限
MAX_BASE_PENSION_INSURANCE = 35283
# PENSION_RATE 养老保险的个人缴纳比例
PENSION_RATE = 0.08


# MIN_BASE_UNEMPLOYMENT_INSURANCE 失业保险的缴纳基数下限
MIN_BASE_UNEMPLOYMENT_INSURANCE = 3613
# MIN_BASE_UNEMPLOYMENT_INSURANCE 失业保险的缴纳基数上限
MAX_BASE_UNEMPLOYMENT_INSURANCE = 35283 
# UNEMPLOYMENT_INSURANCE_RATE 失业保险的个人缴纳比例
UNEMPLOYMENT_INSURANCE_RATE = 0.005


# MIN_BASE_MEDICAL_INSURANCE 医疗保险的缴纳基数下限
MIN_BASE_MEDICAL_INSURANCE = 5360
# MAX_BASE_MEDICAL_INSURANCE 医疗保险的缴纳基数上限
MAX_BASE_MEDICAL_INSURANCE = 35283
# MEDICAL_INSURANCE_RATE 医疗保险的个人缴纳比例
MEDICAL_INSURANCE_RATE = 0.02


# MIN_BASE_HOUSING_FUND 住房公积金的缴纳基数下限
MIN_BASE_HOUSING_FUND = 2200
# MAX_BASE_HOUSING_FUND 住房公积金的缴纳基数上限
MAX_BASE_HOUSING_FUND = 35283
# HOUSING_FUND_RATE 住房公积金个人缴纳比例
HOUSING_FUND_RATE = 0.12


# BASE_FEE_DEFAULT 除医疗保险外四险一金最低缴纳金额
BASE_FEE_DEFAULT = 0
# BASE_FEE_MEDICAL 医疗保险最低缴纳金额
BASE_FEE_MEDICAL = 3


# tax_free_house_rent_allowance 个税租房专项减免单月金额
tax_free_house_rent_allowance = 1500
# annual_tax_free_house_rent_allowance 个税租房专项减免全年总金额上限
annual_tax_free_house_rent_allowance = 12000


# base_tax_free_salary 个税起征点月薪
base_tax_free_salary = 5000.0


# salary_tax_rate_dict a dict for limit to tax rage and reduce num
salary_tax_rate_dict = {
    36000.0: (0.03, 0),
    144000.0: (0.1, 2520),
    300000.0: (0.2, 16920),
    420000.0: (0.25, 31920),
    660000.0: (0.3, 52920),
    960000.0: (0.35, 85920),
    100000000000000000: (0.45, 181920)
}

# new_salary_tax_rate_dict a dict for limit to tax rage and reduce num
new_salary_tax_rate_dict = {
    0: (0, 0),
    36000.0: (0.03, 0),
    144000.0: (0.1, 2520),
    300000.0: (0.2, 16920),
    420000.0: (0.25, 31920),
    660000.0: (0.3, 52920),
    960000.0: (0.35, 85920),
    100000000000000000: (0.45, 181920)
}