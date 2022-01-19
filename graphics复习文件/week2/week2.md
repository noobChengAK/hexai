---

---

# week 2 关键点总结

***KEYWORDS：***

`Fractal Modelling`

`recursive subdivision`

`L-System`

`Textual SCRIPT`

---

## polygons

<mark>Not everything is a polygon</mark>

举例：

1. 水

2. 火焰/烟

3. 树木

4. 头发，山等

---

## Generative modelling

### Fractals

#### 定义

self-similar (same kind of shape with different scales)

#### 其他内容

the objects have the similar shape called "Fractal shape" 

e.g.: broccoli(花菜🥦)

##### 如何测量fractal curves/曲线(求解长度)

方法：**使用recursive subdivision**

取中点，将线二分，重复步骤

The solution will **depends on the ruler we use** (how short is the length that we match the curve)

步骤：

1. get the mid point, display it randomly

2. replace the first line with two new lines

3. repeat recursively until meet the required level

##### 解决3d 地形建模（terrain generation）

定义：**将一个平面切割成四个，不断循环♻️**直到模拟出地形

---

### Grammer-based moddelling

#### 简易FLR方式

| F   | 前进1    |
|:---:| ------ |
| L   | 左转一定角度 |
| R   | 右转一定角度 |

注意在<mark>L和F时，不进行移动</mark>

F --> FLFRRFLF

通过将F替换为其他如FLFRRFLF来实现Fractal（举例：雪花❄️）

#### L-System

 特点：添加了 [push 和 pop] 功能

> 举例：F ---》 F [RF] F [LF] F

此时添加了 '[]' 之后，此时括号内的操作为脱离主要部分的分支操作

用途： 可用于模拟部分 树🌲，植物的生长过程

---

### Particle systems

particle system

<mark>变量</mark>

section1

- site

- shape

- colour

- opacity

section2

- position

- velocity

- acceleration

section3

- age

- time

- lifetime

#### <mark> 粒子系统设计方式</mark>

1. 移除超过寿命的

2. 创造新的粒子并初始化

3. 更新每个粒子的状态（位置 + 颜色/加速度）

4. 渲染当前的粒子

#### 粒子系统管理

引擎通过`Textual SCRIPT`来进行驱动

SCRIPT中包含了：

- laws

- initial values

- limits等

#### 计算方式

1. <mark>Euler Integration</mark>
   
       use iterative method
   
           v = v + at 
   
           x = x + vt

2. <mark>Verlet Integration</mark> (更加精确因为直接计算了位置)

        x = 2x - x + at^2

#### 渲染方式

渲染方式：

1. 像素/一组像素

2. 使用线连接 新和旧的particle之间的像素

3.  gaussian kernals
   
   这个方法可以<mark>避免/减少aliasing</mark>

4. - small alpha-textured
   
   - billboards 朝向viewer的screen-aligned quads

    

## 
