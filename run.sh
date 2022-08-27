clear
cd /home/pi/Desktop/projects/diabetech/
source venv/bin/activate
export FLASK_APP=app
echo '________  .__      ___.           __                .__'
echo '\______ \ |__|____ \_ |__   _____/  |_  ____   ____ |  |__  '
echo ' |    |  \|  \__  \ | __ \_/ __ \   __\/ __ \_/ ___\|  |  \ '
echo ' |        \  |/ __ \| \_\ \  ___/|  | \  ___/\  \___|   Y  \'
echo '/_______  /__(____  /___  /\___  >__|  \___  >\___  >___|  /'
echo '        \/        \/    \/     \/          \/     \/     \/ '
flask run --host=0.0.0.0
