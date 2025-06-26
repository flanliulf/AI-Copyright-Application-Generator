# UI设计规范 - 优雅复古风格

> 📜 **使用说明**：本文档为优雅复古风格的UI设计规范示例文档。
> 
> 🎭 **目的**：定义基于20世纪初期印刷品美学的设计理念，重现古典印刷工艺的精致细节，营造温暖怀旧且充满文化底蕴的视觉体验。

## 项目设计定位

### 设计理念
**古典雅致 · 印刷美学 · 温暖怀旧**

深度还原20世纪初期的优雅印刷美学，通过仿古纸张质感、经典衬线字体和传统印刷色调，创造如同翻阅古老书籍般的温馨体验。设计强调文化传承与工艺精神，每个细节都体现出对传统印刷艺术的敬意，如同百年老牌出版社的经典作品和维多利亚时代的精装书籍。

### 目标用户群体
- **文化爱好者**：对古典文化和历史有浓厚兴趣的学者
- **文学读者**：喜爱阅读经典文学作品的知识分子
- **艺术收藏家**：欣赏传统工艺美术的收藏爱好者
- **学术研究者**：从事人文学科研究的专业人士
- **优雅生活追求者**：注重生活品味和文化修养的用户群体

### 设计创新点
1. **仿古纸张质感**：模拟羊皮纸和古籍纸张的温润质感
2. **传统印刷配色**：深棕、暗红、墨绿等经典印刷色调
3. **古典装饰元素**：花边、徽章、装饰线条等传统图案
4. **多层次质感系统**：纸张纹理、墨迹效果、烫金细节
5. **复古印刷字体**：Baskerville、Garamond等经典衬线字体

### 适用场景
**📚 优雅复古风格** - 传统文化的数字传承

本设计风格专为重视文化传承和古典美学的应用场景设计，适合具有深厚文化底蕴的用户群体：

#### 最适合的项目类型
- **文化教育平台**：古典文学阅读、历史文化学习、艺术鉴赏应用
- **学术研究工具**：人文学科研究平台、古籍数字化、学术论文管理
- **图书馆系统**：数字图书馆、古籍检索、文献管理系统
- **博物馆应用**：文物展示平台、历史文化介绍、虚拟展览
- **高端出版平台**：精装书籍展示、文学作品发布、期刊管理
- **文化艺术机构**：画廊管理、艺术品收藏、文化活动平台
- **精品电商平台**：古董收藏、艺术品交易、奢侈品展示

#### 目标用户群体
- **文化学者**：从事人文社会科学研究的专业人士
- **文学爱好者**：喜爱古典文学和诗歌的读者群体
- **艺术鉴赏家**：对传统艺术有深度理解的收藏家
- **教育工作者**：文史哲专业的教师和学者
- **文化机构从业者**：博物馆、图书馆、出版社工作人员

#### 设计优势
- 浓厚的文化底蕴和历史传承感
- 独特的高雅品味和精致质感
- 温暖舒适的阅读和浏览体验
- 强烈的专业性和权威性

## 色彩系统

### 古典印刷色彩
**温润怀旧的传统色调**

#### 主色调
- **羊皮纸色**：`#F5F1E8` (Parchment - 古老羊皮纸的温润色)
- **米色**：`#F0E6D2` (Cream - 陈年书页的淡黄色)
- **象牙白**：`#FFF8DC` (Ivory - 象牙般的温润白色)
- **旧纸色**：`#E8DCC6` (Aged Paper - 泛黄书页的怀旧色)

#### 经典印刷色
- **深棕色**：`#4A3C28` (Deep Brown - 古典印刷的深棕墨色)
- **暗红色**：`#8B3A3A` (Dark Red - 传统印刷的暗红色)
- **墨绿色**：`#2F4F2F` (Forest Green - 古典装帧的墨绿色)
- **深蓝色**：`#2F4F4F` (Dark Slate - 古典印刷的深蓝色)

#### 装饰色彩
- **烫金色**：`#B8860B` (Antique Gold - 古典烫金的典雅金色)
- **古铜色**：`#CD7F32` (Bronze - 古铜色装饰元素)
- **银灰色**：`#C0C0C0` (Silver - 银色装饰细节)
- **紫色**：`#663399` (Royal Purple - 皇家紫色强调色)

