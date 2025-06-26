# UI设计规范 - 包豪斯风格

> 📐 **使用说明**：本文档为包豪斯风格的UI设计规范示例文档。
> 
> 🎯 **目的**：定义基于20世纪早期德国包豪斯学校功能主义美学的设计理念、风格和规范，体现"形式服从功能"的设计哲学，营造理性、前卫且具有工业美感的视觉效果。

## 项目设计定位

### 设计理念
**功能至上 · 几何纯粹 · 理性秩序**

严格遵循包豪斯学校的功能主义美学原则，运用基本几何形状作为核心设计元素，限制色彩为基本原色系统，强调清晰理性的排版布局。通过严格的网格系统和无装饰的设计语言，打造如同1920年代包豪斯教材般的纯粹视觉体验，体现工业时代的理性美学。

### 目标用户群体
- **艺术设计师**：追求纯粹美学体验的设计专业人士
- **建筑师**：欣赏功能主义设计理念的建筑从业者
- **工业设计师**：重视形式与功能关系的产品设计师
- **学术研究者**：对设计史和设计理论有深度理解的学者
- **极简主义者**：追求简洁高效体验的用户群体

### 设计创新点
1. **纯粹几何系统**：严格使用方形、圆形、三角形基本形状
2. **原色限制调色板**：仅使用红、黄、蓝三原色配以黑白灰
3. **无衬线字体体系**：采用Futura或Helvetica等经典包豪斯字体
4. **严格网格布局**：强调水平垂直线条的模块化设计
5. **功能驱动设计**：每个元素都有明确的功能目的

### 适用场景
**🏛️ 包豪斯风格** - 功能主义美学的纯粹体现

本设计风格专为追求纯粹功能美学和理性设计的应用场景设计，适合对设计有深度理解的专业用户群体：

#### 最适合的项目类型
- **设计工具平台**：专业设计软件、创意工具、设计协作平台
- **建筑设计系统**：建筑设计软件、空间规划工具、工程管理系统
- **艺术展览平台**：美术馆管理系统、艺术作品展示平台
- **学术研究工具**：设计理论研究平台、学术资源管理系统
- **工业设计应用**：产品设计工具、制造流程管理系统
- **极简办公软件**：专注效率的办公工具、项目管理系统
- **品牌设计平台**：企业VI设计工具、品牌资产管理系统

#### 目标用户群体
- **专业设计师**：对设计美学有专业要求的创意工作者
- **艺术从业者**：美术馆策展人、艺术教育工作者
- **建筑师**：建筑设计师、城市规划师、室内设计师
- **学术研究者**：设计史学者、美学理论研究者
- **极简主义拥护者**：追求纯粹功能体验的用户群体

#### 设计优势
- 强烈的历史文化底蕴和美学价值
- 极致的功能性和实用性
- 永不过时的经典设计语言
- 强化专业性和权威性的品牌形象

## 色彩系统

### 基本原色系统
**严格遵循包豪斯三原色理念**

#### 主色调
- **包豪斯红**：`#E31E24` (Pure Red - 纯红色)
- **包豪斯黄**：`#FFD100` (Pure Yellow - 纯黄色)  
- **包豪斯蓝**：`#0055A4` (Pure Blue - 纯蓝色)

#### 中性色系
- **纯黑**：`#000000` (Pure Black)
- **纯白**：`#FFFFFF` (Pure White)
- **中性灰**：`#808080` (50% Gray)
- **浅灰**：`#D3D3D3` (Light Gray)
- **深灰**：`#404040` (Dark Gray)

### 色彩使用原则
1. **禁止渐变**：不使用任何过渡色或渐变效果
2. **高对比度**：确保色彩之间形成清晰对比
3. **功能性着色**：色彩必须服务于功能识别
4. **面积控制**：原色作为强调色，大面积使用黑白灰

## 几何形状系统

### 基本形状元素
**严格限制为三种基本几何形状**

#### 方形系统
```css
.square-element {
    width: 48px;
    height: 48px;
    background: #E31E24;
    border: none;
    border-radius: 0;
}

.rectangle-element {
    width: 120px;
    height: 48px;
    background: #0055A4;
    border: none;
    border-radius: 0;
}
```

