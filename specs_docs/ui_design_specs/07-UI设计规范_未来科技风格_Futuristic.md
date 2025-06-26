# UI设计规范 - 未来科技风格

> 🚀 **使用说明**：本文档为未来科技风格的UI设计规范示例文档。
> 
> 🌌 **目的**：定义高度发达的数字界面美学，呈现几十年后的未来界面体验，融合HUD显示、全息投影和高科技视觉元素，营造信息密集且充满科技感的视觉体验。

## 项目设计定位

### 设计理念
**数字未来 · HUD界面 · 信息密集**

深度模拟高度发达的未来数字界面，通过深色背景、霓虹色彩和动态数据流，创造如《银翼杀手2049》和《攻壳机动队》般的沉浸式科技体验。设计强调信息密度和数据可视化，每个界面元素都充满未来感的功能指示，如同操作来自几十年后的高科技设备。

### 目标用户群体
- **科技工作者**：程序员、数据科学家、系统管理员
- **科幻爱好者**：热爱科幻电影、游戏和文学的用户群体
- **专业分析师**：金融分析师、数据分析师、网络安全专家
- **游戏玩家**：喜爱科幻游戏和高科技界面的玩家
- **创意设计师**：追求前卫视觉体验的设计师和艺术家

### 设计创新点
1. **HUD界面系统**：模拟增强现实和全息显示界面
2. **动态数据流**：实时滚动的代码和数据元素
3. **多层深度视觉**：通过半透明叠加创造空间深度
4. **霓虹荧光效果**：高饱和度的发光色彩系统
5. **信息密集设计**：高密度的数据展示和功能指示

### 适用场景
**🛸 未来科技风格** - 数字时代的极致体验

本设计风格专为需要展现高科技感和未来感的专业应用场景设计，适合技术导向和数据密集的用户群体：

#### 最适合的项目类型
- **数据分析平台**：大数据可视化、商业智能、数据挖掘工具
- **开发者工具**：IDE界面、代码编辑器、API监控平台
- **网络安全系统**：安全监控、威胁检测、系统管理工具
- **金融交易平台**：股票交易、加密货币、量化交易系统
- **科研分析工具**：科学计算、模拟仿真、实验数据分析
- **游戏相关应用**：电竞平台、游戏管理、直播工具
- **IoT控制系统**：智能家居、工业控制、设备监控平台

#### 目标用户群体
- **技术专家**：需要处理复杂数据和系统的专业人士
- **科幻文化爱好者**：对未来科技有强烈兴趣的用户群体
- **专业交易员**：需要多屏监控和快速决策的金融从业者
- **研发工程师**：从事前沿技术开发的工程师和研究员
- **电竞玩家**：追求高科技感游戏体验的用户群体

#### 设计优势
- 强烈的专业感和科技感
- 高效的信息密度和数据展示
- 沉浸式的工作体验
- 独特的品牌差异化

## 色彩系统

### 未来科技色彩语言
**高饱和荧光的数字调色板**

#### 主色调
- **深空黑**：`#000000` (Deep Space Black - 宇宙深处的纯黑)
- **电路蓝**：`#000B1A` (Circuit Blue - 电路板的深蓝背景)
- **矩阵绿**：`#001A0D` (Matrix Green - 黑客帝国的深绿)
- **钢铁灰**：`#0D1117` (Steel Gray - 金属质感的深灰)

#### 霓虹色系
- **霓虹蓝**：`#00D9FF` (Neon Blue - 强烈的电子蓝)
- **电子紫**：`#8B5CF6` (Electric Purple - 高饱和紫色)
- **激光绿**：`#00FF88` (Laser Green - 激光器的绿光)
- **等离子粉**：`#FF0080` (Plasma Pink - 等离子体的粉色)
- **全息黄**：`#FFD700` (Hologram Yellow - 全息投影的金黄)

#### 功能色彩
- **危险红**：`#FF0040` (Danger Red - 警告系统的红色)
- **成功绿**：`#00FF40` (Success Green - 系统正常的绿色)
- **警告橙**：`#FF8000` (Warning Orange - 注意提示的橙色)
- **信息蓝**：`#0080FF` (Info Blue - 信息提示的蓝色)

