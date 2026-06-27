"""命令行入口：生成并打印模拟班级花名册。

用法::

    python -m alt_simu_class
"""

from alt_simu_class.classroom import Classroom
# from classroom import Classroom


def main() -> None:
    """程序主入口，创建班级并打印花名册。"""
    classroom = Classroom()
    classroom.print_roster()


if __name__ == "__main__":
    main()