#### 圆形系统
```css
.circle-element {
    width: 48px;
    height: 48px;
    background: #FFD100;
    border-radius: 50%;
    border: none;
}

.circle-button {
    width: 64px;
    height: 64px;
    background: #000000;
    border-radius: 50%;
    border: 2px solid #FFFFFF;
}
```

#### 三角形系统
```css
.triangle-element {
    width: 0;
    height: 0;
    border-left: 24px solid transparent;
    border-right: 24px solid transparent;
    border-bottom: 42px solid #E31E24;
}

.triangle-indicator {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 14px solid #000000;
}
```

## 排版系统

### 字体规范
**严格使用无衬线字体**

#### 主字体层级
```css
.bauhaus-font-system {
    font-family: 'Futura', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
    font-weight: normal;
    letter-spacing: 0.05em;
}

.title-primary {
    font-size: 48px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    line-height: 1.2;
}

.title-secondary {
    font-size: 32px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    line-height: 1.3;
}

.body-text {
    font-size: 16px;
    font-weight: normal;
    line-height: 1.5;
    letter-spacing: 0.02em;
}

.caption-text {
    font-size: 12px;
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    line-height: 1.4;
}
```

### 网格系统
**严格的模块化布局**

#### 基础网格
```css
.bauhaus-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-gap: 24px;
    max-width: 1200px;
    margin: 0 auto;
}

.grid-module {
    grid-column: span 3;
    aspect-ratio: 1:1;
    background: #FFFFFF;
    border: 2px solid #000000;
}

.grid-module-wide {
    grid-column: span 6;
    aspect-ratio: 2:1;
    background: #D3D3D3;
    border: 1px solid #000000;
}
```

#### 排版对齐
- **左对齐**：所有文本默认左对齐
- **垂直韵律**：严格遵循24px基础行高倍数
- **水平间距**：使用24px的倍数进行布局间距

## 组件设计规范

### 按钮组件
**几何形状驱动的功能性按钮**

```css
.btn-bauhaus-primary {
    width: 120px;
    height: 48px;
    background: #E31E24;
    color: #FFFFFF;
    border: none;
    border-radius: 0;
    font-family: 'Futura', sans-serif;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.btn-bauhaus-primary:hover {
    background: #000000;
}

.btn-bauhaus-secondary {
    width: 120px;
    height: 48px;
    background: #FFFFFF;
    color: #000000;
    border: 2px solid #000000;
    border-radius: 0;
    font-family: 'Futura', sans-serif;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.btn-circle {
    width: 56px;
    height: 56px;
    background: #FFD100;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
```

### 卡片组件
**严格几何边界的内容容器**

```css
.card-bauhaus {
    background: #FFFFFF;
    border: 3px solid #000000;
    border-radius: 0;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: none;
}

.card-bauhaus-accent {
    background: #FFD100;
    border: 3px solid #000000;
    border-radius: 0;
    padding: 24px;
    margin-bottom: 24px;
}

.card-header {
    border-bottom: 2px solid #000000;
    padding-bottom: 12px;
    margin-bottom: 24px;
}

.card-header h3 {
    font-size: 24px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0;
}
```

### 表单组件
**功能性优先的输入控件**

```css
.form-bauhaus {
    display: grid;
    grid-gap: 24px;
}

.input-bauhaus {
    width: 100%;
    height: 48px;
    background: #FFFFFF;
    border: 2px solid #000000;
    border-radius: 0;
    padding: 0 16px;
    font-family: 'Helvetica', sans-serif;
    font-size: 16px;
    outline: none;
}

.input-bauhaus:focus {
    border-color: #E31E24;
    background: #FFFFFF;
}

.label-bauhaus {
    font-family: 'Futura', sans-serif;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #000000;
    margin-bottom: 8px;
    display: block;
}

.checkbox-bauhaus {
    width: 20px;
    height: 20px;
    border: 2px solid #000000;
    border-radius: 0;
    background: #FFFFFF;
}

.checkbox-bauhaus:checked {
    background: #E31E24;
}
```

