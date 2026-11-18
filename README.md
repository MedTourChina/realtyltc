# Lantern · 中国置业决策框架

一个**非商业**的英文信息站,帮在中国的外国人建立买房前的判断逻辑:
**资格 → 动机 → 城市 → 资产 → 交割**,五层依次可否决。

没有公司主体,不做广告,不收佣金,不导流,不收集任何数据。

- 纯静态站点,零后端、零数据库、零表单
- Python 3.10+ 生成,无第三方依赖
- 部署在 Cloudflare Pages,GitHub Actions 自动构建

---

## 一、本地运行

```bash
python build.py                              # 生成到 dist/
python -m http.server 8099 --directory dist  # 预览 http://127.0.0.1:8099
```

或者一步到位(默认 8080 端口):

```bash
python build.py --serve
```

重建社交分享图(需要 Pillow,可选):

```bash
python build.py --og
```

发布前自检(内链、锚点、title/description/canonical 是否齐全):

```bash
python check.py     # 退出码 0 才算通过
```

---

## 二、目录结构

```
realtyltc/
├── build.py                  # 生成器入口:读内容 → 写 dist/ + sitemap + robots
├── check.py                  # 静态检查:死链、锚点、元数据
├── sitegen/
│   ├── config.py             # 站点名、导航、五层框架定义、声明文案
│   ├── layout.py             # HTML 骨架、页头页脚、可复用组件
│   ├── md.py                 # 极简 Markdown 渲染器(支持 :::answer 等区块)
│   ├── svg.py                # 图标、品牌标、程序化城市天际线
│   ├── pages.py              # 首页 / 城市 / 指南
│   └── pages_extra.py        # 框架五章 / 工具 / 独立页 / FAQ
├── content/
│   ├── cities.json           # 12 座城市档案
│   ├── faq.json              # 17 条问答
│   ├── framework/*.md        # 五层框架正文(标题与顺序在 config.py)
│   ├── guides/*.md           # 10 篇规则深读
│   └── pages/*.md            # verify / about / privacy / terms / disclaimer
├── static/
│   ├── css/site.css          # 全站样式,单文件
│   ├── js/main.js            # 导航、目录高亮
│   ├── js/calc.js            # 三个计算器(纯前端,零网络请求)
│   └── img/og.png            # 社交分享图
├── docs/01-规划总案.md        # 定位、框架、内容策略、红线、里程碑
└── dist/                     # 构建产物(不入库)
```

---

## 三、内容怎么改

| 想改什么 | 改哪里 |
|---|---|
| 城市信息、价格带、板块、风险 | `content/cities.json` |
| 新增一篇指南 | `content/guides/` 新建 `.md`,写好 frontmatter |
| 框架五章正文 | `content/framework/{eligibility,motive,city,asset,closing}.md` |
| 框架标题、顺序、摘要 | `sitegen/config.py` 的 `LAYERS` |
| 独立页(verify/about/法务) | `content/pages/*.md` |
| FAQ | `content/faq.json` |
| 导航、页脚、免责声明 | `sitegen/config.py` |
| 页面结构 | `sitegen/pages.py`、`sitegen/pages_extra.py` |
| 样式 | `static/css/site.css` |

### 指南的 frontmatter

```yaml
---
title: Can foreigners buy property in China? The rules, city by city
description: 一句话说明,会进 meta description 和卡片
category: Legal & eligibility      # Legal & eligibility | Money & tax | Transaction | Living
slug: can-foreigners-buy-property-in-china
answer: 摘要,用于结构化数据
updated: 2026-03-04                 # 会显示"最后复核日期"
read: 9
related: the-one-year-rule, escrow-and-payment-stages
---
```

正文里可用自定义区块:

```
:::answer      短答案(琥珀底色)
:::note        说明
:::warn        风险提示
:::kill        止损条件(红底)
:::rule        经验法则(蓝底)
:::checklist   自查清单
:::
```

### 新增城市的步骤

1. 在 `content/cities.json` 追加一个对象(字段照抄现有城市)
2. 重新构建 —— 城市索引页、对比表、详情页、sitemap 会自动更新
3. 跑 `python check.py` 确认没有死链

`GUIDE_LAYERS`(在 `build.py`)决定每篇指南归属哪一层,框架章节页会据此自动列出相关指南。

---

## 四、发布到 GitHub + Cloudflare Pages

**仓库已经建好并推送完成:https://github.com/MedTourChina/realtyltc**

### 当前状态

| 环节 | 状态 |
|---|---|
| GitHub 仓库 + 代码推送 | ✅ 已完成 |
| CI 构建与自检(`verify` 任务) | ✅ 每次推送自动跑 |
| Cloudflare Pages 部署 | ⏸ 开关默认关闭,等你绑定 |

Cloudflare 那一步没配之前,`deploy` 任务会被跳过(不是失败),所以仓库不会挂红叉。这是由 `.github/workflows/deploy.yml` 里的 `if: vars.CLOUDFLARE_PAGES_READY == 'true'` 控制的。

### 你回来之后要做的三步

**第 1 步:在 Cloudflare 建一个同名空项目**

控制台 → *Workers & Pages* → *Create* → *Pages* → **Upload assets**(Direct Upload)→ 项目名填 `realtyltc` → 建好即可,不用真的上传文件。

