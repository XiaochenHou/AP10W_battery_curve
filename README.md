<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://www.iflytek.com/index.html">
    <img src="images/logo.png" alt="Logo">
  </a>

  <h3 align="center">电池曲线提取工具</h3>

  <p align="center">
    以电量变化和时间变化为基准提取相关数据
  </p>
</div>


## 关于项目
此项目用于对抓取到的AP10W电量log进行数据的处理以及提取，目的是为后期制图和分析作准备。
抓log命令为：
   ```sh
   while true;do date;sleep 1s;dumpsys battery;sleep 1s;done
   ```

<p align="right">(<a href="#top">回到顶部</a>)</p>



### 第三方依赖以及工具使用

* [pandas](https://pandas.pydata.org/)
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* [pycharm](https://www.jetbrains.com/pycharm/)

<p align="right">(<a href="#top">回到顶部</a>)</p>

## 安装

1. 安装各个依赖的第三方库(更新可能不及时请自行检查安装依赖)
    ```sh
   pip3 install pandas openpyxl scikit-learn numpy matplotlib
   ```
2. 克隆这个仓库到本地
   ```sh
   git clone https://github.com/XiaochenHou/AP10W_battery_curve.git
   ```
3. 进入文件夹
   ```sh
   cd AP10W_battery_curve
   ```
<p align="right">(<a href="#top">回到顶部</a>)</p>


## 使用指南
**2022.2.15更新：v4.0版本更新，加入自动生成曲线图**
<br >
1. 可以通过--wg来取消生成曲线图without graph
   ```sh
   battery2 --wg
   ```

---
**2022.2.9更新：现已将文件打包成.exe格式文件，可以在windows下直接运行**
<br >
1. 使用说明：
   ```sh
   battery2 -h
   ```
2. 运行命令：
   ```sh
   battery2 [文件或文件夹路径]
   ```

---

1. 利用-h来查看帮助
   ```sh
   python3 battery2.py -h
   ```
2. 基础用法，中括号替换为log的路径，**必须为.log和.txt结尾的文件或包含文件的目录**
   ```sh
   python3 battery2.py [log的路径]
   ```
3. 拓展用法
   ```sh
   python3 battery2.py [log的路径] -d [xlsx目标路径] -i [获取log的周期默认为2] --wg [withoutgraph不生成图片])
   ```  
<p align="right">(<a href="#top">回到顶部</a>)</p>

## 许可证

根据 MIT 许可证分发。 有关更多信息，请参阅`LICENSE.txt`。

<p align="right">(<a href="#top">回到顶部</a>)</p>

## 联系方式

侯啸辰 - xchou2@iflytek.com - 13661045480(微信同号)

项目链接: [GitHub](https://github.com/XiaochenHou/AP10W_battery_curve) |
[Gitee](https://gitee.com/xiaochenhou/AP10W_battery_curve)

<p align="right">(<a href="#top">回到顶部</a>)</p>