## 布局模式

### 模块化网格布局
**基于包豪斯设计原理的页面结构**

#### 主页面布局
```css
.page-bauhaus {
    display: grid;
    grid-template-areas: 
        "header header header"
        "sidebar main main"
        "footer footer footer";
    grid-template-rows: 80px 1fr 60px;
    grid-template-columns: 240px 1fr 1fr;
    min-height: 100vh;
    gap: 0;
}

.header-bauhaus {
    grid-area: header;
    background: #000000;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    padding: 0 24px;
    border-bottom: 4px solid #E31E24;
}

.sidebar-bauhaus {
    grid-area: sidebar;
    background: #D3D3D3;
    border-right: 2px solid #000000;
    padding: 24px;
}

.main-bauhaus {
    grid-area: main;
    background: #FFFFFF;
    padding: 24px;
}

.footer-bauhaus {
    grid-area: footer;
    background: #808080;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    padding: 0 24px;
}
```

#### 内容网格系统
```css
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
    padding: 24px 0;
}

.grid-item {
    background: #FFFFFF;
    border: 2px solid #000000;
    aspect-ratio: 1:1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.grid-item::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 8px;
    width: 16px;
    height: 16px;
    background: #E31E24;
}
```

## 导航系统

### 主导航
**几何形状指示的功能导航**

```css
.nav-bauhaus {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.nav-item {
    display: flex;
    align-items: center;
    height: 48px;
    padding: 0 16px;
    background: #D3D3D3;
    border-bottom: 1px solid #000000;
    color: #000000;
    text-decoration: none;
    font-family: 'Futura', sans-serif;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: background-color 0.2s ease;
}

.nav-item:hover {
    background: #FFD100;
}

.nav-item.active {
    background: #E31E24;
    color: #FFFFFF;
}

.nav-item::before {
    content: '';
    width: 8px;
    height: 8px;
    background: currentColor;
    margin-right: 12px;
}

.nav-item.primary::before {
    border-radius: 0; /* 方形 */
}

.nav-item.secondary::before {
    border-radius: 50%; /* 圆形 */
}

.nav-item.tertiary::before {
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 8px solid currentColor;
    background: transparent;
}
```

### 面包屑导航
```css
.breadcrumb-bauhaus {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid #000000;
    margin-bottom: 24px;
}

.breadcrumb-item {
    font-family: 'Helvetica', sans-serif;
    font-size: 14px;
    color: #000000;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}

.breadcrumb-separator {
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 10px solid #000000;
}
```

## 数据可视化规范

### 图表色彩系统
**功能性颜色编码**

```css
.chart-bauhaus {
    --chart-red: #E31E24;
    --chart-yellow: #FFD100;
    --chart-blue: #0055A4;
    --chart-black: #000000;
    --chart-gray: #808080;
}

.bar-chart-item {
    fill: var(--chart-red);
    stroke: var(--chart-black);
    stroke-width: 2;
}

.line-chart {
    stroke: var(--chart-blue);
    stroke-width: 3;
    fill: none;
}

.pie-chart-segment:nth-child(1) {
    fill: var(--chart-red);
}

.pie-chart-segment:nth-child(2) {
    fill: var(--chart-yellow);
}

.pie-chart-segment:nth-child(3) {
    fill: var(--chart-blue);
}
```

### 图标系统
**纯几何形状图标**

```css
.icon-bauhaus {
    display: inline-block;
    width: 24px;
    height: 24px;
    position: relative;
}

.icon-square {
    background: #000000;
    width: 100%;
    height: 100%;
}

.icon-circle {
    background: #000000;
    width: 100%;
    height: 100%;
    border-radius: 50%;
}

.icon-triangle {
    width: 0;
    height: 0;
    border-left: 12px solid transparent;
    border-right: 12px solid transparent;
    border-bottom: 24px solid #000000;
}

.icon-plus {
    position: relative;
    background: transparent;
}

.icon-plus::before,
.icon-plus::after {
    content: '';
    position: absolute;
    background: #000000;
}

.icon-plus::before {
    width: 20px;
    height: 4px;
    top: 10px;
    left: 2px;
}

.icon-plus::after {
    width: 4px;
    height: 20px;
    top: 2px;
    left: 10px;
}
```

