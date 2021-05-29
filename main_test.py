from sanic import Sanic

from common.email import EmailClient
from common.utils import ConfigFile
from routes.user_routes import user_blue_print
from routes.vehicle_routes import car_blue_print
from routes.advertisement_routes import advertisement_blue_print

conf = ConfigFile.getInstance()['SERVER']

EmailClient()

app = Sanic("buyanycaronline")
app.blueprint(user_blue_print)
app.blueprint(car_blue_print)
app.blueprint(advertisement_blue_print)

if __name__ == '__main__':
    app.run(host=conf["IP"], port=conf["PORT"])
