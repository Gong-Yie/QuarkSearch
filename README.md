# QuarkSearch-快搜

![QuarkSearch](/QuarkSearch.jpg)

QuarkSearch，一款基于langchain框架的多agent搜索增强工具

~~使用mcp进行搜索~~使用tools进行搜索

## 快搜能干什么

首先将你脑海中想搜索的模糊的概念交给快搜，快搜对其进行增强（列出所有可能的结果）。接着，快搜将在各个平台进行搜索，最后把最符合你想搜索的结果返回给你，这就是快搜。

## 设计思路

![设计思路](/设计思路.png)

## 环境要求

~~Node.js~~
~~Rust~~
~~移除了mcp，所以不需要了~~
python 3.10+

## 食用方式

首先clone项目

```bash
git@github.com:Gong-Yie/QuarkSearch.git
```

接着创建虚拟环境（推荐）

```bash
python -m venv .venv
venv\Script\activate
```

然后下载依赖

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

创建.env文件,并填写好相关API

```bash
cp .env.example .env
```

最后运行main.py即可

```bash
python main.py
```

## 快搜的目标(开发进度)

- [x] 简单的搜索词增强
- [x] 搜索词翻译扩展
- [ ] 各大平台的检索 ~~完成了一部分~~
- [ ] 判断相关性
- [ ] 流程透明化
- [ ] 好看的Web-UI

### 快搜接入的搜索平台

- [x] bilibili
- [x] github
- [ ] 必应
- [ ] google
- [ ] 中国知网
- [ ] 微信
- [ ] 等

## 注意事项

github相关搜索需要github个人访问令牌（Personal Access Token）
获取方式：

1. 登录 GitHub，点击头像 → Settings。

2. 在页面左侧找到 Developer settings → Personal access tokens → Tokens (classic)。

3. 点击 Generate new token (classic)。

4. 为 Token 命名，并勾选 repo 和 user 等所需权限。

5. 点击 Generate token，并立即复制保存生成的 Token。

## 最后

欢迎来[快搜交流群](https://qm.qq.com/q/DipVDg2A5G)玩

![交流群](/交流群.jpg)
