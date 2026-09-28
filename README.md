# CBR Clinical Decision Support Demo

一个基于前面实操流程搭建的最小可运行 CBR 系统原型：

**Retrieve → Reuse → Revise → Retain**

当前版本：
- Python + Streamlit + SQLite
- 486 个教学用模拟病例
- 5 个教学属性
- Top-K 相似病例检索
- 成功病例筛选
- 历史治疗方案汇总
- Revise 优先级
- Retain 新病例

> 仅用于教学和科研原型，不可用于真实临床决策。

## 启动

在项目目录打开终端：

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器一般会打开：

```text
http://localhost:8501
```

## 下一步换成脊柱侧弯

主要修改：
1. `similarity.py`：把当前5个属性替换为 Cobb angle、Risser、curve type、skeletal maturity、ATR 等真实变量，并重新定义权重/局部相似度。
2. `db.py`：改成企业真实病例字段。
3. `app.py`：把输入表单改成真实脊柱侧弯患者表单。
4. 导入企业病例后，验证系统相似度与临床专家判断的一致性。


## UI V2
- 医疗科技风视觉设计
- 首页总览与 KPI 卡片
- 更清晰的 Retrieve / Reuse / Revise / Retain 流程
- 已加入 Railway 启动配置