#### 功能色彩
- **成功色**：`#556B2F` (Olive Green - 橄榄绿成功提示)
- **警告色**：`#B8860B` (Antique Gold - 古金色警告)
- **错误色**：`#A0522D` (Sienna - 赭石色错误提示)
- **信息色**：`#4682B4` (Steel Blue - 钢蓝色信息提示)

### 色彩使用原则
1. **温暖基调**：以米色、羊皮纸色为主要背景色
2. **低饱和度**：使用柔和的低饱和度色彩，避免刺眼
3. **层次丰富**：通过深浅变化创造丰富的视觉层次
4. **文化内涵**：每种颜色都体现传统文化的典雅气质

## 排版系统

### 经典衬线字体
**传统印刷的优雅字体**

#### 字体层级
```css
.elegant-typography {
    font-family: 'Baskerville', 'Garamond', 'Georgia', 'Times New Roman', serif;
    font-weight: 400;
    line-height: 1.8; /* 古典书籍的宽松行距 */
    letter-spacing: 0.02em;
    color: #4A3C28;
}

.title-elegant {
    font-size: 36px;
    font-weight: 600;
    line-height: 1.4;
    color: #4A3C28;
    margin-bottom: 32px;
    letter-spacing: 0.05em;
    text-align: center;
}

.subtitle-elegant {
    font-size: 24px;
    font-weight: 500;
    line-height: 1.6;
    color: #8B3A3A;
    margin-bottom: 24px;
    letter-spacing: 0.03em;
}

.body-elegant {
    font-size: 16px;
    font-weight: 400;
    line-height: 1.8;
    color: #4A3C28;
    max-width: 700px;
    text-align: justify; /* 两端对齐，如古典书籍 */
}

.caption-elegant {
    font-size: 14px;
    font-weight: 300;
    color: #8B3A3A;
    line-height: 1.6;
    font-style: italic;
}

.quote-elegant {
    font-size: 18px;
    font-weight: 400;
    line-height: 1.8;
    color: #2F4F2F;
    font-style: italic;
    padding: 24px 32px;
    border-left: 4px solid #B8860B;
    background: rgba(184, 134, 11, 0.05);
}
```

#### 装饰性字体
```css
.decorative-initial {
    float: left;
    font-size: 64px;
    line-height: 50px;
    padding-right: 8px;
    padding-top: 4px;
    color: #B8860B;
    font-family: 'Garamond', serif;
    font-weight: 700;
}

.chapter-number {
    font-size: 48px;
    font-weight: 300;
    color: #8B3A3A;
    text-align: center;
    margin-bottom: 16px;
    font-family: 'Baskerville', serif;
}

.ornamental-text {
    font-size: 20px;
    text-align: center;
    color: #B8860B;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
```

### 传统排版规范
**古典书籍的版式美学**

#### 页面留白
```css
.page-margins {
    --margin-top: 80px;
    --margin-bottom: 80px;
    --margin-inner: 120px; /* 内侧较宽，便于装订 */
    --margin-outer: 80px;
}

.content-area {
    max-width: 800px;
    margin: 0 auto;
    padding: var(--margin-top) var(--margin-outer) var(--margin-bottom);
}

.text-block {
    margin-bottom: 32px;
    text-indent: 2em; /* 段落首行缩进 */
}
```

## 组件设计规范

### 古典装饰组件
**传统工艺美术元素**

#### 按钮组件
```css
.btn-elegant-primary {
    background: linear-gradient(135deg, #B8860B 0%, #CD7F32 100%);
    color: #F5F1E8;
    border: 2px solid #B8860B;
    border-radius: 8px;
    padding: 14px 28px;
    font-family: 'Baskerville', serif;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(184, 134, 11, 0.3);
    position: relative;
    overflow: hidden;
}

.btn-elegant-primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
}

.btn-elegant-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(184, 134, 11, 0.4);
}

.btn-elegant-primary:hover::before {
    left: 100%;
}

.btn-elegant-secondary {
    background: transparent;
    color: #8B3A3A;
    border: 2px solid #8B3A3A;
    border-radius: 8px;
    padding: 12px 26px;
    font-family: 'Baskerville', serif;
    font-size: 16px;
    font-weight: 400;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-elegant-secondary:hover {
    background: #8B3A3A;
    color: #F5F1E8;
    box-shadow: 0 4px 12px rgba(139, 58, 58, 0.3);
}
```

