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
  
次にYOLOの起動  
YOLOv5_rosのyolov5_2.launchを起動する　v１は学習データが古く少ない  
yolov5_2.launch内の以下のコメントのようにカメラからの画像かパブリッシュした画像を使うのかを目的に合わせて選択  

    <!-- ROS topics -->
    <!-- ここからどちらかを選びinput_image_topicを上書きする
    <arg name="input_image_topic" default="/usb_cam/image_raw/compressed"/>
    <arg name="input_image_topic" default="/image_topic"/>    
    -->

起動後
senkai.pyを起動すると旋回が始まる  
senkai.pyだけはjetsonではなくraspicatのラズパイで起動しないと通信のラグがあるため正確さに欠ける
detect.launchだと即旋回が始まるが、mainだとカメラに写ってから旋回が始まる  
なので、横断歩道が見えないような位置でスタートする際に起動しておく  

# 途中＆発展
ハフ変換で横断歩道の線を検出する際、奥の方の線は傾きが弱いためあまり必要ではない  
そこで以下の部分で角度の取得に制限を追加しようと試みている
    height, width = image.shape[:2]
    edited_height = height *  0.2 #上から何％カットするか1.0で100％
    edited_width = width * 1/2
    #print(height, width)
  
見えたら即旋回だと使いづらい→バウンディングボックスの高さや位置で閾値を設け、例えば画面の下半分に写ったから旋回開始等にする
横断歩道が全く見えない時にグルグル旋回
