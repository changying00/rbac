/* =========================================================
   RBAC 权限管理平台 — 公共交互脚本
   侧边栏注入 / 菜单展开 / 模拟操作反馈
   （纯前端演示，无后端请求）
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 菜单数据（对应需求树） ---------- */
  var MENU = [
    {
      id: "dashboard",
      label: "工作台",
      icon: "bi-speedometer2",
      href: "index.html",
      children: []
    },
    {
      id: "user",
      label: "用户管理",
      icon: "bi-people",
      href: "#",
      children: [
        { label: "用户", href: "users.html", page: "users.html" },
        { label: "角色", href: "roles.html", page: "roles.html" },
        { label: "用户角色", href: "user-roles.html", page: "user-roles.html" },
        { label: "部门", href: "departments.html", page: "departments.html" }
      ]
    },
    {
      id: "resource",
      label: "资源管理",
      icon: "bi-diagram-3",
      href: "#",
      children: [
        { label: "系统", href: "systems.html", page: "systems.html" },
        { label: "模块", href: "modules.html", page: "modules.html" },
        { label: "功能", href: "functions.html", page: "functions.html" },
        { label: "按钮", href: "buttons.html", page: "buttons.html" }
      ]
    },
    {
      id: "permission",
      label: "权限管理",
      icon: "bi-shield-check",
      href: "#",
      children: [
        { label: "功能权限", href: "function-perms.html", page: "function-perms.html" },
        { label: "数据权限", href: "data-perms.html", page: "data-perms.html" }
      ]
    },
    {
      id: "menu",
      label: "菜单管理",
      icon: "bi-menu-button-wide",
      href: "#",
      children: [
        { label: "动态菜单", href: "dynamic-menu.html", page: "dynamic-menu.html" }
      ]
    },
    {
      id: "logs",
      label: "日志管理",
      icon: "bi-journal-text",
      href: "#",
      children: [
        { label: "登录日志", href: "login-logs.html", page: "login-logs.html" },
        { label: "操作日志", href: "op-logs.html", page: "op-logs.html" }
      ]
    },
    {
      id: "system",
      label: "系统管理",
      icon: "bi-gear",
      href: "#",
      children: [
        { label: "参数配置", href: "params.html", page: "params.html" },
        { label: "字典", href: "dict.html", page: "dict.html" },
        { label: "系统设置", href: "settings.html", page: "settings.html" }
      ]
    }
  ];

  var PAGE_LABELS = {
    "index.html": "工作台",
    "users.html": "用户",
    "roles.html": "角色",
    "user-roles.html": "用户角色",
    "departments.html": "部门管理",
    "systems.html": "系统",
    "modules.html": "模块",
    "functions.html": "功能",
    "buttons.html": "按钮",
    "function-perms.html": "功能权限",
    "data-perms.html": "数据权限",
    "dynamic-menu.html": "动态菜单",
    "login-logs.html": "登录日志",
    "op-logs.html": "操作日志",
    "params.html": "参数配置",
    "dict.html": "字典",
    "settings.html": "系统设置"
  };

  function currentPage() {
    var path = window.location.pathname.split("/").pop();
    return path || "index.html";
  }

  /* ---------- 渲染侧边栏 ---------- */
  function renderSidebar() {
    var host = document.getElementById("sidebar");
    if (!host) return;

    var page = currentPage();
    var html = [];

    html.push('<div class="sidebar-brand">');
    html.push('  <a href="index.html"><i class="bi bi-shield-lock"></i><span>RBAC 权限平台</span></a>');
    html.push("</div>");

    html.push('<ul class="sidebar-nav">');

    MENU.forEach(function (item) {
      var hasChildren = item.children && item.children.length > 0;
      var isRootActive = item.href === page || (item.href === "index.html" && page === "index.html");
      var childActive = hasChildren && item.children.some(function (c) { return c.page === page; });
      var open = isRootActive || childActive;
      var liClass = [];
      if (isRootActive || (childActive && !hasChildren)) liClass.push("active");
      if (hasChildren && open) liClass.push("open");

      if (!hasChildren) {
        html.push('<li class="' + liClass.join(" ") + '">');
        html.push('  <a href="' + item.href + '"><i class="bi ' + item.icon + '"></i><span>' + item.label + "</span></a>");
        html.push("</li>");
        return;
      }

      html.push('<li class="' + liClass.join(" ") + '" data-group="' + item.id + '">');
      html.push('  <a href="' + item.href + '" class="nav-toggle">');
      html.push('    <i class="bi ' + item.icon + '"></i><span>' + item.label + "</span>");
      html.push('    <i class="bi bi-chevron-down nav-arrow"></i>');
      html.push("  </a>");
      html.push('  <ul class="sub-menu">');
      item.children.forEach(function (child) {
        var childCls = child.page === page ? "active" : "";
        html.push('    <li class="' + childCls + '"><a href="' + child.href + '">' + child.label + "</a></li>");
      });
      html.push("  </ul>");
      html.push("</li>");
    });

    html.push("</ul>");
    html.push('<div class="sidebar-footer"><span>v1.0.0 · 前端演示版</span></div>');
    host.innerHTML = html.join("");
  }

  /* ---------- 渲染顶栏面包屑 ---------- */
  function renderTopbar() {
    var host = document.getElementById("topbar");
    if (!host) return;

    var page = currentPage();
    var label = PAGE_LABELS[page] || "页面";

    // 找到所属一级菜单
    var groupLabel = "";
    MENU.forEach(function (item) {
      if (item.children && item.children.some(function (c) { return c.page === page; })) {
        groupLabel = item.label;
      }
      if (item.href === page && !item.children.length) {
        groupLabel = item.label;
      }
    });

    host.innerHTML = [
      '<button type="button" class="btn-sidebar-toggle" id="sidebarToggle" title="折叠/展开菜单">',
      '  <i class="bi bi-list"></i>',
      "</button>",
      '<nav aria-label="breadcrumb">',
      '  <ol class="breadcrumb mb-0 breadcrumb-wrap">',
      '    <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none">首页</a></li>',
      groupLabel && groupLabel !== label
        ? '    <li class="breadcrumb-item">' + groupLabel + "</li>"
        : "",
      '    <li class="breadcrumb-item active" aria-current="page">' + label + "</li>",
      "  </ol>",
      "</nav>",
      '<div class="topbar-actions">',
      '  <button type="button" class="icon-btn js-demo-action" title="搜索"><i class="bi bi-search"></i></button>',
      '  <button type="button" class="icon-btn js-demo-action" title="通知">',
      '    <i class="bi bi-bell"></i><span class="badge-dot"></span>',
      "  </button>",
      '  <div class="dropdown user-dropdown">',
      '    <button class="dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">',
      '      <span class="avatar">管</span><span>管理员</span><i class="bi bi-chevron-down small"></i>',
      "    </button>",
      '    <ul class="dropdown-menu dropdown-menu-end">',
      '      <li><h6 class="dropdown-header">admin@rbac.demo</h6></li>',
      '      <li><a class="dropdown-item" href="#"><i class="bi bi-person me-2"></i>个人中心</a></li>',
      '      <li><a class="dropdown-item" href="#"><i class="bi bi-sliders me-2"></i>偏好设置</a></li>',
      "      <li><hr class=\"dropdown-divider\"></li>",
      '      <li><a class="dropdown-item text-danger" href="#"><i class="bi bi-box-arrow-right me-2"></i>退出登录</a></li>',
      "    </ul>",
      "  </div>",
      "</div>"
    ].join("");
  }

  /* ---------- 侧边栏交互 ---------- */
  function bindSidebar() {
    var sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    // 一级菜单展开/收起
    sidebar.addEventListener("click", function (e) {
      var toggle = e.target.closest(".nav-toggle");
      if (toggle) {
        e.preventDefault();
        var li = toggle.parentElement;
        // 同级互斥
        var siblings = sidebar.querySelectorAll(".sidebar-nav > li");
        var wasOpen = li.classList.contains("open");
        siblings.forEach(function (s) { s.classList.remove("open"); });
        if (!wasOpen) li.classList.add("open");
        return;
      }
    });

    // 折叠按钮
    var btn = document.getElementById("sidebarToggle");
    if (btn) {
      btn.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 991.98px)").matches) {
          document.body.classList.toggle("sidebar-open");
        } else {
          document.body.classList.toggle("sidebar-collapsed");
        }
      });
    }

    // 点击遮罩关闭移动端侧边栏
    document.addEventListener("click", function (e) {
      if (
        document.body.classList.contains("sidebar-open") &&
        !e.target.closest("#sidebar") &&
        !e.target.closest("#sidebarToggle")
      ) {
        document.body.classList.remove("sidebar-open");
      }
    });
  }

  /* ---------- 模拟操作提示 ---------- */
  function toast(msg) {
    var el = document.createElement("div");
    el.className = "rbac-toast";
    el.innerHTML = '<i class="bi bi-info-circle me-2"></i>' + (msg || "操作成功（演示）");
    document.body.appendChild(el);
    requestAnimationFrame(function () {
      el.classList.add("show");
    });
    setTimeout(function () {
      el.classList.remove("show");
      setTimeout(function () { el.remove(); }, 300);
    }, 2200);
  }

  function bindDemoActions() {
    // 新增 / 编辑 / 删除 / 导出 / 刷新 等按钮：仅提示，不请求后端
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-demo]");
      if (!btn) return;
      var action = btn.getAttribute("data-demo") || "操作";
      toast(action + "：演示环境不处理后端逻辑");
    });

    // 表单提交阻止默认行为
    document.addEventListener("submit", function (e) {
      e.preventDefault();
      toast("表单已提交（演示，未发送请求）");
    });
  }

  /* ---------- 初始化 ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    renderSidebar();
    renderTopbar();
    bindSidebar();
    bindDemoActions();
  });
})();
