# ros-selective-bridge
a GUI wrapper for ros1_bridge parameter_bridge can select which topic for bridging

* Support both ros1 & ros2 bridging
* it's wrapper for paramter_bridge


![selectTivebdg](https://user-images.githubusercontent.com/25432456/99883902-92bf4c80-2c6d-11eb-9675-acebf7eee8d7.png)

* Simple UI Manual
- Double click cell with you want to exclude
- Export your exclude topic list
- Load your exclude Topic list
- highlighted cells mean excluded topics
- Reset means just kill bridge

## How to install
just execute `python install.py in the directory` then script will make shortcut to your Desktop
(Adobe Bridge icon)


## TODO
* support argument slient launch `artiv_bdg.py --silent --preset "blah.kansan"