#### 卡片组件
```css
.card-elegant {
    background: #F5F1E8;
    border: 1px solid #E8DCC6;
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 32px;
    box-shadow: 0 8px 24px rgba(74, 60, 40, 0.12);
    position: relative;
    overflow: hidden;
}

.card-elegant::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #B8860B, #CD7F32, #B8860B);
}

.card-elegant-deluxe {
    background: linear-gradient(135deg, #F5F1E8 0%, #F0E6D2 100%);
    border: 2px solid #B8860B;
    box-shadow: 
        0 8px 24px rgba(74, 60, 40, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.card-header-elegant {
    border-bottom: 2px solid #E8DCC6;
    padding-bottom: 16px;
    margin-bottom: 24px;
    text-align: center;
    position: relative;
}

.card-header-elegant::after {
    content: '❦';
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: #F5F1E8;
    color: #B8860B;
    font-size: 20px;
    padding: 0 8px;
}

.card-title-elegant {
    font-size: 22px;
    font-weight: 600;
    color: #4A3C28;
    margin: 0;
    font-family: 'Baskerville', serif;
}
```

#### 表单组件
```css
.form-elegant {
    max-width: 500px;
    margin: 0 auto;
    background: #F5F1E8;
    padding: 40px;
    border-radius: 16px;
    border: 2px solid #E8DCC6;
    box-shadow: 0 12px 32px rgba(74, 60, 40, 0.15);
}

.input-elegant {
    width: 100%;
    background: #FFF8DC;
    border: 2px solid #E8DCC6;
    border-radius: 8px;
    padding: 14px 18px;
    font-family: 'Baskerville', serif;
    font-size: 16px;
    color: #4A3C28;
    outline: none;
    transition: all 0.3s ease;
}

.input-elegant:focus {
    border-color: #B8860B;
    background: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(184, 134, 11, 0.1);
}

.input-elegant::placeholder {
    color: #8B7355;
    font-style: italic;
}

.label-elegant {
    display: block;
    font-size: 14px;
    font-weight: 500;
    color: #4A3C28;
    margin-bottom: 8px;
    font-family: 'Baskerville', serif;
    letter-spacing: 0.02em;
}

.select-elegant {
    width: 100%;
    background: #FFF8DC;
    border: 2px solid #E8DCC6;
    border-radius: 8px;
    padding: 14px 18px;
    font-family: 'Baskerville', serif;
    font-size: 16px;
    color: #4A3C28;
    cursor: pointer;
    outline: none;
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%234A3C28' viewBox='0 0 16 16'%3e%3cpath d='M8 13.1l4.7-4.7-1.4-1.4L8 10.3 4.7 7l-1.4 1.4z'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 16px center;
    background-size: 16px;
}

.checkbox-elegant {
    width: 20px;
    height: 20px;
    border: 2px solid #8B3A3A;
    border-radius: 4px;
    background: #FFF8DC;
    cursor: pointer;
    position: relative;
    transition: all 0.3s ease;
}

.checkbox-elegant:checked {
    background: #8B3A3A;
    border-color: #8B3A3A;
}

.checkbox-elegant:checked::after {
    content: '✓';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #F5F1E8;
    font-size: 14px;
    font-weight: bold;
}
```

## 装饰元素系统

### 古典装饰图案
**传统工艺美术元素**

#### 花边装饰
```css
.ornamental-border {
    border: 2px solid #B8860B;
    border-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 20'%3e%3cpath d='M0 10 Q 25 0 50 10 T 100 10' stroke='%23B8860B' stroke-width='2' fill='none'/%3e%3c/svg%3e") 2;
    padding: 24px;
    margin: 32px 0;
}

.corner-ornament {
    position: absolute;
    width: 40px;
    height: 40px;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3e%3cpath d='M20 5 Q 35 5 35 20 Q 35 35 20 35 Q 5 35 5 20 Q 5 5 20 5' stroke='%23B8860B' stroke-width='1' fill='none'/%3e%3c/svg%3e");
    opacity: 0.6;
}

.corner-ornament.top-left { top: 0; left: 0; }
.corner-ornament.top-right { top: 0; right: 0; transform: scaleX(-1); }
.corner-ornament.bottom-left { bottom: 0; left: 0; transform: scaleY(-1); }
.corner-ornament.bottom-right { bottom: 0; right: 0; transform: scale(-1); }

.fleuron {
    text-align: center;
    font-size: 24px;
    color: #B8860B;
    margin: 32px 0;
}

.fleuron::before {
    content: '❦ ❦ ❦';
    letter-spacing: 16px;
}
```