#### 透明度系统
- **重度透明**：`rgba(0, 217, 255, 0.1)` - 背景层
- **中度透明**：`rgba(0, 217, 255, 0.3)` - 边框层  
- **轻度透明**：`rgba(0, 217, 255, 0.7)` - 内容层
- **高亮透明**：`rgba(0, 217, 255, 0.9)` - 强调层

### 色彩使用原则
1. **发光效果**：所有亮色都应有发光(glow)效果
2. **层次透明**：使用多层透明度创造深度
3. **功能编码**：不同颜色代表不同的系统状态
4. **动态变化**：颜色应根据数据状态动态变化

## 排版系统

### 未来界面字体
**等宽科技字体系统**

#### 字体族系
```css
.futuristic-typography {
    font-family: 'Space Mono', 'Fira Code', 'Source Code Pro', 'Courier New', monospace;
    font-weight: 400;
    line-height: 1.4;
    letter-spacing: 0.05em;
}

.display-tech {
    font-size: 48px;
    font-weight: 700;
    text-transform: uppercase;
    color: #00D9FF;
    text-shadow: 0 0 20px rgba(0, 217, 255, 0.8);
    letter-spacing: 0.1em;
    margin-bottom: 24px;
}

.header-hud {
    font-size: 24px;
    font-weight: 600;
    color: #00FF88;
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 16px;
}

.body-matrix {
    font-size: 14px;
    font-weight: 400;
    color: #00D9FF;
    line-height: 1.6;
    letter-spacing: 0.02em;
}

.code-display {
    font-size: 12px;
    font-weight: 400;
    color: #00FF88;
    background: rgba(0, 255, 136, 0.1);
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid rgba(0, 255, 136, 0.3);
    letter-spacing: 0.05em;
}

.data-label {
    font-size: 10px;
    font-weight: 600;
    color: #8B5CF6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.8;
}
```

#### HUD界面排版
```css
.hud-element {
    position: relative;
    padding: 16px;
    border: 1px solid rgba(0, 217, 255, 0.3);
    background: rgba(0, 11, 26, 0.8);
    backdrop-filter: blur(10px);
}

.hud-corner {
    position: absolute;
    width: 12px;
    height: 12px;
    border: 2px solid #00D9FF;
}

.hud-corner.top-left {
    top: -1px;
    left: -1px;
    border-right: none;
    border-bottom: none;
}

.hud-corner.top-right {
    top: -1px;
    right: -1px;
    border-left: none;
    border-bottom: none;
}

.hud-corner.bottom-left {
    bottom: -1px;
    left: -1px;
    border-right: none;
    border-top: none;
}

.hud-corner.bottom-right {
    bottom: -1px;
    right: -1px;
    border-left: none;
    border-top: none;
}
```

## 组件设计规范

### 高科技界面组件
**未来感的交互元素**

#### 按钮组件
```css
.btn-futuristic {
    background: linear-gradient(45deg, rgba(0, 217, 255, 0.2), rgba(139, 92, 246, 0.2));
    border: 1px solid #00D9FF;
    color: #00D9FF;
    padding: 12px 24px;
    font-family: 'Space Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
}

.btn-futuristic::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.4), transparent);
    transition: left 0.5s ease;
}

.btn-futuristic:hover {
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
    text-shadow: 0 0 10px rgba(0, 217, 255, 0.8);
}

.btn-futuristic:hover::before {
    left: 100%;
}

.btn-danger-tech {
    border-color: #FF0040;
    color: #FF0040;
    background: linear-gradient(45deg, rgba(255, 0, 64, 0.2), rgba(139, 92, 246, 0.2));
}

.btn-danger-tech:hover {
    box-shadow: 0 0 20px rgba(255, 0, 64, 0.5);
    text-shadow: 0 0 10px rgba(255, 0, 64, 0.8);
}
```

