#!/usr/bin/env python3
"""Generate LPTHW skeleton + priority track lessons (original study guides)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "content" / "tracks"

LPTHW_TITLES = {
    0: "The Setup",
    1: "A Good First Program",
    2: "Comments and Pound Characters",
    3: "Numbers and Math",
    4: "Variables and Names",
    5: "More Variables and Printing",
    6: "Strings and Text",
    7: "More Printing",
    8: "Printing, Printing",
    9: "Printing, Printing, Printing",
    10: "What Was That?",
    11: "Asking Questions",
    12: "Prompting People",
    13: "Parameters, Unpacking, Variables",
    14: "Prompting and Passing",
    15: "Reading Files",
    16: "Reading and Writing Files",
    17: "More Files",
    18: "Names, Variables, Code, Functions",
    19: "Functions and Variables",
    20: "Functions and Files",
    21: "Functions Can Return Something",
    22: "What Do You Know So Far?",
    23: "Strings, Bytes and Character Encodings",
    24: "More Practice",
    25: "Even More Practice",
    26: "Congratulations, Take a Test!",
    27: "Memorizing Logic",
    28: "Boolean Practice",
    29: "What If",
    30: "Else and If",
    31: "Making Decisions",
    32: "Loops and Lists",
    33: "While Loops",
    34: "Accessing Elements of Lists",
    35: "Branches and Functions",
    36: "Designing and Debugging",
    37: "Symbol Review",
    38: "Doing Things to Lists",
    39: "Dictionaries, Oh Lovely Dictionaries",
    40: "Modules, Classes, and Objects",
    41: "Learning to Speak Object Oriented",
    42: "Is-A, Has-A, Objects, and Classes",
    43: "Basic Object-Oriented Analysis and Design",
    44: "Inheritance Versus Composition",
    45: "You Make a Game",
    46: "A Project Skeleton",
    47: "Automated Testing",
    48: "Advanced User Input",
    49: "Making Sentences",
    50: "Your First Website",
    51: "Getting Input from a Browser",
    52: "The Start of Your Web Game",
}

FULL_LPTHW = {
    0: {
        "body": '# Ex 0 · The Setup\n\n对照你的书完成环境确认。本站用本机 `python3` 执行代码。\n\n## 目标\n- 确认本机 Python 可运行\n- 习惯：先读说明 → 改代码 → 运行 → 看输出\n\n## 说明\n这一课没有花哨语法。跑通版本信息，就算环境就绪。\n\n## 自检\n- [ ] 下方代码能跑出版本信息\n- [ ] 你知道「运行」按钮会执行入口文件\n',
        "entry": 'ex00.py',
        "starterFiles": {
            'ex00.py': 'import sys\n\nprint("Python OK")\nprint(sys.version)\n',
        },
        "timeoutSec": 5,
    },
    1: {
        "body": '# Ex 1 · A Good First Program\n\n练习 `print`。多敲几遍，观察引号与括号。\n\n## 目标\n- 写出至少三行 `print`\n- 理解字符串要用引号包住\n\n## 说明\nPython 靠缩进组织代码；本课先专注输出。少写一个括号或引号都会报错——那是正常的学习过程。\n\n## 自检\n- [ ] 至少三行不同输出\n- [ ] 故意改错一次，再修好\n',
        "entry": 'ex01.py',
        "starterFiles": {
            'ex01.py': 'print("Hello World!")\nprint("Hello Again")\nprint("I like typing this.")\nprint("This is fun.")\n',
        },
        "timeoutSec": 5,
    },
    2: {
        "body": '# Ex 2 · Comments and Pound Characters\n\n`#` 后面是注释。用注释给未来的自己留言。\n\n## 目标\n- 会写行首注释与行尾注释\n- 知道注释不会被执行\n\n## 自检\n- [ ] 至少有两处 `#` 注释\n- [ ] 注释掉一行 `print` 后再运行，确认少了一行输出\n',
        "entry": 'ex02.py',
        "starterFiles": {
            'ex02.py': '# A comment, this is so you can read your program later.\n# Anything after the # is ignored by Python.\n\nprint("I could have code like this.")  # and the comment after is ignored\n\n# print("This will not run.")\nprint("This will run.")\n',
        },
        "timeoutSec": 5,
    },
    3: {
        "body": '# Ex 3 · Numbers and Math\n\n练习 `+ - * / % < > <= >=`。先心算再核对输出。\n\n## 目标\n- 区分整数运算与浮点除法\n- 看懂比较表达式的 True/False\n\n## 自检\n- [ ] 至少改一组数字并预测结果\n- [ ] 理解 `%` 是取余\n',
        "entry": 'ex03.py',
        "starterFiles": {
            'ex03.py': 'print("I will now count my chickens:")\nprint("Hens", 25 + 30 / 6)\nprint("Roosters", 100 - 25 * 3 % 4)\nprint("Now I will count the eggs:")\nprint(3 + 2 + 1 - 5 + 4 % 2 - 1 / 4 + 6)\nprint("Is it true that 3 + 2 < 5 - 7?")\nprint(3 + 2 < 5 - 7)\nprint("What is 3 + 2?", 3 + 2)\nprint("What is 5 - 7?", 5 - 7)\n',
        },
        "timeoutSec": 5,
    },
    4: {
        "body": '# Ex 4 · Variables and Names\n\n给值起名字。变量名要可读。\n\n## 目标\n- 用变量保存数字并做运算\n- 用逗号把文字和变量一起 `print`\n\n## 自检\n- [ ] 改掉 `cars` 等数字后，后续输出一起变\n- [ ] 变量名没有空格、不以数字开头\n',
        "entry": 'ex04.py',
        "starterFiles": {
            'ex04.py': 'cars = 100\nspace_in_a_car = 4.0\ndrivers = 30\npassengers = 90\ncars_not_driven = cars - drivers\ncars_driven = drivers\ncarpool_capacity = cars_driven * space_in_a_car\naverage_passengers_per_car = passengers / cars_driven\n\nprint("There are", cars, "cars available.")\nprint("There are only", drivers, "drivers available.")\nprint("There will be", cars_not_driven, "empty cars today.")\nprint("We can transport", carpool_capacity, "people today.")\nprint("We have", passengers, "to carpool today.")\nprint("We need to put about", average_passengers_per_car, "in each car.")\n',
        },
        "timeoutSec": 5,
    },
    5: {
        "body": '# Ex 5 · More Variables and Printing\n\n用 f-string 或 `.format` 把变量嵌进字符串。\n\n## 目标\n- 用 f-string 插入变量\n- 区分「字符串里的文字」和「算出来的值」\n\n## 自检\n- [ ] 改名字/年龄后输出跟着变\n- [ ] 至少两处 f-string\n',
        "entry": 'ex05.py',
        "starterFiles": {
            'ex05.py': 'my_name = "Zed A. Shaw"\nmy_age = 35\nmy_height = 74  # inches\nmy_weight = 180  # lbs\nmy_eyes = "Blue"\nmy_teeth = "White"\nmy_hair = "Brown"\n\nprint(f"Let\'s talk about {my_name}.")\nprint(f"He\'s {my_height} inches tall.")\nprint(f"He\'s {my_weight} pounds heavy.")\nprint(f"He\'s got {my_eyes} eyes and {my_hair} hair.")\nprint(f"His teeth are usually {my_teeth} depending on the coffee.")\ntotal = my_age + my_height + my_weight\nprint(f"If I add {my_age}, {my_height}, and {my_weight} I get {total}.")\n',
        },
        "timeoutSec": 5,
    },
    6: {
        "body": '# Ex 6 · Strings and Text\n\n字符串可以拼接、格式化，也可以嵌进别的字符串。\n\n## 目标\n- 使用 f-string 与 `+` 拼接\n- 看懂「字符串里再放变量」\n\n## 自检\n- [ ] 改 `types_of_people` 后相关句子变化\n- [ ] 至少一种拼接方式自己改写过\n',
        "entry": 'ex06.py',
        "starterFiles": {
            'ex06.py': 'types_of_people = 10\nx = f"There are {types_of_people} types of people."\n\nbinary = "binary"\ndo_not = "don\'t"\ny = f"Those who know {binary} and those who {do_not}."\n\nprint(x)\nprint(y)\nprint(f"I said: {x}")\nprint(f"I also said: \'{y}\'")\n\nhilarious = False\njoke_evaluation = "Isn\'t that joke so funny?! {}"\nprint(joke_evaluation.format(hilarious))\n\nw = "This is the left side of..."\ne = "a string with a right side."\nprint(w + e)\n',
        },
        "timeoutSec": 5,
    },
    7: {
        "body": '# Ex 7 · More Printing\n\n继续练 `print`：多行输出、拼接、`end=` 控制换行。\n\n## 目标\n- 熟练打印多段文字\n- 用 `end=" "` 让下一行接在同一行\n\n## 自检\n- [ ] 看到雪人那一行是拼出来的\n- [ ] 试着改 `end` 观察效果\n',
        "entry": 'ex07.py',
        "starterFiles": {
            'ex07.py': 'print("Mary had a little lamb.")\nprint("Its fleece was white as {}.".format("snow"))\nprint("And everywhere that Mary went.")\nprint("." * 10)  # what did that do?\n\nend1 = "C"\nend2 = "h"\nend3 = "e"\nend4 = "e"\nend5 = "s"\nend6 = "e"\nend7 = "B"\nend8 = "u"\nend9 = "r"\nend10 = "g"\nend11 = "e"\nend12 = "r"\n\nprint(end1 + end2 + end3 + end4 + end5 + end6, end=" ")\nprint(end7 + end8 + end9 + end10 + end11 + end12)\n',
        },
        "timeoutSec": 5,
    },
    8: {
        "body": '# Ex 8 · Printing, Printing\n\n用 `.format()` 按位置填坑。同一个格式串可以反复用。\n\n## 目标\n- 看懂 `{}` 占位符\n- 一次传入多个参数\n\n## 自检\n- [ ] 改格式串里的文字，输出跟着变\n- [ ] 试着少传/多传参数，读懂报错\n',
        "entry": 'ex08.py',
        "starterFiles": {
            'ex08.py': 'formatter = "{} {} {} {}"\n\nprint(formatter.format(1, 2, 3, 4))\nprint(formatter.format("one", "two", "three", "four"))\nprint(formatter.format(True, False, False, True))\nprint(formatter.format(formatter, formatter, formatter, formatter))\nprint(formatter.format(\n    "Try your",\n    "Own text here",\n    "Maybe a poem",\n    "Or a song about fear",\n))\n',
        },
        "timeoutSec": 5,
    },
    9: {
        "body": '# Ex 9 · Printing, Printing, Printing\n\n多行字符串：`\\n` 换行，或用三引号保留格式。\n\n## 目标\n- 用 `\\n` 手动换行\n- 用 `"""..."""` 写一段多行文字\n\n## 自检\n- [ ] days / months 输出格式清楚\n- [ ] 三引号段落里至少改一行字\n',
        "entry": 'ex09.py',
        "starterFiles": {
            'ex09.py': 'days = "Mon Tue Wed Thu Fri Sat Sun"\nmonths = "Jan\\nFeb\\nMar\\nApr\\nMay\\nJun\\nJul\\nAug"\n\nprint("Here are the days:", days)\nprint("Here are the months:", months)\n\nprint("""\nThere\'s something going on here.\nWith the three double-quotes.\nWe\'ll be able to type as much as we like.\nEven 4 lines if we want, or 5, or 6.\n""")\n',
        },
        "timeoutSec": 5,
    },
    10: {
        "body": '# Ex 10 · What Was That?\n\n转义字符：`\\n` `\\t` `\\\\` 以及引号转义。\n\n## 目标\n- 认识常见转义\n- 会在字符串里嵌套引号\n\n## 自检\n- [ ] 能指出哪一行用了 tab\n- [ ] 试着打印带双引号的句子\n',
        "entry": 'ex10.py',
        "starterFiles": {
            'ex10.py': 'tabby_cat = "\\tI\'m tabbed in."\npersian_cat = "I\'m split\\non a line."\nbackslash_cat = "I\'m \\\\ a \\\\ cat."\n\nfat_cat = """\nI\'ll do a list:\n\\t* Cat food\n\\t* Fishies\n\\t* Catnip\\n\\t* Grass\n"""\n\nprint(tabby_cat)\nprint(persian_cat)\nprint(backslash_cat)\nprint(fat_cat)\n',
        },
        "timeoutSec": 5,
    },
    11: {
        "body": '# Ex 11 · Asking Questions\n\n`input()` 从终端读一行。运行后在下方终端输入答案并回车。\n\n## 目标\n- 用 `input()` 读入用户输入\n- 把读到的值嵌进 f-string 打印\n\n## 自检\n- [ ] 运行后能在终端打字并回车\n- [ ] 最终总结句包含你输入的三个值\n',
        "entry": 'ex11.py',
        "starterFiles": {
            'ex11.py': 'print("How old are you?", end=" ")\nage = input()\nprint("How tall are you?", end=" ")\nheight = input()\nprint("How much do you weigh?", end=" ")\nweight = input()\nprint(f"So, you\'re {age} old, {height} tall and {weight} heavy.")\n',
        },
        "timeoutSec": 3,
    },
    12: {
        "body": '# Ex 12 · Prompting People\n\n`input("提示语")` 可以把提示直接写在括号里。\n\n## 目标\n- 用带提示的 `input`\n- 整理并回显用户信息\n\n## 自检\n- [ ] 三个问题都用 `input("...")` 形式\n- [ ] 回显正确\n',
        "entry": 'ex12.py',
        "starterFiles": {
            'ex12.py': 'age = input("How old are you? ")\nheight = input("How tall are you? ")\nweight = input("How much do you weigh? ")\n\nprint(f"So, you\'re {age} old, {height} tall and {weight} heavy.")\n',
        },
        "timeoutSec": 3,
    },
    13: {
        "body": '# Ex 13 · Parameters, Unpacking, Variables\n\n`sys.argv` 接收命令行参数。本课在参数不足时使用默认值，保证直接点运行也能学到概念。\n\n## 目标\n- 理解 `sys.argv[0]` 是脚本名\n- 参数不够时优雅回退到默认值\n\n## 自检\n- [ ] 无参数运行仍有完整输出\n- [ ] 若环境支持传参，可试 `python ex13.py apple orange pear`\n',
        "entry": 'ex13.py',
        "starterFiles": {
            'ex13.py': 'import sys\n\nscript = sys.argv[0]\nif len(sys.argv) >= 4:\n    first, second, third = sys.argv[1], sys.argv[2], sys.argv[3]\nelse:\n    print("Usage: python ex13.py first second third")\n    print("(missing args — using defaults)\\n")\n    first, second, third = "first", "second", "third"\n\nprint("The script is called:", script)\nprint("Your first variable is:", first)\nprint("Your second variable is:", second)\nprint("Your third variable is:", third)\n',
        },
        "timeoutSec": 5,
    },
    14: {
        "body": '# Ex 14 · Prompting and Passing\n\n结合 `sys.argv` 与 `input()`：参数给用户名，其余问题现场问。\n\n## 目标\n- 从 argv 取用户名（缺省则默认）\n- 再用 `input` 问后续问题\n\n## 自检\n- [ ] 无参数时仍能完成对话\n- [ ] 提示语里出现用户名\n',
        "entry": 'ex14.py',
        "starterFiles": {
            'ex14.py': 'import sys\n\nscript = sys.argv[0]\nif len(sys.argv) >= 2:\n    user_name = sys.argv[1]\nelse:\n    print("Usage: python ex14.py your_name  (using default name)")\n    user_name = "Learner"\n\nprompt = f"{script} ({user_name})> "\n\nprint(f"Hi {user_name}, I\'m the {script} script.")\nprint("I\'d like to ask you a few questions.")\nlikes = input(f"Do you like me {user_name}? ")\nlives = input(f"Where do you live {user_name}? ")\ncomputer = input("What kind of computer do you have? ")\n\nprint(f"""\nAlright, so you said {likes} about liking me.\nYou live in {lives}. Not sure where that is.\nAnd you have a {computer} computer. Nice.\n""")\n',
        },
        "timeoutSec": 3,
    },
    15: {
        "body": '# Ex 15 · Reading Files\n\n右侧文件树里有 `sample.txt`。用 `open` / `read` 读出内容。\n\n## 目标\n- 用 `with open(...)` 打开文件\n- 用 `read()` 打印全部内容\n\n## 自检\n- [ ] 能看到 sample.txt 的三行文字\n- [ ] 试着改 sample.txt 再跑一次\n',
        "entry": 'ex15.py',
        "starterFiles": {
            'ex15.py': 'filename = "sample.txt"\nwith open(filename) as f:\n    print(f"Here is your file {filename}:")\n    print(f.read())\n',
            'sample.txt': 'This is stuff I typed into a file.\nIt is really cool stuff.\nLots and lots of fun to have in here.\n',
        },
        "timeoutSec": 5,
    },
    16: {
        "body": '# Ex 16 · Reading and Writing Files\n\n练习 `write`。运行后刷新文件树，打开新文件确认内容。\n\n## 目标\n- 用 `"w"` 模式写入（会截断旧内容）\n- 写入多行并确认文件生成\n\n## 自检\n- [ ] 运行后出现 `out.txt`\n- [ ] 文件内容与代码一致\n',
        "entry": 'ex16.py',
        "starterFiles": {
            'ex16.py': 'filename = "out.txt"\nwith open(filename, "w") as f:\n    f.write("I am truncating and writing.\\n")\n    f.write("Line two.\\n")\n    f.write("Line three.\\n")\nprint(f"Wrote {filename}")\n',
        },
        "timeoutSec": 5,
    },
    17: {
        "body": '# Ex 17 · More Files\n\n从一个文件读，写到另一个文件——迷你「复制」。\n\n## 目标\n- 读 `from.txt` 全文\n- 写入 `to.txt` 并核对长度\n\n## 自检\n- [ ] `to.txt` 内容与 `from.txt` 一致\n- [ ] 打印了复制的字节/字符数\n',
        "entry": 'ex17.py',
        "starterFiles": {
            'ex17.py': 'from_file = "from.txt"\nto_file = "to.txt"\n\nprint(f"Copying from {from_file} to {to_file}")\nwith open(from_file) as infile:\n    data = infile.read()\n\nprint(f"The input file is {len(data)} characters long")\nwith open(to_file, "w") as outfile:\n    outfile.write(data)\n\nprint("All done. Re-read the copy:")\nwith open(to_file) as f:\n    print(f.read())\n',
            'from.txt': 'Line A from the source file.\nLine B is also here.\nCopy me please.\n',
        },
        "timeoutSec": 5,
    },
    18: {
        "body": '# Ex 18 · Names, Variables, Code, Functions\n\n函数：给一段代码起名字，之后反复调用。\n\n## 目标\n- 用 `def` 定义函数\n- 理解参数就像函数里的变量\n\n## 自检\n- [ ] 至少两个函数被调用\n- [ ] 改参数再跑，输出变化符合预期\n',
        "entry": 'ex18.py',
        "starterFiles": {
            'ex18.py': 'def print_two(*args):\n    arg1, arg2 = args\n    print(f"arg1: {arg1}, arg2: {arg2}")\n\n\ndef print_two_again(arg1, arg2):\n    print(f"arg1: {arg1}, arg2: {arg2}")\n\n\ndef print_one(arg1):\n    print(f"arg1: {arg1}")\n\n\ndef print_none():\n    print("I got nothin\'.")\n\n\nprint_two("Zed", "Shaw")\nprint_two_again("Zed", "Shaw")\nprint_one("First!")\nprint_none()\n',
        },
        "timeoutSec": 5,
    },
    19: {
        "body": '# Ex 19 · Functions and Variables\n\n函数参数名可以和外面的变量名相同，但它们不是同一个盒子。\n\n## 目标\n- 用不同方式给函数传参\n- 体会「调用时传入的值」才重要\n\n## 自检\n- [ ] 同名变量在函数内外互不影响（本课演示）\n- [ ] 至少改一次调用参数\n',
        "entry": 'ex19.py',
        "starterFiles": {
            'ex19.py': 'def cheese_and_crackers(cheese_count, boxes_of_crackers):\n    print(f"You have {cheese_count} cheeses!")\n    print(f"You have {boxes_of_crackers} boxes of crackers!")\n    print("Man that\'s enough for a party!")\n    print("Get a blanket.\\n")\n\n\nprint("We can just give the function numbers directly:")\ncheese_and_crackers(20, 30)\n\nprint("OR, we can use variables from our script:")\namount_of_cheese = 10\namount_of_crackers = 50\ncheese_and_crackers(amount_of_cheese, amount_of_crackers)\n\nprint("We can even do math inside too:")\ncheese_and_crackers(10 + 20, 5 + 6)\n\nprint("And we can combine the two, variables and math:")\ncheese_and_crackers(amount_of_cheese + 100, amount_of_crackers + 1000)\n',
        },
        "timeoutSec": 5,
    },
    20: {
        "body": '# Ex 20 · Functions and Files\n\n把读文件的步骤拆成小函数，主流程更清晰。\n\n## 目标\n- 函数接收文件对象并操作\n- 练习 `seek(0)` 回到文件开头\n\n## 自检\n- [ ] 三份打印内容都能看到\n- [ ] 理解为什么第二次全文打印前要 seek\n',
        "entry": 'ex20.py',
        "starterFiles": {
            'ex20.py': 'def print_all(f):\n    print(f.read())\n\n\ndef rewind(f):\n    f.seek(0)\n\n\ndef print_a_line(line_count, f):\n    print(line_count, f.readline(), end="")\n\n\ncurrent_file = open("story.txt")\n\nprint("First let\'s print the whole file:\\n")\nprint_all(current_file)\n\nprint("Now let\'s rewind, kind of like a tape.")\nrewind(current_file)\n\nprint("Let\'s print three lines:")\ncurrent_line = 1\nprint_a_line(current_line, current_file)\ncurrent_line += 1\nprint_a_line(current_line, current_file)\ncurrent_line += 1\nprint_a_line(current_line, current_file)\n\ncurrent_file.close()\n',
            'story.txt': 'This is line 1\nThis is line 2\nThis is line 3\n',
        },
        "timeoutSec": 5,
    },
    21: {
        "body": '# Ex 21 · Functions Can Return Something\n\n`return` 把结果交回调用方，而不是只打印。\n\n## 目标\n- 写带返回值的函数\n- 把返回值赋给变量再继续算\n\n## 自检\n- [ ] 年龄相关公式能打印出数字\n- [ ] 试着 `return` 一个你自己的表达式\n',
        "entry": 'ex21.py',
        "starterFiles": {
            'ex21.py': 'def add(a, b):\n    print(f"ADDING {a} + {b}")\n    return a + b\n\n\ndef subtract(a, b):\n    print(f"SUBTRACTING {a} - {b}")\n    return a - b\n\n\ndef multiply(a, b):\n    print(f"MULTIPLYING {a} * {b}")\n    return a * b\n\n\ndef divide(a, b):\n    print(f"DIVIDING {a} / {b}")\n    return a / b\n\n\nprint("Let\'s do some math with just functions!")\nage = add(30, 5)\nheight = subtract(78, 4)\nweight = multiply(90, 2)\niq = divide(100, 2)\n\nprint(f"Age: {age}, Height: {height}, Weight: {weight}, IQ: {iq}")\n\nprint("Here is a puzzle.")\nwhat = add(age, subtract(height, multiply(weight, divide(iq, 2))))\nprint("That becomes:", what, "Can you do it by hand?")\n',
        },
        "timeoutSec": 5,
    },
    22: {
        "body": '# Ex 22 · What Do You Know So Far?\n\n复习课：把目前学过的关键词/概念打印成清单，对照自查。\n\n## 目标\n- 用代码列出已学概念\n- 标出还不熟的一项去复习\n\n## 自检\n- [ ] 清单能完整打印\n- [ ] 至少补充一项你自己的笔记到列表里\n',
        "entry": 'ex22.py',
        "starterFiles": {
            'ex22.py': 'concepts = [\n    ("print", "输出到终端"),\n    ("#", "注释"),\n    ("变量", "给值起名字"),\n    ("字符串", "引号包住的文字"),\n    ("input", "从终端读入"),\n    ("sys.argv", "命令行参数"),\n    ("open/read/write", "文件读写"),\n    ("def / return", "函数与返回值"),\n]\n\nprint("=== LPTHW so far ===")\nfor i, (name, tip) in enumerate(concepts, start=1):\n    print(f"{i:02d}. {name:16} — {tip}")\n\nprint("\\nPick one weak item and re-run an earlier exercise.")\n',
        },
        "timeoutSec": 5,
    },
    23: {
        "body": '# Ex 23 · Strings, Bytes and Character Encodings\n\n`str` 是文字，`bytes` 是原始字节。编解码用 UTF-8 最常见。\n\n## 目标\n- 用 `.encode("utf-8")` / `.decode("utf-8")`\n- 看懂中文等多字节字符\n\n## 自检\n- [ ] 编码后看到 `b\'...\'`\n- [ ] 解码后文字恢复\n',
        "entry": 'ex23.py',
        "starterFiles": {
            'ex23.py': 'text = "你好, LPTHW! café ☕"\nprint("original:", text)\nprint("type:", type(text))\n\nraw = text.encode("utf-8")\nprint("encoded bytes:", raw)\nprint("byte length:", len(raw), "| char length:", len(text))\n\nback = raw.decode("utf-8")\nprint("decoded:", back)\nprint("round-trip ok?", back == text)\n\nprint("\\nHex view:", raw.hex(" "))\n',
        },
        "timeoutSec": 5,
    },
    24: {
        "body": '# Ex 24 · More Practice\n\n综合小练习：转义、格式化、函数、简单运算。\n\n## 目标\n- 把前面几课手法串起来\n- 读懂每一行在干什么\n\n## 自检\n- [ ] 全部输出无报错\n- [ ] 试着改 `secret_formula` 的返回值\n',
        "entry": 'ex24.py',
        "starterFiles": {
            'ex24.py': 'print("Let\'s practice everything.")\nprint("You\'d need to know \'bout escapes with \\\\ that do:")\nprint("\\n newlines and \\t tabs.")\n\npoem = """\n\\tThe lovely world\nwith logic so firmly planted\ncannot discern \\n the needs of love\nnor comprehend passion from intuition\nand requires an explanation\n\\n\\t\\twhere there is none.\n"""\nprint("--------------")\nprint(poem)\nprint("--------------")\n\nfive = 10 - 2 + 3 - 6\nprint(f"This should be five: {five}")\n\n\ndef secret_formula(started):\n    jelly_beans = started * 500\n    jars = jelly_beans / 1000\n    crates = jars / 100\n    return jelly_beans, jars, crates\n\n\nstart_point = 10000\nbeans, jars, crates = secret_formula(start_point)\nprint("With a starting point of: {}".format(start_point))\nprint(f"We\'d have {beans} beans, {jars} jars, and {crates} crates.")\n\nstart_point = start_point / 10\nprint("We can also do that this way:")\nformula = secret_formula(start_point)\nprint("We\'d have {} beans, {} jars, and {} crates.".format(*formula))\n',
        },
        "timeoutSec": 5,
    },
    25: {
        "body": '# Ex 25 · Even More Practice\n\n写一组处理句子的小函数，在主程序里组合调用。\n\n## 目标\n- 拆词、排序、弹出等列表操作\n- 函数返回列表供下一步使用\n\n## 自检\n- [ ] 每个函数都至少被调用一次\n- [ ] 理解 `pop(0)` 与 `pop(-1)` 的差别\n',
        "entry": 'ex25.py',
        "starterFiles": {
            'ex25.py': 'def break_words(stuff):\n    """This function will break up words for us."""\n    return stuff.split()\n\n\ndef sort_words(words):\n    """Sorts the words."""\n    return sorted(words)\n\n\ndef print_first_word(words):\n    word = words.pop(0)\n    print(word)\n\n\ndef print_last_word(words):\n    word = words.pop(-1)\n    print(word)\n\n\ndef sort_sentence(sentence):\n    return sort_words(break_words(sentence))\n\n\ndef print_first_and_last(sentence):\n    words = break_words(sentence)\n    print_first_word(words)\n    print_last_word(words)\n\n\ndef print_first_and_last_sorted(sentence):\n    words = sort_sentence(sentence)\n    print_first_word(words)\n    print_last_word(words)\n\n\nsentence = "All good things come to those who wait."\nwords = break_words(sentence)\nprint("words:", words)\nsorted_words = sort_words(words)\nprint("sorted:", sorted_words)\nprint("first/last from copy of words:")\nprint_first_and_last(sentence)\nprint("first/last from sorted:")\nprint_first_and_last_sorted(sentence)\n',
        },
        "timeoutSec": 5,
    },
    26: {
        "body": '# Ex 26 · Congratulations, Take a Test!\n\n找 bug 风格练习：下面代码里埋了几处小错误/别扭写法，先跑通，再按注释清理。\n\n## 目标\n- 根据报错或错误输出定位问题\n- 学会「读 traceback → 改一行 → 再跑」\n\n## 自检\n- [ ] 程序能完整跑完\n- [ ] 你至少主动修过一处（或解释为何这样写）\n',
        "entry": 'ex26.py',
        "starterFiles": {
            'ex26.py': '# Drill: read carefully. One intentional quirk is documented.\nprint("How old are you?", end=" ")\n# For sandbox auto-run friendliness we also accept a default:\ntry:\n    age = input()\nexcept EOFError:\n    age = "25"\n    print(age, "(default)")\n\nprint("How tall are you?", end=" ")\ntry:\n    height = input()\nexcept EOFError:\n    height = "180cm"\n    print(height, "(default)")\n\nprint(f"So you\'re {age} old and {height} tall.")\n\ndef add(a, b):\n    return a + b\n\n\n# BUGFIX practice: this used to miss a return / wrong names.\nprint("10 + 5 =", add(10, 5))\nwords = "fixing bugs is a skill".split()\nprint("sorted words:", sorted(words))\n',
        },
        "timeoutSec": 3,
    },
    27: {
        "body": '# Ex 27 · Memorizing Logic\n\n布尔逻辑：`and` `or` `not` 与真值表。先背，再打印验证。\n\n## 目标\n- 打印一小份真值表\n- 记住 `not` 的优先级直觉\n\n## 自检\n- [ ] 表中每一行你都能口头解释\n- [ ] 试着加一行自己的表达式\n',
        "entry": 'ex27.py',
        "starterFiles": {
            'ex27.py': 'print("True and True  =>", True and True)\nprint("True and False =>", True and False)\nprint("False and True =>", False and True)\nprint("False and False=>", False and False)\nprint()\nprint("True or True   =>", True or True)\nprint("True or False  =>", True or False)\nprint("False or True  =>", False or True)\nprint("False or False =>", False or False)\nprint()\nprint("not True  =>", not True)\nprint("not False =>", not False)\nprint()\nprint("1 != 0 =>", 1 != 0)\nprint("1 == 0 =>", 1 == 0)\nprint("1 > 0 and 2 < 5 =>", 1 > 0 and 2 < 5)\n',
        },
        "timeoutSec": 5,
    },
    28: {
        "body": '# Ex 28 · Boolean Practice\n\n更多布尔表达式练习：先猜结果，再看程序输出。\n\n## 目标\n- 对一列表达式做「心算 vs 实算」\n- 习惯用括号让优先级清晰\n\n## 自检\n- [ ] 至少猜对一半再对答案\n- [ ] 改写其中两行加括号\n',
        "entry": 'ex28.py',
        "starterFiles": {
            'ex28.py': 'exprs = [\n    "True and True",\n    "False and True",\n    "1 == 1 and 2 == 1",\n    \'"test" == "test"\',\n    "1 == 1 or 2 != 1",\n    "True and 1 == 1",\n    "False and 0 != 0",\n    "True or 1 == 1",\n    \'"test" == "testing"\',\n    "1 != 0 and 2 == 1",\n    \'"test" != "testing"\',\n    \'"test" == 1\',\n    "not (True and False)",\n    "not (1 == 1 and 0 != 1)",\n    "not (10 == 1 or 1000 == 1000)",\n]\n\nfor e in exprs:\n    print(f"{e:40} => {eval(e)}")\n',
        },
        "timeoutSec": 5,
    },
    29: {
        "body": '# Ex 29 · What If\n\n`if`：条件为真才执行缩进块。\n\n## 目标\n- 写几个独立的 `if`\n- 观察缩进块何时执行\n\n## 自检\n- [ ] 改数字让某条 if 从不执行 / 总会执行\n- [ ] 缩进保持一致\n',
        "entry": 'ex29.py',
        "starterFiles": {
            'ex29.py': 'people = 20\ncats = 30\ndogs = 15\n\nif people < cats:\n    print("Too many cats! The world is doomed!")\n\nif people > cats:\n    print("Not many cats! The world is saved!")\n\nif people < dogs:\n    print("The world is drooled on!")\n\nif people > dogs:\n    print("The world is dry!")\n\ndogs += 5\n\nif people >= dogs:\n    print("People are greater than or equal to dogs.")\n\nif people <= dogs:\n    print("People are less than or equal to dogs.")\n\nif people == dogs:\n    print("People are dogs.")\n',
        },
        "timeoutSec": 5,
    },
    30: {
        "body": '# Ex 30 · Else and If\n\n`if / elif / else` 组成互斥分支，最多走一条路。\n\n## 目标\n- 写完整的 if-elif-else 链\n- 理解顺序很重要\n\n## 自检\n- [ ] 调换人数后走不同分支\n- [ ] else 只在前面都不成立时出现\n',
        "entry": 'ex30.py',
        "starterFiles": {
            'ex30.py': 'people = 30\ncars = 40\ntrucks = 15\n\nif cars > people:\n    print("We should take the cars.")\nelif cars < people:\n    print("We should not take the cars.")\nelse:\n    print("We can\'t decide.")\n\nif trucks > cars:\n    print("That\'s too many trucks.")\nelif trucks < cars:\n    print("Maybe we could take the trucks.")\nelse:\n    print("We still can\'t decide.")\n\nif people > trucks:\n    print("Alright, let\'s just take the trucks.")\nelse:\n    print("Fine, let\'s stay home then.")\n',
        },
        "timeoutSec": 5,
    },
    31: {
        "body": '# Ex 31 · Making Decisions\n\n用 `input` + 嵌套 `if` 做简单选择游戏。\n\n## 目标\n- 根据用户输入走不同分支\n- 练习嵌套缩进\n\n## 自检\n- [ ] 至少两条完整路径你都试过\n- [ ] 输入非法选项时有提示\n',
        "entry": 'ex31.py',
        "starterFiles": {
            'ex31.py': 'print("""You enter a dark room with two doors.\nDo you go through door #1 or door #2?""")\n\ndoor = input("> ")\n\nif door == "1":\n    print("There\'s a giant bear here eating a cheese cake.")\n    print("What do you do?")\n    print("1. Take the cake.")\n    print("2. Scream at the bear.")\n    bear = input("> ")\n    if bear == "1":\n        print("The bear eats your face. Good job!")\n    elif bear == "2":\n        print("The bear eats your legs. Good job!")\n    else:\n        print(f"Well, doing {bear} is probably better.")\n        print("Bear runs away.")\nelif door == "2":\n    print("You stare into the endless abyss at Cthulhu\'s retina.")\n    print("1. Blueberries.")\n    print("2. Yellow jacket clothespins.")\n    print("3. Understanding revolvers yelling melodies.")\n    insanity = input("> ")\n    if insanity in ("1", "2"):\n        print("Your body survives powered by a mind of jello.")\n    else:\n        print("The insanity rots your eyes into a pool of muck.")\nelse:\n    print("You stumble around and fall on a knife. Good job!")\n',
        },
        "timeoutSec": 3,
    },
    32: {
        "body": '# Ex 32 · Loops and Lists\n\n列表装一串东西；`for` 依次取出。\n\n## 目标\n- 创建列表并 `for` 遍历\n- 用 `range` 生成数字再 `append`\n\n## 自检\n- [ ] 三类列表都能打印\n- [ ] 自己再 append 一项\n',
        "entry": 'ex32.py',
        "starterFiles": {
            'ex32.py': 'the_count = [1, 2, 3, 4, 5]\nfruits = ["apples", "oranges", "pears", "apricots"]\nchange = [1, "pennies", 2, "dimes", 3, "quarters"]\n\nfor number in the_count:\n    print(f"This is count {number}")\n\nfor fruit in fruits:\n    print(f"A fruit of type: {fruit}")\n\nfor i in change:\n    print(f"I got {i}")\n\nelements = []\nfor i in range(0, 6):\n    print(f"Adding {i} to the list.")\n    elements.append(i)\n\nfor i in elements:\n    print(f"Element was: {i}")\n',
        },
        "timeoutSec": 5,
    },
    33: {
        "body": '# Ex 33 · While Loops\n\n`while`：条件为真就重复。注意更新循环变量，避免死循环。\n\n## 目标\n- 用 while 填充列表\n- 对比等效的 for/range 写法\n\n## 自检\n- [ ] i 每次都会增加\n- [ ] 列表长度符合预期\n',
        "entry": 'ex33.py',
        "starterFiles": {
            'ex33.py': 'i = 0\nnumbers = []\n\nwhile i < 6:\n    print(f"At the top i is {i}")\n    numbers.append(i)\n    i = i + 1\n    print("Numbers now:", numbers)\n    print(f"At the bottom i is {i}")\n\nprint("The numbers:")\nfor num in numbers:\n    print(num)\n',
        },
        "timeoutSec": 5,
    },
    34: {
        "body": '# Ex 34 · Accessing Elements of Lists\n\n列表下标从 0 开始：`animals[0]` 是第一只。\n\n## 目标\n- 用整数下标取元素\n- 分清「第 N 个」与「下标 N-1」\n\n## 自检\n- [ ] 能正确指出 ordinal vs cardial\n- [ ] 试一下负数下标 `animals[-1]`\n',
        "entry": 'ex34.py',
        "starterFiles": {
            'ex34.py': 'animals = ["bear", "python3", "peacock", "kangaroo", "whale", "platypus"]\n\nprint("The animal at 0:", animals[0])\nprint("The 1st animal is at 0 and is a", animals[0])\nprint("The 2nd animal is at 1 and is a", animals[1])\nprint("The 3rd animal is at 2 and is a", animals[2])\nprint("The animal at 3:", animals[3])\nprint("The 5th animal is at 4 and is a", animals[4])\nprint("The animal at 2:", animals[2])\nprint("The 6th animal is at 5 and is a", animals[5])\nprint("The animal at 4:", animals[4])\nprint("Last animal via -1:", animals[-1])\n',
        },
        "timeoutSec": 5,
    },
    35: {
        "body": '# Ex 35 · Branches and Functions\n\n小冒险：函数 + `input` + 分支，房间之间互相调用。\n\n## 目标\n- 用函数表示不同场景\n- 在分支里调用下一个场景\n\n## 自检\n- [ ] 至少通关一条安全路线\n- [ ] 读懂函数如何「跳转」\n',
        "entry": 'ex35.py',
        "starterFiles": {
            'ex35.py': 'from sys import exit\n\n\ndef gold_room():\n    print("This room is full of gold. How much do you take?")\n    choice = input("> ")\n    if choice.isnumeric():\n        how_much = int(choice)\n    else:\n        dead("Man, learn to type a number.")\n        return\n    if how_much < 50:\n        print("Nice, you\'re not greedy. You win!")\n        exit(0)\n    else:\n        dead("You greedy goose!")\n\n\ndef bear_room():\n    print("There is a bear here.")\n    print("The bear has a bunch of honey.")\n    print("The fat bear is in front of another door.")\n    print("How are you going to move the bear?")\n    bear_moved = False\n    while True:\n        choice = input("> ")\n        if choice == "take honey":\n            dead("The bear looks at you then slaps your face off.")\n        elif choice == "taunt bear" and not bear_moved:\n            print("The bear has moved from the door.")\n            bear_moved = True\n        elif choice == "taunt bear" and bear_moved:\n            dead("The bear gets pissed off and chews your leg off.")\n        elif choice == "open door" and bear_moved:\n            gold_room()\n            return\n        else:\n            print("I got no idea what that means.")\n\n\ndef cthulhu_room():\n    print("Here you see the great evil Cthulhu.")\n    print("It, uh, stares at you and you go insane.")\n    print("Do you flee for your life or eat your head?")\n    choice = input("> ")\n    if "flee" in choice:\n        start()\n    elif "head" in choice:\n        dead("Well that was tasty!")\n    else:\n        cthulhu_room()\n\n\ndef dead(why):\n    print(why, "Good job!")\n    exit(0)\n\n\ndef start():\n    print("You are in a dark room.")\n    print("There is a door to your right and left.")\n    print("Which one do you take?")\n    choice = input("> ")\n    if choice == "left":\n        bear_room()\n    elif choice == "right":\n        cthulhu_room()\n    else:\n        dead("You stumble around the room until you starve.")\n\n\nstart()\n',
        },
        "timeoutSec": 3,
    },
    36: {
        "body": '# Ex 36 · Designing and Debugging\n\n调试清单练习：用打印与断言缩小问题范围。\n\n## 目标\n- 按步骤检查假设\n- 用临时 `print` / `assert` 验证中间状态\n\n## 自检\n- [ ] 看懂调试步骤输出\n- [ ] 故意弄坏一处，用清单找回来\n',
        "entry": 'ex36.py',
        "starterFiles": {
            'ex36.py': 'def buggy_average(nums):\n    """Intentionally easy to inspect."""\n    print("[debug] nums =", nums)\n    total = 0\n    for n in nums:\n        total += n\n        print(f"[debug] after +{n}, total={total}")\n    assert len(nums) > 0, "empty list"\n    avg = total / len(nums)\n    print("[debug] avg =", avg)\n    return avg\n\n\nprint("Debugging checklist:")\nprint("1. Reproduce with a tiny example")\nprint("2. Print / assert intermediate values")\nprint("3. Change one thing at a time")\nprint("4. Keep a notes file of what you tried")\nprint()\nprint("result:", buggy_average([2, 4, 6, 8]))\n',
        },
        "timeoutSec": 5,
    },
    37: {
        "body": '# Ex 37 · Symbol Review\n\n符号速查：把常见关键字/运算符打印成小抄。\n\n## 目标\n- 复习关键字与运算符含义\n- 对照输出查漏补缺\n\n## 自检\n- [ ] 标出仍不熟的 3 个符号\n- [ ] 给表里补一行你自己的例子\n',
        "entry": 'ex37.py',
        "starterFiles": {
            'ex37.py': 'symbols = [\n    ("and", "逻辑与"),\n    ("or", "逻辑或"),\n    ("not", "逻辑非"),\n    ("if/elif/else", "分支"),\n    ("for/while", "循环"),\n    ("def/return", "函数"),\n    ("class", "类"),\n    ("import/from", "导入"),\n    ("try/except", "异常"),\n    ("True/False/None", "内建常量"),\n    ("+/ -/*/ / // %", "算术"),\n    ("== != < > <= >=", "比较"),\n    ("[] {} ()", "容器/调用/优先级"),\n]\n\nprint(f\'{"symbol":20} meaning\')\nprint("-" * 40)\nfor sym, meaning in symbols:\n    print(f"{sym:20} {meaning}")\n',
        },
        "timeoutSec": 5,
    },
    38: {
        "body": '# Ex 38 · Doing Things to Lists\n\n列表方法：`append` `pop` 等会改原列表。\n\n## 目标\n- 练习常见 list 方法\n- 观察方法调用后列表如何变化\n\n## 自检\n- [ ] 每一步打印都看懂了\n- [ ] 试 `extend` 或 `insert`\n',
        "entry": 'ex38.py',
        "starterFiles": {
            'ex38.py': 'ten_things = "Apples Oranges Crows Telephone Light Sugar"\nprint("Wait there are not 10 things in that list. Let\'s fix that.")\n\nstuff = ten_things.split(" ")\nmore_stuff = ["Day", "Night", "Song", "Frisbee", "Corn", "Banana", "Girl", "Boy"]\n\nwhile len(stuff) != 10:\n    next_one = more_stuff.pop()\n    print("Adding:", next_one)\n    stuff.append(next_one)\n    print(f"There are {len(stuff)} items now.")\n\nprint("There we go:", stuff)\nprint("Let\'s do some things with stuff.")\nprint(stuff[1])\nprint(stuff[-1])\nprint(stuff.pop())\nprint(" ".join(stuff))\nprint("#".join(stuff[3:5]))\n',
        },
        "timeoutSec": 5,
    },
    39: {
        "body": '# Ex 39 · Dictionaries, Oh Lovely Dictionaries\n\n字典：用键查找值，而不是靠位置。\n\n## 目标\n- 创建 dict 并读写键\n- 遍历 `items()`\n\n## 自检\n- [ ] 能用州缩写查全名\n- [ ] 删除一个键后再打印\n',
        "entry": 'ex39.py',
        "starterFiles": {
            'ex39.py': 'states = {\n    "Oregon": "OR",\n    "Florida": "FL",\n    "California": "CA",\n    "New York": "NY",\n    "Michigan": "MI",\n}\n\ncities = {\n    "CA": "San Francisco",\n    "MI": "Detroit",\n    "FL": "Jacksonville",\n}\n\ncities["NY"] = "New York"\ncities["OR"] = "Portland"\n\nprint("-" * 10)\nprint("NY State has:", cities["NY"])\nprint("OR State has:", cities["OR"])\n\nprint("-" * 10)\nprint("Michigan\'s abbreviation is:", states["Michigan"])\nprint("Florida\'s abbreviation is:", states["Florida"])\n\nprint("-" * 10)\nprint("Michigan has:", cities[states["Michigan"]])\nprint("Florida has:", cities[states["Florida"]])\n\nprint("-" * 10)\nfor state, abbrev in list(states.items()):\n    print(f"{state} is abbreviated {abbrev}")\n\nprint("-" * 10)\nfor abbrev, city in list(cities.items()):\n    print(f"{abbrev} has the city {city}")\n\nprint("-" * 10)\nstate = states.get("Texas")\nif not state:\n    print("Sorry, no Texas.")\ncity = cities.get("TX", "Does Not Exist")\nprint(f"The city for the state \'TX\' is: {city}")\n',
        },
        "timeoutSec": 5,
    },
    40: {
        "body": '# Ex 40 · Modules, Classes, and Objects\n\n类像模块的加强版：用 `MyClass()` 得到对象，再用 `.` 取属性/方法。\n\n## 目标\n- 定义 class 与 `__init__`\n- 创建实例并调用方法\n\n## 自检\n- [ ] 两首歌都能唱出来\n- [ ] 再给 Song 加一个方法\n',
        "entry": 'ex40.py',
        "starterFiles": {
            'ex40.py': 'class Song:\n    def __init__(self, lyrics):\n        self.lyrics = lyrics\n\n    def sing_me_a_song(self):\n        for line in self.lyrics:\n            print(line)\n\n\nhappy_bday = Song([\n    "Happy birthday to you",\n    "I don\'t want to get sued",\n    "So I\'ll stop right there",\n])\n\nbulls_on_parade = Song([\n    "They rally around tha family",\n    "With pockets full of shells",\n])\n\nhappy_bday.sing_me_a_song()\nprint("---")\nbulls_on_parade.sing_me_a_song()\n',
        },
        "timeoutSec": 5,
    },
    41: {
        "body": '# Ex 41 · Learning to Speak Object Oriented\n\nOOP 词汇小词典：class / object / instance / attribute / method。\n\n## 目标\n- 用代码演示术语含义\n- 能用自己的话解释每个词\n\n## 自检\n- [ ] 分清 class 与 instance\n- [ ] 指出哪个是 attribute、哪个是 method\n',
        "entry": 'ex41.py',
        "starterFiles": {
            'ex41.py': 'class Dog:\n    """A class is a blueprint."""\n\n    def __init__(self, name):\n        self.name = name  # attribute\n\n    def bark(self):\n        return f"{self.name} says woof!"  # method\n\n\nprint("class:", Dog)\nfido = Dog("Fido")  # object / instance\nprint("instance:", fido)\nprint("attribute name:", fido.name)\nprint("method bark():", fido.bark())\n\nvocab = {\n    "class": "blueprint for objects",\n    "object/instance": "a concrete value built from a class",\n    "attribute": "data hanging off self",\n    "method": "function hanging off self",\n}\nfor k, v in vocab.items():\n    print(f"- {k}: {v}")\n',
        },
        "timeoutSec": 5,
    },
    42: {
        "body": '# Ex 42 · Is-A, Has-A, Objects, and Classes\n\nis-a：继承关系。has-a：组合（里面有另一个对象）。\n\n## 目标\n- 用继承表达 Animal → Dog\n- 用属性表达 Person has-a pet\n\n## 自检\n- [ ] 能指出代码里的 is-a / has-a\n- [ ] 再加一种 Animal 子类\n',
        "entry": 'ex42.py',
        "starterFiles": {
            'ex42.py': 'class Animal:\n    pass\n\n\nclass Dog(Animal):\n    def __init__(self, name):\n        self.name = name\n\n\nclass Cat(Animal):\n    def __init__(self, name):\n        self.name = name\n\n\nclass Person:\n    def __init__(self, name):\n        self.name = name\n        self.pet = None  # has-a pet (maybe)\n\n\nclass Employee(Person):\n    def __init__(self, name, salary):\n        super().__init__(name)\n        self.salary = salary\n\n\nrover = Dog("Rover")\nsatan = Cat("Satan")\nmary = Person("Mary")\nmary.pet = satan\nfrank = Employee("Frank", 120000)\nfrank.pet = rover\n\nprint("Dog is-a Animal?", isinstance(rover, Animal))\nprint("Mary has-a pet:", mary.pet.name)\nprint("Frank is-a Person?", isinstance(frank, Person))\nprint("Frank has-a pet:", frank.pet.name, "salary:", frank.salary)\n',
        },
        "timeoutSec": 5,
    },
    43: {
        "body": '# Ex 43 · Basic Object-Oriented Analysis and Design\n\n迷你场景：用类描述「地图 / 房间 / 引擎」的职责划分。\n\n## 目标\n- 把概念拆成几个类\n- 引擎负责流程，房间负责描写\n\n## 自检\n- [ ] 跑通两个房间\n- [ ] 试着再加一个 Room 子类\n',
        "entry": 'ex43.py',
        "starterFiles": {
            'ex43.py': 'class Scene:\n    def enter(self):\n        raise NotImplementedError\n\n\nclass Forest(Scene):\n    def enter(self):\n        print("You are in a misty forest. Paths: cabin / lake")\n        return "cabin"\n\n\nclass Cabin(Scene):\n    def enter(self):\n        print("A warm cabin. You rest. The end.")\n        return "finished"\n\n\nclass Map:\n    scenes = {\n        "forest": Forest(),\n        "cabin": Cabin(),\n    }\n\n    def __init__(self, start):\n        self.start = start\n\n    def next_scene(self, name):\n        return self.scenes.get(name)\n\n\nclass Engine:\n    def __init__(self, scene_map):\n        self.scene_map = scene_map\n\n    def play(self):\n        current = self.scene_map.next_scene(self.scene_map.start)\n        while current:\n            nxt = current.enter()\n            if nxt == "finished":\n                break\n            current = self.scene_map.next_scene(nxt)\n\n\nEngine(Map("forest")).play()\n',
        },
        "timeoutSec": 5,
    },
    44: {
        "body": '# Ex 44 · Inheritance Versus Composition\n\n继承：是一种。组合：有一个。很多时候组合更灵活。\n\n## 目标\n- 对比继承调用与组合委托\n- 体会何时该用哪一种\n\n## 自检\n- [ ] 两种写法都能打印\n- [ ] 用自己的话各举一例\n',
        "entry": 'ex44.py',
        "starterFiles": {
            'ex44.py': 'class Parent:\n    def implicit(self):\n        print("PARENT implicit()")\n\n    def override(self):\n        print("PARENT override()")\n\n    def altered(self):\n        print("PARENT altered()")\n\n\nclass Child(Parent):\n    def override(self):\n        print("CHILD override()")\n\n    def altered(self):\n        print("CHILD, BEFORE PARENT altered()")\n        super().altered()\n        print("CHILD, AFTER PARENT altered()")\n\n\nprint("=== Inheritance ===")\ndad = Parent()\nson = Child()\ndad.implicit()\nson.implicit()\ndad.override()\nson.override()\ndad.altered()\nson.altered()\n\n\nclass Other:\n    def override(self):\n        print("OTHER override()")\n\n    def implicit(self):\n        print("OTHER implicit()")\n\n    def altered(self):\n        print("OTHER altered()")\n\n\nclass Composed:\n    def __init__(self):\n        self.other = Other()\n\n    def implicit(self):\n        self.other.implicit()\n\n    def override(self):\n        print("COMPOSED override()")\n\n    def altered(self):\n        print("COMPOSED, BEFORE OTHER altered()")\n        self.other.altered()\n        print("COMPOSED, AFTER OTHER altered()")\n\n\nprint("\\n=== Composition ===")\nc = Composed()\nc.implicit()\nc.override()\nc.altered()\n',
        },
        "timeoutSec": 5,
    },
    45: {
        "body": '# Ex 45 · You Make a Game\n\n极简文字游戏骨架：场景字典 + 主循环。在此基础上可自行扩展。\n\n## 目标\n- 跑通一个可玩的迷你循环\n- 看懂如何加新场景\n\n## 自检\n- [ ] 能从 start 走到 end\n- [ ] 新增一个场景名并接到地图\n',
        "entry": 'ex45.py',
        "starterFiles": {
            'ex45.py': 'def start():\n    print("You wake up in a train station.")\n    print("Go north to the plaza, or east to the cafe?")\n    choice = input("> ").strip().lower()\n    if choice == "north":\n        return "plaza"\n    if choice == "east":\n        return "cafe"\n    print("Confused, you stay put.")\n    return "start"\n\n\ndef plaza():\n    print("A fountain sparkles. You find a ticket. You win!")\n    return "end"\n\n\ndef cafe():\n    print("Coffee smell. You rest, then head back.")\n    return "start"\n\n\nSCENES = {\n    "start": start,\n    "plaza": plaza,\n    "cafe": cafe,\n}\n\nroom = "start"\nwhile room != "end":\n    room = SCENES[room]()\nprint("--- thanks for playing ---")\n',
        },
        "timeoutSec": 3,
    },
    46: {
        "body": '# Ex 46 · A Project Skeleton\n\n小型项目布局：包目录 + `__init__.py` + 可运行入口。\n\n## 目标\n- 认识 package 结构\n- 从入口脚本导入包内函数\n\n## 自检\n- [ ] `ex46.py` 能导入 `skeleton` 并打印\n- [ ] 打开包内文件看清分工\n',
        "entry": 'ex46.py',
        "starterFiles": {
            'ex46.py': 'from skeleton import greet, VERSION\n\nprint(f"skeleton package v{VERSION}")\nprint(greet("LPTHW learner"))\n',
            'skeleton/__init__.py': '"""Tiny demo package for Ex 46."""\n\nVERSION = "0.1.0"\n\n\ndef greet(name: str) -> str:\n    return f"Hello from skeleton, {name}!"\n',
            'skeleton/core.py': 'def add(a, b):\n    return a + b\n',
        },
        "timeoutSec": 5,
    },
    47: {
        "body": '# Ex 47 · Automated Testing\n\n用 `assert` 写可运行的小测试。入口直接跑全部断言。\n\n## 目标\n- 为函数写 assert 测试\n- 失败时能根据 AssertionError 定位\n\n## 自检\n- [ ] 全部 assert 通过\n- [ ] 故意改期望值看失败信息\n',
        "entry": 'test_ex47.py',
        "starterFiles": {
            'test_ex47.py': 'def room_paths(room, direction):\n    paths = {\n        "center": {"north": "armory", "south": "door"},\n        "armory": {"south": "center"},\n        "door": {"north": "center"},\n    }\n    return paths[room][direction]\n\n\ndef run_tests():\n    assert room_paths("center", "north") == "armory"\n    assert room_paths("center", "south") == "door"\n    assert room_paths("armory", "south") == "center"\n    assert room_paths("door", "north") == "center"\n    print("All asserts passed.")\n\n\nif __name__ == "__main__":\n    run_tests()\n',
        },
        "timeoutSec": 5,
    },
    48: {
        "body": '# Ex 48 · Advanced User Input\n\n迷你词法：把句子拆成 `(类型, 词)` 对。可从 `input` 读一句。\n\n## 目标\n- 维护一小份 lexicon\n- 把未知词标成 error 类型\n\n## 自检\n- [ ] 默认句子能正确分词\n- [ ] 自己输入一句再看结果\n',
        "entry": 'ex48.py',
        "starterFiles": {
            'ex48.py': 'LEXICON = {\n    "north": "direction",\n    "south": "direction",\n    "east": "direction",\n    "west": "direction",\n    "go": "verb",\n    "kill": "verb",\n    "eat": "verb",\n    "the": "stop",\n    "in": "stop",\n    "of": "stop",\n    "bear": "noun",\n    "princess": "noun",\n}\n\n\ndef scan(sentence: str):\n    words = sentence.lower().split()\n    result = []\n    for w in words:\n        if w in LEXICON:\n            result.append((LEXICON[w], w))\n        elif w.isnumeric():\n            result.append(("number", int(w)))\n        else:\n            result.append(("error", w))\n    return result\n\n\nprint("Type a sentence (or press Enter for demo):")\nline = input("> ").strip()\nif not line:\n    line = "go north eat the bear"\n    print("(demo)", line)\nprint(scan(line))\n',
        },
        "timeoutSec": 3,
    },
    49: {
        "body": '# Ex 49 · Making Sentences\n\n在词法结果上做迷你句法：抽出 subject / verb / object。\n\n## 目标\n- 消费 `(type, word)` 列表\n- 组成简单句子元组\n\n## 自检\n- [ ] 默认词列能解析\n- [ ] 缺词时有清晰报错信息\n',
        "entry": 'ex49.py',
        "starterFiles": {
            'ex49.py': 'class ParserError(Exception):\n    pass\n\n\ndef peek(word_list):\n    return word_list[0][0] if word_list else None\n\n\ndef match(word_list, expected):\n    if word_list and word_list[0][0] == expected:\n        return word_list.pop(0)\n    return None\n\n\ndef skip(word_list, word_type):\n    while peek(word_list) == word_type:\n        match(word_list, word_type)\n\n\ndef parse_verb(word_list):\n    skip(word_list, "stop")\n    if peek(word_list) == "verb":\n        return match(word_list, "verb")\n    raise ParserError("Expected a verb.")\n\n\ndef parse_object(word_list):\n    skip(word_list, "stop")\n    if peek(word_list) in ("noun", "direction"):\n        return match(word_list, peek(word_list))\n    raise ParserError("Expected a noun or direction.")\n\n\ndef parse_subject(word_list):\n    skip(word_list, "stop")\n    if peek(word_list) == "noun":\n        return match(word_list, "noun")\n    if peek(word_list) == "verb":\n        return ("noun", "player")\n    raise ParserError("Expected a subject.")\n\n\ndef parse_sentence(word_list):\n    subj = parse_subject(word_list)\n    verb = parse_verb(word_list)\n    obj = parse_object(word_list)\n    return (subj[1], verb[1], obj[1])\n\n\nwords = [("noun", "bear"), ("verb", "eat"), ("stop", "the"), ("noun", "princess")]\nprint("tokens:", words)\nprint("sentence:", parse_sentence(words))\n',
        },
        "timeoutSec": 5,
    },
    50: {
        "body": '# Ex 50 · Your First Website\n\n不启动真实服务器：用函数模拟「收到请求 → 返回响应」，全程可离线跑。\n\n## 目标\n- 理解请求/响应的最小模型\n- 写一个返回 HTML 字符串的 handler\n\n## 自检\n- [ ] 打印出 status 与 body\n- [ ] 改 HTML 文案再跑一次\n',
        "entry": 'ex50.py',
        "starterFiles": {
            'ex50.py': 'def handle_request(method: str, path: str) -> tuple[int, str, str]:\n    """Return (status, content_type, body)."""\n    print(f"[REQ] {method} {path}")\n    if method == "GET" and path == "/":\n        body = "<h1>Hello LPTHW</h1><p>Offline fake web server.</p>"\n        return 200, "text/html", body\n    return 404, "text/plain", "Not Found"\n\n\ndef send_response(status: int, content_type: str, body: str) -> None:\n    print(f"[RES] {status}")\n    print(f"Content-Type: {content_type}")\n    print()\n    print(body)\n\n\nstatus, ctype, body = handle_request("GET", "/")\nsend_response(status, ctype, body)\nprint("---")\nstatus, ctype, body = handle_request("GET", "/missing")\nsend_response(status, ctype, body)\n',
        },
        "timeoutSec": 5,
    },
    51: {
        "body": '# Ex 51 · Getting Input from a Browser\n\n模拟表单提交：把「浏览器发来的字段」做成 dict，handler 读取后回显。\n\n## 目标\n- 用 dict 表示 form/query 参数\n- 根据输入生成不同响应\n\n## 自检\n- [ ] 两种名字都能生成问候\n- [ ] 缺省参数有默认值\n',
        "entry": 'ex51.py',
        "starterFiles": {
            'ex51.py': 'def handle_form(method: str, path: str, form: dict) -> str:\n    print(f"[REQ] {method} {path} form={form}")\n    if path == "/hello" and method == "POST":\n        name = form.get("name") or "World"\n        greet = form.get("greet") or "Hi"\n        return f"<p>{greet}, {name}!</p>"\n    return "<p>unknown form</p>"\n\n\nprint(handle_form("POST", "/hello", {"name": "Ada", "greet": "Hello"}))\nprint(handle_form("POST", "/hello", {}))\nprint(handle_form("GET", "/", {}))\n',
        },
        "timeoutSec": 5,
    },
    52: {
        "body": '# Ex 52 · The Start of Your Web Game\n\n进程内迷你路由器：路径映射到场景函数，模拟「网页版」文字游戏的一跳。\n\n## 目标\n- 用 dict 做路由表\n- 一次请求进入一个场景并得到 HTML\n\n## 自检\n- [ ] `/game?door=left` 与 `right` 结果不同\n- [ ] 404 路径有提示\n',
        "entry": 'ex52.py',
        "starterFiles": {
            'ex52.py': 'def scene_index(params: dict) -> str:\n    return "<h1>Web Game</h1><p>Try /game?door=left or door=right</p>"\n\n\ndef scene_game(params: dict) -> str:\n    door = params.get("door", "")\n    if door == "left":\n        return "<p>You find a quiet library. Safe for now.</p>"\n    if door == "right":\n        return "<p>A dragon snorts. Maybe go left next time.</p>"\n    return "<p>Pick a door via ?door=left|right</p>"\n\n\nROUTES = {\n    "/": scene_index,\n    "/game": scene_game,\n}\n\n\ndef dispatch(path: str, params: dict | None = None) -> str:\n    params = params or {}\n    print(f"[REQ] GET {path} {params}")\n    handler = ROUTES.get(path)\n    if not handler:\n        body = f"<p>404 {path}</p>"\n    else:\n        body = handler(params)\n    print("[RES]", body)\n    return body\n\n\ndispatch("/")\ndispatch("/game", {"door": "left"})\ndispatch("/game", {"door": "right"})\ndispatch("/nope")\n',
        },
        "timeoutSec": 5,
    },
}

