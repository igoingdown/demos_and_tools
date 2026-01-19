import unittest
import sys
import os
from unittest.mock import MagicMock

# Mock matplotlib to allow running tests in environments without it
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()

# Add support for direct execution
try:
    from tools.income_calculator.calculate import Calculator, SpecialDeduction, SpecialExpenseDeduction
    from tools.income_calculator.config_loader import load_config
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from tools.income_calculator.calculate import Calculator, SpecialDeduction, SpecialExpenseDeduction
    from tools.income_calculator.config_loader import load_config

class TestCalculator(unittest.TestCase):
    def setUp(self):
        # 加载默认配置
        self.config = load_config()
        
        # 使用新的默认收入列表
        self.raw_salary_list = [55688.0, 52000.0, 82020.0, 58000.0, 58000.0, 58000.0, 
                               58000.0, 58000.0, 58000.0, 58000.0, 58000.0, 58000.0]
        self.registered_insurance_base_list = [35000.0] * 12
        self.special_expense_deduction_list = [{
            "base_fee": 1500,
            "is_salary": True,
            "valid_months": list(range(1, 13))
        }]
        self.calculator = Calculator(
            self.config,
            self.raw_salary_list,
            self.registered_insurance_base_list,
            unemployment_insurance_needed=True,
            medical_insurance_needed=True,
            special_expense_deduction_list=self.special_expense_deduction_list
        )

    def test_special_deduction(self):
        """测试专项扣除计算，覆盖边界"""
        deduction = SpecialDeduction(0.08, 1000, 10000)
        # 正常区间
        self.assertEqual(deduction.get_fee(5000), 5000*0.08)
        # 低于最低基数，应该用min_base
        self.assertEqual(deduction.get_fee(500), 1000*0.08)
        # 高于最高基数，应该用max_base
        self.assertEqual(deduction.get_fee(15000), 10000*0.08)
        # fee_base 非0
        deduction2 = SpecialDeduction(0.1, 1000, 2000, fee_base=50)
        self.assertEqual(deduction2.get_fee(1500), 1500*0.1+50)
        # 负数基数
        self.assertEqual(deduction2.get_fee(-100), 1000*0.1+50)

    def test_special_expense_deduction(self):
        """测试专项附加扣除计算，覆盖边界"""
        deduction = SpecialExpenseDeduction(1500, True, [1, 2, 3])
        self.assertEqual(deduction.get_fee(1), 1500)
        self.assertEqual(deduction.get_fee(4), 0)
        # 负数月份
        self.assertEqual(deduction.get_fee(-1), 0)
        # 空valid_months
        deduction2 = SpecialExpenseDeduction(1000, False, [])
        self.assertEqual(deduction2.get_fee(1), 0)

    def test_calculate_tax_sum(self):
        """测试税费计算，覆盖异常"""
        tax_sum, after_tax_income = self.calculator.calculate_tax_sum(1)
        self.assertIsInstance(tax_sum, int)
        self.assertIsInstance(after_tax_income, int)
        self.assertGreater(tax_sum, 0)
        self.assertLess(after_tax_income, self.raw_salary_list[0])
        # 异常：长度不一致
        with self.assertRaises(ValueError):
            Calculator(self.config, [10000], [10000, 10000])

    def test_calculate_every_month_salary(self):
        """测试每月工资计算"""
        self.calculator.calculate_every_month_salary()
        # 验证结果列表不为空
        self.assertGreater(len(self.calculator.result), 0)
        # 12个月
        self.assertEqual(len(self.calculator.result), 12)
        # 验证第一个月的收入是否正确
        first_month = self.calculator.result[0]
        self.assertEqual(first_month[1], self.raw_salary_list[0])  # 总税前收入
        self.assertGreater(first_month[10], 0)  # 总纳税额
        self.assertLess(first_month[11], first_month[1])  # 总税后收入小于税前收入

    def test_full_year_tax_curve(self):
        """测试税收曲线图生成"""
        # 由于 matplotlib 被 mock，这里我们只验证 savefig 是否被调用
        # 需要获取 mock 对象
        import matplotlib.pyplot as plt
        
        self.calculator.calculate_every_month_salary()
        self.calculator.print_tax_curve()
        
        # 验证 savefig 被调用
        if isinstance(plt, MagicMock):
             plt.savefig.assert_called()
        else:
             # 如果不是 mock (例如在有 matplotlib 的环境中运行)，则检查文件
             import os
             self.assertTrue(os.path.exists('tax_curve.png'))
             if os.path.exists('tax_curve.png'):
                 os.remove('tax_curve.png')

if __name__ == '__main__':
    unittest.main()
