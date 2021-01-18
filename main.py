#! /usr/bin/env python

"""
A script to calculate the cost of slipstream
"""
import typer
import wasabi

add_price = 0
accessories = {"Crocodile Pillow for back seat": 4000,
               "Multicolor LED Footstep Matrix": 12000,
               "Best Value Car Cleaning Kits": 8000,
               "Smooth 7D Car Floor Mats": 5500,
               "Desginer Seat Covers for seats": 35000,
               "Dashboard Figurine Idols": 7200,
               "Rear Liftgate Sunshade": 1750,
               "Slipstream Model Key Band": 1330,
               "Front and Back Bumpers": 40000
               }
comfort = ""
color = ""
sports = False
accessories_user = []
mobile_app = False
tachyon = False
calculate = False
fine = ""
logo = """
 *     .----------------.  .----------------.  .----------------.
 *    | .--------------. || .--------------. || .--------------. |
 *    | |     ______   | || |     ______   | || |     ______   | |
 *    | |   .' ___  |  | || |   .' ___  |  | || |   .' ___  |  | |
 *    | |  / .'   \_|  | || |  / .'   \_|  | || |  / .'   \_|  | |
 *    | |  | |         | || |  | |         | || |  | |         | |
 *    | |  \ `.___.'\  | || |  \ `.___.'\  | || |  \ `.___.'\  | |
 *    | |   `._____.'  | || |   `._____.'  | || |   `._____.'  | |
 *    | |              | || |              | || |              | |
 *    | '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'
"""


class Slipstream:
    """
    Base Class for Slipstream
    """

    def __init__(self, color, comfort, accessories):
        self.color = color
        self.comfort = comfort
        self.accessories = accessories

    @staticmethod
    def get_tax():
        return 10


class Photon(Slipstream):
    def __init__(self, color, comfort, accessories):
        super().__init__(color, comfort, accessories)
        self.price = 655000


class Tachyon(Slipstream):
    def __init__(self, color, comfort, accessories, sports, mobile_app):
        super().__init__(color, comfort, accessories)
        self.price = 675000
        self.sports = sports
        self.mobile_app = mobile_app


def ask_color():
    typer.echo(typer.style("Q) Which color car do you want?",
                           fg=typer.colors.GREEN))
    black = typer.style("black", fg=typer.colors.BRIGHT_BLACK)
    red = typer.style(
        "red",
        fg=typer.colors.BRIGHT_RED,
    )
    white = typer.style("white", fg=typer.colors.WHITE)
    print(black, white, red)
    global color
    color = input("")
    global add_price
    if color != "white":
        add_price = add_price + 10000


def ask_comfort():
    typer.echo(
        typer.style(
            "Q) What comfort level do you want?",
            fg=typer.colors.GREEN
        )
    )
    print("Normal", "Premium", "Royal")
    global comfort
    comfort = input("")
    global add_price
    if comfort == "Premium":
        add_price += 7500
    if comfort == "Royal":
        add_price += 10000


def ask_accessories():
    typer.echo(
        typer.style(
            "Q) Press y for accessories you want and n for others.",
            fg=typer.colors.GREEN
        )
    )
    global accessories_user, add_price
    accessories_user = list()
    for accessory in accessories:
        typer.echo(typer.style(accessory, fg=typer.colors.GREEN))
        add = input("")
        if add == 'y':
            accessories_user.append(accessory)
            accessory_price = accessories.get(accessory)
            if accessory_price:
                add_price += accessory_price


def final_confirm_and_answer(car):
    import json
    price = car.price
    typer.clear()
    typer.echo(typer.style("Is this fine?(y for yes)", fg=typer.colors.GREEN))
    car_dict = car.__dict__
    del car_dict['price']
    if tachyon:
        typer.echo('Tachyon')
    else:
        typer.echo('Photon')
    typer.echo(json.dumps(car_dict, sort_keys=True, indent=4))
    fine = input("")
    global calculate
    if fine == "y":
        calculate = True
        typer.echo(typer.style("Calculating....", fg=typer.colors.GREEN))
        price = round(price*((100+car.get_tax())/100), 2)
        price = str(price)
        price_list = price.split('.')
        try:
            price_decimal = price_list[1]
        except IndexError:
            price_decimal = 0
        except Exception:
            price_decimal = 0
        finally:
            if price_decimal == 0:
                price_decimal = str(00)
            if len(price_decimal) != 2:
                price_decimal = str(price_decimal) + str(0)
        price_list[1] = price_decimal
        price = str(price_list[0]) + '.' + str(price_list[1])

        typer.echo(
            typer.style(
                "The car will cost you Rs." + str(price),
                fg=typer.colors.GREEN
            )
        )
        typer.echo(
            wasabi.msg.warn("For Discounts contact your nearest showroom")
        )


def calculate_price():
    typer.clear()
    typer.echo(
        typer.style(
            logo,
            fg=typer.colors.GREEN
        )
    )
    typer.echo(
        typer.style(
            "Welcome to Car Cost Calculator - CCC", fg=typer.colors.GREEN, bold=True
        )
    )
    typer.echo(
        typer.style(
            "Q) If you want to buy tachyon press y, otherwise press any other key-)",
            fg=typer.colors.GREEN
        )
    )
    add = input("")
    global tachyon
    if add == 'y':
        tachyon = True

    ask_color()
    while color not in ["black", "red", "white"]:
        wasabi.msg.fail("Please choose a valid option")
        ask_color()
    ask_comfort()
    while comfort not in ["Normal", "Premium", "Royal"]:
        wasabi.msg.fail("Please choose a valid option")
        ask_comfort()
    ask_accessories()
    if tachyon:
        typer.echo(
            typer.style(
                "Q) Do you want to buy tachyon sports model(y for yes)",
                fg=typer.colors.GREEN
            )
        )
        ans = input("")
        global sports
        if ans == 'y':
            sports = True
        typer.echo(
            typer.style(
                "Q) Do you want to buy mobile app(y for yes)",
                fg=typer.colors.GREEN
            )
        )
        ans = input("")
        global mobile_app
        if ans == 'y':
            mobile_app = True
        car = Tachyon(color=color, comfort=comfort,
                      accessories=accessories_user, sports=sports, mobile_app=mobile_app)
        car.price += add_price
    else:
        car = Photon(color=color, comfort=comfort,
                     accessories=accessories_user)
        car.price += add_price
    final_confirm_and_answer(car)


if __name__ == "__main__":
    while not calculate:
        calculate_price()
