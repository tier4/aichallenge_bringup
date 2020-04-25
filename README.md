2020/3/30 経路追従サンプルを追加  
2020/3/31 GPSセンサのパラメータに誤りがあったためlexus.jsonを修正  
2020/4/1 initial_pose_publisher.pyのinstall文がCMakeLists.txtから漏れていたため追加  
2020/4/15 ビルドテスト用Dockerfileを追加、uploadの手順を追記、信号認識シナリオの時間帯を変更  

# オンライン評価環境におけるlaunch手順ならびそのサンプル

オンライン評価環境においては以下の手順とコマンドにより評価を行います。

1. シミュレータの起動

本READMEに記述された手順と同様にしてシミュレータをAPIモードで起動します。

2. シナリオスクリプトの実行
```
python3 (シナリオ名)_eval.py
```

このとき再生されるシナリオは本パッケージのscenarioディレクトリの中にあるpythonスクリプトに若干の修正（自車両の初速や、他車との相対的な位置関係等）を入れたものとなります。  
ただし、初期姿勢に関してはサンプルシナリオと全く同じ値となっております。

3. Autoware並びに参加者の皆様のノードの起動
```
roslaunch aichallenge_bringup aichallenge_bringup.launch acc:=(true or false) avoid:=(true or false) traffic_light:=(true or false)
```

上記のコマンドを用いてシナリオごとに参加者の皆様が作成されたlaunchファイルを呼び出し、評価を行います。

# オンライン評価環境にファイルをアップする手順

## Dockerでビルドが通る＋スコアが出ることを確認
requirement: docker>=19.03

```
cd sample_aichallenge_ws
docker build -t <tagName> .
docker run -it --rm --gpus all -p 9090:9090 <tagName> bash
```

Dockerコンテナ内で
```
. ~/aichallenge_ws/install/setup.bash
roslaunch aichallenge_bringup aichallenge_bringup.launch avoid:=true
```

on host machine running the simulator:
```
python3 avoid.py
```

To check the score:
```
# コンテナ内に入る
docker exec -it <tagName> su autoware
# 内で
. ~/aichallenge_ws/install/setup.bash
rostopic echo /obstacle_avoid/score
```

## ソースコードをtar.gzに圧縮する
こちらのスクリプトを使ってソースを圧縮します。
https://github.com/tier4/aichallenge_bringup/blob/master/create-tar-file.sh
```
cp create-tar-file.sh ~/aichallenge_ws/
cd ~/aichallenge_ws/
chmod +x create-tar-file.sh
./create-tar-file.sh
```

出来上がったtarファイルを[webページ](https://simulation.tier4.jp)にログイン後アップロード

## 採点時の実行フロー
提出いただいたあとは下記の手順で実行され、点数が記録されます。

また、アップロードの際は事前に手元の環境にて[スコアが出ることの確認](https://github.com/tier4/aichallenge_bringup#docker%E3%81%A7%E3%83%93%E3%83%AB%E3%83%89%E3%81%8C%E9%80%9A%E3%82%8B%E3%82%B9%E3%82%B3%E3%82%A2%E3%81%8C%E5%87%BA%E3%82%8B%E3%81%93%E3%81%A8%E3%82%92%E7%A2%BA%E8%AA%8D)を行っていただくことを推奨しております。

1. 上記のDockerfileでビルド
https://github.com/tier4/aichallenge_bringup/blob/master/Dockerfile

2. aichallenge_bringup.launchと採点用シナリオの実行

具体的には以下を実行します。（avoid以外のシナリオに関しても同様です）
```
. ~/aichallenge_ws/install/setup.bash
roslaunch aichallenge_bringup aichallenge_bringup.launch avoid:=true &
sleep 10
python3 avoid.py
```


3. 点数トピックの出力を記録

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
git lfs clone https://github.com/
/aichallenge_bringup.git  
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

steering_angleに関しては-1から1の値をfloatで入力してください。

その値に比例して~39.4から39.4の範囲で車両の操舵角が変化します。

正の値を入力した場合右にステアがきれます。

linear_accelerationはアクセル・ブレーキの入力値を-1~1の範囲で正規化したものとなります。

正の値を入力した場合加速、負の値を入力した場合減速します。  
