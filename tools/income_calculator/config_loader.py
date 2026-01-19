import json
import os
from typing import Dict, Any

# 默认配置，作为 fallback
DEFAULT_CONFIG = {
    "pension": {"rate": 0.08, "min": 3613, "max": 35283},
    "unemployment": {"rate": 0.005, "min": 3613, "max": 35283},
    "medical": {"rate": 0.02, "min": 5360, "max": 35283, "base_fee": 3},
    "housing_fund": {"rate": 0.12, "min": 2200, "max": 35283},
    "tax_threshold": 5000.0,
    "tax_rates": [
        {"limit": 36000.0, "rate": 0.03, "deduction": 0},
        {"limit": 144000.0, "rate": 0.1, "deduction": 2520},
        {"limit": 300000.0, "rate": 0.2, "deduction": 16920},
        {"limit": 420000.0, "rate": 0.25, "deduction": 31920},
        {"limit": 660000.0, "rate": 0.3, "deduction": 52920},
        {"limit": 960000.0, "rate": 0.35, "deduction": 85920},
        {"limit": None, "rate": 0.45, "deduction": 181920}
    ]
}

def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    加载配置。
    如果提供了 config_path，则从文件加载。
    否则尝试加载 default_config.json。
    如果文件不存在，使用内置默认配置。
    """
    config = DEFAULT_CONFIG.copy()
    
    paths_to_try = []
    if config_path:
        paths_to_try.append(config_path)
    
    # 尝试在当前脚本同级目录查找 default_config.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_json_path = os.path.join(current_dir, 'default_config.json')
    paths_to_try.append(default_json_path)

    for path in paths_to_try:
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    # 简单的字典合并（只覆盖顶层键）
                    config.update(file_config)
                    # 处理 limit: null 转为 None (JSON null -> Python None)
                    # 实际上 json.load 已经自动处理了 null -> None，但在 config 中 tax_rates 结构需要确保一致性
                print(f"Loaded configuration from: {path}")
                return config
            except Exception as e:
                print(f"Warning: Failed to load config from {path}: {e}")
    
    print("Using built-in default configuration.")
    return config
