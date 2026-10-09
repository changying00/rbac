# RBAC 权限管理平台（前端演示）

基于 **Bootstrap 5** 构建的 RBAC 权限管理平台前台界面。  
**仅绘制页面效果，不包含任何后端处理**（所有按钮/表单仅弹出演示提示，不发起请求）。

## 功能结构

```
RBAC 权限管理平台
│
├── ① 用户管理
│     ├── 用户        users.html
│     ├── 角色        roles.html
│     ├── 用户角色    user-roles.html
│     └── 部门        departments.html
│
├── ② 资源管理
│     ├── 系统        systems.html
│     ├── 模块        modules.html
│     ├── 功能        functions.html
│     └── 按钮        buttons.html
│
├── ③ 权限管理
│     ├── 功能权限    function-perms.html
│     └── 数据权限    data-perms.html
│
├── ④ 菜单管理
│     └── 动态菜单    dynamic-menu.html
│
├── ⑤ 日志管理
│     ├── 登录日志    login-logs.html
│     └── 操作日志    op-logs.html
│
└── ⑥ 系统管理
      ├── 参数配置    params.html
      ├── 字典        dict.html
      └── 系统设置    settings.html

工作台（总览）  index.html
```

## 快速预览

1. 直接用浏览器打开 `index.html`（无需服务器、无需安装依赖）。
2. 左侧菜单可切换各模块；顶栏面包屑、用户下拉可交互。
3. 列表页支持：搜索条件区、表格、分页、新增/编辑弹窗、操作按钮提示。

> 建议使用 Chrome / Edge 等现代浏览器。

## 技术说明

| 项 | 说明 |
|---|---|
| UI 框架 | Bootstrap 5.3（CDN） |
| 图标 | Bootstrap Icons（CDN） |
| 图表 | Chart.js（仅工作台，CDN） |
| 交互 | 原生 JavaScript（`assets/js/app.js`） |
| 样式 | 自定义 `assets/css/style.css`（深色侧边栏 + 浅色内容区） |

### 目录结构

```
RBAC/
├── index.html              # 工作台
├── users.html              # 用户
├── roles.html              # 角色
├── user-roles.html         # 用户角色
├── departments.html        # 部门管理
├── systems.html            # 系统
├── modules.html            # 模块
├── functions.html          # 功能
├── buttons.html            # 按钮
├── function-perms.html     # 功能权限
├── data-perms.html         # 数据权限
├── dynamic-menu.html       # 动态菜单
├── login-logs.html         # 登录日志
├── op-logs.html            # 操作日志
├── params.html             # 参数配置
├── dict.html               # 字典
├── settings.html           # 系统设置
├── assets/
│   ├── css/style.css       # 全局样式
│   └── js/app.js           # 侧边栏/顶栏注入与交互
└── README.md
```

## 设计要点

- **侧边栏**：按需求树组织 6 大模块，支持展开/收起、折叠、当前页高亮；移动端可抽屉式打开。
- **列表页统一范式**：页头操作区 → 搜索筛选卡片 → 数据表格（状态徽章 / 行操作）→ 分页。
- **弹窗表单**：新增/编辑使用 Bootstrap Modal，字段贴近真实 RBAC 建模（角色编码、权限标识、数据范围等）。
- **权限演示**：功能权限树勾选、数据权限范围说明、按钮级权限列表，体现 RBAC 核心概念。
- **演示隔离**：全局监听 `data-demo` 与表单 submit，仅 toast 提示“演示环境不处理后端逻辑”。

## 页面清单速查

| 模块 | 页面 | 核心 UI |
|---|---|---|
| 工作台 | index | 统计卡片、Chart.js 趋势图、最近动态、快捷入口 |
| 用户 | users | 用户表、部门/状态筛选、新增用户弹窗 |
| 角色 | roles | 角色表、角色详情、权限树配置弹窗 |
| 用户角色 | user-roles | 用户-角色对照、分配角色弹窗、RBAC 说明 |
| 部门管理 | departments | 组织架构树、部门详情、下级部门列表、新增/编辑弹窗 |
| 系统 | systems | 系统资源卡片 + 列表 |
| 模块 | modules | 所属系统筛选、路由路径展示 |
| 功能 | functions | 权限标识、请求方式、类型徽章 |
| 按钮 | buttons | 按钮级权限标识、类型标签 |
| 功能权限 | function-perms | 角色选择 + 资源权限树 + 授权概况 |
| 数据权限 | data-perms | 数据范围配置表、范围说明手风琴、配置弹窗 |
| 动态菜单 | dynamic-menu | 菜单树、角色预览渲染结果 |
| 登录日志 | login-logs | 认证结果、IP/设备、失败原因 |
| 操作日志 | op-logs | 操作类型徽章、请求地址、耗时、高危统计 |
| 参数配置 | params | 键值参数表、分组筛选、内置标记 |
| 字典 | dict | 字典类型 + 字典项双栏、标签样式 |
| 系统设置 | settings | 基础信息 / 安全 / 会话 / 界面偏好开关表单 |

## 说明

- 本项目为**纯静态 HTML/CSS/JS** 演示工程，数据均为界面示意用的假数据。
- 若需接入真实后端，可在各列表页增加 fetch/axios 调用，并将 `data-demo` 提示替换为真实业务逻辑。
