# alt_simu_class

一个模拟小学六年级班级成员名单的 Python 小程序。

## ✨ 特性

- 📋 **自动生成班级花名册**：包含学号、姓名、性别、生日、年龄
- 🎓 **真实学龄映射**：根据中国小学学制，自动推算六年级学生的出生日期范围
- 🔢 **自动编号**：学号从 1 开始连续分配
- 📅 **年龄自动计算**：根据当天日期动态计算每位学生的实际年龄
- 🎯 **可复现**：支持随机种子，方便调试和测试

## 📦 安装

```bash
pip install .
```

开发模式安装（含测试依赖）：

```bash
pip install -e ".[dev]"
```

## 🔗 依赖

- [alt_generate_zh_name](https://github.com/ashida2016/alt_generate_zh_name) — 自动生成中国学生个人基础信息（姓名、性别、生日）
- [pandas](https://pandas.pydata.org/) ≥ 2.0

## 🚀 快速上手

### 命令行运行

```bash
python -m alt_simu_class
```

输出示例：

```
==================================================
  小学六年级班级花名册  （共 45 人）
==================================================
 学号  姓名 性别         生日  年龄
  1 郭柏泽  男 2014-03-28  12
  2 张辰锋  男 2014-07-10  11
  3 杨可琳  女 2014-02-02  12
  ...
==================================================
```

### 代码中使用

```python
from alt_simu_class import Classroom

# 创建默认班级（45 人）
classroom = Classroom()
classroom.print_roster()

# 自定义人数 + 可复现
classroom = Classroom(size=30, seed=42)
print(classroom.roster)
```

## 📖 API

### `Classroom(size, *, seed)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `size` | `int` | `45` | 班级人数 |
| `seed` | `int \| None` | `None` | 随机种子 |

**属性**：

| 属性 | 类型 | 说明 |
|------|------|------|
| `grade` | `int` | 年级，固定为 `6` |
| `size` | `int` | 班级人数 |
| `roster` | `pd.DataFrame` | 花名册，列为 `["学号", "姓名", "性别", "生日", "年龄"]` |

**方法**：

| 方法 | 说明 |
|------|------|
| `print_roster()` | 将格式化的花名册打印到终端 |

## 🧪 测试

```bash
pytest tests/ -v
```

## 📄 许可证

Apache License 2.0
