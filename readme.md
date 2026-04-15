# 落雪查分器调用小程序

一个基于落雪查分器 API 的舞萌DX、中二节奏（CHUNITHM）查分工具。

## 功能特性

- 支持舞萌（maimai）玩家数据查询
  - 玩家基本信息
  - B50 成绩（Best 35 + Best 15）
- 支持中二节奏（CHUNITHM）玩家数据查询
  - 玩家基本信息
  - Best 30、New Best 成绩

## 环境变量配置

在运行程序前，请设置以下环境变量：

```bash
# 开发者 API 密钥
export LX_API="你的开发者API密钥"

# 舞萌好友码
export MAI_USER_ID="舞萌好友码"

# 中二节奏好友码
export CHUNI_USER_ID="中二节奏好友码"
```

## 使用方法

1. 确保已安装 Python 3.10
2. 安装依赖：
```bash
pip install -r requirements.txt
```
3. 设置环境变量（见上文）
4. 运行程序：
```bash
python mai.py
python chuni.py
```

## 文件说明

- `mai.py` - 舞萌（maimai）查分模块
- `chuni.py` - 中二节奏（CHUNITHM）查分模块
- `requirements.txt` - Python 依赖包列表

## ⚠️ AI 生成声明

**本仓库代码完全由 AI 生成，作者不对代码质量进行任何保证！**

使用本代码所产生的任何后果，由使用者自行承担。

## 相关链接

- 落雪查分器：https://maimai.lxns.net/

---

*本仓库作为子模块引入博客使用，开源协议详见独立的 LICENSE 文件。*
