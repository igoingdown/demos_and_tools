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
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 常量定义
BASE_TAX_FREE_SALARY = 5000  # 每月基本免税额度
DEFAULT_MONTHS = 12  # 默认计算月数

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

def find_tax_range(before_tax_income_sum: float) -> Tuple[float, float]:
    """
    根据累计收入查找对应的税率和速算扣除数
    
    Args:
        before_tax_income_sum: 累计税前收入
        
    Returns:
        Tuple[float, float]: (税率, 速算扣除数)
    """
    for k, v in salary_tax_rate_dict.items():
        if before_tax_income_sum > k:
            continue
        return v
    return salary_tax_rate_dict[max(salary_tax_rate_dict.keys())]

class SpecialDeduction:
    """专项扣除基类（三险一金）"""
    
    def __init__(self, rate: float, min_base: float, max_base: float, fee_base: float = BASE_FEE_DEFAULT):
        """
        初始化专项扣除
        
        Args:
            rate: 扣除比例
            min_base: 最低基数
            max_base: 最高基数
            fee_base: 基础费用
        """
        self.rate = rate
        self.max_base = max_base
        self.min_base = min_base
        self.fee_base = fee_base

    def get_fee(self, base: float) -> float:
        """
        计算扣除费用
        
        Args:
            base: 计算基数
            
        Returns:
            float: 扣除费用
        """
        base = max(min(base, self.max_base), self.min_base)
        fee = base * self.rate
        fee += self.fee_base
        return fee

class SpecialExpenseDeduction:
    """专项附加扣除基类"""
    
    def __init__(self, base_fee: float, is_salary: bool, valid_months: List[int]):
        """
        初始化专项附加扣除
        
        Args:
            base_fee: 基础费用
            is_salary: 是否计入工资
            valid_months: 有效月份列表
        """
        self.base_fee = base_fee
        self.is_salary = is_salary
        self.valid_months = valid_months

    def get_fee(self, month: int) -> float:
        """
        获取指定月份的扣除费用
        
        Args:
            month: 月份
            
        Returns:
            float: 扣除费用
        """
        return self.base_fee if month in self.valid_months else 0