> 这一步不能省。`wrangler pages deploy` 在非交互环境(CI)里不会自动创建项目,项目不存在会直接失败。

**第 2 步:拿两个值**

1. **API Token**:Cloudflare 控制台 → 右上头像 → *My Profile* → *API Tokens* → *Create Token* → 用 **Edit Cloudflare Workers** 模板,或自定义:权限 `Account · Cloudflare Pages · Edit`,资源限定到你的账号。
2. **Account ID**:控制台 → *Workers & Pages* → 概览页右侧可见。

**第 3 步:配置并打开开关**

仓库 → *Settings* → *Secrets and variables* → *Actions*:

1. 在 **Secrets** 里加两个:`CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`
2. 在 **Variables** 里加一个:`CLOUDFLARE_PAGES_READY` = `true` ← **这个变量一存,下次推送就会真的部署**

然后推任意 commit(或到 *Actions* 页点 *Run workflow*),拿到 `https://realtyltc.pages.dev`。

### 完整流程概览

推 `main` → `verify` 任务构建 + 自检 → `deploy` 任务(开关打开时)发布到 Cloudflare Pages。

`wrangler.toml` 里的 `name` 要和工作流里的 `--project-name` 保持一致(现在两处都是 `realtyltc`)。

### 路线 B(备选):零 Secret,直接把 dist 提交上去

不想配 token、不想依赖 CI 时用这条。

```bash
# 1. 允许提交构建产物
#    编辑 .gitignore,删掉 "dist/" 这一行

# 2. 本地构建并提交
python build.py
git add dist && git commit -m "build: publish dist"
git push
```

然后 Cloudflare 控制台 → *Workers & Pages* → *Create* → *Pages* → *Connect to Git* → 选仓库,设置:

| 设置项 | 值 |
|---|---|
| Framework preset | `None` |
| Build command | 留空 |
| Build output directory | `dist` |

优点:不用 API Token、不依赖 CI、不存在构建环境差异。
缺点:每次改内容都要本地 `python build.py` 后再提交。

### 绑定域名 realty.lifetourchina.com

站点域名已写进 `sitegen/config.py` 的 `SITE_URL`,它决定 canonical、sitemap 和 og:url —— **换域名必须改这里并重新构建**。

绑定步骤:

1. Cloudflare Pages 项目 → *Custom domains* → *Set up a custom domain* → 填 `realty.lifetourchina.com`
2. 因为 `lifetourchina.com` 这个区(zone)本身就在 Cloudflare 上,Pages 会直接替你写好一条 `realty` 的 CNAME,指向 `realtyltc.pages.dev`——点确认即可,不用去 DNS 面板手动加
3. 等状态从 *Initializing* 变成 *Active*(通常 1–5 分钟,证书签发完成后自动 HTTPS)
4. 项目 → *Settings* → 打开 *Always Use HTTPS*;可选开 HSTS

> 如果 `lifetourchina.com` 的 NS 不在 Cloudflare(比如还在阿里云),那么第 2 步不会自动完成,需要手动在域名服务商处添加:
> `类型 CNAME · 主机记录 realty · 记录值 realtyltc.pages.dev`,然后再回 Pages 点一次校验。

绑定完成后验证一遍:

```bash
curl -I https://realty.lifetourchina.com/
# 期望:HTTP/2 200,并且能看到 content-security-policy 响应头(_headers 生效)
curl -s https://realty.lifetourchina.com/sitemap.xml | head -5
# 期望:<loc>https://realty.lifetourchina.com/...</loc>
```

### 上线后检查清单

- [ ] 五类页面都返回 200:`/`、`/framework/`、`/cities/shanghai/`、`/tools/purchase-cost/`、`/verify/`
- [ ] `/sitemap.xml`、`/robots.txt`、`/404.html` 可访问,且 404 页面真的返回 404
- [ ] 分享到社交平台时卡片图 `og.png` 正常显示
- [ ] 三个计算器能算出结果(纯前端,断网也应可用)
- [ ] 手机宽度下导航能开合、表格能横向滚动
- [ ] `_headers` 生效(响应头里能看到 CSP)

---

## 五、维护节奏

| 内容类型 | 复审间隔 |
|---|---|
| 资格、税费、年限(政策类) | 60 天 |
| 城市档案(价格、租金) | 90 天 |
| 流程与操作类 | 180 天 |

复审时只做三件事:数字是否仍成立、外链是否还有效、有没有新规。
改完把 frontmatter 里的 `updated` 更新,页面上的"最后复核日期"会自动跟着变。

---

## 六、刻意不做的事

| 不做 | 原因 |
|---|---|
| 表单 / 邮件订阅 / 账号 | 没有主体就不该持有用户数据 |
| 后端 / 数据库 | 纯静态 = 没有运行时 = 没有 CVE |
| 广告 / 联盟返佣 / 佣金 | 一旦有利益,内容可信度立刻打折 |
| 具体机构推荐 | 只教怎么筛,不给名单 |
| 房源库 | 打不过平台,也不需要 |
| 价格预测 | 最容易写、最不诚实 |
| 第三方字体 / 统计脚本 | 一个请求都不外发 |

---

## 七、许可

正文内容版权归作者所有。欢迎引用并注明来源,欢迎链接;请勿整站转载,也请勿用于特定交易的"专业意见"包装。
