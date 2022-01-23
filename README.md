# spotirecord - celebrating music (again)

### Installation instructions
(under construction but here are some notes)
+ Install [Spotifyd](https://spotifyd.github.io/spotifyd/installation/Raspberry-Pi.html) on your Raspberry pi
+ Come back and pull this repository 
+ navigate to the repository directory and run `sudo pip3 install -r requirements.txt`. Make sure you run as superuser, this is needed when working with the RGB stripes.
+ in order to get numpy to work on the raspberry pi you'll need to run `sudo apt-get install libatlas-base-dev`
+ Take a look at the config at ``spotirecord/config/config.yml``
+ Go back to the root directory and run ``sudo python3 -m spotirecord``.