rules = [
    {
        "type": "header",
        "pattern": r"(Date of last issue.+?)2019/\d+/\d+",
        "replace_to": "[1]2019/12/20"
    }, {
        "type": "header",
        "pattern": r"(Revision Date: ?\r)2019/\d+/\d+",
        "replace_to": "[1]2019/12/20"
    }, {
        "type": "header",
        "pattern": r"(修订日期.+)2019年\d+月\d+日",
        "replace_to": "[1]2019年12月20日"
    }, {
        "type": "body",
        "pattern": r"(修订日期.+)2019年\d+月\d+日",
        "replace_to": "[1]2019年12月20日"
    }
]
body_start = 0
body_end = 100
