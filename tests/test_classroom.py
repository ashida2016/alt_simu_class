"""Classroom 类的单元测试。"""

from __future__ import annotations

import datetime

import pandas as pd
import pytest

from alt_simu_class.classroom import Classroom


class TestClassroomInit:
    """测试 Classroom 初始化行为。"""

    def test_default_size(self) -> None:
        """默认班级人数应为 45。"""
        classroom = Classroom(seed=0)
        assert classroom.size == 45
        assert len(classroom.roster) == 45

    def test_custom_size(self) -> None:
        """可自定义班级人数。"""
        classroom = Classroom(size=10, seed=0)
        assert classroom.size == 10
        assert len(classroom.roster) == 10

    def test_invalid_size(self) -> None:
        """人数小于 1 应抛出 ValueError。"""
        with pytest.raises(ValueError, match="班级人数必须 ≥ 1"):
            Classroom(size=0)

    def test_grade_is_six(self) -> None:
        """年级固定为 6。"""
        classroom = Classroom(size=1, seed=0)
        assert classroom.grade == 6


class TestRosterColumns:
    """测试花名册的列结构。"""

    def test_columns(self) -> None:
        """花名册应包含预期的列。"""
        classroom = Classroom(size=5, seed=0)
        expected_columns = ["学号", "姓名", "性别", "生日", "年龄"]
        assert classroom.roster.columns.tolist() == expected_columns

    def test_student_ids(self) -> None:
        """学号应从 1 开始连续编号。"""
        classroom = Classroom(size=10, seed=0)
        expected_ids = list(range(1, 11))
        assert classroom.roster["学号"].tolist() == expected_ids


class TestRosterData:
    """测试花名册的数据内容。"""

    def test_gender_values(self) -> None:
        """性别只能是 '男' 或 '女'。"""
        classroom = Classroom(size=30, seed=0)
        assert set(classroom.roster["性别"].unique()).issubset({"男", "女"})

    def test_birthday_range(self) -> None:
        """生日应在六年级对应的范围内。"""
        classroom = Classroom(size=30, seed=0)
        start = datetime.date(2013, 9, 1)
        end = datetime.date(2014, 8, 31)
        for birthday in classroom.roster["生日"]:
            assert start <= birthday <= end

    def test_age_calculation(self) -> None:
        """年龄应根据今天的日期正确计算。"""
        classroom = Classroom(size=5, seed=42)
        today = datetime.date.today()
        for _, row in classroom.roster.iterrows():
            birthday = row["生日"]
            expected_age = (
                today.year
                - birthday.year
                - ((today.month, today.day) < (birthday.month, birthday.day))
            )
            assert row["年龄"] == expected_age


class TestReproducibility:
    """测试随机种子的可复现性。"""

    def test_same_seed_same_result(self) -> None:
        """相同种子应生成相同的花名册。"""
        c1 = Classroom(size=10, seed=42)
        c2 = Classroom(size=10, seed=42)
        pd.testing.assert_frame_equal(c1.roster, c2.roster)

    def test_different_seed_different_result(self) -> None:
        """不同种子应生成不同的花名册。"""
        c1 = Classroom(size=10, seed=1)
        c2 = Classroom(size=10, seed=2)
        assert not c1.roster.equals(c2.roster)


class TestPrintRoster:
    """测试花名册打印功能。"""

    def test_print_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """print_roster 应输出包含标题和分隔线的格式化内容。"""
        classroom = Classroom(size=3, seed=0)
        classroom.print_roster()
        captured = capsys.readouterr().out

        assert "小学六年级班级花名册" in captured
        assert "共 3 人" in captured
        assert "=" * 50 in captured