#### 徽章和标记
```css
.vintage-badge {
    display: inline-block;
    background: linear-gradient(135deg, #B8860B 0%, #CD7F32 100%);
    color: #F5F1E8;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border: 2px solid #B8860B;
    box-shadow: 0 4px 12px rgba(184, 134, 11, 0.3);
    position: relative;
}

.vintage-badge::before {
    content: '';
    position: absolute;
    top: -4px;
    left: -4px;
    right: -4px;
    bottom: -4px;
    border: 1px solid #B8860B;
    border-radius: 24px;
    opacity: 0.5;
}

.ribbon {
    position: relative;
    background: #8B3A3A;
    color: #F5F1E8;
    padding: 12px 24px;
    margin: 16px 0;
    font-family: 'Baskerville', serif;
    font-weight: 500;
    text-align: center;
}

.ribbon::before,
.ribbon::after {
    content: '';
    position: absolute;
    top: 0;
    width: 0;
    height: 0;
    border-style: solid;
}

.ribbon::before {
    left: -20px;
    border-width: 22px 20px 22px 0;
    border-color: transparent #8B3A3A transparent transparent;
}

.ribbon::after {
    right: -20px;
    border-width: 22px 0 22px 20px;
    border-color: transparent transparent transparent #8B3A3A;
}
```

#### 分隔装饰
```css
.elegant-divider {
    text-align: center;
    margin: 48px 0;
    position: relative;
    height: 2px;
    background: linear-gradient(to right, transparent, #B8860B, transparent);
}

.elegant-divider::before {
    content: '◆';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #F5F1E8;
    color: #B8860B;
    font-size: 16px;
    padding: 0 16px;
}

.ornamental-divider {
    text-align: center;
    margin: 40px 0;
    color: #B8860B;
    font-size: 20px;
}

.ornamental-divider::before {
    content: '❦ ◆ ❦';
    letter-spacing: 8px;
}

.chapter-break {
    text-align: center;
    margin: 64px 0;
    padding: 24px 0;
    border-top: 2px solid #E8DCC6;
    border-bottom: 2px solid #E8DCC6;
    color: #8B3A3A;
    font-family: 'Baskerville', serif;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
```

## 布局模式

### 古典版式布局
**传统书籍的页面设计**

#### 主页面布局
```css
.page-elegant {
    min-height: 100vh;
    background: linear-gradient(135deg, #F5F1E8 0%, #F0E6D2 100%);
    display: grid;
    grid-template-columns: 1fr minmax(320px, 900px) 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas: 
        ". header ."
        ". main ."
        ". footer .";
    gap: 0;
    position: relative;
}

.page-elegant::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        radial-gradient(circle at 25% 25%, rgba(184, 134, 11, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 75% 75%, rgba(139, 58, 58, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
}

.header-elegant {
    grid-area: header;
    padding: 32px 0;
    border-bottom: 2px solid #E8DCC6;
    text-align: center;
    position: relative;
}

.main-elegant {
    grid-area: main;
    padding: 64px 32px;
    display: flex;
    flex-direction: column;
    gap: 48px;
}

.footer-elegant {
    grid-area: footer;
    padding: 32px 0;
    border-top: 2px solid #E8DCC6;
    text-align: center;
    background: rgba(240, 230, 210, 0.5);
}
```

