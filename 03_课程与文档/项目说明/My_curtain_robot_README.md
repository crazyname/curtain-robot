

- 首先这是一个网上的一款窗帘机器人

------

> 其实去年我就见过这个东西，现在淘宝也有卖的，价格400-800左右。据说是英国的一个公司做的，我看完就很佩服这个创意，想想网上卖的那些自动窗帘，或者小米搞得只能窗帘，装庞大的电机，装庞大的滑轨，而且原有的设备和布局也发生了变化！然而这个小东西，却可以推动窗帘，即装即用！很赞的创意！
> 参考链接：[https://www.xsrjt.com/znyj/148999.html](https://www.xsrjt.com/znyj/148999.html)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200617233739738.gif#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020061723354243.GIF#pic_center)

然后呢，我也想搞一个，说干就干！计划从电路板，外壳装配，微信小程序，**全部来自己完成**！



<div style="height: 0;padding-bottom:65%;position: relative;"><br><iframe width="760" height="510" src="//player.bilibili.com/player.html?aid=711002801&bvid=BV1mD4y1D7Hs&cid=203915780&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen style="position: absolute;height: 105%;width: 100%;"> </iframe><br></div>  





![在这里插入图片描述](https://img-blog.csdnimg.cn/20200618000602439.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 单单元器件选型，我就做了好久，由于其工作场景为低功耗，同时需要蓝牙以及陀螺仪和光照传感器来进行中断唤醒，所以就需要讲单片机、蓝牙、传感器全部进入低功耗，而不能将其电源断开，所以元器件的选型尤为重要！我选择的几款设备功耗都是非常低的。
> 令我比较惊艳的是蓝牙模块PW02：[http://www.phangwei.com/page116/?article_id=73](http://www.phangwei.com/page116/?article_id=73) 你想象不到的小尺寸，太惊艳了！

<!--more-->

- 电路图绘制

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020061723595789.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 目前原理图为第二版，第一版出现了一些问题：
> 1.第一版STM32内部的时钟误差太大，无法实现相对精准的定时，第二版添加了RTC时钟
> 2.第二版添加了陀螺仪芯片，用来感知用户手动拉窗帘时的加速度，进而控制窗帘
> 3.第一版的光传感器芯片，嘉立创商城的原理图是有问题的，就很尴尬，后面会改第二版来解决

- PCB设计

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200618001929656.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 外壳部分主要做了几点优化和设计
> 1.多处安装轴承来减小摩擦，同时外壳与轴承和电机装配处，留出0.1mm的公差，便于安装
> 2.为了缩短外壳尺寸，将电机隐藏在滚轮中间，堪称完美
> 3.整体的外观采用的是天猫精灵空调遥控的外观，圆形（没审美就用最简单的外形，哈哈）

- 外壳设计

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200620181138746.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 微信小程序的开发就比较简单了
> 1.最惊艳的就是ColorUI的加持，相当之漂亮，而且有很多的动画和特效
> 2.功能包括了连接，列表显示，滑动列表连接
> 3.微信小程序与蓝牙连接以后会将当前的北京时间发送至硬件单片机，方便单片机进行RTC对表
> 4.其中记忆功能是和硬件相关联的功能

- 微信小程序开发
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200618104327405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 硬件部分的开发就行对简单一些了，主要配置STOP模式低功耗，以及串口中断唤醒
> 注意事项：
> 1.低功耗配置
> 2.内部RTC时钟不准（第二版会添加RTC晶振）
> 3.蓝牙授时RTC对表，这样可以做到用户一旦使用，就会进行一次RTC对表，保证了时间的相对准确
> 4.由于N20电机是普通的减速电机不是步进电机，所以无法精确地定位窗帘位置，所以可以让用户在第一次使用的时候，手动录入一次窗帘的开启和关闭，依靠时间来定位电机运转的距离（后期待优化更好的方案），会记录在Flash中，及时下次开机或者断电以后依然可以进行记忆。除非用户又进行了记忆操作（此处对应微信小程序中的记忆按钮的操作）

- 硬件程序开发

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200618114343913.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 挂钩处，是非标准件所以很难买到，这是自己用钳子手动做出来的，（………）
> 轴承也是量了挂钩尺寸以后，在淘宝买的，轴承可以起到把滑动摩擦转为滚动摩擦的作用，减小挂钩与滑竿之间的摩擦力
> 同时，滚轮上的橡胶垫，则是为了增大滚轮与滑竿之间的摩擦力，同时内部安装了弹簧，来加大滚轮与滑竿之间的压迫力，增大摩擦！

- 成品展示

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020061810440537.JPG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

------

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200618104426755.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N3aXRjaF9sb3ZlX2Nhc2U=,size_16,color_FFFFFF,t_70#pic_center)

> 视频演示

后续还会进行优化，并且录制演示视频。静候佳音！

