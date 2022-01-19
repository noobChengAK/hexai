---

---

# week3 关键内容

***KEYWORDS：***

`making the model`

`profile`

`revolve`

`making the model`

`apparent / surface corlour`表面颜色

`Visual illusion（视觉错觉）`

`active vision approach（主动视觉）`

`The law of sines（三角测距法）`

`difference image`

`similar triangles`

---

## making the model

1. by hand

2. interactive systems
   
   1. e.g. sketchup 软件

3. Algorithmically
   
   1. e.g. 使用类似midpoint- subdivision的方法将一个正多边形逐渐模拟成球型（不断重复的变成更多面体）

4. CAD techniques
   
   <mark>几种方法：</mark>
   
   - profile 之后 revolve（旋转）（画侧面曲线轮廓之后通过旋转生成建模物体）
   
   - extrude（挤压） 和 tapers（锥形物体）拼接
   
   - lofting(楼面)

5. Generative modelling 
   
   - Fractal modelling
   
   - grammerbased modelling 
   
   - partical system

6. Acquiring geometry directly (通过各种方法来直接获得现实中物体的模型)
   
   ---

## The hard bit of extracting the image directly

## 从图像中直接获取信息的难点

   hard bits：

- apparent / surface corlour
  
  - <mark>apparent colour is product of</mark>  `reflectivity` `illuminant` and `传感器的sensitivity`

- Visual illusion（视觉错觉）
  
  ---
  
  ## automated model creation
  
  ## 自动化模型创建
  
  ### laser scanning
  
  #### 2d
  
     原理：<mark>The law of sines（三角测距法）</mark>
  
     公式：
  
     $$
     \frac{A}{\sin a }  = \frac{B}{\sin b } = \frac{C}{\sin c }
     $$
  
     方法：
  
  1. 我们已知相机与`激光发射器之间连线的夹角`和`二者之间的距离`
  
  2. 通过调整已知的相机到激光发射器的距离和三角形180°，得到最后的激光发射器到物体表面的距离
     
     <mark>由此便可由一维光线得到二维数据</mark> --》获得 `profile`
     
     #### 3d
     
     由2d的光线（一条直线）得到3d数据
     
     #### 结构光 structured light scanning
     
     原理：通过制造`difference image` 实现还原轮廓
     
     系统结构（similar triangles相似三角形）：
     
     公式：<mark>已知H，F，Y 求 R</mark>
     
     $$
     \frac{Y}{F} =\frac{H}{(F + R)}  

     $$
  - 相机高度 : H
  
  - 相机焦距 focal length  :  F
  
  - 成像屏像素的 y 坐标： Y
  
  - 相机焦点到物体表面的距离 ：R
    
    ### geometry from images

## automated model creation

## 自动化模型创建

### laser scanning

#### 2d

原理：The law of sines（三角测距法）

公式：

$$
 \frac{A}{\sin a } = \frac{B}{\sin b } = \frac{C}{\sin c }
 $$

方法：

1. 我们已知相机与`激光发射器之间连线的夹角`和`二者之间的距离`

2. 通过调整已知的相机到激光发射器的距离和三角形180°，得到最后的激光发射器到物体表面的距离
   
   由此便可由一维光线得到二维数据 --》获得 `profile`
   
   #### 3d
   
   由2d的光线（一条直线）得到3d数据
   
   #### 结构光 structured light scanning
   
   原理：通过制造`difference image` 实现还原轮廓
   
   系统结构（similar triangles相似三角形）：
   
   公式：已知H，F，Y 求 R
   
   $$
   \frac{Y}{F} =\frac{H}{(F + R)}  

   $$
- 相机高度 : H

- 相机焦距 focal length : F

- 成像屏像素的 y 坐标： Y

- 相机焦点到物体表面的距离 ：R

### geometry from images

## 
