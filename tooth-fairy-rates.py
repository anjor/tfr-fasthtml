from enum import Enum
from fasthtml.common import *


def render(tf_rate):
    return Tr(
        Td(tf_rate.location),
        Td(tf_rate.rate),
    )


app, rt, tf_rates, TF_Rate = fast_app(
    "tf_rates.db",
    live=True,
    render=render,
    id=int,
    location=str,
    rate=float,
    pk="id",
)


@rt("/")
def get():
    return Titled(
        "Tooth Fairy Rates",
        Form(
            Input(id="location", placeholder="Location"),
            Input(id="rate", placeholder="Rate (in local currency)"),
            Button("Add Rate"),
            action="/add_rate",
            method="post",
        ),
        Table(
            *tf_rates(),
        ),
    )


@dataclass
class TFRate:
    location: str
    rate: float


@rt("/add_rate")
def post(rate: TFRate):
    r = TF_Rate(location=rate.location, rate=rate.rate)
    tf_rates.insert(r)
    return RedirectResponse("/", status_code=303)


serve()
