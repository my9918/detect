# detect

#流れは以下の通り  
TFを取得  
YOLOで横断歩道の検出  
ハフ変換で角度取得  
TFを監視しながら目的の角度まで旋回  

# 2つのlaunchの違い
トリガーのファイルが違う  
detectがYOLOにカメラとは違う画像を食わせその画像（角度）に対して姿勢修正を行うシミュレーター内や画像処理ができているかを確認する検証用  
mainが文字通りメインとして使うYOLOにカメラ画像を食わせて画像処理も行う本番用

# 起動するもの
まずlaunchをどちらか立ち上げる
detectならimage_pub.pyを立ち上げて画像をパブリッシュしておく
しっかりパブリッシュされているか確認したかったらimage_viewer.pyを使用

次にYOLOを起動するのだが


    <!-- ROS topics -->
    <!-- ここからどちらかを選びinput_image_topicを上書きする
    <arg name="input_image_topic" default="/usb_cam/image_raw/compressed"/>
    <arg name="input_image_topic" default="/image_topic"/>    
    -->