## 动效规范

### 基础过渡
**理性克制的功能性动效**

```css
.transition-bauhaus {
    transition: all 0.2s linear;
}

.hover-effect {
    transition: background-color 0.2s linear;
}

.click-effect {
    transition: transform 0.1s linear;
}

.click-effect:active {
    transform: scale(0.95);
}

/* 禁止复杂动画 */
.no-complex-animation {
    animation: none;
    transform: none;
    filter: none;
}
```

### 状态变化
```css
.state-active {
    background: #E31E24;
    color: #FFFFFF;
    border-color: #E31E24;
}

.state-disabled {
    background: #D3D3D3;
    color: #808080;
    border-color: #808080;
    cursor: not-allowed;
}

.state-loading::after {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid #808080;
    border-top: 2px solid #000000;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

## 响应式设计原则

### 断点设置
**基于模块化网格的响应式适配**

```css
/* 移动端 */
@media (max-width: 767px) {
    .bauhaus-grid {
        grid-template-columns: 1fr;
        grid-gap: 16px;
        padding: 16px;
    }
    
    .page-bauhaus {
        grid-template-areas: 
            "header"
            "main"
            "sidebar"
            "footer";
        grid-template-rows: 60px 1fr auto 50px;
        grid-template-columns: 1fr;
    }
    
    .title-primary {
        font-size: 32px;
    }
}

/* 平板端 */
@media (min-width: 768px) and (max-width: 1024px) {
    .bauhaus-grid {
        grid-template-columns: repeat(8, 1fr);
        grid-gap: 20px;
    }
    
    .grid-module {
        grid-column: span 2;
    }
    
    .grid-module-wide {
        grid-column: span 4;
    }
}

/* 桌面端 */
@media (min-width: 1025px) {
    .bauhaus-grid {
        grid-template-columns: repeat(12, 1fr);
        grid-gap: 24px;
    }
}
```

## 可访问性规范

### 对比度要求
**高对比度设计原则**

```css
.high-contrast {
    color: #000000;
    background: #FFFFFF;
    border: 2px solid #000000;
}

.contrast-warning {
    color: #FFFFFF;
    background: #E31E24;
    border: 2px solid #000000;
}

.contrast-info {
    color: #FFFFFF;
    background: #0055A4;
    border: 2px solid #000000;
}
```

### 键盘导航
```css
.focusable:focus {
    outline: 3px solid #E31E24;
    outline-offset: 2px;
}

.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000000;
    color: #FFFFFF;
    padding: 8px;
    text-decoration: none;
    transition: top 0.2s;
}

.skip-link:focus {
    top: 6px;
}
```

## 设计原则总结

### 核心原则
1. **形式服从功能**：每个设计元素都必须有明确的功能目的
2. **几何纯粹性**：严格使用基本几何形状，避免装饰性元素
3. **色彩克制**：限制使用三原色系统，大面积使用中性色
4. **排版理性**：采用严格的网格系统和清晰的字体层级
5. **工业美感**：体现机械时代的精确性和功能性

### 禁止事项
- ❌ 装饰性图案和纹理
- ❌ 复杂的渐变和阴影效果
- ❌ 衬线字体和花体字
- ❌ 不规则形状和曲线装饰
- ❌ 过度的动画效果

### 设计检查清单
- ✅ 是否使用了基本几何形状？
- ✅ 色彩是否限制在原色系统内？
- ✅ 字体是否为无衬线字体？
- ✅ 布局是否遵循严格网格？
- ✅ 每个元素是否有明确功能？
- ✅ 整体是否体现工业美感？

---

> **设计哲学引用**：
> 
> *"The ultimate goal of the architect...is to create a paradise. Every house, every product of architecture... should be a fruit of our endeavor to build an earthly paradise for people."*
> 
> — Walter Gropius, 包豪斯学校创始人
> 
> *"Form follows function – that has been misunderstood. Form and function should be one, joined in a spiritual union."*
> 
> — Frank Lloyd Wright (深受包豪斯影响的建筑师)