#### 数据面板组件
```css
.data-panel {
    background: rgba(0, 11, 26, 0.9);
    border: 1px solid rgba(0, 217, 255, 0.3);
    border-radius: 8px;
    padding: 20px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(15px);
}

.data-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00D9FF, #8B5CF6, #00FF88);
    animation: scanLine 3s linear infinite;
}

@keyframes scanLine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 16px;
}

.data-item {
    background: rgba(0, 217, 255, 0.05);
    border: 1px solid rgba(0, 217, 255, 0.2);
    padding: 12px;
    border-radius: 4px;
}

.data-value {
    font-size: 24px;
    font-weight: 700;
    color: #00D9FF;
    text-shadow: 0 0 10px rgba(0, 217, 255, 0.6);
}

.data-unit {
    font-size: 12px;
    color: #8B5CF6;
    margin-left: 4px;
}
```

#### 输入组件
```css
.input-tech {
    width: 100%;
    background: rgba(0, 11, 26, 0.8);
    border: 1px solid rgba(0, 217, 255, 0.3);
    border-radius: 4px;
    padding: 12px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 14px;
    color: #00D9FF;
    outline: none;
    transition: all 0.3s ease;
}

.input-tech:focus {
    border-color: #00D9FF;
    box-shadow: 0 0 15px rgba(0, 217, 255, 0.3);
    background: rgba(0, 11, 26, 0.9);
}

.input-tech::placeholder {
    color: rgba(0, 217, 255, 0.5);
    font-style: italic;
}

.input-group {
    position: relative;
    margin-bottom: 20px;
}

.input-label {
    position: absolute;
    top: -8px;
    left: 12px;
    background: #000B1A;
    color: #8B5CF6;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0 8px;
}
```

## HUD界面系统

### 全息显示元素
**增强现实式的界面框架**

#### HUD框架
```css
.hud-frame {
    position: relative;
    border: 2px solid rgba(0, 217, 255, 0.6);
    background: rgba(0, 11, 26, 0.7);
    backdrop-filter: blur(10px);
    padding: 24px;
    margin: 20px 0;
}

.hud-frame::before,
.hud-frame::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    border: 3px solid #00D9FF;
}

.hud-frame::before {
    top: -3px;
    left: -3px;
    border-right: none;
    border-bottom: none;
}

.hud-frame::after {
    bottom: -3px;
    right: -3px;
    border-left: none;
    border-top: none;
}

.hud-title {
    position: absolute;
    top: -12px;
    left: 24px;
    background: #000B1A;
    color: #00D9FF;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0 12px;
}

.hud-status {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    background: #00FF88;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
```

#### 数据流动效果
```css
.data-stream {
    position: relative;
    height: 200px;
    overflow: hidden;
    background: rgba(0, 11, 26, 0.8);
    border: 1px solid rgba(0, 217, 255, 0.3);
}

.stream-line {
    position: absolute;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, transparent, #00D9FF, transparent);
    animation: streamFlow 2s linear infinite;
}

.stream-line:nth-child(1) { left: 10%; animation-delay: 0s; }
.stream-line:nth-child(2) { left: 30%; animation-delay: 0.5s; }
.stream-line:nth-child(3) { left: 50%; animation-delay: 1s; }
.stream-line:nth-child(4) { left: 70%; animation-delay: 1.5s; }
.stream-line:nth-child(5) { left: 90%; animation-delay: 0.3s; }

@keyframes streamFlow {
    0% { transform: translateY(-100%); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(100%); opacity: 0; }
}

.code-matrix {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #00FF88;
    line-height: 1.2;
    opacity: 0.6;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
    pointer-events: none;
}

.matrix-char {
    animation: matrixRain 3s linear infinite;
    display: inline-block;
}

@keyframes matrixRain {
    0% { transform: translateY(-100vh); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(100vh); opacity: 0; }
}
```

## 数据可视化系统

### 未来感图表
**高科技数据展示**

#### 圆形进度指示器
```css
.circular-progress {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 20px auto;
}

.progress-ring {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: conic-gradient(
        from 0deg,
        #00D9FF 0deg,
        #8B5CF6 120deg,
        rgba(0, 217, 255, 0.2) 360deg
    );
    position: relative;
    animation: rotate 4s linear infinite;
}

.progress-ring::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 8px;
    right: 8px;
    bottom: 8px;
    background: #000B1A;
    border-radius: 50%;
}

.progress-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
    font-weight: 700;
    color: #00D9FF;
    text-shadow: 0 0 10px rgba(0, 217, 255, 0.8);
    z-index: 1;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

#### 科技感图表
```css
.tech-chart {
    background: rgba(0, 11, 26, 0.9);
    border: 1px solid rgba(0, 217, 255, 0.3);
    border-radius: 8px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}