class Calculator:
    """个税计算器"""
    
    def __init__(self,
                 raw_salary_list: List[float],
                 registered_insurance_base_list: List[float],
                 housing_fund_needed: bool = True,
                 unemployment_insurance_needed: bool = True,
                 pension_needed: bool = True,
                 medical_insurance_needed: bool = True,
                 special_expense_deduction_list: List[Dict[str, Any]] = None):
        """
        初始化计算器
        
        Args:
            raw_salary_list: 税前收入列表
            registered_insurance_base_list: 社保基数列表
            housing_fund_needed: 是否需要计算公积金
            unemployment_insurance_needed: 是否需要计算失业保险
            pension_needed: 是否需要计算养老保险
            medical_insurance_needed: 是否需要计算医疗保险
            special_expense_deduction_list: 专项附加扣除列表
        """
        print(len(raw_salary_list), len(registered_insurance_base_list))
        if len(raw_salary_list) != len(registered_insurance_base_list):
            raise ValueError("税前收入列表和社保基数列表长度必须相同")

        self.raw_salary_list = raw_salary_list
        self.registered_insurance_base_list = registered_insurance_base_list
        self.result = []

        # 初始化三险一金计算器
        self.unemployment_insurance = SpecialDeduction(
            UNEMPLOYMENT_INSURANCE_RATE,
            MIN_BASE_UNEMPLOYMENT_INSURANCE,
            MAX_BASE_UNEMPLOYMENT_INSURANCE
        )
        self.pension = SpecialDeduction(
            PENSION_RATE,
            MIN_BASE_PENSION_INSURANCE,
            MAX_BASE_PENSION_INSURANCE
        )
        self.medical_insurance = SpecialDeduction(
            MEDICAL_INSURANCE_RATE,
            MIN_BASE_MEDICAL_INSURANCE,
            MAX_BASE_MEDICAL_INSURANCE,
            fee_base=BASE_FEE_MEDICAL
        )
        self.housing_fund = SpecialDeduction(
            HOUSING_FUND_RATE,
            MIN_BASE_HOUSING_FUND,
            MAX_BASE_HOUSING_FUND
        )

        self.housing_fund_needed = housing_fund_needed
        self.unemployment_insurance_needed = unemployment_insurance_needed
        self.pension_needed = pension_needed
        self.medical_insurance_needed = medical_insurance_needed

        # 初始化专项附加扣除
        self.special_expense_deduction_list = []
        if special_expense_deduction_list:
            for item in special_expense_deduction_list:
                self.special_expense_deduction_list.append(
                    SpecialExpenseDeduction(
                        item["base_fee"],
                        item["is_salary"],
                        item["valid_months"]
                    )
                )

    def calculate_tax_sum(self, cur_month: int) -> Tuple[int, int]:
        """
        计算累计税费
        
        Args:
            cur_month: 当前月份
            
        Returns:
            Tuple[int, int]: (累计税费, 累计税后收入)
        """
        result_item = [cur_month]
        before_tax_income_sum = sum(self.raw_salary_list[:cur_month])
        result_item.append(before_tax_income_sum)

        # 计算各项保险费用
        pension_fee = sum([self.pension.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]]) if self.pension_needed else 0
        before_tax_income_sum -= pension_fee
        result_item.append(pension_fee)

        unemployment_insurance_fee = sum([self.unemployment_insurance.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]]) if self.unemployment_insurance_needed else 0
        before_tax_income_sum -= unemployment_insurance_fee
        result_item.append(unemployment_insurance_fee)

        medical_insurance_fee = sum([self.medical_insurance.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]]) if self.medical_insurance_needed else 0
        before_tax_income_sum -= medical_insurance_fee
        result_item.append(medical_insurance_fee)

        housing_fund_fee = sum([self.housing_fund.get_fee(x) for x in self.registered_insurance_base_list[:cur_month]]) if self.housing_fund_needed else 0
        before_tax_income_sum -= housing_fund_fee
        result_item.append(housing_fund_fee)

        after_tax_income_sum = before_tax_income_sum

        # 计算专项附加扣除
        special_deduction_sum = 0
        for special_expense_deduction in self.special_expense_deduction_list:
            deduction_value = sum([special_expense_deduction.get_fee(x + 1) for x in range(cur_month)])
            special_deduction_sum += deduction_value
            before_tax_income_sum -= deduction_value
            if not special_expense_deduction.is_salary:
                after_tax_income_sum -= deduction_value
        result_item.append(special_deduction_sum)

        # 计算免税额度
        tax_free_sum = BASE_TAX_FREE_SALARY * cur_month
        before_tax_income_sum -= tax_free_sum
        result_item.append(tax_free_sum)

        result_item.append(before_tax_income_sum)
        
        # 计算税率和税费
        rate, reduce_num = find_tax_range(before_tax_income_sum)
        result_item.append(rate)
        tax_sum = before_tax_income_sum * rate - reduce_num
        result_item.append(tax_sum)

        # 计算税后收入
        after_tax_income_sum -= tax_sum
        result_item.append(after_tax_income_sum)
        
        self.result.append(result_item)
        return int(tax_sum), int(after_tax_income_sum)

    def calculate_every_month_salary(self) -> None:
        """计算每月工资"""
        cur_tax_sum = 0
        cur_after_tax_income_sum = 0
        for i in range(len(self.raw_salary_list)):
            # 计算当月社保明细
            month = i + 1
            base = self.registered_insurance_base_list[i]
            pension_fee = self.pension.get_fee(base) if self.pension_needed else 0
            unemployment_fee = self.unemployment_insurance.get_fee(base) if self.unemployment_insurance_needed else 0
            medical_fee = self.medical_insurance.get_fee(base) if self.medical_insurance_needed else 0
            housing_fund_fee = self.housing_fund.get_fee(base) if self.housing_fund_needed else 0
            total_insurance = pension_fee + unemployment_fee + medical_fee + housing_fund_fee

            # 打印社保明细
            print(f"\n{month}月社保明细：")
            print(f"社保基数：{base:.2f}元")
            if self.pension_needed:
                print(f"养老保险：{pension_fee:.2f}元")
            if self.unemployment_insurance_needed:
                print(f"失业保险：{unemployment_fee:.2f}元")
            if self.medical_insurance_needed:
                print(f"医疗保险：{medical_fee:.2f}元")
            if self.housing_fund_needed:
                print(f"住房公积金：{housing_fund_fee:.2f}元")
            print(f"社保总计：{total_insurance:.2f}元")

            # 计算税费和税后收入
            tax_sum, after_tax_income_sum = self.calculate_tax_sum(i + 1)
            print(f"{month}月缴税{tax_sum - cur_tax_sum}￥, "
                  f"税后收入{after_tax_income_sum - cur_after_tax_income_sum}￥, "
                  f"累计收入{after_tax_income_sum}￥")
            cur_tax_sum = tax_sum
            cur_after_tax_income_sum = after_tax_income_sum
        write_csv("income.csv", result_header, self.result)

    def print_tax_curve(self) -> None:
        """绘制税收曲线图，包含累计/月度纳税额和税后收入"""
        months = [item[0] for item in self.result]
        tax_amounts = [item[10] for item in self.result]  # 总纳税额
        monthly_tax = [tax_amounts[i] - (tax_amounts[i-1] if i > 0 else 0) for i in range(len(tax_amounts))]
        after_tax_income = [item[11] for item in self.result]  # 累计税后收入
        monthly_after_tax_income = [after_tax_income[i] - (after_tax_income[i-1] if i > 0 else 0) for i in range(len(after_tax_income))]

        plt.figure(figsize=(12, 10))
        
        # 累计纳税额和累计税后收入
        plt.subplot(2, 1, 1)
        plt.plot(months, tax_amounts, marker='o', label='累计纳税额')
        plt.plot(months, after_tax_income, marker='s', label='累计税后收入')
        plt.title('个人所得税累计纳税额与累计税后收入变化曲线')
        plt.xlabel('月份')
        plt.ylabel('金额（元）')
        plt.grid(True)
        plt.legend()
        
        # 月度纳税额和月度税后收入
        plt.subplot(2, 1, 2)
        plt.bar(months, monthly_tax, label='月度纳税额', alpha=0.7)
        plt.plot(months, monthly_after_tax_income, marker='d', color='orange', label='月度税后收入')
        plt.title('月度个人所得税纳税额与税后收入')
        plt.xlabel('月份')
        plt.ylabel('金额（元）')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('tax_curve.png', dpi=300, bbox_inches='tight')
        plt.close()

