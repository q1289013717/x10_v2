# X10 平台部署指南 — GitHub + CloudBase + Neon.tech（全部免费，国内可用）

```
┌──────────────────┐     ┌──────────────────────────┐     ┌──────────────────┐
│  GitHub Pages    │────▶│  CloudBase 云托管          │────▶│  Neon.tech       │
│  前端 Vue3       │     │  后端 FastAPI (Docker)     │     │  PostgreSQL      │
│  免费 CDN        │     │  个人版 15万CU/月 免费     │     │  免费 0.5GB      │
└──────────────────┘     └──────────────────────────┘     └──────────────────┘
```

---

## 总览：你需要 3 个东西

| 组件 | 平台 | 费用 | 需要准备 |
|------|------|------|----------|
| 代码仓库 | GitHub | 免费 | GitHub 账号 |
| 数据库 | Neon.tech | 免费 0.5GB | GitHub 账号一键登录（选新加坡节点） |
| 后端服务 | CloudBase 云托管 | 个人版 15万CU/月免费 | 腾讯云账号（微信扫码 + 实名认证） |
| 前端页面 | GitHub Pages | 免费 | 同上 GitHub |

---

## 第 0 步：推代码到 GitHub

```bash
cd F:\workbuddy\x10
git init
git add .
git commit -m "x10 platform ready for deploy"
git branch -M main
git remote add origin https://github.com/你的用户名/x10.git
git push -u origin main
```

---

## 第 1 步：Neon.tech 创建免费数据库（3 分钟）

1. 打开 https://neon.tech → **Sign Up**（用 GitHub 一键登录）
2. 创建 Project：
   - **Region 选 Singapore（新加坡）** ← 国内访问延迟约 240ms，可选的就他了
   - 其他默认，点 Create
3. 创建后你会看到 **Connection string**，类似：
   ```
   postgresql://x10db_owner:npg_xxxxxx@ep-cool-pond-xxx.ap-southeast-1.aws.neon.tech/x10db?sslmode=require
   ```
4. ⚠️ **复制保存这个连接串**，下一步马上要用。

---

## 第 2 步：CloudBase 云托管部署后端（10 分钟）

### 2.1 开通云开发

1. 打开 https://console.cloud.tencent.com/tcb
2. 微信扫码登录 → 需要 **实名认证**（国内云服务都这样）
3. 新建环境：
   - 名称：`x10`
   - 套餐：**个人版**（15万CU/月，够用了）
   - 区域：**上海** 或离你最近的
4. 等 1-2 分钟环境初始化

### 2.2 开通云托管

1. 在云开发控制台左侧菜单 → **云托管**
2. 点 **开通云托管**
3. 选 **个人版**配额
4. 关联 GitHub：点右上角 **设置** → **代码源** → 绑定 GitHub 账号

### 2.3 新建服务并部署

1. 在云托管页面点 **新建服务**
2. 配置如下：

   | 字段 | 值 |
   |------|-----|
   | 服务名称 | `x10-backend` |
   | 部署方式 | **代码仓库** |
   | 代码源 | **GitHub** |
   | 仓库 | 选择 `你的用户名/x10` |
   | 分支 | `main` |
   | Dockerfile 路径 | `x10-backend/Dockerfile` |
   | 构建目录 | `x10-backend` |
   | 端口 | `8000` |

3. **环境变量**：

   ```
   DATABASE_URL  =  postgresql://x10db_owner:npg_xxx@ep-xxx.ap-southeast-1.aws.neon.tech/x10db?sslmode=require
   SECRET_KEY    =  vVFlonIzX-3YahLzOC9MMmT-e_YowAbOaYW-UsksnOY
   CORS_ORIGINS  =  *
   ```
   > CORS_ORIGINS 先填 `*`，拿到前端地址后再改精确值。

4. 资源配置选 **最小规格**（0.25 核 / 0.5GB 内存）→ 省钱
5. 实例数：**最少 0，最多 3**（没请求时自动缩容到 0，不花钱）
6. 点 **创建并部署**，等 3-5 分钟

### 2.4 获取访问地址

部署成功后，在云托管 → 服务列表 → 点进 `x10-backend`：
- 你会看到 **默认域名**，类似：
  ```
  https://x10-backend-xxxxx.ap-shanghai.run.tcloudbase.com
  ```
- ⚠️ **复制保存这个地址**。

验证：浏览器打开 `https://你的域名/docs`，看到 FastAPI 自动文档 = 部署成功。

---

## 第 3 步：GitHub Pages 部署前端（3 分钟）

### 3.1 设置 GitHub Secrets

1. 打开你的 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点 **New repository secret**：
   - Name: `VITE_API_BASE_URL`
   - Value: `https://x10-backend-xxxxx.ap-shanghai.run.tcloudbase.com`（第 2 步拿到的后端地址）
3. 点 **Add secret**

### 3.2 启用 GitHub Pages

1. GitHub 仓库 → **Settings** → **Pages**
2. Source 选 **GitHub Actions**

### 3.3 触发部署

1. GitHub 仓库 → **Actions** 标签
2. 左边选 **Deploy Frontend to GitHub Pages**
3. 点 **Run workflow** → **Run workflow**
4. 等 1-2 分钟，部署完你会看到：
   ```
   https://你的用户名.github.io/x10
   ```

---

## 第 4 步：收紧 CORS

拿到前端地址后，回到 CloudBase 云托管 → x10-backend 服务 → **版本配置** → 编辑环境变量：

```
CORS_ORIGINS  =  https://你的用户名.github.io
```

点 **保存** → 重新部署新版本。

---

## 第 5 步：验证

1. 打开 `https://你的用户名.github.io/x10`
2. 自动跳转到登录页
3. 默认管理员：`admin` / `123123`
4. 测试：登录 → 创建任务 → 写日报 → 查看告警面板

---

## 🎯 以后更新代码

只需 **git push** 到 main 分支：

- **前端**：GitHub Actions 自动构建并部署到 GitHub Pages
- **后端**：CloudBase 云托管检测到 GitHub push 自动构建新镜像并部署

全程自动化，不需要手动操作。

---

## 💰 费用预估

| 资源 | 免费额度 | 预估月费用 |
|------|---------|------------|
| GitHub Pages | 无限 | ¥0 |
| Neon.tech PostgreSQL | 0.5GB 存储 | ¥0 |
| CloudBase 云托管 | 15万 CU/月 | ¥0（小项目完全够用）|

**15万 CU 能跑多久？** 最低配置 0.25 核 × 24小时 × 30天 = 约 64.8万 CU。但云托管会在没请求时**自动缩容到 0**，实际消耗远低于这个数。一个小团队每天用几小时，15万 CU 绰绰有余。

即使超了：超出的 CU 按 **0.000111 元/CU** 计费，15万 CU 也就十几块钱。

---

## 故障排查

| 现象 | 检查 |
|------|------|
| 登录转圈没反应 | F12 → Network → 看 API 请求地址对不对 |
| 后端 502 / 404 | CloudBase 控制台 → 云托管 → 查看日志 |
| 数据库连接失败 | 检查 DATABASE_URL 格式，确保 sslmode=require |
| CORS 报错 | 回到第 4 步，确认 CORS_ORIGINS 写了前端完整域名 |
| 页面空白 | 确认 VITE_API_BASE_URL secret 已设置，重新 push |
| 后端启动慢 | 第一次冷启动约 5-10 秒，正常现象 |
| CloudBase 需要实名？ | 是的，国内云服务都需要，微信扫码 + 身份证即可 |
| Neon 连不上？ | 确认选的**新加坡节点**（不是美国），美国延迟太高 |
