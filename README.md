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