#### 书籍式布局
```css
.book-layout {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 48px;
    max-width: 1000px;
    margin: 0 auto;
    padding: 48px 32px;
}

.table-of-contents {
    background: #F0E6D2;
    border: 2px solid #E8DCC6;
    border-radius: 12px;
    padding: 24px;
    height: fit-content;
    position: sticky;
    top: 32px;
}

.content-main {
    background: #F5F1E8;
    border: 2px solid #E8DCC6;
    border-radius: 16px;
    padding: 48px;
    box-shadow: 
        0 12px 32px rgba(74, 60, 40, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.chapter-layout {
    margin-bottom: 64px;
    padding-bottom: 48px;
    border-bottom: 1px solid #E8DCC6;
}

.chapter-layout:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.two-column-text {
    columns: 2;
    column-gap: 48px;
    column-rule: 1px solid #E8DCC6;
    text-align: justify;
    line-height: 1.8;
}
```

#### 网格系统
```css
.elegant-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
    margin: 48px 0;
}

.grid-item-elegant {
    background: #F5F1E8;
    border: 2px solid #E8DCC6;
    border-radius: 12px;
    padding: 32px;
    position: relative;
    transition: all 0.3s ease;
}

.grid-item-elegant:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(74, 60, 40, 0.15);
    border-color: #B8860B;
}

.grid-item-elegant::before {
    content: '';
    position: absolute;
    top: 16px;
    right: 16px;
    width: 24px;
    height: 24px;
    background: radial-gradient(circle, #B8860B 30%, transparent 30%);
    opacity: 0.3;
}
```

## 导航系统

### 古典导航设计
**优雅的导航美学**

```css
.nav-elegant {
    display: flex;
    align-items: center;
    gap: 40px;
    padding: 0 32px;
    font-family: 'Baskerville', serif;
}

.nav-item-elegant {
    color: #4A3C28;
    text-decoration: none;
    font-size: 16px;
    font-weight: 500;
    padding: 12px 16px;
    position: relative;
    transition: color 0.3s ease;
    letter-spacing: 0.02em;
}

.nav-item-elegant::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #B8860B, #CD7F32);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

.nav-item-elegant:hover {
    color: #8B3A3A;
}

.nav-item-elegant:hover::after {
    width: 100%;
}

.nav-item-elegant.active {
    color: #8B3A3A;
}

.nav-item-elegant.active::after {
    width: 100%;
}

.logo-elegant {
    font-size: 28px;
    font-weight: 700;
    color: #B8860B;
    text-decoration: none;
    margin-right: auto;
    font-family: 'Baskerville', serif;
    letter-spacing: 0.05em;
    position: relative;
}

.logo-elegant::after {
    content: '◆';
    margin-left: 8px;
    font-size: 16px;
    color: #8B3A3A;
}

.breadcrumb-elegant {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 32px;
    font-size: 14px;
    color: #8B7355;
    font-family: 'Baskerville', serif;
}

.breadcrumb-item-elegant {
    text-decoration: none;
    color: inherit;
    transition: color 0.3s ease;
}

.breadcrumb-item-elegant:hover {
    color: #B8860B;
}

.breadcrumb-separator {
    color: #B8860B;
    font-weight: 500;
}
```

### 移动端导航
```css
.mobile-nav-elegant {
    position: fixed;
    top: 0;
    left: -280px;
    width: 280px;
    height: 100vh;
    background: linear-gradient(135deg, #F5F1E8 0%, #F0E6D2 100%);
    border-right: 2px solid #E8DCC6;
    transition: left 0.3s ease;
    z-index: 1000;
    padding: 32px 24px;
    box-shadow: 4px 0 20px rgba(74, 60, 40, 0.15);
}

.mobile-nav-elegant.active {
    left: 0;
}

.mobile-nav-toggle {
    display: none;
    flex-direction: column;
    gap: 4px;
    cursor: pointer;
    padding: 8px;
}

.mobile-nav-line {
    width: 24px;
    height: 2px;
    background: #4A3C28;
    border-radius: 1px;
    transition: all 0.3s ease;
}

@media (max-width: 768px) {
    .nav-elegant {
        display: none;
    }
    
    .mobile-nav-toggle {
        display: flex;
    }
}
```

## 动效规范

### 优雅过渡动效
**古典美学的动态表现**

