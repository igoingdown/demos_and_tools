import csv
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform

def write_csv(file_path, header, data):
    """
    将数据写入 CSV 文件
    """
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def set_chinese_font():
    """
    动态检测并设置 matplotlib 的中文字体
    """
    system_fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    # 常见中文字体名称列表 (英文名和中文名)
    common_cn_fonts = [
        'Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 
        'Heiti TC', 'WenQuanYi Micro Hei', 'Droid Sans Fallback', 'Noto Sans CJK SC'
    ]
    
    found_font = None
    for font_path in system_fonts:
        try:
            font_prop = font_manager.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            
            # 检查字体名称是否在我们的列表中
            if font_name in common_cn_fonts:
                found_font = font_name
                break
                
            # 也可以尝试通过字体文件路径名称来模糊匹配
            # 这里简化处理，优先匹配常用列表
        except:
            continue
            
    if found_font:
        plt.rcParams['font.sans-serif'] = [found_font] + plt.rcParams['font.sans-serif']
    else:
        # Fallback list
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'sans-serif']
        
    plt.rcParams['axes.unicode_minus'] = False