def float_list(string: str) -> List[float]:
    """
    将逗号分隔的字符串转换为浮点数列表
    
    Args:
        string: 逗号分隔的字符串
        
    Returns:
        List[float]: 浮点数列表
    """
    try:
        return [float(x) for x in string.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid float value")

def parse_args() -> argparse.Namespace:
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description="个人所得税计算器")
    parser.add_argument('--raw', type=float_list, default=[58000.0, 58000.0,58000.0,58000.0,
                                                           58000.0, 58000.0, 58000.0, 58000.0, 
                                                           58000.0, 58000.0, 58000.0, 58000.0],
                      help='税前收入列表，用逗号分隔')
    parser.add_argument('--base', type=float_list, default=[35283.0] * DEFAULT_MONTHS,
                      help='社保基数列表，用逗号分隔')
    parser.add_argument('--special_deduction', type=float_list, default=[0] * DEFAULT_MONTHS,
                      help='专项附加扣除列表，用逗号分隔')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    special_expense_deduction_list = [{
        "base_fee": args.special_deduction[0],
        "is_salary": True,
        "valid_months": list(range(1, len(args.raw) + 1))
    }]

    calculator = Calculator(
        args.raw,
        args.base,
        unemployment_insurance_needed=True,
        medical_insurance_needed=True,
        special_expense_deduction_list=special_expense_deduction_list
    )
    calculator.calculate_every_month_salary()
    calculator.print_tax_curve()