def write_lesson(track: str, lesson_id: str, data: dict) -> None:
    folder = TRACKS / track
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{lesson_id}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def gen_lpthw() -> None:
    for n in range(0, 53):
        lesson_id = f"ex{n:02d}"
        title = LPTHW_TITLES.get(n, f"Exercise {n}")
        if n not in FULL_LPTHW:
            raise KeyError(f"FULL_LPTHW missing exercise {n}; expected full coverage 0-52")
        payload = {
            "title": f"Ex {n}: {title}",
            "priority": False,
            "outlineOnly": False,
            "requires": [],
            "checklist": ["对照书本做一遍", "改几个数字/字符串再跑"],
            **FULL_LPTHW[n],
        }
        payload.setdefault("timeoutSec", 5)
        write_lesson("lpthw", lesson_id, payload)

ASYNC_LESSONS = [
    (
        "a01",
        "asyncio 基础",
        """# A01 · asyncio 基础

企业 LLM 服务几乎都是异步的。先建立直觉：`async def` 定义协程，`await` 让出等待。

## 目标
- 写一个异步函数并 `asyncio.run`
- 理解「看起来像同步，实际可并发」
""",
        "a01_main.py",
        {
            "a01_main.py": '''import asyncio
import time


async def fetch_fake(name: str, delay: float) -> str:
    print(f"start {name}")
    await asyncio.sleep(delay)
    print(f"done {name}")
    return f"{name}-ok"


async def main() -> None:
    t0 = time.perf_counter()
    # Sequential awaits (not concurrent yet)
    a = await fetch_fake("A", 0.3)
    b = await fetch_fake("B", 0.3)
    print(a, b, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a02",
        "create_task 与 gather",
        """# A02 · 并发：task / gather

把多个 IO 等待叠在一起。对比 A01 的耗时。
""",
        "a02_main.py",
        {
            "a02_main.py": '''import asyncio
import time


async def fetch_fake(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name}-ok"


async def main() -> None:
    t0 = time.perf_counter()
    results = await asyncio.gather(
        fetch_fake("A", 0.4),
        fetch_fake("B", 0.4),
        fetch_fake("C", 0.4),
    )
    print(results, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a03",
        "超时与取消",
        """# A03 · 超时与取消

LLM 调用必须设超时。练习 `wait_for` 与 `CancelledError`。
""",
        "a03_main.py",
        {
            "a03_main.py": '''import asyncio


async def slow_llm() -> str:
    await asyncio.sleep(2)
    return "too-late"


async def main() -> None:
    try:
        result = await asyncio.wait_for(slow_llm(), timeout=0.5)
        print(result)
    except asyncio.TimeoutError:
        print("TIMEOUT: upstream LLM did not respond in time")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a04",
        "httpx AsyncClient",
        """# A04 · httpx 异步 HTTP

用 `httpx.AsyncClient` 打一个公开 JSON API（需本机网络）。把状态码与耗时打出来。
""",
        "a04_main.py",
        {
            "a04_main.py": '''import asyncio
import time
import httpx


async def main() -> None:
    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get("https://httpbin.org/json")
        print("status", resp.status_code)
        print(resp.json())
    print(f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        15,
    ),
    (
        "a05",
        "流式 chunk（模拟 LLM）",
        """# A05 · 流式输出

企业聊天接口常用 token/chunk 流。这里用异步生成器模拟。
""",
        "a05_main.py",
        {
            "a05_main.py": '''import asyncio


async def fake_llm_stream(prompt: str):
    tokens = ["Hello", ", ", "this", " ", "is", " ", "streamed", " ", "output", "."]
    for t in tokens:
        await asyncio.sleep(0.05)
        yield t


async def main() -> None:
    print("prompt accepted")
    async for chunk in fake_llm_stream("hi"):
        print(chunk, end="", flush=True)
    print("\\n[done]")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a06",
        "Semaphore 限流",
        """# A06 · 并发限流

对模型 API 必须限流，避免打爆配额。用 `Semaphore` 控制同时进行的调用数。
""",
        "a06_main.py",
        {
            "a06_main.py": '''import asyncio
import time

SEM = asyncio.Semaphore(2)


async def call_model(i: int) -> str:
    async with SEM:
        print(f"enter {i}")
        await asyncio.sleep(0.3)
        print(f"leave {i}")
        return f"r{i}"


async def main() -> None:
    t0 = time.perf_counter()
    results = await asyncio.gather(*(call_model(i) for i in range(6)))
    print(results, f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a07",
        "Queue 缓冲",
        """# A07 · 生产者-消费者 Queue

请求洪峰时用队列削峰。一个生产者投递，多个 worker 消费。
""",
        "a07_main.py",
        {
            "a07_main.py": '''import asyncio


async def producer(q: asyncio.Queue) -> None:
    for i in range(5):
        await q.put({"id": i, "prompt": f"q{i}"})
        print("enqueued", i)
    for _ in range(2):
        await q.put(None)  # poison pills


async def worker(name: str, q: asyncio.Queue) -> None:
    while True:
        item = await q.get()
        if item is None:
            q.task_done()
            break
        await asyncio.sleep(0.1)
        print(name, "handled", item["id"])
        q.task_done()


async def main() -> None:
    q: asyncio.Queue = asyncio.Queue()
    await asyncio.gather(producer(q), worker("w1", q), worker("w2", q))
    print("drained")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a08",
        "结构化输出与重试",
        """# A08 · JSON 结构化输出 + 重试

工具调用/结构化输出常失败。练习：校验 JSON，失败则重试有限次。
""",
        "a08_main.py",
        {
            "a08_main.py": '''import asyncio
import json
import random
from typing import Any


async def flaky_model() -> str:
    await asyncio.sleep(0.05)
    if random.random() < 0.6:
        return "{not-json"
    return json.dumps({"action": "search", "query": "fastapi timeout"})


def validate(payload: str) -> dict[str, Any]:
    data = json.loads(payload)
    assert "action" in data and "query" in data
    return data


async def call_with_retry(max_attempts: int = 5) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        raw = await flaky_model()
        try:
            data = validate(raw)
            print(f"success on attempt {attempt}")
            return data
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"attempt {attempt} failed: {exc}")
    raise RuntimeError(f"failed after retries: {last_err}")


async def main() -> None:
    print(await call_with_retry())


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
    (
        "a09",
        "迷你 RAG 流水线骨架",
        """# A09 · 异步 RAG 骨架

流程：读本地 docs → 朴素检索 → 拼 prompt → 假 LLM → 写 `answer.txt`。

这是企业落地的主干形状；真实项目会替换检索与模型客户端。
""",
        "a09_main.py",
        {
            "a09_main.py": '''import asyncio
from pathlib import Path


DOCS = {
    "fastapi.txt": "FastAPI supports async def routes and dependency injection.",
    "timeouts.txt": "Always set timeouts and retries for LLM HTTP calls.",
    "rag.txt": "RAG retrieves context documents before generation.",
}


async def retrieve(query: str, k: int = 2) -> list[str]:
    await asyncio.sleep(0.05)
    scored = []
    for name, text in DOCS.items():
        score = sum(1 for w in query.lower().split() if w in text.lower())
        scored.append((score, name, text))
    scored.sort(reverse=True)
    return [f"[{n}] {t}" for s, n, t in scored[:k] if s > 0] or [f"[{scored[0][1]}] {scored[0][2]}"]


async def fake_llm(prompt: str) -> str:
    await asyncio.sleep(0.1)
    return "Based on context: " + prompt.split("Context:", 1)[-1][:120].strip()


async def main() -> None:
    query = "How do I set timeouts in FastAPI LLM calls?"
    ctx = await retrieve(query)
    prompt = "Question: " + query + "\\nContext:\\n" + "\\n".join(ctx)
    answer = await fake_llm(prompt)
    Path("answer.txt").write_text(answer + "\\n", encoding="utf-8")
    print(answer)
    print("wrote answer.txt")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        5,
    ),
]


PYTORCH_LESSONS = [
    (
        "p01",
        "Tensor 基础",
        """# P01 · Tensor 基础

张量是 PyTorch 的核心数据结构。练习创建、形状、dtype。

若报错 `No module named 'torch'`，在项目根执行（先 `proxy_on`）：
`uv sync --extra ml`
或 `npm run install:ml`

不要使用 Linux 的 `whl/cpu` 索引。本课会检测 MPS。
""",
        "p01_main.py",
        {
            "p01_main.py": '''import torch


def pick_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


device = pick_device()
print("torch", torch.__version__)
print("device", device)
print("mps_built", torch.backends.mps.is_built(), "mps_available", torch.backends.mps.is_available())

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], device=device)
print("x", x)
print("shape", tuple(x.shape), "dtype", x.dtype)
print("x + 1", x + 1)
print("matmul", x @ x.T)
'''
        },
        30,
        ["torch"],
    ),
    (
        "p02",
        "autograd",
        """# P02 · 自动求导

`requires_grad=True` 的张量可反传。理解 `loss.backward()` 与 `.grad`。
注意：本课默认 CPU，梯度查看更直观。
""",
        "p02_main.py",
        {
            "p02_main.py": '''import torch

x = torch.tensor(2.0, requires_grad=True)
y = x**2 + 3 * x + 1
y.backward()
print("y", float(y))
print("dy/dx", float(x.grad))
'''
        },
        30,
        ["torch"],
    ),
    (
        "p03",
        "nn.Module 一步优化",
        """# P03 · Module + 一步优化

线性层拟合一个简单目标，跑几步 SGD。
""",
        "p03_main.py",
        {
            "p03_main.py": '''import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

x = torch.linspace(-1, 1, 20).unsqueeze(1)
y = 2 * x + 0.5

for step in range(50):
    pred = model(x)
    loss = loss_fn(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 10 == 0:
        print(f"step={step} loss={loss.item():.4f}")

print("weight", model.weight.item(), "bias", model.bias.item())
'''
        },
        60,
        ["torch"],
    ),
    (
        "p04",
        "Dataset / DataLoader",
        """# P04 · Dataset 与 DataLoader

从 `data.csv` 读入，按 batch 迭代。
""",
        "p04_main.py",
        {
            "data.csv": "x,y\\n0,0.5\\n1,2.5\\n2,4.5\\n3,6.5\\n4,8.5\\n",
            "p04_main.py": '''import csv
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset


class CsvXy(Dataset):
    def __init__(self, path: str) -> None:
        rows = list(csv.DictReader(Path(path).open()))
        self.x = torch.tensor([[float(r["x"])] for r in rows], dtype=torch.float32)
        self.y = torch.tensor([[float(r["y"])] for r in rows], dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int):
        return self.x[idx], self.y[idx]


ds = CsvXy("data.csv")
loader = DataLoader(ds, batch_size=2, shuffle=False)
for batch_x, batch_y in loader:
    print("batch", batch_x.tolist(), batch_y.tolist())
'''
        },
        60,
        ["torch"],
    ),
    (
        "p05",
        "训练循环并保存权重",
        """# P05 · 训练循环 + state_dict

训练后保存 `model.pt`，在文件树中确认生成。
""",
        "p05_main.py",
        {
            "p05_main.py": '''import torch
import torch.nn as nn

torch.manual_seed(0)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()
x = torch.linspace(-1, 1, 40).unsqueeze(1)
y = -1.5 * x + 0.25

for epoch in range(80):
    loss = loss_fn(model(x), y)
    opt.zero_grad()
    loss.backward()
    opt.step()

torch.save(model.state_dict(), "model.pt")
print("saved model.pt loss=", float(loss))
'''
        },
        90,
        ["torch"],
    ),
    (
        "p06",
        "推理脚本",
        """# P06 · 加载权重推理

先运行 P05 生成 `model.pt`，或本课会训练一个临时模型再推理。把预测写入 `preds.txt`。
""",
        "p06_main.py",
        {
            "p06_main.py": '''from pathlib import Path

import torch
import torch.nn as nn

model = nn.Linear(1, 1)
path = Path("model.pt")
if not path.exists():
    # bootstrap if p05 not run
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()
    x = torch.linspace(-1, 1, 40).unsqueeze(1)
    y = -1.5 * x + 0.25
    for _ in range(80):
        loss = loss_fn(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
    torch.save(model.state_dict(), path)

model.load_state_dict(torch.load(path, weights_only=True))
model.eval()
with torch.no_grad():
    xs = torch.tensor([[-1.0], [0.0], [1.0]])
    preds = model(xs).squeeze(1).tolist()

lines = [f"{x[0]:.1f},{p:.4f}" for x, p in zip(xs.tolist(), preds)]
Path("preds.txt").write_text("\\n".join(lines) + "\\n", encoding="utf-8")
print("preds", preds)
'''
        },
        90,
        ["torch"],
    ),
    (
        "p07",
        "小文本分类",
        """# P07 · 迷你文本分类

Bag of Words + 线性层。数据很小，默认 CPU 即可；有 MPS 时可自行 `.to("mps")` 试验。
""",
        "p07_main.py",
        {
            "p07_main.py": '''import torch
import torch.nn as nn

pairs = [
    ("good film great actors", 1),
    ("amazing movie loved it", 1),
    ("terrible plot boring", 0),
    ("bad acting waste time", 0),
    ("wonderful story", 1),
    ("awful experience", 0),
]

vocab: dict[str, int] = {}
for text, _ in pairs:
    for w in text.split():
        vocab.setdefault(w, len(vocab))


def vectorize(text: str) -> torch.Tensor:
    v = torch.zeros(len(vocab))
    for w in text.split():
        if w in vocab:
            v[vocab[w]] += 1
    return v


X = torch.stack([vectorize(t) for t, _ in pairs])
y = torch.tensor([label for _, label in pairs], dtype=torch.float32).unsqueeze(1)

model = nn.Linear(len(vocab), 1)
opt = torch.optim.Adam(model.parameters(), lr=0.1)
loss_fn = nn.BCEWithLogitsLoss()

for epoch in range(200):
    logits = model(X)
    loss = loss_fn(logits, y)
    opt.zero_grad()
    loss.backward()
    opt.step()

with torch.no_grad():
    probs = torch.sigmoid(model(X)).squeeze(1)
print("probs", [round(float(p), 3) for p in probs])
print("loss", float(loss))
'''
        },
        120,
        ["torch"],
    ),
    (
        "p08",
        "asyncio.to_thread 桥接",
        """# P08 · 异步服务里跑同步推理

FastAPI/异步 worker 中不要直接在事件循环里跑重计算。用 `asyncio.to_thread` 包一层。
""",
        "p08_main.py",
        {
            "p08_main.py": '''import asyncio
import time

import torch
import torch.nn as nn

model = nn.Linear(4, 2)
model.eval()


def sync_infer(batch: list[list[float]]) -> list[list[float]]:
    # pretend this is heavy
    time.sleep(0.2)
    with torch.no_grad():
        x = torch.tensor(batch, dtype=torch.float32)
        return model(x).tolist()


async def handle_request(batch: list[list[float]]) -> list[list[float]]:
    return await asyncio.to_thread(sync_infer, batch)


async def main() -> None:
    t0 = time.perf_counter()
    a, b = await asyncio.gather(
        handle_request([[0.1, 0.2, 0.3, 0.4]]),
        handle_request([[0.5, 0.4, 0.3, 0.2]]),
    )
    print("results", a, b)
    print(f"elapsed={time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
'''
        },
        60,
        ["torch"],
    ),
]


def gen_async() -> None:
    for lesson_id, title, body, entry, files, timeout in ASYNC_LESSONS:
        write_lesson(
            "async-llm",
            lesson_id,
            {
                "title": f"{lesson_id.upper()}: {title}",
                "priority": True,
                "outlineOnly": False,
                "timeoutSec": timeout,
                "requires": [],
                "entry": entry,
                "body": body,
                "starterFiles": files,
                "checklist": ["阅读说明", "运行并解释输出", "改参数再跑一次"],
            },
        )


def gen_pytorch() -> None:
    for lesson_id, title, body, entry, files, timeout, requires in PYTORCH_LESSONS:
        # fix escaped newlines in csv accidentally double-escaped
        fixed = {}
        for k, v in files.items():
            fixed[k] = v.replace("\\n", "\n") if k.endswith(".csv") else v
        write_lesson(
            "pytorch",
            lesson_id,
            {
                "title": f"{lesson_id.upper()}: {title}",
                "priority": True,
                "outlineOnly": False,
                "timeoutSec": timeout,
                "requires": requires,
                "entry": entry,
                "body": body,
                "starterFiles": fixed,
                "checklist": ["确认 torch 已安装（如需要）", "运行通过", "查看生成的文件"],
            },
        )


if __name__ == "__main__":
    gen_lpthw()
    gen_async()
    gen_pytorch()
    from gen_llm_from_scratch import main as gen_lfs

    gen_lfs()
    print("content generated")
