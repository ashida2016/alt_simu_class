"""班级模拟核心模块：生成并管理一个模拟班级的学生名单。"""

from __future__ import annotations

import datetime

import pandas as pd
from alt_generate_zh_name import generate


# ── 年级与学年映射 ────────────────────────────────────────────────
# 中国小学学制：每年 9 月入学，六年级学生为入学后第 6 个学年。
# 以当前时间 2026 年为参考，六年级学生于 2020 年 9 月入学一年级，
# 即出生于 2013-09-01 ～ 2014-08-31 之间。
_GRADE_6_BIRTH_START = datetime.date(2013, 9, 1)
_GRADE_6_BIRTH_END = datetime.date(2014, 8, 31)

# 一个标准班级的默认人数
_DEFAULT_CLASS_SIZE = 45


class Classroom:
    """模拟一个小学六年级班级。

    Attributes:
        grade: 年级，固定为 6。
        size: 班级人数。
        roster: 包含所有学生信息的 ``pd.DataFrame``，
            列为 ``["学号", "姓名", "性别", "生日", "年龄"]``。

    Examples:
        >>> classroom = Classroom(size=5, seed=42)
        >>> classroom.roster.columns.tolist()
        ['学号', '姓名', '性别', '生日', '年龄']
    """

    def __init__(
        self,
        size: int = _DEFAULT_CLASS_SIZE,
        *,
        seed: int | None = None,
    ) -> None:
        """初始化班级并生成学生名单。

        Args:
            size: 班级人数，默认 ``45``。
            seed: 随机种子，用于生成可复现的结果。

        Raises:
            ValueError: 如果 ``size < 1``。
        """
        if size < 1:
            raise ValueError(f"班级人数必须 ≥ 1，收到 {size}")

        self.grade: int = 6
        self.size: int = size
        self.roster: pd.DataFrame = self._generate_roster(size, seed)

    def _generate_roster(
        self,
        size: int,
        seed: int | None,
    ) -> pd.DataFrame:
        """调用 alt_generate_zh_name 生成学生数据并添加学号和年龄。

        Args:
            size: 生成的学生数量。
            seed: 随机种子。

        Returns:
            包含 ``["学号", "姓名", "性别", "生日", "年龄"]`` 列的
            ``pd.DataFrame``。
        """
        # 使用 alt_generate_zh_name 生成基础信息
        df = generate(
            size,
            birth_start=_GRADE_6_BIRTH_START,
            birth_end=_GRADE_6_BIRTH_END,
            seed=seed,
        )

        # 添加学号（从 1 开始）
        df.insert(0, "学号", range(1, size + 1))

        # 计算年龄（以今天为参考）
        today = datetime.date.today()
        df["年龄"] = df["生日"].apply(
            lambda b: (
                today.year
                - b.year
                - ((today.month, today.day) < (b.month, b.day))
            )
        )

        return df

    def print_roster(self) -> None:
        """将班级花名册打印到终端。

        输出格式包含班级信息标题和完整的学生名单表格。
        """
        header = f"{'=' * 50}"
        title = f"  小学六年级班级花名册  （共 {self.size} 人）"

        print(header)
        print(title)
        print(header)
        print(self.roster.to_string(index=False))
        print(header)
