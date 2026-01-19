# 个人收入计算器 (Income Calculator)

这是一个基于 Python 的新个人所得税（累计预扣法）计算工具。它可以帮助用户计算每月的社保缴纳、个税缴纳以及最终的税后收入，并生成详细的 CSV 报表和可视化图表。

## 1. 项目更新说明 (New Features)

-   **配置分离**: 所有的社保参数、税率等现在存储在 `default_config.json` 中，用户可以通过 JSON 文件自定义配置，不再需要修改代码。
-   **CSV 导入**: 支持直接导入包含每月收入详情的 CSV 文件，无需在命令行输入长串数字。
-   **模块独立**: 移除了对外部 `write_csv` 模块的依赖，工具现在可以独立运行。
-   **图表优化**: 自动检测系统中可用的中文字体，解决图表乱码问题。
-   **数据校验**: 增加了对输入数据的完整性校验。

## 2. 快速开始

### 依赖

-   Python 3.x
-   `matplotlib`: 用于绘图

### 安装依赖

```bash
pip install matplotlib
```

### 运行方式

**方式 1: 使用默认配置运行 (推荐)**

直接运行脚本，默认使用北京地区社保配置（内置于 `default_config.json`）：

```bash
python3 calculate.py
```

**方式 2: 使用 CSV 文件导入数据 (推荐)**

创建一个 CSV 文件（参考 `template.csv`），包含 `RawSalary` (税前收入), `InsuranceBase` (社保基数), `SpecialDeduction` (专项附加扣除) 三列。

```bash
python3 calculate.py --file my_salary.csv
```

**方式 3: 自定义配置文件**

如果你在其他城市，或者社保比例有调整，可以创建一个新的 JSON 配置文件（参考 `default_config.json`），然后加载它：

```bash
python3 calculate.py --config shanghai_2024.json
```

**方式 4: 命令行参数 (传统模式)**

仍然支持通过命令行参数直接指定数据：

```bash
python3 calculate.py --raw 50000,50000... --base 35000,35000...
```

## 3. 文件说明

-   `calculate.py`: 主程序，负责计算逻辑和 CLI 交互。
-   `config_loader.py`: 负责加载和合并配置。
-   `utils.py`: 工具函数，包括 CSV 写入和字体检测。
-   `default_config.json`: 默认的社保和个税配置（参考北京标准）。
-   `template.csv`: 数据导入模板。
-   `income.csv`: 输出结果表格。
-   `tax_curve.png`: 输出结果图表。

## 4. 详细配置

`default_config.json` 结构示例：

```json
{
    "pension": {
        "rate": 0.08,  // 个人养老保险比例
        "min": 3613,   // 基数下限
        "max": 35283   // 基数上限
    },
    ...
    "tax_threshold": 5000.0, // 起征点
    "tax_rates": [ ... ]     // 税率表
}
```

修改此文件或创建新文件即可调整计算逻辑。
