# week7

# 

# 

***KEYWORDS：***

`Raytracing` 

`Radiosity`

`opaque透明的`

`transparent可以透过的`

`flux`

`global illumination`

`entirely object space algorithm 全局算法`

`form factor 波形系数`

`patch 面片`

`occlude 遮挡`

---

## Raytracing

隶属于<mark>直接光照法</mark>

此时我们使用ray tracing 的方式来获得光的显示效果。

倾向于<mark>只在一个表面</mark>上模拟<mark>一次光的反射</mark>

方式：

1. 从光源开始

2. <mark>从相机/viewer 到pannel上的像素之间的连线开始计算光的路径等其他因素</mark>

        其中大部分用<mark>虚线箭头表示光返回光源的线</mark>，<mark>表示相机/物体之间的线用实线</mark>

假如移动观看的视角，需要重新进行计算

---

## Radiosity

隶属于<mark>Global Illumination</mark>`全局光照`

`entirely object space algorithm`

优点：`全局光照：`模拟光在一个场景裡的多次反射，通常会导致<mark>更柔和更自然的影子和反射</mark>

能量不断交换直到达到一个稳定的state

基本的辐射度算法方法其基础在于热辐射的理论，因为辐射度依赖于<mark>两个表面之间光能的传输</mark>。为了简化计算，辐射度算法假设该数值在整个面片上恒定（完全或理想漫反射，或者说面片，然后把它们组合起来得到最后的图像。

在这个分解之后，光能传输的量可以通过使用已知的反射表面的反射率和两个面片的*波形系数*来计算。<mark>`波形系数` form factor </mark>是一个`Dimensionless quantity`，它根据两个面片的几何朝向来计算，可以视为第一个面片所有可能发射区域的被第二个面片所覆盖的部分所占的比例。

更精确的讲，辐射度是每单位时间离开曲面片的能量，是发射和反射能量的组合

移动观看视角/ `patch` 不需要进行重新计算

### 光源light sosurce

在radiosity中，光源是结构中的一部分，是一个`area light source`面光源，而不是点光源`point light source`

### **color bleeding**

指表面会显示出 旁边表面颜色的反射

### flux

定义： flow of particals

the flux leaving surface at point X

### patch

`patch`表示面片

影响的三个因素：

- size of the patches
  
  - patches大小会影响emitting能量多少

- distance between two patches and their orientation with each other

- 有物体/效果 在两个patches 之间 产生了 `occlude 遮挡`光线，会在能量传输的时候产生损失（阴影/减少）

## PROS/CONS

在笔记中还没有看

 
