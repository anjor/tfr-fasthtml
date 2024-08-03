from datetime import datetime
from fasthtml.common import *


def render(tf_rate):
    return Tr(
        Td(tf_rate.created_at),
        Td(tf_rate.location),
        Td(tf_rate.rate),
    )


app, rt, tf_rates, TF_Rate = fast_app(
    "tf_rates.db",
    live=True,
    render=render,
    id=int,
    created_at=datetime,
    location=str,
    rate=float,
    pk="id",
)


@rt("/")
def get():

    sorted_rates = sorted(tf_rates(), key=lambda x: x.location)

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
            Tr(Th(B("Date")), Th(B("Location")), Th(B("Rate"))),
            *sorted_rates,
        ),
    )


@dataclass
class TFRate:
    location: str
    rate: float


@rt("/add_rate")
def post(rate: TFRate):
    r = TF_Rate(
        created_at=datetime.today().strftime("%Y-%m-%d"),
        location=rate.location,
        rate=rate.rate,
    )
    tf_rates.insert(r)
    return RedirectResponse("/", status_code=303)


serve()
