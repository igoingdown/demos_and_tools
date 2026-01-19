#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   计算新个税下的个人收入。
===============================================================================
"""

import argparse
import csv
import os
import sys
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt

# 尝试导入，支持模块运行和直接脚本运行
try:
    from tools.income_calculator.config_loader import load_config
    from tools.income_calculator.utils import write_csv, set_chinese_font
except ImportError:
    # 如果直接运行脚本，可能找不到 tools 包，尝试添加项目根目录到 sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from tools.income_calculator.config_loader import load_config
    from tools.income_calculator.utils import write_csv, set_chinese_font

# 常量定义
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

class SpecialDeduction:
    """专项扣除基类（三险一金）"""
    
    def __init__(self, rate: float, min_base: float, max_base: float, fee_base: float = 0):
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
                 config: Dict[str, Any],
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
            config: 配置字典
            raw_salary_list: 税前收入列表
            registered_insurance_base_list: 社保基数列表
            housing_fund_needed: 是否需要计算公积金
            unemployment_insurance_needed: 是否需要计算失业保险
            pension_needed: 是否需要计算养老保险
            medical_insurance_needed: 是否需要计算医疗保险
            special_expense_deduction_list: 专项附加扣除列表
        """
        self.config = config
        
        # 数据校验
        self._validate_input(raw_salary_list, registered_insurance_base_list)

        self.raw_salary_list = raw_salary_list
        self.registered_insurance_base_list = registered_insurance_base_list
        self.result = []

        # 初始化三险一金计算器
        self.unemployment_insurance = SpecialDeduction(
            config['unemployment']['rate'],
            config['unemployment']['min'],
            config['unemployment']['max']
        )
        self.pension = SpecialDeduction(
            config['pension']['rate'],
            config['pension']['min'],
            config['pension']['max']
        )
        self.medical_insurance = SpecialDeduction(
            config['medical']['rate'],
            config['medical']['min'],
            config['medical']['max'],
            fee_base=config['medical'].get('base_fee', 0)
        )
        self.housing_fund = SpecialDeduction(
            config['housing_fund']['rate'],
            config['housing_fund']['min'],
            config['housing_fund']['max']
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

    def _validate_input(self, raw_salary: List[float], insurance_base: List[float]):
        """校验输入数据"""
        if len(raw_salary) != len(insurance_base):
            raise ValueError(f"税前收入列表长度({len(raw_salary)})和社保基数列表长度({len(insurance_base)})必须相同")
        
        for val in raw_salary:
            if val < 0:
                raise ValueError(f"税前收入不能为负数: {val}")
                
        for val in insurance_base:
            if val < 0:
                raise ValueError(f"社保基数不能为负数: {val}")

    def _find_tax_range(self, before_tax_income_sum: float) -> Tuple[float, float]:
        """根据累计收入查找对应的税率和速算扣除数"""
        tax_rates = self.config['tax_rates']
        # 假设 tax_rates 是按 limit 排序的，且最后一个 limit 是 None (无限大)
        for item in tax_rates:
            limit = item['limit']
            if limit is not None and before_tax_income_sum <= limit:
                return item['rate'], item['deduction']
            if limit is None: # 最后一个兜底
                return item['rate'], item['deduction']
        return 0.45, 181920 # Fallback

    def calculate_tax_sum(self, cur_month: int) -> Tuple[int, int]:
        """计算累计税费"""
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
        tax_free_sum = self.config['tax_threshold'] * cur_month
        before_tax_income_sum -= tax_free_sum
        result_item.append(tax_free_sum)

        result_item.append(before_tax_income_sum)
        
        # 计算税率和税费
        rate, reduce_num = self._find_tax_range(before_tax_income_sum)
        result_item.append(rate)
        tax_sum = before_tax_income_sum * rate - reduce_num
        # 税费不能小于0
        tax_sum = max(0, tax_sum)
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
        
        # 清空之前的结果，防止多次调用叠加
        self.result = []
        
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
        """绘制税收曲线图"""
        # 设置中文字体
        set_chinese_font()
        
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
    try:
        return [float(x) for x in string.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid float value")

def parse_csv_file(file_path: str) -> Tuple[List[float], List[float], List[float]]:
    """读取 CSV 文件获取收入数据"""
    raw_salary = []
    base = []
    special_deduction = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_salary.append(float(row.get('RawSalary', 0)))
            base.append(float(row.get('InsuranceBase', 0)))
            special_deduction.append(float(row.get('SpecialDeduction', 0)))
            
    return raw_salary, base, special_deduction

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="个人所得税计算器")
    parser.add_argument('--config', type=str, help='配置文件路径 (JSON)')
    parser.add_argument('--file', type=str, help='输入数据 CSV 文件路径 (包含 RawSalary, InsuranceBase, SpecialDeduction 列)')
    
    parser.add_argument('--raw', type=float_list, 
                      default=[58000.0] * DEFAULT_MONTHS,
                      help='税前收入列表，用逗号分隔 (当不使用 --file 时生效)')
    parser.add_argument('--base', type=float_list, 
                      default=[35283.0] * DEFAULT_MONTHS,
                      help='社保基数列表，用逗号分隔 (当不使用 --file 时生效)')
    parser.add_argument('--special_deduction', type=float_list, 
                      default=[0] * DEFAULT_MONTHS,
                      help='专项附加扣除列表，用逗号分隔 (当不使用 --file 时生效)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 准备数据
    if args.file:
        try:
            raw_salary, base, special_deduction_vals = parse_csv_file(args.file)
            print(f"Loaded {len(raw_salary)} records from {args.file}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            sys.exit(1)
    else:
        raw_salary = args.raw
        base = args.base
        special_deduction_vals = args.special_deduction

    # 构造专项附加扣除列表
    # 注意：这里的逻辑是将输入的 deduction 值应用到所有月份，或者如果输入是列表，则对应月份
    # 为了简化，这里假设 special_deduction_vals 每个元素对应一个月的扣除额
    # 但 Calculator 接收的是 "special_expense_deduction_list" (项目列表)，每个项目有 valid_months
    # 我们需要构建一个单一的 "通用扣除项"，它的每个月费用可能不同。
    # 遗憾的是 SpecialExpenseDeduction 类设计是 "fixed base_fee for valid_months".
    # 如果每个月不一样，我们需要创建 12 个 Deduction item，或者修改 SpecialExpenseDeduction 逻辑。
    # 为了兼容旧逻辑（旧逻辑是 args.special_deduction[0] * 12），我们看看：
    # 旧代码: "base_fee": args.special_deduction[0], "valid_months": range(1, len+1)
    # 这意味着旧代码其实只支持每个月扣一样的钱。
    # 既然我们要支持 CSV 导入每月的不同扣除，我们需要改进 SpecialExpenseDeduction 或者创建多个。
    # 让我们创建 12 个 SpecialExpenseDeduction，每个只对当月有效。
    
    special_expense_deduction_list = []
    for i, fee in enumerate(special_deduction_vals):
        if fee > 0:
            special_expense_deduction_list.append({
                "base_fee": fee,
                "is_salary": True,
                "valid_months": [i + 1] # 只对第 i+1 个月有效
            })

    try:
        calculator = Calculator(
            config,
            raw_salary,
            base,
            unemployment_insurance_needed=True,
            medical_insurance_needed=True,
            special_expense_deduction_list=special_expense_deduction_list
        )
        calculator.calculate_every_month_salary()
        calculator.print_tax_curve()
        print("\nCalculation completed. Results saved to income.csv and tax_curve.png")
    except Exception as e:
        print(f"Error during calculation: {e}")
        # import traceback; traceback.print_exc()
