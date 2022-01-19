# week6

***KEYWORDS：***

`Rendering equation`

`BRDF`

`BTDF`

`BSSCDF`

`BSDF`

`refract（折射）`

`reflect（反射）`

`wavelength`

`radiance`

`irradiance`

`radiation flux 辐射流/能量`

`scattered (分散的)`

---

## rendering equation

<mark>关键</mark>：该方程现实中不能成立/运行，因为会涉及到无限的光线以及反射折射，以及光的角度

所以运行不了，只能进行限制和简化公式来达成效果

$$
L_{o}(x, \vec{w})=L_{e}(x, \vec{w})+\int_{\Omega} f_{r}\left(x, \vec{w}^{\prime}, \vec{w}\right) L_{i}\left(x, \vec{w}^{\prime}\right)\left(\vec{w}^{\prime} \cdot \vec{n}\right) d \vec{w}^{\prime}
$$

$$
Lo(x,ω,λ,t) =Le(x,ω,λ,t) +∫Ωfr(x,ω′,ω,λ,t)Li(x,ω′,λ,t)(−ω′·n)δω′

$$

- <mark>λ</mark> is a specific wavelength of light

- <mark>t</mark> is time

- <mark>Lo(x,ω,λ,t)</mark> is the total amount of light of wavelengthλdirected outward along direc-tionωat timetfrom a particular position x

- <mark>fr(x,ω′,ω,λ,t)</mark> is thebidirectional reflectance distribution function (BRDF)

  ---

## BRDF functions

$$
fr(ωi,ωo) =δLr(ωo)/δEi(ωi)=δLr(ωo)/Ei(ωi) cosθiδωi
$$

FRom BRDF we can calculate output `radiation flux` /` energy` of the insert lights with λ

OUTPUT : E as `irradiance`

INPUT : L as `radiance`

for all diffuse light

### BTDF

BTDF is on the <mark>opposite side</mark> of the surface if there is<mark>` refract(折射)</mark>` happend 

e.g. 玻璃等

### BSSDF

e.g. 光透过手，手轮廓周围的朦胧感的光（没完全折射出去的光）

---

## BSDF

<mark>BSDF = BRDF + BTDF + BSSDF</mark>

S for scattered (分散的)

---

## 
