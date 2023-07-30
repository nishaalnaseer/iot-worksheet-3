import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.models import Response
from starlette.responses import JSONResponse, HTMLResponse

from src.models import *
import aiomysql
import src.sql_scripts as scripts
from datetime import date, datetime, time
import plotly.graph_objects as go
from time import time as time_stamp
from fastapi.templating import Jinja2Templates


app = FastAPI()
pool: aiomysql.pool
with open("src/config.json", 'r') as f:
    config = json.load(f)
templates = Jinja2Templates(directory="templates")


async def create_connection_pool():
    """function to initialise db connection pool"""
    global pool
    pool = await aiomysql.create_pool(
        host=config["db_ip"],
        user=config["username"],
        password=config["password"],
        db=config["db"],
        port=config["port"],
        minsize=100,
        maxsize=500,
        autocommit=True
    )


async def fetch(
        script: str, fetch_all: bool = True,
        values: tuple = ()
):
    """general function to fetch sum things based on script
    and values"""
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(script, values)
            if fetch_all:
                fetched = await cursor.fetchall()
            else:
                fetched = await cursor.fetchone()
        await connection.commit()

    return fetched


async def insert(script: str, values: tuple = ()):
    """general function to insert some things to db based on script and values"""
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(script, values)
        # await connection.commit()


def to_datetime(unix_timestamp):
    """get date and time from unix date time"""
    return datetime.fromtimestamp(unix_timestamp)


def bytes_to_int(stuff: bytes):
    return int.from_bytes(stuff, byteorder='big', signed=False)


@app.on_event("startup")
async def startup() -> None:
    """this function is run on server startup"""
    await create_connection_pool()


@app.get("/")
async def root():
    """root end point to test connection"""
    return JSONResponse(
        status_code=200,
        content={"message": "Hello world!"}
    )


@app.post("/periodic_report")
async def periodic_report(report: Report):
    await insert(
        values=(
            report.time,
            report.accel_x,
            report.accel_y,
            report.accel_z,
            report.temp,
            report.light_level,
            report.touch_pin0,
            report.touch_pin1,
            report.touch_pin2,
        ),
        script=scripts.insert_report
    )

    return JSONResponse(status_code=201, content={"message": "Report Submitted"})


@app.get("/report", response_class=HTMLResponse)
async def get_report(
        report_type: ReportType, start: date,
        request: Request, end: date | None = None
):
    if report_type == ReportType.LIGHT:
        script = scripts.select_light
    elif report_type == ReportType.TEMPS:
        script = scripts.select_temps
    elif report_type == ReportType.PINS:
        script = scripts.select_pins
    else:
        raise HTTPException(
            status_code=422
        )

    if end is None:
        end_timestamp = int(time_stamp())
    else:
        end_timestamp = int(datetime.combine(end, time()).timestamp())

    start_timestamp = int(datetime.combine(start, time()).timestamp())

    if end_timestamp < start_timestamp:
        raise HTTPException(
            422,
            "End date must be greater than start date"
        )

    rows = await fetch(
        script=script,
        values=(start_timestamp, end_timestamp,)
    )
    x_values = [to_datetime(row[0]) for row in rows]

    if report_type != ReportType.PINS:
        y_values = [row[1] for row in rows]
        fig = go.Figure(data=go.Scatter(x=x_values, y=y_values))
    else:
        print(type(rows[0][1]))
        pin0 = [bytes_to_int(row[1]) for row in rows]
        pin1 = [bytes_to_int(row[2]) for row in rows]
        pin2 = [bytes_to_int(row[3]) for row in rows]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_values, y=pin0, mode='lines', name='Pin0'))
        fig.add_trace(go.Scatter(x=x_values, y=pin1, mode='lines', name='Pin1'))
        fig.add_trace(go.Scatter(x=x_values, y=pin2, mode='lines', name='Pin2'))
        fig.update_layout(title='Microbit Pins Touch Sensor Data',
                          xaxis_title='DateTime',
                          yaxis_title='Pins')

    # Return the graph as an interactive HTML file
    html_content = fig.to_html(full_html=False)

    return html_content