```css
.elegant-transition {
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.gentle-hover {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.gentle-hover:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(74, 60, 40, 0.15);
}

.fade-in-elegant {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInElegant 0.8s ease-out forwards;
}

@keyframes fadeInElegant {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.page-turn {
    animation: pageTurn 0.6s ease-in-out;
}

@keyframes pageTurn {
    0% { transform: rotateY(0deg); }
    50% { transform: rotateY(-90deg); }
    100% { transform: rotateY(0deg); }
}

.vintage-glow {
    position: relative;
    overflow: hidden;
}

.vintage-glow::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(184, 134, 11, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.5s ease;
}

.vintage-glow:hover::before {
    opacity: 1;
}
```

## 响应式设计

### 古典美学的适配
**保持优雅的响应式原则**

```css
/* 移动端优化 */
@media (max-width: 767px) {
    .page-elegant {
        grid-template-columns: 1fr;
        padding: 0 16px;
    }
    
    .title-elegant {
        font-size: 28px;
        margin-bottom: 24px;
    }
    
    .subtitle-elegant {
        font-size: 20px;
        margin-bottom: 16px;
    }
    
    .card-elegant {
        padding: 24px;
        margin-bottom: 24px;
        border-radius: 8px;
    }
    
    .book-layout {
        grid-template-columns: 1fr;
        gap: 32px;
    }
    
    .two-column-text {
        columns: 1;
        column-gap: 0;
        column-rule: none;
    }
    
    .content-main {
        padding: 32px 24px;
    }
}

/* 平板端适配 */
@media (min-width: 768px) and (max-width: 1024px) {
    .page-elegant {
        grid-template-columns: 1fr minmax(320px, 700px) 1fr;
    }
    
    .elegant-grid {
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 24px;
    }
    
    .book-layout {
        grid-template-columns: 180px 1fr;
        gap: 32px;
    }
}

/* 大屏优化 */
@media (min-width: 1200px) {
    .page-elegant {
        grid-template-columns: 1fr minmax(320px, 1100px) 1fr;
    }
    
    .title-elegant {
        font-size: 42px;
    }
    
    .content-main {
        padding: 64px;
    }
    
    .main-elegant {
        gap: 64px;
    }
}
```

## 可访问性规范

### 包容性古典设计
**优雅的无障碍体验**

```css
.accessible-elegant {
    /* 确保充足的颜色对比度 */
    color: #4A3C28;
    background: #F5F1E8;
}

.focus-elegant:focus {
    outline: 3px solid #B8860B;
    outline-offset: 2px;
    border-radius: 4px;
}

.skip-to-main-elegant {
    position: absolute;
    top: -40px;
    left: 24px;
    background: #4A3C28;
    color: #F5F1E8;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 4px;
    transition: top 0.3s;
    font-family: 'Baskerville', serif;
    font-weight: 500;
}

.skip-to-main-elegant:focus {
    top: 24px;
}

.sr-only-elegant {
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

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
    .card-elegant {
        border: 3px solid #4A3C28;
    }
    
    .btn-elegant-primary {
        border: 3px solid #4A3C28;
    }
}

/* 减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## 设计原则总结

### 优雅复古核心原则
1. **文化传承**：体现20世纪初期印刷工艺的精致美学
2. **温暖怀旧**：使用温润的米色调营造舒适的阅读氛围
3. **工艺精神**：注重细节装饰和传统工艺元素
4. **典雅品味**：展现深厚的文化底蕴和高雅品位
5. **阅读友好**：优化文字排版，提供舒适的阅读体验

### 设计禁忌
- ❌ 刺眼的高饱和度色彩
- ❌ 现代科技风的冷色调
- ❌ 过于简洁的极简设计
- ❌ 快速或激烈的动画效果
- ❌ 无衬线字体作为主要字体

### 设计检查清单
- ✅ 是否使用了温润的古典色调？
- ✅ 字体是否采用优雅的衬线字体？
- ✅ 是否包含传统装饰元素？
- ✅ 排版是否体现古典书籍美学？
- ✅ 整体是否传达文化底蕴？
- ✅ 用户体验是否优雅舒适？

---

> **古典美学引用**：
> 
> *"Beauty is truth, truth beauty, —that is all ye know on earth, and all ye need to know."*
> 
> — John Keats，英国浪漫主义诗人
> 
> *"The beautiful is always bizarre."*
> 
> — Charles Baudelaire，法国诗人

> **设计哲学**：
> 
> *优雅不是被注意到，而是被记住*
> 
> *真正的奢华在于细节的完美*