.chart-grid {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        linear-gradient(rgba(0, 217, 255, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 217, 255, 0.1) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
}

.chart-bar {
    background: linear-gradient(180deg, #00D9FF, #8B5CF6);
    margin: 4px 0;
    height: 24px;
    border-radius: 2px;
    position: relative;
    overflow: hidden;
    animation: chartGlow 3s ease-in-out infinite alternate;
}

@keyframes chartGlow {
    0% { box-shadow: 0 0 5px rgba(0, 217, 255, 0.3); }
    100% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.8); }
}

.chart-bar::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: chartScan 2s linear infinite;
}

@keyframes chartScan {
    0% { left: -100%; }
    100% { left: 100%; }
}
```

## 布局模式

### 信息密集布局
**多层次的数据展示**

#### 主控制台布局
```css
.control-console {
    min-height: 100vh;
    background: #000000;
    display: grid;
    grid-template-areas: 
        "header header header"
        "sidebar main-display info-panel"
        "footer footer footer";
    grid-template-rows: 60px 1fr 40px;
    grid-template-columns: 280px 1fr 320px;
    gap: 1px;
    border: 2px solid rgba(0, 217, 255, 0.3);
}

.console-header {
    grid-area: header;
    background: rgba(0, 11, 26, 0.9);
    border-bottom: 1px solid rgba(0, 217, 255, 0.3);
    display: flex;
    align-items: center;
    padding: 0 20px;
    position: relative;
}

.console-sidebar {
    grid-area: sidebar;
    background: rgba(0, 11, 26, 0.8);
    border-right: 1px solid rgba(0, 217, 255, 0.3);
    padding: 20px;
    overflow-y: auto;
}

.main-display {
    grid-area: main-display;
    background: rgba(0, 11, 26, 0.6);
    padding: 20px;
    position: relative;
    overflow: hidden;
}

.info-panel {
    grid-area: info-panel;
    background: rgba(0, 11, 26, 0.8);
    border-left: 1px solid rgba(0, 217, 255, 0.3);
    padding: 20px;
    overflow-y: auto;
}

