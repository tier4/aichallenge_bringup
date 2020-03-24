# AIチャレンジ参加用リポジトリ
## セットアップ
### autowareのセットアップ
https://gitlab.com/autowarefoundation/autoware.ai/autoware/-/wikis/Source-Build  
### git-lfsのインストール
https://packagecloud.io/github/git-lfs/install  
### 本レポジトリのcloneとビルド
```
mkdir -p ~/aichallenge_ws/src  
cd ~/aichallenge_ws  
colcon build  
cd src  
git lfs clone https://github.com/tier4/aichallenge_bringup.git  
cd ../  
colcon build
```
### シミュレータのダウンロードと起動
大会HPからシミュレータのバイナリをダウンロード  
https://www.jsae.or.jp/jaaic/rule.html

![画面](/image/initial.png)  

Web UIでアカウント登録を行った後mapダウンロード画面に移行する　　

![画面](/image/map.png)  

add newをクリックしたあとMap NameにBorregas Avenue,Map URLに[url](https://assets.lgsvlsimulator.com/513316ab0ed5896f91cf7e6ff4e138b068993626/environment_BorregasAve)を入力

その後Vehicleダウンロード画面に移行する
![画面](/image/vehicle.png)  
Vehicle NameにLexus,Vechiel URLに[url](https://assets.lgsvlsimulator.com/aa4f921b6d4a48c6da8f7a88496a5daeca075da9/vehicle_Lexus2016RXHybrid)を入力

![画面](/image/setting.png)  
Bridge TypeにROSを選択、本レポジトリのdata以下にあるlexus.jsonの中身をSensorsに貼り付ける

その後simulation画面に移行する
![画面](/image/simulation_general.png)
Simulation Nameに適当な名前をつけたあと、Map&Vehiclesを設定する。

![画面](/image/simulation_map_vehicles.png)
MapはBorregas Avenueを選択、VehicleはLexusを設定して(ROSの動作するPCのIPアドレス):9090の形式でrosbridgeに対する接続設定を実施

![画面](/image/simulation_run.png)
右下の赤色の三角をクリック、シミュレーションを開始

ターミナルを開いて以下のコマンドを入力  
```
source autoware.ai/install/local_setup.bash  
source aichallenge_ws/install/local_setup.bash  
roslaunch aichallenge_bringup aichallenge_bringup.launch
```

別なターミナルを開いて以下のコマンドを入力
```
rviz
```
![画面](/image/rviz.png)

rvizのGUIが表示されたら左上のFileからOpen Configを選択し、aichallenge_bringupパッケージのdataの中にあるaichallenge.rvizを選ぶ。

## シナリオを実行して点数を算出する
### LGSVL Simulator Python APIのセットアップ
https://github.com/lgsvl/PythonAPI
この記述に従ってPythonAPIをインストール

### シミュレータの操作
Web UIのSimulationタブを開いてシミュレーションを選択しレンチのボタンをクリック、API Onlyにチェックを入れる
![画面](/image/simulator_scenario.png)
以下のコマンドを叩いてシナリオを実行

シナリオ1:ACC
```
roscd aichallnge_bringup/scenario
python3 acc.py
```
スコアは/acc/scoreトピックにstd_msgs/Float32で配信される

シナリオ2:障害物回避
```
roscd aichallnge_bringup/scenario
python3 avoid.py
```
スコアは/obstacle_avoid/scoreトピックにstd_msgs/Float32で配信される

シナリオ3:信号機認識
```
roscd aichallnge_bringup/scenario
python3 traffic_light.py
```
スコアは/traffic_light/scoreトピックにstd_msgs/Float32で配信される

### 車両の制御コマンド
車両にはautoware_msgs/VehicleCmd型で制御コマンドを送ることができます。
本コンテストにおいてサポートしているコマンドはVehicleCmdの中のcontrol_cmd内部に存在するlinear_acceleration,steering_angleとなります。
また、gearの値は必ず64（ドライブ）に設定してください。
本コンテストのタスクにはバック走行が無いためバックギアはサポートいたしません。


```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
autoware_msgs/SteerCmd steer_cmd
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  int32 steer
autoware_msgs/AccelCmd accel_cmd
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  int32 accel
autoware_msgs/BrakeCmd brake_cmd
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  int32 brake
autoware_msgs/LampCmd lamp_cmd
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  int32 l
  int32 r
int32 gear
int32 mode
geometry_msgs/TwistStamped twist_cmd
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  geometry_msgs/Twist twist
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
autoware_msgs/ControlCommand ctrl_cmd
  float64 linear_velocity
  float64 linear_acceleration
  float64 steering_angle
int32 emergency
```