.console-footer {
    grid-area: footer;
    background: rgba(0, 11, 26, 0.9);
    border-top: 1px solid rgba(0, 217, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
}
```

#### 多窗口系统
```css
.window-system {
    position: relative;
    height: 600px;
    background: #000000;
    overflow: hidden;
}

.tech-window {
    position: absolute;
    background: rgba(0, 11, 26, 0.9);
    border: 1px solid rgba(0, 217, 255, 0.5);
    border-radius: 8px;
    min-width: 300px;
    min-height: 200px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
}

.window-header {
    background: rgba(0, 217, 255, 0.1);
    border-bottom: 1px solid rgba(0, 217, 255, 0.3);
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: move;
}

.window-title {
    font-size: 12px;
    font-weight: 600;
    color: #00D9FF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.window-controls {
    display: flex;
    gap: 8px;
}

.window-control {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    cursor: pointer;
}

.control-close { background: #FF0040; }
.control-minimize { background: #FFD700; }
.control-maximize { background: #00FF88; }

.window-content {
    padding: 16px;
    height: calc(100% - 40px);
    overflow: auto;
}
```

## 动效规范

### 高科技动效
**未来感的交互反馈**

```css
.tech-transition {
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.hologram-effect {
    position: relative;
    animation: hologramFlicker 0.1s infinite linear;
}

@keyframes hologramFlicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.98; }
}

.scan-effect {
    position: relative;
    overflow: hidden;
}

.scan-effect::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(0, 217, 255, 0.3) 50%, 
        transparent 100%);
    animation: scanEffect 3s linear infinite;
}

@keyframes scanEffect {
    0% { left: -100%; }
    100% { left: 100%; }
}

.glitch-effect {
    position: relative;
    animation: glitch 0.3s infinite;
}

@keyframes glitch {
    0%, 90%, 100% { transform: translate(0); }
    10% { transform: translate(-2px, -1px); }
    20% { transform: translate(2px, 1px); }
    30% { transform: translate(-1px, 2px); }
    40% { transform: translate(1px, -1px); }
    50% { transform: translate(-2px, 1px); }
    60% { transform: translate(2px, -2px); }
    70% { transform: translate(-1px, -1px); }
    80% { transform: translate(1px, 2px); }
}

.data-load {
    animation: dataLoad 2s linear infinite;
}

@keyframes dataLoad {
    0% { 
        background-position: -200px 0;
        opacity: 0.5;
    }
    50% {
        opacity: 1;
    }
    100% { 
        background-position: calc(200px + 100%) 0;
        opacity: 0.5;
    }
}

.power-on {
    animation: powerOn 1s ease-out;
}

@keyframes powerOn {
    0% {
        opacity: 0;
        transform: scale(0.8);
        filter: brightness(0);
    }
    50% {
        opacity: 0.8;
        filter: brightness(1.5);
    }
    100% {
        opacity: 1;
        transform: scale(1);
        filter: brightness(1);
    }
}
```

## 响应式设计

### 未来界面适配
**多设备的科技体验**

```css
/* 移动端适配 */
@media (max-width: 767px) {
    .control-console {
        grid-template-areas: 
            "header"
            "main-display"
            "sidebar"
            "info-panel"
            "footer";
        grid-template-rows: 60px 1fr auto auto 40px;
        grid-template-columns: 1fr;
    }
    
    .display-tech {
        font-size: 32px;
    }
    
    .data-panel {
        padding: 16px;
        margin: 12px 0;
    }
    
    .tech-window {
        position: static;
        width: 100%;
        margin-bottom: 16px;
    }
}

/* 平板端适配 */
@media (min-width: 768px) and (max-width: 1024px) {
    .control-console {
        grid-template-columns: 240px 1fr 280px;
    }
    
    .data-grid {
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }
}

/* 超宽屏优化 */
@media (min-width: 1600px) {
    .control-console {
        grid-template-columns: 320px 1fr 400px;
    }
    
    .display-tech {
        font-size: 64px;
    }
    
    .main-display {
        padding: 32px;
    }
}
```

## 可访问性规范

### 高对比度科技界面
**包容性的未来体验**

```css
.accessible-tech {
    /* 确保足够的对比度 */
    color: #00D9FF;
    background: #000000;
}

.focus-tech:focus {
    outline: 2px solid #00FF88;
    outline-offset: 2px;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    .hologram-effect,
    .scan-effect,
    .glitch-effect,
    .data-load {
        animation: none;
    }
    
    .tech-transition {
        transition: none;
    }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
    .data-panel {
        border-color: #FFFFFF;
        background: #000000;
    }
    
    .btn-futuristic {
        border-color: #FFFFFF;
        color: #FFFFFF;
    }
}

.sr-tech {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

## 设计原则总结

### 未来科技核心原则
1. **信息密度优先**：最大化数据展示和功能可见性
2. **HUD界面思维**：模拟增强现实和全息显示
3. **动态视觉反馈**：所有交互都应有科技感的动效
4. **发光美学**：使用霓虹色彩和发光效果
5. **多层深度**：通过透明度和模糊创造空间层次

### 设计禁忌
- ❌ 温暖色调和有机形状
- ❌ 传统的扁平化设计
- ❌ 过于简洁的信息展示
- ❌ 慢速或静态的界面
- ❌ 低对比度的色彩搭配

### 设计检查清单
- ✅ 是否使用了深色背景和霓虹色彩？
- ✅ 界面是否充满科技感和未来感？
- ✅ 是否有足够的动态元素和数据流？
- ✅ HUD框架是否清晰可见？
- ✅ 信息密度是否足够高？
- ✅ 发光效果是否恰当？

---

> **科幻美学引用**：
> 
> *"The future is not some place we are going to, but one we are creating. The paths are not to be found, but made."*
> 
> — 未来主义设计哲学
> 
> *"In the digital realm, information is power, and interface is the gateway to that power."*
> 
> — 《银翼杀手2049》设计理念